"""Starting setup task: clear storage."""
import os

from custom_components.racelandshop.share import get_racelandshop

from ...enums import RacelandshopSetupTask


async def async_clear_storage():
    """Async wrapper for clear_storage"""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Setup task %s", RacelandshopSetupTask.CATEGORIES)
    await racelandshop.hass.async_add_executor_job(_clear_storage)


def _clear_storage():
    """Clear old files from storage."""
    racelandshop = get_racelandshop()
    storagefiles = ["racelandshop"]
    for s_f in storagefiles:
        path = f"{racelandshop.core.config_path}/.storage/{s_f}"
        if os.path.isfile(path):
            racelandshop.log.info(f"Cleaning up old storage file {path}")
            os.remove(path)
