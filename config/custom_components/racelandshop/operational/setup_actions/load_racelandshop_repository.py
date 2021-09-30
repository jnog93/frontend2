"""Starting setup task: load RACELANDSHOP repository."""
from custom_components.racelandshop.const import INTEGRATION_VERSION
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.functions.information import get_repository
from custom_components.racelandshop.helpers.functions.register_repository import (
    register_repository,
)
from custom_components.racelandshop.share import get_racelandshop

from ...enums import RacelandshopSetupTask


async def async_load_racelandshop_repository():
    """Load RACELANDSHOP repositroy."""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Setup task %s", RacelandshopSetupTask.RACELANDSHOP_REPO)

    try:
        repository = racelandshop.get_by_name("racelandshop/integration")
        if repository is None:
            await register_repository("racelandshop/integration", "integration")
            repository = racelandshop.get_by_name("racelandshop/integration")
        if repository is None:
            raise RacelandshopException("Unknown error")
        repository.data.installed = True
        repository.data.installed_version = INTEGRATION_VERSION
        repository.data.new = False
        racelandshop.repo = repository.repository_object
        racelandshop.data_repo, _ = await get_repository(
            racelandshop.session, racelandshop.configuration.token, "racelandshop/default", None
        )
    except RacelandshopException as exception:
        if "403" in f"{exception}":
            racelandshop.log.critical("GitHub API is ratelimited, or the token is wrong.")
        else:
            racelandshop.log.critical(f"[{exception}] - Could not load RACELANDSHOP!")
        return False
    return True
