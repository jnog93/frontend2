"""Constants used by multiple Tasmota modules."""
CONF_DISCOVERY_PREFIX = "discovery_prefix"

DATA_REMOVE_DISCOVER_COMPONENT = "raceland_discover_{}"
DATA_UNSUB = "raceland_subscriptions"

DEFAULT_PREFIX = "raceland/discovery"

DOMAIN = "raceland"

PLATFORMS = [
    "binary_sensor",
    "cover",
    "fan",
    "light",
    "sensor",
    "switch",
]

TASMOTA_EVENT = "raceland_event"
