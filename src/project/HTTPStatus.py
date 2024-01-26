from enum import IntEnum


class HTTPStatus(IntEnum):
    """HTTP status codes"""

    def __new__(cls, value, phrase, description=""):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        obj.description = description
        return obj

    @property
    def is_informational(self):
        return 100 <= self <= 199

    @property
    def is_success(self):
        return 200 <= self <= 299

    @property
    def is_redirection(self):
        return 300 <= self <= 399

    @property
    def is_client_error(self):
        return 400 <= self <= 499

    @property
    def is_server_error(self):
        return 500 <= self <= 599

    # informational
    CONTINUE = 100, "Continue", "Request received, please continue"
    SWITCHING_PROTOCOLS = (
        101,
        "Switching Protocols",
        "Switching to new protocol; obey Upgrade header",
    )

    # success
    OK = 200, "OK", "Request fulfilled, document follows"
    CREATED = 201, "Created", "Document created, URL follows"
    ACCEPTED = (202, "Accepted", "Request accepted, processing continues off-line")

    # redirection
    MULTIPLE_CHOICES = (
        300,
        "Multiple Choices",
        "Object has several resources -- see URI list",
    )
    MOVED_PERMANENTLY = (
        301,
        "Moved Permanently",
        "Object moved permanently -- see URI list",
    )

    # client error
    BAD_REQUEST = (400, "Bad Request", "Bad request syntax or unsupported method")
    UNAUTHORIZED = (401, "Unauthorized", "No permission -- see authorization schemes")
    PAYMENT_REQUIRED = (402, "Payment Required", "No payment -- see charging schemes")
    FORBIDDEN = (403, "Forbidden", "Request forbidden -- authorization will not help")
    NOT_FOUND = (404, "Not Found", "Nothing matches the given URI")

    # server errors
    INTERNAL_SERVER_ERROR = (
        500,
        "Internal Server Error",
        "Server got itself in trouble",
    )
    NOT_IMPLEMENTED = (501, "Not Implemented", "Server does not support this operation")
    BAD_GATEWAY = (502, "Bad Gateway", "Invalid responses from another server/proxy")
