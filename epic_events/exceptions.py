"""Custom application exceptions."""


class EpicEventsError(Exception):
    """Base exception for Epic Events application."""


class PermissionDeniedError(EpicEventsError):
    """Raised when user does not have permission."""


class InvalidDataError(EpicEventsError):
    """Raised when provided data is invalid."""


class ObjectNotFoundError(EpicEventsError):
    """Raised when an object is not found."""


class BusinessRuleError(EpicEventsError):
    """Raised when a business rule is not respected."""
