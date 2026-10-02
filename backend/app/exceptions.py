class DomainError(Exception):
    """A business rule was violated.

    Services raise these instead of HTTPException so they stay independent of
    HTTP. The API layer turns them into responses (see main.py).
    """


class NotFoundError(DomainError):
    """A referenced resource does not exist."""


class ConflictError(DomainError):
    """The request conflicts with existing data (e.g. a duplicate)."""


class BadRequestError(DomainError):
    """The request is well-formed but not allowed."""
