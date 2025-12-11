class NotEnoughArgumentsException(Exception):
    """
    Exception raised when not enough arguments are provided to a function or method.
    """

    def __init__(self, message: str = "Not enough arguments provided."):
        super().__init__(message)
        self.message = message
