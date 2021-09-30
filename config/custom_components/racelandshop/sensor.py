"""Sensor platform for RACELANDSHOP."""
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from custom_components.racelandshop.const import DOMAIN, INTEGRATION_VERSION, NAME_SHORT
from custom_components.racelandshop.share import get_racelandshop


async def async_setup_platform(
    _hass, _config, async_add_entities, _discovery_info=None
):
    """Setup sensor platform."""
    async_add_entities([RACELANDSHOPSensor()])


async def async_setup_entry(_hass, _config_entry, async_add_devices):
    """Setup sensor platform."""
    async_add_devices([RACELANDSHOPSensor()])


class RACELANDSHOPDevice(Entity):
    """RACELANDSHOP Device class."""

    @property
    def device_info(self):
        """Return device information about RACELANDSHOP."""
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME_SHORT,
            "manufacturer": "racelandshop.xyz",
            "model": "",
            "sw_version": INTEGRATION_VERSION,
            "entry_type": "service",
        }


class RACELANDSHOPSensor(RACELANDSHOPDevice):
    """RACELANDSHOP Sensor class."""

    def __init__(self):
        """Initialize."""
        self._state = None
        self.repositories = []

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    async def async_update(self):
        """Manual updates of the sensor."""
        self._update()

    @callback
    def _update_and_write_state(self, *_):
        """Update the sensor and write state."""
        self._update()
        self.async_write_ha_state()

    @callback
    def _update(self):
        """Update the sensor."""
        racelandshop = get_racelandshop()
        if racelandshop.status.background_task:
            return

        self.repositories = []

        for repository in racelandshop.repositories:
            if (
                repository.pending_upgrade
                and repository.data.category in racelandshop.common.categories
            ):
                self.repositories.append(repository)
        self._state = len(self.repositories)

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return (
            "0717a0cd-745c-48fd-9b16-c8534c9704f9-bc944b0f-fd42-4a58-a072-ade38d1444cd"
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "racelandshop"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "racelandshop:racelandshop"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "pending update(s)"

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        repositories = []
        for repository in self.repositories:
            repositories.append(
                {
                    "name": repository.data.full_name,
                    "display_name": repository.display_name,
                    "installed_version": repository.display_installed_version,
                    "available_version": repository.display_available_version,
                }
            )
        return {"repositories": repositories}

    async def async_added_to_hass(self) -> None:
        """Register for status events."""
        self.async_on_remove(
            self.hass.bus.async_listen("racelandshop/status", self._update_and_write_state)
        )
