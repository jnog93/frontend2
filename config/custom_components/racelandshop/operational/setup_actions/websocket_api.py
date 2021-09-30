"""Register WS API endpoints for RACELANDSHOP."""
from homeassistant.components import websocket_api

from custom_components.racelandshop.api.acknowledge_critical_repository import (
    acknowledge_critical_repository,
)
from custom_components.racelandshop.api.check_local_path import check_local_path
from custom_components.racelandshop.api.get_critical_repositories import (
    get_critical_repositories,
)
from custom_components.racelandshop.api.racelandshop_config import racelandshop_config
from custom_components.racelandshop.api.racelandshop_removed import racelandshop_removed
from custom_components.racelandshop.api.racelandshop_repositories import racelandshop_repositories
from custom_components.racelandshop.api.racelandshop_repository import racelandshop_repository
from custom_components.racelandshop.api.racelandshop_repository_data import racelandshop_repository_data
from custom_components.racelandshop.api.racelandshop_settings import racelandshop_settings
from custom_components.racelandshop.api.racelandshop_status import racelandshop_status
from custom_components.racelandshop.share import get_racelandshop

from ...enums import RacelandshopSetupTask


async def async_setup_racelandshop_websockt_api():
    """Set up WS API handlers."""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Setup task %s", RacelandshopSetupTask.WEBSOCKET)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_settings)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_config)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_repositories)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_repository)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_repository_data)
    websocket_api.async_register_command(racelandshop.hass, check_local_path)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_status)
    websocket_api.async_register_command(racelandshop.hass, racelandshop_removed)
    websocket_api.async_register_command(racelandshop.hass, acknowledge_critical_repository)
    websocket_api.async_register_command(racelandshop.hass, get_critical_repositories)
