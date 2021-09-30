# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring,no-member
from custom_components.racelandshop.helpers.methods import (
    RacelandshopHelperMethods,
    RepositoryHelperMethods,
)
from custom_components.racelandshop.helpers.properties import RepositoryHelperProperties


class RepositoryHelpers(
    RepositoryHelperMethods,
    RepositoryHelperProperties,
):
    """Helper class for repositories"""


class RacelandshopHelpers(RacelandshopHelperMethods):
    """Helper class for RACELANDSHOP"""
