"""Class for integrations in RACELANDSHOP."""
from homeassistant.loader import async_get_custom_components

from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.filters import (
    get_first_directory_in_directory,
)
from custom_components.racelandshop.helpers.functions.information import (
    get_integration_manifest,
)


class RacelandshopIntegration(RacelandshopRepository):
    """Integrations in RACELANDSHOP."""

    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.category = RacelandshopCategory.INTEGRATION
        self.content.path.remote = "custom_components"
        self.content.path.local = self.localpath

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.racelandshop.core.config_path}/custom_components/{self.data.domain}"

    async def async_post_installation(self):
        """Run post installation steps."""
        if self.data.config_flow:
            if self.data.full_name != "racelandshop/integration":
                await self.reload_custom_components()
            if self.data.first_install:
                self.pending_restart = False
                return
        self.pending_restart = True

    async def validate_repository(self):
        """Validate."""
        await self.common_validate()

        # Custom step 1: Validate content.
        if self.data.content_in_root:
            self.content.path.remote = ""

        if self.content.path.remote == "custom_components":
            name = get_first_directory_in_directory(self.tree, "custom_components")
            if name is None:
                raise RacelandshopException(
                    f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
                )
            self.content.path.remote = f"custom_components/{name}"

        try:
            await get_integration_manifest(self)
        except RacelandshopException as exception:
            if self.racelandshop.system.action:
                raise RacelandshopException(f"::error:: {exception}") from exception
            self.logger.error("%s %s", self, exception)

        # Handle potential errors
        if self.validate.errors:
            for error in self.validate.errors:
                if not self.racelandshop.status.startup:
                    self.logger.error("%s %s", self, error)
        return self.validate.success

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
            return

        if self.data.content_in_root:
            self.content.path.remote = ""

        if self.content.path.remote == "custom_components":
            name = get_first_directory_in_directory(self.tree, "custom_components")
            self.content.path.remote = f"custom_components/{name}"

        try:
            await get_integration_manifest(self)
        except RacelandshopException as exception:
            self.logger.error("%s %s", self, exception)

        # Set local path
        self.content.path.local = self.localpath

    async def reload_custom_components(self):
        """Reload custom_components (and config flows)in HA."""
        self.logger.info("Reloading custom_component cache")
        del self.racelandshop.hass.data["custom_components"]
        await async_get_custom_components(self.racelandshop.hass)
        self.logger.info("Custom_component cache reloaded")
