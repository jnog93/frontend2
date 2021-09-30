from custom_components.racelandshop.validate.base import (
    ActionValidationBase,
    ValidationException,
)


class RepositoryTopics(ActionValidationBase):
    def check(self):
        if not self.repository.data.topics:
            raise ValidationException("The repository has no topics")
