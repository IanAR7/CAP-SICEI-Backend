class CannotCreateException(Exception):
    """Exception raised when a resource cannot be created."""

    def __init__(self, message: str = "Cannot create resource"):
        self.message = message
        super().__init__(self.message)
