from custom_components.racelandshop.validate.base import (
    ActionValidationBase,
    ValidationException,
)


class RepositoryDescription(ActionValidationBase):
    def check(self):
        if not self.repository.data.description:
            raise ValidationException("The repository has no description")
