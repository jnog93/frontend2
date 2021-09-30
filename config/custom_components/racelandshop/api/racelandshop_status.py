"""API Handler for racelandshop_status"""
import voluptuous as vol
from homeassistant.components import websocket_api

from custom_components.racelandshop.share import get_racelandshop


@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "racelandshop/status"})
async def racelandshop_status(_hass, connection, msg):
    """Handle get media player cover command."""
    racelandshop = get_racelandshop()
    content = {
        "startup": racelandshop.status.startup,
        "background_task": racelandshop.status.background_task,
        "lovelace_mode": racelandshop.system.lovelace_mode,
        "reloading_data": racelandshop.status.reloading_data,
        "upgrading_all": racelandshop.status.upgrading_all,
        "disabled": racelandshop.system.disabled,
        "disabled_reason": racelandshop.system.disabled_reason,
        "has_pending_tasks": racelandshop.queue.has_pending_tasks,
        "stage": racelandshop.stage,
    }
    connection.send_message(websocket_api.result_message(msg["id"], content))
