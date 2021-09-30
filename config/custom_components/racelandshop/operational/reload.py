"""Reload RACELANDSHOP"""


async def async_reload_entry(hass, config_entry):
    """Reload RACELANDSHOP."""
    from custom_components.racelandshop.operational.remove import async_remove_entry
    from custom_components.racelandshop.operational.setup import async_setup_entry

    await async_remove_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
