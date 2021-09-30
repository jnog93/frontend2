"""API Handler for racelandshop_settings"""
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components import websocket_api

from custom_components.racelandshop.helpers.functions.logger import getLogger
from custom_components.racelandshop.share import get_racelandshop

_LOGGER = getLogger()


@websocket_api.async_response
@websocket_api.websocket_command(
    {
        vol.Required("type"): "racelandshop/settings",
        vol.Optional("action"): cv.string,
        vol.Optional("categories"): cv.ensure_list,
    }
)
async def racelandshop_settings(hass, connection, msg):
    """Handle get media player cover command."""
    racelandshop = get_racelandshop()

    action = msg["action"]
    _LOGGER.debug("WS action '%s'", action)

    if action == "set_fe_grid":
        racelandshop.configuration.frontend_mode = "Grid"

    elif action == "onboarding_done":
        racelandshop.configuration.onboarding_done = True

    elif action == "set_fe_table":
        racelandshop.configuration.frontend_mode = "Table"

    elif action == "set_fe_compact_true":
        racelandshop.configuration.frontend_compact = False

    elif action == "set_fe_compact_false":
        racelandshop.configuration.frontend_compact = True

    elif action == "clear_new":
        for repo in racelandshop.repositories:
            if repo.data.new and repo.data.category in msg.get("categories", []):
                _LOGGER.debug(
                    "Clearing new flag from '%s'",
                    repo.data.full_name,
                )
                repo.data.new = False
    else:
        _LOGGER.error("WS action '%s' is not valid", action)
    hass.bus.async_fire("racelandshop/config", {})
    await racelandshop.data.async_write()
    connection.send_message(websocket_api.result_message(msg["id"], {}))
