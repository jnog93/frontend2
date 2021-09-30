"""RACELANDSHOP System info."""
from typing import Optional
import attr

from ..const import INTEGRATION_VERSION
from ..enums import RacelandshopStage


@attr.s
class RacelandshopSystem:
    """RACELANDSHOP System info."""

    disabled: bool = False
    disabled_reason: Optional[str] = None
    running: bool = False
    version: str = INTEGRATION_VERSION
    stage: RacelandshopStage = attr.ib(RacelandshopStage)
    action: bool = False
