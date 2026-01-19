from domain.errors.base_errors import DomainError


class UserAlreadyExists(DomainError):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"User with email {email} already exists")


class InvalidCredentials(DomainError):
    def __init__(self, reason: str = "Invalid credentials") -> None:
        super().__init__(reason)
