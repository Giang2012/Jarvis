from enum import Enum


class Intent(Enum):

    OPEN = "open"

    CLOSE = "close"

    SEARCH = "search"

    CHAT = "chat"

    UNKNOWN = "unknown"