# pylint: disable=missing-docstring,invalid-name
import asyncio

from aiogithubapi import AIOGitHubAPIException

from custom_components.racelandshop.helpers.classes.exceptions import (
    RacelandshopException,
    RacelandshopNotModifiedException,
    RacelandshopRepositoryArchivedException,
)
from custom_components.racelandshop.helpers.functions.logger import getLogger
from custom_components.racelandshop.helpers.functions.register_repository import (
    register_repository,
)

max_concurrent_tasks = asyncio.Semaphore(15)
sleeper = 5

_LOGGER = getLogger()


class RacelandshopTaskFactory:
    def __init__(self):
        self.tasks = []
        self.running = False

    async def safe_common_update(self, repository):
        async with max_concurrent_tasks:
            try:
                await repository.common_update()
            except RacelandshopNotModifiedException:
                pass
            except (AIOGitHubAPIException, RacelandshopException) as exception:
                _LOGGER.error("%s - %s", repository.data.full_name, exception)

            # Due to GitHub ratelimits we need to sleep a bit
            await asyncio.sleep(sleeper)

    async def safe_update(self, repository):
        async with max_concurrent_tasks:
            try:
                await repository.update_repository()
            except RacelandshopNotModifiedException:
                pass
            except RacelandshopRepositoryArchivedException as exception:
                _LOGGER.warning("%s - %s", repository.data.full_name, exception)
            except (AIOGitHubAPIException, RacelandshopException) as exception:
                _LOGGER.error("%s - %s", repository.data.full_name, exception)

            # Due to GitHub ratelimits we need to sleep a bit
            await asyncio.sleep(sleeper)

    async def safe_register(self, repo, category):
        async with max_concurrent_tasks:
            try:
                await register_repository(repo, category)
            except (AIOGitHubAPIException, RacelandshopException) as exception:
                _LOGGER.error("%s - %s", repo, exception)

            # Due to GitHub ratelimits we need to sleep a bit
            await asyncio.sleep(sleeper)
