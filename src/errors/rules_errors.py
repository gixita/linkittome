# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class OneVotePerWordError(Error):
    """Raised when trying to create more than one vote on word."""
    pass


class EverybodyCanVoteError(Error):
    """Raised when the input value is too large"""
    pass


class AllWordsTogetherError(Error):
    """Raised when the input value is too large"""
    pass


class WaitForAdminError(Error):
    """Raised when the input value is too large"""
    pass


class ImmutableVoteError(Error):
    """Raised when trying to modify an immutable vote"""
    pass
