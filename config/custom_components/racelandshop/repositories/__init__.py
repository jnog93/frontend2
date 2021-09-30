"""Initialize repositories."""
from custom_components.racelandshop.repositories.appdaemon import RacelandshopAppdaemon
from custom_components.racelandshop.repositories.integration import RacelandshopIntegration
from custom_components.racelandshop.repositories.netdaemon import RacelandshopNetdaemon
from custom_components.racelandshop.repositories.plugin import RacelandshopPlugin
from custom_components.racelandshop.repositories.python_script import RacelandshopPythonScript
from custom_components.racelandshop.repositories.theme import RacelandshopTheme

RERPOSITORY_CLASSES = {
    "theme": RacelandshopTheme,
    "integration": RacelandshopIntegration,
    "python_script": RacelandshopPythonScript,
    "appdaemon": RacelandshopAppdaemon,
    "netdaemon": RacelandshopNetdaemon,
    "plugin": RacelandshopPlugin,
}
