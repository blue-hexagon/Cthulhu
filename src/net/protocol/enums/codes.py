from enum import Enum
from typing import Tuple


class StatusCode(Enum):
    # Informational
    INITIALIZING = (100, "Initializing the connection.")
    CONNECTION_ESTABLISHED = (101, "Connection successfully established.")
    AUTHENTICATING = (102, "Authenticating the client.")

    # Success
    SUCCESS = (200, "Request successfully processed.")
    OPERATION_COMPLETED = (201, "Operation completed successfully.")
    ACTION_ACCEPTED = (202, "Action accepted for processing.")

    # Redirection
    REDIRECT = (300, "Request redirected.")
    TEMPORARY_REDIRECT = (301, "Temporary redirect.")
    PERMANENT_REDIRECT = (302, "Permanent redirect.")

    # Client Error
    BAD_REQUEST = (400, "The request cannot be fulfilled due to bad syntax.")
    UNAUTHORIZED = (401, "Authentication is required.")
    FORBIDDEN = (403, "The server understood the request, but refuses to authorize it.")
    NOT_FOUND = (404, "The requested resource could not be found.")
    REQUEST_TIMEOUT = (408, "The server timed out waiting for the request.")
    TOO_MANY_REQUESTS = (429, "The user has sent too many requests in a given amount of time.")
    TOKEN_MISMATCH = (450, "Token authentication failed because tokens did not match.")

    # Server Error
    INTERNAL_SERVER_ERROR = (500, "A generic error message, given when an unexpected condition was encountered.")
    SERVICE_UNAVAILABLE = (503, "The server is currently unavailable.")

    @property
    def code(self):
        return self.value[0]

    @property
    def description(self):
        return self.value[1]

    def __get__(self, instance, owner) -> Tuple[int, str]:
        return self.value

    def stringify(self):
        return f"[{self.code}]: {self.description}"


