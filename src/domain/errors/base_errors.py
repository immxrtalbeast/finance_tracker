class DomainError(Exception):
    """Базовый для доменных ошибок."""


class NotFound(DomainError):
    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} {identifier} not found")


class Forbidden(DomainError):
    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} {identifier} forbidden")
