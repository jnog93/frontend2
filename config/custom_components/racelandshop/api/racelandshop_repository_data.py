"""API Handler for racelandshop_repository_data"""
import sys

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from aiogithubapi import AIOGitHubAPIException
from homeassistant.components import websocket_api

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException
from custom_components.racelandshop.helpers.functions.logger import getLogger
from custom_components.racelandshop.helpers.functions.misc import extract_repository_from_url
from custom_components.racelandshop.helpers.functions.register_repository import (
    register_repository,
)
from custom_components.racelandshop.share import get_racelandshop

_LOGGER = getLogger()


@websocket_api.async_response
@websocket_api.websocket_command(
    {
        vol.Required("type"): "racelandshop/repository/data",
        vol.Optional("action"): cv.string,
        vol.Optional("repository"): cv.string,
        vol.Optional("data"): cv.string,
    }
)
async def racelandshop_repository_data(hass, connection, msg):
    """Handle get media player cover command."""
    racelandshop = get_racelandshop()
    repo_id = msg.get("repository")
    action = msg.get("action")
    data = msg.get("data")

    if repo_id is None:
        return

    if action == "add":
        repo_id = extract_repository_from_url(repo_id)
        if repo_id is None:
            return

        if repo_id in racelandshop.common.skip:
            racelandshop.common.skip.remove(repo_id)

        if not racelandshop.get_by_name(repo_id):
            try:
                registration = await register_repository(repo_id, data.lower())
                if registration is not None:
                    raise RacelandshopException(registration)
            except (
                Exception,
                BaseException,
            ) as exception:  # pylint: disable=broad-except
                hass.bus.async_fire(
                    "racelandshop/error",
                    {
                        "action": "add_repository",
                        "exception": str(sys.exc_info()[0].__name__),
                        "message": str(exception),
                    },
                )
        else:
            hass.bus.async_fire(
                "racelandshop/error",
                {
                    "action": "add_repository",
                    "message": f"Repository '{repo_id}' exists in the store.",
                },
            )

        repository = racelandshop.get_by_name(repo_id)
    else:
        repository = racelandshop.get_by_id(repo_id)

    if repository is None:
        hass.bus.async_fire("racelandshop/repository", {})
        return

    _LOGGER.debug("Running %s for %s", action, repository.data.full_name)
    try:
        if action == "set_state":
            repository.state = data

        elif action == "set_version":
            repository.data.selected_tag = data
            await repository.update_repository()

            repository.state = None

        elif action == "install":
            was_installed = repository.data.installed
            repository.data.selected_tag = data
            await repository.update_repository()
            await repository.async_install()
            repository.state = None
            if not was_installed:
                hass.bus.async_fire("racelandshop/reload", {"force": True})

        elif action == "add":
            repository.state = None

        else:
            repository.state = None
            _LOGGER.error("WS action '%s' is not valid", action)

        message = None
    except AIOGitHubAPIException as exception:
        message = exception
    except AttributeError as exception:
        message = f"Could not use repository with ID {repo_id} ({exception})"
    except (Exception, BaseException) as exception:  # pylint: disable=broad-except
        message = exception

    if message is not None:
        _LOGGER.error(message)
        hass.bus.async_fire("racelandshop/error", {"message": str(message)})

    await racelandshop.data.async_write()
    connection.send_message(websocket_api.result_message(msg["id"], {}))
