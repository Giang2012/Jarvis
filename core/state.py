from enum import Enum


class AIState(Enum):

    READY = "READY"

    LISTENING = "LISTENING"

    THINKING = "THINKING"

    EXECUTING = "EXECUTING"

    SPEAKING = "SPEAKING"

    ERROR = "ERROR"