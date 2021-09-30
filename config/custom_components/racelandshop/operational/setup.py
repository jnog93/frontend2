"""Setup RACELANDSHOP."""
from datetime import datetime
from aiogithubapi import AIOGitHubAPIException, GitHub
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.const import __version__ as HAVERSION
from homeassistant.core import CoreState
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.event import async_call_later

from custom_components.racelandshop.const import (
    DOMAIN,
    RACELANDSHOP_GITHUB_API_HEADERS,
    INTEGRATION_VERSION,
    STARTUP,
)
from custom_components.racelandshop.enums import RacelandshopDisabledReason, RacelandshopStage, LovelaceMode
from custom_components.racelandshop.racelandshopbase.configuration import Configuration
from custom_components.racelandshop.racelandshopbase.data import RacelandshopData
from custom_components.racelandshop.helpers.functions.constrains import check_constrains
from custom_components.racelandshop.helpers.functions.remaining_github_calls import (
    get_fetch_updates_for,
)
from custom_components.racelandshop.operational.reload import async_reload_entry
from custom_components.racelandshop.operational.remove import async_remove_entry
from custom_components.racelandshop.operational.setup_actions.clear_storage import (
    async_clear_storage,
)
from custom_components.racelandshop.operational.setup_actions.frontend import (
    async_setup_frontend,
)
from custom_components.racelandshop.operational.setup_actions.load_racelandshop_repository import (
    async_load_racelandshop_repository,
)
from custom_components.racelandshop.operational.setup_actions.sensor import async_add_sensor
from custom_components.racelandshop.operational.setup_actions.websocket_api import (
    async_setup_racelandshop_websockt_api,
)
from custom_components.racelandshop.share import get_racelandshop

try:
    from homeassistant.components.lovelace import system_health_info
except ImportError:
    from homeassistant.components.lovelace.system_health import system_health_info


async def _async_common_setup(hass):
    """Common setup stages."""
    racelandshop = get_racelandshop()
    racelandshop.hass = hass
    racelandshop.system.running = True
    racelandshop.session = async_create_clientsession(hass)


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    from homeassistant import config_entries

    racelandshop = get_racelandshop()
    if hass.data.get(DOMAIN) is not None:
        return False
    if config_entry.source == config_entries.SOURCE_IMPORT:
        hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
        return False

    await _async_common_setup(hass)

    racelandshop.configuration = Configuration.from_dict(
        config_entry.data, config_entry.options
    )
    racelandshop.configuration.config_type = "flow"
    racelandshop.configuration.config_entry = config_entry

    return await async_startup_wrapper_for_config_entry()


async def async_setup(hass, config):
    """Set up this integration using yaml."""
    racelandshop = get_racelandshop()
    if DOMAIN not in config:
        return True
    if racelandshop.configuration and racelandshop.configuration.config_type == "flow":
        return True

    await _async_common_setup(hass)

    racelandshop.configuration = Configuration.from_dict(config[DOMAIN])
    racelandshop.configuration.config_type = "yaml"
    await async_startup_wrapper_for_yaml()
    return True


async def async_startup_wrapper_for_config_entry():
    """Startup wrapper for ui config."""
    racelandshop = get_racelandshop()
    racelandshop.configuration.config_entry.add_update_listener(async_reload_entry)
    try:
        startup_result = await async_racelandshop_startup()
    except AIOGitHubAPIException:
        startup_result = False
    if not startup_result:
        racelandshop.system.disabled = True
        raise ConfigEntryNotReady
    racelandshop.enable()
    return startup_result


async def async_startup_wrapper_for_yaml(_=None):
    """Startup wrapper for yaml config."""
    racelandshop = get_racelandshop()
    try:
        startup_result = await async_racelandshop_startup()
    except AIOGitHubAPIException:
        startup_result = False
    if not startup_result:
        racelandshop.system.disabled = True
        racelandshop.log.info("Could not setup RACELANDSHOP, trying again in 15 min")
        async_call_later(racelandshop.hass, 900, async_startup_wrapper_for_yaml)
        return
    racelandshop.enable()


