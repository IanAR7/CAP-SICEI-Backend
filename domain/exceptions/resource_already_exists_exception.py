class ResourceAlreadyExistsException(Exception):
    """
    Exception raised when a resource already exists.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
