# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring,no-member
from custom_components.racelandshop.helpers.methods.installation import (
    RepositoryMethodInstall,
    RepositoryMethodPostInstall,
    RepositoryMethodPreInstall,
)
from custom_components.racelandshop.helpers.methods.registration import (
    RepositoryMethodPostRegistration,
    RepositoryMethodPreRegistration,
    RepositoryMethodRegistration,
)
from custom_components.racelandshop.helpers.methods.reinstall_if_needed import (
    RepositoryMethodReinstallIfNeeded,
)


class RepositoryHelperMethods(
    RepositoryMethodReinstallIfNeeded,
    RepositoryMethodInstall,
    RepositoryMethodPostInstall,
    RepositoryMethodPreInstall,
    RepositoryMethodPreRegistration,
    RepositoryMethodRegistration,
    RepositoryMethodPostRegistration,
):
    """Collection of repository methods that are nested to all repositories."""


class RacelandshopHelperMethods:
    """Helper class for RACELANDSHOP methods"""
