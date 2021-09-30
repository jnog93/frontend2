"""Base RACELANDSHOP class."""
import logging
from typing import List, Optional, TYPE_CHECKING
import pathlib

import attr
from aiogithubapi.github import AIOGitHubAPI
from aiogithubapi.objects.repository import AIOGitHubAPIRepository
from homeassistant.core import HomeAssistant

from .enums import RacelandshopDisabledReason, RacelandshopStage
from .helpers.functions.logger import getLogger
from .racelandshopbase.configuration import Configuration
from .models.core import RacelandshopCore
from .models.frontend import RacelandshopFrontend
from .models.system import RacelandshopSystem

if TYPE_CHECKING:
    from .helpers.classes.repository import RacelandshopRepository


class RacelandshopCommon:
    """Common for RACELANDSHOP."""

    categories: List = []
    default: List = []
    installed: List = []
    skip: List = []


class RacelandshopStatus:
    """RacelandshopStatus."""

    startup: bool = True
    new: bool = False
    background_task: bool = False
    reloading_data: bool = False
    upgrading_all: bool = False


@attr.s
class RacelandshopBaseAttributes:
    """Base RACELANDSHOP class."""

    _default: Optional[AIOGitHubAPIRepository]
    _github: Optional[AIOGitHubAPI]
    _hass: Optional[HomeAssistant]
    _configuration: Optional[Configuration]
    _repository: Optional[AIOGitHubAPIRepository]
    _stage: RacelandshopStage = RacelandshopStage.SETUP
    _common: Optional[RacelandshopCommon]

    core: RacelandshopCore = attr.ib(RacelandshopCore)
    common: RacelandshopCommon = attr.ib(RacelandshopCommon)
    status: RacelandshopStatus = attr.ib(RacelandshopStatus)
    frontend: RacelandshopFrontend = attr.ib(RacelandshopFrontend)
    log: logging.Logger = getLogger()
    system: RacelandshopSystem = attr.ib(RacelandshopSystem)
    repositories: List["RacelandshopRepository"] = []


@attr.s
class RacelandshopBase(RacelandshopBaseAttributes):
    """Base RACELANDSHOP class."""

    @property
    def stage(self) -> RacelandshopStage:
        """Returns a RacelandshopStage object."""
        return self._stage

    @stage.setter
    def stage(self, value: RacelandshopStage) -> None:
        """Set the value for the stage property."""
        self._stage = value

    @property
    def github(self) -> Optional[AIOGitHubAPI]:
        """Returns a AIOGitHubAPI object."""
        return self._github

    @github.setter
    def github(self, value: AIOGitHubAPI) -> None:
        """Set the value for the github property."""
        self._github = value

    @property
    def repository(self) -> Optional[AIOGitHubAPIRepository]:
        """Returns a AIOGitHubAPIRepository object representing racelandshop/integration."""
        return self._repository

    @repository.setter
    def repository(self, value: AIOGitHubAPIRepository) -> None:
        """Set the value for the repository property."""
        self._repository = value

    @property
    def default(self) -> Optional[AIOGitHubAPIRepository]:
        """Returns a AIOGitHubAPIRepository object representing racelandshop/default."""
        return self._default

    @default.setter
    def default(self, value: AIOGitHubAPIRepository) -> None:
        """Set the value for the default property."""
        self._default = value

    @property
    def hass(self) -> Optional[HomeAssistant]:
        """Returns a HomeAssistant object."""
        return self._hass

    @hass.setter
    def hass(self, value: HomeAssistant) -> None:
        """Set the value for the default property."""
        self._hass = value

    @property
    def configuration(self) -> Optional[Configuration]:
        """Returns a Configuration object."""
        return self._configuration

    @configuration.setter
    def configuration(self, value: Configuration) -> None:
        """Set the value for the default property."""
        self._configuration = value

    @property
    def integration_dir(self) -> pathlib.Path:
        """Return the RACELANDSHOP integration dir."""
        return pathlib.Path(__file__).parent

    def disable(self, reason: RacelandshopDisabledReason) -> None:
        """Disable RACELANDSHOP."""
        self.system.disabled = True
        self.system.disabled_reason = reason
        self.log.error("RACELANDSHOP is disabled - %s", reason)

    def enable(self) -> None:
        """Enable RACELANDSHOP."""
        self.system.disabled = False
        self.system.disabled_reason = None
        self.log.info("RACELANDSHOP is enabled")
