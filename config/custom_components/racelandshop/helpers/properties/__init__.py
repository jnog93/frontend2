# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring,no-member
from custom_components.racelandshop.helpers.properties.can_be_installed import (
    RepositoryPropertyCanBeInstalled,
)
from custom_components.racelandshop.helpers.properties.custom import RepositoryPropertyCustom
from custom_components.racelandshop.helpers.properties.pending_update import (
    RepositoryPropertyPendingUpdate,
)


class RepositoryHelperProperties(
    RepositoryPropertyPendingUpdate,
    RepositoryPropertyCustom,
    RepositoryPropertyCanBeInstalled,
):
    pass
