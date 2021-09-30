"""Custom Exceptions."""


class RacelandshopException(Exception):
    """Super basic."""


class RacelandshopRepositoryArchivedException(RacelandshopException):
    """For repositories that are archived."""


class RacelandshopNotModifiedException(RacelandshopException):
    """For responses that are not modified."""


class RacelandshopExpectedException(RacelandshopException):
    """For stuff that are expected."""
