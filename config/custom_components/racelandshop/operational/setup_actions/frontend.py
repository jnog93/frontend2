from racelandshop_frontend.version import VERSION as FE_VERSION
from racelandshop_frontend import locate_dir

from custom_components.racelandshop.helpers.functions.logger import getLogger
from custom_components.racelandshop.webresponses.frontend import RacelandshopFrontendDev
from custom_components.racelandshop.helpers.functions.information import get_frontend_version
from custom_components.racelandshop.share import get_racelandshop

from ...enums import RacelandshopSetupTask


URL_BASE = "/racelandshopfiles"


async def async_setup_frontend():
    """Configure the RACELANDSHOP frontend elements."""
    racelandshop = get_racelandshop()
    racelandshop.log.info("Setup task %s", RacelandshopSetupTask.FRONTEND)
    hass = racelandshop.hass

    # Register themes
    hass.http.register_static_path(f"{URL_BASE}/themes", hass.config.path("themes"))

    # Register frontend
    if racelandshop.configuration.frontend_repo_url:
        getLogger().warning(
            "Frontend development mode enabled. Do not run in production."
        )
        hass.http.register_view(RacelandshopFrontendDev())
    else:
        #
        hass.http.register_static_path(
            f"{URL_BASE}/frontend", locate_dir(), cache_headers=False
        )

    # Custom iconset
    hass.http.register_static_path(
        f"{URL_BASE}/iconset.js", str(racelandshop.integration_dir / "iconset.js")
    )
    if "frontend_extra_module_url" not in hass.data:
        hass.data["frontend_extra_module_url"] = set()
    hass.data["frontend_extra_module_url"].add("/racelandshopfiles/iconset.js")

    # Register www/community for all other files
    use_cache = racelandshop.core.lovelace_mode == "storage"
    racelandshop.log.info(
        "%s mode, cache for /racelandshopfiles/: %s",
        racelandshop.core.lovelace_mode,
        use_cache,
    )
    hass.http.register_static_path(
        URL_BASE,
        hass.config.path("www/community"),
        cache_headers=use_cache,
    )

    racelandshop.frontend.version_running = FE_VERSION
    racelandshop.frontend.version_expected = await hass.async_add_executor_job(
        get_frontend_version
    )

    # Add to sidepanel
    if "racelandshop" not in hass.data.get("frontend_panels", {}):
        hass.components.frontend.async_register_built_in_panel(
            component_name="custom",
            sidebar_title=racelandshop.configuration.sidepanel_title,
            sidebar_icon=racelandshop.configuration.sidepanel_icon,
            frontend_url_path="racelandshop",
            config={
                "_panel_custom": {
                    "name": "racelandshop-frontend",
                    "embed_iframe": True,
                    "trust_external": False,
                    "js_url": f"/racelandshopfiles/frontend/entrypoint.js?racelandshoptag={FE_VERSION}",
                }
            },
            require_admin=True,
        )
