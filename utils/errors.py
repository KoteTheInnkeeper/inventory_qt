class BooleanStateUndefined(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidType(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class DatabaseIntegrityError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class ProductsNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        
class ProductNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class NoProductsSpecified(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class BlankFieldError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)