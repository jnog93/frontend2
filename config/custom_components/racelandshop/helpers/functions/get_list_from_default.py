"""Helper to get default repositories."""
import json
from typing import List

from aiogithubapi import AIOGitHubAPIException

from custom_components.racelandshop.enums import RacelandshopCategory
from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.share import get_racelandshop


async def async_get_list_from_default(default: RacelandshopCategory) -> List:
    """Get repositories from default list."""
    racelandshop = get_racelandshop()
    repositories = []

    try:
        content = await racelandshop.data_repo.get_contents(
            default, racelandshop.data_repo.default_branch
        )
        repositories = json.loads(content.content)

    except (AIOGitHubAPIException, RacelandshopException) as exception:
        racelandshop.log.error(exception)

    except (Exception, BaseException) as exception:
        racelandshop.log.error(exception)

    racelandshop.log.debug("Got %s elements for %s", len(repositories), default)

    return repositories
