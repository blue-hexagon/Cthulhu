from enum import Enum


class SenderIdentity(Enum):
    Server = -1
    Client = 1

    def __str__(self) -> int:
        return self.value

    def __int__(self) -> int:
        return self.value

    def matches_identity(self, identity):
        return self.value == identity.value


if __name__ == "__main__":
    # TODO: transfer the same logic to a test file and finish tests for class
    client = SenderIdentity.Client
    server = SenderIdentity.Server
    print(server.matches_identity(SenderIdentity.Server))
