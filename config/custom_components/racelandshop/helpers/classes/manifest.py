"""
Manifest handling of a repository.

https://racelandshop.xyz/docs/publish/start#racelandshopjson
"""
from typing import List

import attr

from custom_components.racelandshop.helpers.classes.exceptions import RacelandshopException


@attr.s(auto_attribs=True)
class RacelandshopManifest:
    """RacelandshopManifest class."""

    name: str = None
    content_in_root: bool = False
    zip_release: bool = False
    filename: str = None
    manifest: dict = {}
    racelandshop: str = None
    hide_default_branch: bool = False
    domains: List[str] = []
    country: List[str] = []
    homeassistant: str = None
    persistent_directory: str = None
    iot_class: str = None
    render_readme: bool = False

    @staticmethod
    def from_dict(manifest: dict):
        """Set attributes from dicts."""
        if manifest is None:
            raise RacelandshopException("Missing manifest data")

        manifest_data = RacelandshopManifest()

        manifest_data.manifest = manifest

        for key in manifest:
            setattr(manifest_data, key, manifest[key])
        return manifest_data
