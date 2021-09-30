"""Class for netdaemon apps in RACELANDSHOP."""
from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.filters import (
    get_first_directory_in_directory,
)


class RacelandshopNetdaemon(RacelandshopRepository):
    """Netdaemon apps in RACELANDSHOP."""

    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.category = RacelandshopCategory.NETDAEMON
        self.content.path.local = self.localpath
        self.content.path.remote = "apps"

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.racelandshop.core.config_path}/netdaemon/apps/{self.data.name}"

    async def validate_repository(self):
        """Validate."""
        await self.common_validate()

        # Custom step 1: Validate content.
        if self.repository_manifest:
            if self.data.content_in_root:
                self.content.path.remote = ""

        if self.content.path.remote == "apps":
            self.data.domain = get_first_directory_in_directory(
                self.tree, self.content.path.remote
            )
            self.content.path.remote = f"apps/{self.data.name}"

        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith(f"{self.content.path.remote}") and treefile.endswith(
                ".cs"
            ):
                compliant = True
                break
        if not compliant:
            raise RacelandshopException(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
            )

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

        # Get appdaemon objects.
        if self.repository_manifest:
            if self.data.content_in_root:
                self.content.path.remote = ""

        if self.content.path.remote == "apps":
            self.data.domain = get_first_directory_in_directory(
                self.tree, self.content.path.remote
            )
            self.content.path.remote = f"apps/{self.data.name}"

        # Set local path
        self.content.path.local = self.localpath

    async def async_post_installation(self):
        """Run post installation steps."""
        try:
            await self.racelandshop.hass.services.async_call(
                "hassio", "addon_restart", {"addon": "c6a2317c_netdaemon"}
            )
        except (Exception, BaseException):  # pylint: disable=broad-except
            pass
