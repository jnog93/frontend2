from custom_components.racelandshop.share import SHARE, get_racelandshop


class ValidationException(Exception):
    pass


class ValidationBase:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.racelandshop = get_racelandshop()
        self.failed = False
        self.logger = repository.logger

    def __init_subclass__(cls, category="common", **kwargs) -> None:
        """Initialize a subclass, register if possible."""
        super().__init_subclass__(**kwargs)
        if SHARE["rules"].get(category) is None:
            SHARE["rules"][category] = []
        if cls not in SHARE["rules"][category]:
            SHARE["rules"][category].append(cls)

    @property
    def action_only(self):
        return False

    async def _async_run_check(self):
        """DO NOT OVERRIDE THIS IN SUBCLASSES!"""
        if self.racelandshop.system.action:
            self.logger.info(f"Running check '{self.__class__.__name__}'")
        try:
            await self.racelandshop.hass.async_add_executor_job(self.check)
            await self.async_check()
        except ValidationException as exception:
            self.failed = True
            self.logger.error(exception)

    def check(self):
        pass

    async def async_check(self):
        pass


class ActionValidationBase(ValidationBase):
    @property
    def action_only(self):
        return True
