""""Starting setup task: Sensor"."""
from homeassistant.helpers import discovery

from custom_components.racelandshop.const import DOMAIN
from custom_components.racelandshop.share import get_racelandshop

from ...enums import RacelandshopSetupTask


async def async_add_sensor():
    """Async wrapper for add sensor"""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Setup task %s", RacelandshopSetupTask.SENSOR)
    if racelandshop.configuration.config_type == "yaml":
        racelandshop.hass.async_create_task(
            discovery.async_load_platform(
                racelandshop.hass, "sensor", DOMAIN, {}, racelandshop.configuration.config
            )
        )
    else:
        racelandshop.hass.async_add_job(
            racelandshop.hass.config_entries.async_forward_entry_setup(
                racelandshop.configuration.config_entry, "sensor"
            )
        )
