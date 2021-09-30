"""Helper to check if path is safe to remove."""
from pathlib import Path

from custom_components.racelandshop.share import get_racelandshop


def is_safe_to_remove(path: str) -> bool:
    """Helper to check if path is safe to remove."""
    racelandshop = get_racelandshop()
    paths = [
        Path(f"{racelandshop.core.config_path}/{racelandshop.configuration.appdaemon_path}"),
        Path(f"{racelandshop.core.config_path}/{racelandshop.configuration.netdaemon_path}"),
        Path(f"{racelandshop.core.config_path}/{racelandshop.configuration.plugin_path}"),
        Path(f"{racelandshop.core.config_path}/{racelandshop.configuration.python_script_path}"),
        Path(f"{racelandshop.core.config_path}/{racelandshop.configuration.theme_path}"),
        Path(f"{racelandshop.core.config_path}/custom_components/"),
    ]
    if Path(path) in paths:
        return False
    return True
