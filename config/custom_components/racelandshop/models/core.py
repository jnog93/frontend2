"""RACELANDSHOP Core info."""
from pathlib import Path

import attr

from ..enums import LovelaceMode


@attr.s
class RacelandshopCore:
    """RACELANDSHOP Core info."""

    config_path = attr.ib(Path)
    ha_version = attr.ib(str)
    lovelace_mode = LovelaceMode("yaml")
