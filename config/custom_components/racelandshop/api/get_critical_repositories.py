"""API Handler for get_critical_repositories"""
import voluptuous as vol
from homeassistant.components import websocket_api

from custom_components.racelandshop.helpers.functions.store import async_load_from_store


@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "racelandshop/get_critical"})
async def get_critical_repositories(hass, connection, msg):
    """Handle get media player cover command."""
    critical = await async_load_from_store(hass, "critical")
    if not critical:
        critical = []
    connection.send_message(websocket_api.result_message(msg["id"], critical))
