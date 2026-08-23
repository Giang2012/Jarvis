from PySide6.QtCore import QObject, Signal

from ai.intent import IntentRecognizer
from ai.reasoner import Reasoner
from ai.executor import Executor
from ai.planner import Planner
from ai.ai_manager import AIManager


class Brain(QObject):

    stateChanged = Signal(str)
    replyReady = Signal(str)

    def __init__(self, services):

        super().__init__()

        self.services = services

        # =========================
        # AI COMPONENTS
        # =========================

        self.intent = IntentRecognizer()

        self.reasoner = Reasoner()

        # =========================
        # SKILL PLANNER
        # =========================

        self.planner = Planner(
            self.services
        )

        # =========================
        # EXECUTOR
        # =========================

        self.executor = Executor(
            self.planner
        )

        # =========================
        # AI FALLBACK
        # =========================

        self.ai = AIManager(
            provider="ollama"
        )

    # =====================================================
    # STATE
    # =====================================================

    def set_state(self, state):

        self.stateChanged.emit(state)

    # =====================================================
    # PROCESS
    # =====================================================

    def process(self, text):

        text = text.strip()

        if not text:
            return ""

        # =========================
        # LISTENING
        # =========================

        self.set_state("LISTENING")

        # =========================
        # INTENT
        # =========================

        intent = self.intent.detect(
            text
        )

        # =========================
        # THINKING
        # =========================

        self.set_state("THINKING")

        # =========================
        # BUILD PLAN
        # =========================

        plan = self.reasoner.build(
            text
        )

        # =========================
        # EXECUTE
        # =========================

        if plan:

            results = self.executor.execute(
                plan
            )

            if results:

                reply = results[0]

                if reply is not None:

                    reply = str(reply)

                    self.set_state("READY")

                    self.replyReady.emit(
                        reply
                    )

                    return reply

        # =========================
        # AI FALLBACK
        # =========================

        reply = self.ai.ask(
            text
        )

        reply = str(reply)

        self.set_state("READY")

        self.replyReady.emit(
            reply
        )

        return reply