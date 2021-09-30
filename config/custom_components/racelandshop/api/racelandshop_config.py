"""API Handler for racelandshop_config"""
import voluptuous as vol
from homeassistant.components import websocket_api

from custom_components.racelandshop.share import get_racelandshop


@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "racelandshop/config"})
async def racelandshop_config(_hass, connection, msg):
    """Handle get media player cover command."""
    racelandshop = get_racelandshop()
    config = racelandshop.configuration

    content = {}
    content["frontend_mode"] = config.frontend_mode
    content["frontend_compact"] = config.frontend_compact
    content["onboarding_done"] = config.onboarding_done
    content["version"] = racelandshop.version
    content["frontend_expected"] = racelandshop.frontend.version_expected
    content["frontend_running"] = racelandshop.frontend.version_running
    content["dev"] = config.dev
    content["debug"] = config.debug
    content["country"] = config.country
    content["experimental"] = config.experimental
    content["categories"] = racelandshop.common.categories

    connection.send_message(websocket_api.result_message(msg["id"], content))
