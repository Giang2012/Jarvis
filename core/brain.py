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
from services.desktop_service import DesktopService
from services.screen_service import ScreenService
from services.screen_observer import ScreenObserver
from services.file_service import FileService
from services.media_service import MediaService
from services.clipboard_service import ClipboardService
from memory.memory_manager import MemoryManager
from core.mode_manager import ModeManager


class Brain(QObject):
    stateChanged = Signal(str)
    replyReady = Signal(str)
    screenObserved = Signal(object)

    def __init__(self):
        super().__init__()
        self.memory = MemoryManager()
        self.mode_manager = ModeManager()
        self.services = ServiceManager()
        for name, service in (
            ("app", AppService()), ("browser", BrowserService()), ("system", SystemService()),
            ("desktop", DesktopService()), ("screen", ScreenService()), ("files", FileService()),
            ("media", MediaService()), ("clipboard", ClipboardService()),
        ):
            self.services.register(name, service)
        self.services.start_all()
        self.intent = IntentRecognizer()
        self.reasoner = Reasoner()
        self.planner = Planner(self.services)
        self.executor = Executor(self.planner)
        self.ai = AIManager(provider="ollama")
        self.screen_observer = ScreenObserver(self.services.get("screen"), interval=5, callback=self._on_screen_observed)

    def set_state(self, state):
        self.stateChanged.emit(state)

    def process(self, text):
        text = str(text or "").strip()
        if not text:
            return ""
        self.set_state("LISTENING")
        self.intent.detect(text)
        self.set_state("THINKING")
        plan = self.reasoner.build(text)
        results = self.executor.execute(plan)
        valid = [str(x) for x in results if x is not None]
        reply = self.ai.ask(text) if (not valid or any(t.action == "CHAT" for t in plan)) else "\n".join(valid)
        self.set_state("READY")
        self.replyReady.emit(str(reply))
        return str(reply)

    def inspect_screen(self, semantic=False):
        service = self.services.get("screen")
        return service.inspect(semantic=semantic) if service else {"error": "Screen service unavailable."}

    def enable_screen_awareness(self, semantic=False, interval=5):
        self.screen_observer.interval = max(1.0, float(interval))
        self.screen_observer.start(semantic=semantic)
        return "Screen awareness enabled."

    def disable_screen_awareness(self):
        self.screen_observer.stop()
        return "Screen awareness disabled."

    def system_status(self):
        service = self.services.get("system")
        return service.status() if service else {"error": "System service unavailable."}

    def _on_screen_observed(self, result):
        self.screenObserved.emit(result)

    def shutdown(self):
        try:
            self.screen_observer.stop()
        except Exception:
            pass
        try:
            self.services.stop_all()
        except Exception:
            pass
