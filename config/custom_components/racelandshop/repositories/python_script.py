"""Class for python_scripts in RACELANDSHOP."""
from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.classes.repository import RacelandshopRepository
from custom_components.racelandshop.helpers.functions.information import find_file_name


class RacelandshopPythonScript(RacelandshopRepository):
    """python_scripts in RACELANDSHOP."""

    category = "python_script"

    def __init__(self, full_name):
        """Initialize."""
        super().__init__()
        self.data.full_name = full_name
        self.data.full_name_lower = full_name.lower()
        self.data.category = RacelandshopCategory.PYTHON_SCRIPT
        self.content.path.remote = "python_scripts"
        self.content.path.local = self.localpath
        self.content.single = True

    @property
    def localpath(self):
        """Return localpath."""
        return f"{self.racelandshop.core.config_path}/python_scripts"

    async def validate_repository(self):
        """Validate."""
        # Run common validation steps.
        await self.common_validate()

        # Custom step 1: Validate content.
        if self.data.content_in_root:
            self.content.path.remote = ""

        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith(f"{self.content.path.remote}") and treefile.endswith(
                ".py"
            ):
                compliant = True
                break
        if not compliant:
            raise RacelandshopException(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
            )

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

    async def update_repository(self, ignore_issues=False, force=False):
        """Update."""
        if not await self.common_update(ignore_issues, force):
            return

        # Get python_script objects.
        if self.data.content_in_root:
            self.content.path.remote = ""

        compliant = False
        for treefile in self.treefiles:
            if treefile.startswith(f"{self.content.path.remote}") and treefile.endswith(
                ".py"
            ):
                compliant = True
                break
        if not compliant:
            raise RacelandshopException(
                f"Repository structure for {self.ref.replace('tags/','')} is not compliant"
            )

        # Update name
        find_file_name(self)
