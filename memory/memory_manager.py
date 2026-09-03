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

        # Context hiện tại của JARVIS
        self.context = {
            "last_app": None,
            "last_search": None,
            "last_topic": None,
        }

    # =========================================================
    # SHORT MEMORY
    # =========================================================

    def remember(self, role, text):

        self.short.add(
            role,
            text
        )

    def history(self):

        return self.short.history()

    # =========================================================
    # CONTEXT
    # =========================================================

    def set_context(self, key, value):

        self.context[key] = value

    def get_context(self, key):

        return self.context.get(key)

    # =========================================================
    # LONG MEMORY
    # =========================================================

    def save(self, key, value):

        self.long.save(
            key,
            value
        )

    def load(self):

        return self.long.load()

    # =========================================================
    # USER MEMORY
    # =========================================================

    def set_user(self, key, value):

        self.user.set(
            key,
            value
        )

    def get_user(self, key):

        return self.user.get(
            key
        )

    # =========================================================
    # PROJECT MEMORY
    # =========================================================

    def update_project(self, name, status):

        self.project.update(
            name,
            status
        )

    def get_project(self, name):

        return self.project.get(name)