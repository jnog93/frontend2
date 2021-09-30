"""Remove RACELANDSHOP."""
from typing import TYPE_CHECKING
from ..const import DOMAIN
from ..enums import RacelandshopDisabledReason
from ..share import get_racelandshop

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry


async def async_remove_entry(hass: "HomeAssistant", config_entry: "ConfigEntry"):
    """Handle removal of an entry."""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Disabling RACELANDSHOP")
    racelandshop.log.info("Removing recurring tasks")
    for task in racelandshop.recuring_tasks:
        task()

    if str(config_entry.state) in ["ConfigEntryState.LOADED", "loaded"]:
        racelandshop.log.info("Removing sensor")
        try:
            await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
        except ValueError:
            pass
    try:
        if "racelandshop" in hass.data.get("frontend_panels", {}):
            racelandshop.log.info("Removing sidepanel")
            hass.components.frontend.async_remove_panel("racelandshop")
    except AttributeError:
        pass
    if DOMAIN in hass.data:
        del hass.data[DOMAIN]
    racelandshop.disable(RacelandshopDisabledReason.REMOVED)
