from PySide6.QtCore import QObject, Signal

from ai.intent import IntentRecognizer
from ai.reasoner import Reasoner
from ai.executor import Executor
from ai.planner import Planner
from ai.ai_manager import AIManager

from services.service_manager import ServiceManager
from services.app_service import AppService
from services.browser_service import BrowserService
from services.system_service import SystemService

from memory.memory_manager import MemoryManager


class Brain(QObject):

    stateChanged = Signal(str)
    replyReady = Signal(str)

    def __init__(self):

        super().__init__()

        # =========================
        # CORE
        # =========================

        self.memory = MemoryManager()

        # =========================
        # SERVICES
        # =========================

        self.services = ServiceManager()

        self.services.register(
            "app",
            AppService()
        )

        self.services.register(
            "browser",
            BrowserService()
        )

        self.services.register(
            "system",
            SystemService()
        )

        self.services.start_all()

        # =========================
        # AI
        # =========================

        self.intent = IntentRecognizer()

        self.reasoner = Reasoner()

        self.planner = Planner(
            self.services
        )

        self.executor = Executor(
            self.planner
        )

        self.ai = AIManager(
            provider="ollama"
        )

    # =========================
    # STATE
    # =========================

    def set_state(self, state):

        self.stateChanged.emit(state)

    # =========================
    # PROCESS
    # =========================

    def process(self, text):

        text = text.strip()

        if not text:
            return ""

        self.set_state("LISTENING")

        # =========================
        # INTENT
        # =========================

        intent = self.intent.detect(text)

        print(
            f"[JARVIS] Intent: {intent}"
        )

        self.set_state("THINKING")

        # =========================
        # BUILD PLAN
        # =========================

        plan = self.reasoner.build(text)

        # =========================
        # EXECUTE PLAN
        # =========================

        results = self.executor.execute(
            plan
        )

        # =========================
        # HANDLE RESULTS
        # =========================

        valid_results = [
            str(result)
            for result in results
            if result is not None
        ]

        # =========================
        # CHAT
        # =========================

        if not valid_results or any(
            task.action == "CHAT"
            for task in plan
        ):

            reply = self.ai.ask(text)

            self.set_state("READY")

            self.replyReady.emit(
                str(reply)
            )

            return str(reply)

        # =========================
        # MULTI-TASK RESPONSE
        # =========================

        reply = "\n".join(
            valid_results
        )

        self.set_state("READY")

        self.replyReady.emit(
            reply
        )

        return reply