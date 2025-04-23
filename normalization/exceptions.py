class InvalidExpression(Exception):
    """Exception raised when an invalid expression is encountered."""
    pass


class InvalidDependency(Exception):
    """Exception raised when a dependency is not valid for a given heading."""
    pass
