from enum import Enum


class JarvisMode(Enum):
    IDLE = "Idle"
    CHAT = "Chat"
    CODING = "Coding"
    LEARNING = "Learning"
    GAMING = "Gaming"


class AIStatus(Enum):
    READY = "Ready"
    LISTENING = "Listening"
    THINKING = "Thinking"
    SPEAKING = "Speaking"
    ERROR = "Error"


class JarvisState:

    def __init__(self):

        self.mode = JarvisMode.IDLE

        self.status = AIStatus.READY

        self.cpu = 0

        self.ram = 0

        self.mic_active = False

        self.ai_online = False

        self.user_name = "Chủ nhân"

        self.current_skill = None                               