class ResourceNotFoundException(Exception):
    """Exception raised when a resource is not found."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
