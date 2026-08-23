from enum import Enum


class AIState(Enum):

    IDLE = 0

    LISTENING = 1

    THINKING = 2

    SPEAKING = 3

    SLEEPING = 4

    ERROR = 5