async def async_racelandshop_startup():
    """RACELANDSHOP startup tasks."""
    racelandshop = get_racelandshop()
    racelandshop.hass.data[DOMAIN] = racelandshop

    try:
        lovelace_info = await system_health_info(racelandshop.hass)
    except (TypeError, KeyError, HomeAssistantError):
        # If this happens, the users YAML is not valid, we assume YAML mode
        lovelace_info = {"mode": "yaml"}
    racelandshop.log.debug(f"Configuration type: {racelandshop.configuration.config_type}")
    racelandshop.version = INTEGRATION_VERSION
    racelandshop.log.info(STARTUP)
    racelandshop.core.config_path = racelandshop.hass.config.path()
    racelandshop.system.ha_version = HAVERSION

    racelandshop.system.lovelace_mode = lovelace_info.get("mode", "yaml")
    racelandshop.core.lovelace_mode = LovelaceMode(lovelace_info.get("mode", "yaml"))

    # Setup websocket API
    await async_setup_racelandshop_websockt_api()

    # Set up frontend
    await async_setup_frontend()

    # Clear old storage files
    await async_clear_storage()

    racelandshop.enable()
    racelandshop.github = GitHub(
        racelandshop.configuration.token,
        async_create_clientsession(racelandshop.hass),
        headers=RACELANDSHOP_GITHUB_API_HEADERS,
    )
    racelandshop.data = RacelandshopData()

    can_update = await get_fetch_updates_for(racelandshop.github)
    if can_update is None:
        racelandshop.log.critical("Your GitHub token is not valid")
        racelandshop.disable(RacelandshopDisabledReason.INVALID_TOKEN)
        return False

    if can_update != 0:
        racelandshop.log.debug(f"Can update {can_update} repositories")
    else:
        reset = datetime.fromtimestamp(int(racelandshop.github.client.ratelimits.reset))
        racelandshop.log.error(
            "RACELANDSHOP is ratelimited, RACELANDSHOP will resume setup when the limit is cleared (%02d:%02d:%02d)",
            reset.hour,
            reset.minute,
            reset.second,
        )
        racelandshop.disable(RacelandshopDisabledReason.RATE_LIMIT)
        return False

    # Check RACELANDSHOP Constrains
    if not await racelandshop.hass.async_add_executor_job(check_constrains):
        if racelandshop.configuration.config_type == "flow":
            if racelandshop.configuration.config_entry is not None:
                await async_remove_entry(racelandshop.hass, racelandshop.configuration.config_entry)
        racelandshop.disable(RacelandshopDisabledReason.CONSTRAINS)
        return False

    # Load RACELANDSHOP
    if not await async_load_racelandshop_repository():
        if racelandshop.configuration.config_type == "flow":
            if racelandshop.configuration.config_entry is not None:
                await async_remove_entry(racelandshop.hass, racelandshop.configuration.config_entry)
        racelandshop.disable(RacelandshopDisabledReason.LOAD_RACELANDSHOP)
        return False

    # Restore from storefiles
    if not await racelandshop.data.restore():
        racelandshop_repo = racelandshop.get_by_name("racelandshop/integration")
        racelandshop_repo.pending_restart = True
        if racelandshop.configuration.config_type == "flow":
            if racelandshop.configuration.config_entry is not None:
                await async_remove_entry(racelandshop.hass, racelandshop.configuration.config_entry)
        racelandshop.disable(RacelandshopDisabledReason.RESTORE)
        return False

    # Setup startup tasks
    if racelandshop.hass.state == CoreState.running:
        async_call_later(racelandshop.hass, 5, racelandshop.startup_tasks)
    else:
        racelandshop.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, racelandshop.startup_tasks)

    # Set up sensor
    await async_add_sensor()

    # Mischief managed!
    await racelandshop.async_set_stage(RacelandshopStage.WAITING)
    racelandshop.log.info(
        "Setup complete, waiting for Home Assistant before startup tasks starts"
    )
    return True
