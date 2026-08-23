from memory.short_memory import ShortMemory
from memory.long_memory import LongMemory
from memory.project_memory import ProjectMemory
from memory.user_memory import UserMemory


class MemoryManager:

    def __init__(self):

        self.short = ShortMemory()

        self.long = LongMemory()

        self.project = ProjectMemory()

        self.user = UserMemory()