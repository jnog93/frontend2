"""Class for themes in RACELANDSHOP."""
from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.information import find_file_name


class RacelandshopTheme(RacelandshopRepository):
    """Themes in RACELANDSHOP."""

    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.category = RacelandshopCategory.THEME
        self.content.path.remote = "themes"
        self.content.path.local = self.localpath
        self.content.single = False

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.racelandshop.core.config_path}/themes/{self.data.file_name.replace('.yaml', '')}"

    async def async_post_installation(self):
        """Run post installation steps."""
        try:
            await self.racelandshop.hass.services.async_call("frontend", "reload_themes", {})
        except (Exception, BaseException):  # pylint: disable=broad-except
            pass

    async def validate_repository(self):
        """Validate."""
        # Run common validation steps.
        await self.common_validate()

        # Custom step 1: Validate content.
        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith("themes/") and treefile.endswith(".yaml"):
                compliant = True
                break
        if not compliant:
            raise RacelandshopException(
                f"Repostitory structure for {self.ref.replace('tags/','')} is not compliant"
            )

        if self.data.content_in_root:
            self.content.path.remote = ""

        # Handle potential errors
        if self.validate.errors:
            for error in self.validate.errors:
                if not self.racelandshop.status.startup:
                    self.logger.error("%s %s", self, error)
        return self.validate.success

    async def async_post_registration(self):
        """Registration."""
        # Set name
        find_file_name(self)
        self.content.path.local = self.localpath

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
            return

        # Get theme objects.
        if self.data.content_in_root:
            self.content.path.remote = ""

        # Update name
        find_file_name(self)
        self.content.path.local = self.localpath
