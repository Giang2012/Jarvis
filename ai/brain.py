from PySide6.QtCore import QObject, Signal

from ai.intent import IntentRecognizer
from ai.reasoner import Reasoner
from ai.executor import Executor
from ai.planner import Planner
from ai.ai_manager import AIManager

from memory.memory_manager import MemoryManager


class Brain(QObject):

    stateChanged = Signal(str)
    replyReady = Signal(str)

    def __init__(self, services):

        super().__init__()

        self.services = services

        # =====================================================
        # MEMORY
        # =====================================================

        self.memory = MemoryManager()

        # =====================================================
        # AI CORE
        # =====================================================

        self.intent = IntentRecognizer()

        self.reasoner = Reasoner(
            self.intent
        )

        # =====================================================
        # SKILLS
        # =====================================================

        self.planner = Planner(
            self.services
        )

        self.executor = Executor(
            self.planner
        )

        # =====================================================
        # LLM
        # =====================================================

        self.ai = AIManager(
            provider="ollama"
        )

    # =========================================================
    # STATE
    # =========================================================

    def set_state(self, state):

        self.stateChanged.emit(state)

    # =========================================================
    # MEMORY
    # =========================================================

    def remember_user(self, text):

        self.memory.short.add(
            "user",
            text
        )

    def remember_ai(self, text):

        self.memory.short.add(
            "assistant",
            text
        )

    # =========================================================
    # PROCESS
    # =========================================================

    def process(self, text):

        text = text.strip()

        if not text:
            return ""

        # -----------------------------------------------------
        # USER MEMORY
        # -----------------------------------------------------

        self.remember_user(text)

        # -----------------------------------------------------
        # LISTENING
        # -----------------------------------------------------

        self.set_state(
            "LISTENING"
        )

        # -----------------------------------------------------
        # INTENT
        # -----------------------------------------------------

        intent = self.intent.detect(
            text
        )

        print(
            f"[JARVIS] Intent: {intent}"
        )

        # -----------------------------------------------------
        # THINKING
        # -----------------------------------------------------

        self.set_state(
            "THINKING"
        )

        # -----------------------------------------------------
        # BUILD PLAN
        # -----------------------------------------------------

        plan = self.reasoner.build(
            text
        )

        print(
            "[JARVIS] Plan:",
            [
                {
                    "action": task.action,
                    "target": task.target
                }
                for task in plan
            ]
        )

        # -----------------------------------------------------
        # EXECUTE
        # -----------------------------------------------------

        results = []

        if plan:

            results = self.executor.execute(
                plan
            )

        # -----------------------------------------------------
        # CLEAN RESULTS
        # -----------------------------------------------------

        valid_results = [
            str(result)
            for result in results
            if result is not None
            and str(result).strip()
        ]

        # -----------------------------------------------------
        # CHAT / FALLBACK
        # -----------------------------------------------------

        should_chat = (
            not valid_results
            or any(
                task.action == "CHAT"
                for task in plan
            )
        )

        if should_chat:

            reply = self.ai.ask(
                text
            )

        else:

            reply = "\n".join(
                valid_results
            )

        # -----------------------------------------------------
        # REMEMBER RESPONSE
        # -----------------------------------------------------

        self.remember_ai(
            str(reply)
        )

        # -----------------------------------------------------
        # READY
        # -----------------------------------------------------

        self.set_state(
            "READY"
        )

        self.replyReady.emit(
            str(reply)
        )

        return str(reply)