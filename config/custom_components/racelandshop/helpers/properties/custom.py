# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring,no-member
from abc import ABC


class RepositoryPropertyCustom(ABC):
    @property
    def custom(self):
        """Return flag if the repository is custom."""
        if str(self.data.id) in self.racelandshop.common.default:
            return False
        if self.data.full_name == "racelandshop/integration":
            return False
        return True
