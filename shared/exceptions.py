class AlreadyExistsError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

class TokenValidationError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)   

class WrongCredentialsError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)

class EmptyError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)    

class MissingError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
