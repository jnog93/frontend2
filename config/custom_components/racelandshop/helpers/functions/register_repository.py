"""Register a repository."""
from aiogithubapi import AIOGitHubAPIException

from custom_components.racelandshop.helpers.classes.exceptions import (
    RacelandshopException,
    RacelandshopExpectedException,
)
from custom_components.racelandshop.share import get_racelandshop

from ...repositories import RERPOSITORY_CLASSES


# @concurrent(15, 5)
async def register_repository(full_name, category, check=True, ref=None):
    """Register a repository."""
    racelandshop = get_racelandshop()

    if full_name in racelandshop.common.skip:
        if full_name != "racelandshop/integration":
            raise RacelandshopExpectedException(f"Skipping {full_name}")

    if category not in RERPOSITORY_CLASSES:
        raise RacelandshopException(f"{category} is not a valid repository category.")

    repository = RERPOSITORY_CLASSES[category](full_name)
    if check:
        try:
            await repository.async_registration(ref)
            if racelandshop.status.new:
                repository.data.new = False
            if repository.validate.errors:
                racelandshop.common.skip.append(repository.data.full_name)
                if not racelandshop.status.startup:
                    racelandshop.log.error("Validation for %s failed.", full_name)
                if racelandshop.system.action:
                    raise RacelandshopException(f"::error:: Validation for {full_name} failed.")
                return repository.validate.errors
            if racelandshop.system.action:
                repository.logger.info("%s Validation completed", repository)
            else:
                repository.logger.info("%s Registration completed", repository)
        except AIOGitHubAPIException as exception:
            racelandshop.common.skip.append(repository.data.full_name)
            raise RacelandshopException(
                f"Validation for {full_name} failed with {exception}."
            ) from None

    if str(repository.data.id) != "0" and (
        exists := racelandshop.get_by_id(repository.data.id)
    ):
        racelandshop.async_remove_repository(exists)

    else:
        if racelandshop.hass is not None and (
            (check and repository.data.new) or racelandshop.status.new
        ):
            racelandshop.hass.bus.async_fire(
                "racelandshop/repository",
                {
                    "action": "registration",
                    "repository": repository.data.full_name,
                    "repository_id": repository.data.id,
                },
            )
    racelandshop.async_add_repository(repository)
