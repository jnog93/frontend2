"""Starting setup task: extra stores."""
from custom_components.racelandshop.const import ELEMENT_TYPES

from ...enums import RacelandshopCategory, RacelandshopSetupTask
from ...share import get_racelandshop


def _setup_extra_stores():
    """Set up extra stores in RACELANDSHOP if enabled in Home Assistant."""
    racelandshop = get_racelandshop()
    racelandshop.log.debug("Starting setup task: Extra stores")
    racelandshop.common.categories = set()
    for category in ELEMENT_TYPES:
        enable_category(racelandshop, RacelandshopCategory(category))

    if RacelandshopCategory.PYTHON_SCRIPT in racelandshop.hass.config.components:
        enable_category(racelandshop, RacelandshopCategory.PYTHON_SCRIPT)

    if (
        racelandshop.hass.services._services.get("frontend", {}).get("reload_themes")
        is not None
    ):
        enable_category(racelandshop, RacelandshopCategory.THEME)

    if racelandshop.configuration.appdaemon:
        enable_category(racelandshop, RacelandshopCategory.APPDAEMON)
    if racelandshop.configuration.netdaemon:
        enable_category(racelandshop, RacelandshopCategory.NETDAEMON)


async def async_setup_extra_stores():
    """Async wrapper for setup_extra_stores"""
    racelandshop = get_racelandshop()
    racelandshop.log.info("setup task %s", RacelandshopSetupTask.CATEGORIES)
    await racelandshop.hass.async_add_executor_job(_setup_extra_stores)


def enable_category(racelandshop, category: RacelandshopCategory):
    """Add category."""
    if category not in racelandshop.common.categories:
        racelandshop.log.info("Enable category: %s", category)
        racelandshop.common.categories.add(category)
