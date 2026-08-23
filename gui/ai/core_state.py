from enum import Enum


class CoreState(Enum):

    IDLE = 0

    LISTENING = 1

    THINKING = 2

    SPEAKING = 3

    ERROR = 4

    SLEEP = 5