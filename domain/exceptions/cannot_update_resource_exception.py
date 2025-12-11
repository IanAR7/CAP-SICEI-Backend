class CannotUpdateResourceException(Exception):
    """
    Exception raised when a resource cannot be updated.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
