"""RACELANDSHOP Startup constrains."""
# pylint: disable=bad-continuation
import os

from custom_components.racelandshop.const import (
    CUSTOM_UPDATER_LOCATIONS,
    CUSTOM_UPDATER_WARNING,
    MINIMUM_HA_VERSION,
)
from custom_components.racelandshop.helpers.functions.misc import version_left_higher_then_right
from custom_components.racelandshop.share import get_racelandshop


def check_constrains():
    """Check RACELANDSHOP constrains."""
    if not constrain_custom_updater():
        return False
    if not constrain_version():
        return False
    return True


def constrain_custom_updater():
    """Check if custom_updater exist."""
    racelandshop = get_racelandshop()
    for location in CUSTOM_UPDATER_LOCATIONS:
        if os.path.exists(location.format(racelandshop.core.config_path)):
            msg = CUSTOM_UPDATER_WARNING.format(location.format(racelandshop.core.config_path))
            racelandshop.log.critical(msg)
            return False
    return True


def constrain_version():
    """Check if the version is valid."""
    racelandshop = get_racelandshop()
    if not version_left_higher_then_right(racelandshop.system.ha_version, MINIMUM_HA_VERSION):
        racelandshop.log.critical(
            "You need HA version %s or newer to use this integration.",
            MINIMUM_HA_VERSION,
        )
        return False
    return True
