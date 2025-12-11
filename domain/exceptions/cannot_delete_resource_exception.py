class CannotDeleteResourceException(Exception):
    """Exception raised when a resource cannot be deleted."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
