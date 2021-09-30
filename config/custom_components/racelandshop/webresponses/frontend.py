from aiohttp import web

from homeassistant.components.http import HomeAssistantView
from custom_components.racelandshop.share import get_racelandshop


class RacelandshopFrontendDev(HomeAssistantView):
    """Dev View Class for RACELANDSHOP."""

    requires_auth = False
    name = "racelandshop_files:frontend"
    url = r"/racelandshopfiles/frontend/{requested_file:.+}"

    async def get(self, request, requested_file):  # pylint: disable=unused-argument
        """Handle RACELANDSHOP Web requests."""
        racelandshop = get_racelandshop()
        requested = requested_file.split("/")[-1]
        request = await racelandshop.session.get(
            f"{racelandshop.configuration.frontend_repo_url}/{requested}"
        )
        if request.status == 200:
            result = await request.read()
            response = web.Response(body=result)
            response.headers["Content-Type"] = "application/javascript"

            return response
