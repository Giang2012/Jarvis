import threading
import time


class ScreenObserver:
    """Optional local polling observer.

    It never uploads frames itself. The callback receives the local inspection
    result and the caller decides what to do with it.
    """

    def __init__(self, screen_service, interval=5.0, callback=None):
        self.screen_service = screen_service
        self.interval = max(1.0, float(interval))
        self.callback = callback
        self._stop = threading.Event()
        self._thread = None

    @property
    def running(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self, semantic=False):
        if self.running:
            return
        self._stop.clear()

        def worker():
            while not self._stop.wait(self.interval):
                try:
                    result = self.screen_service.inspect(semantic=semantic)
                    if self.callback:
                        self.callback(result)
                except Exception as exc:
                    if self.callback:
                        self.callback({"error": str(exc)})

        self._thread = threading.Thread(
            target=worker, name="JARVIS-ScreenObserver", daemon=True
        )
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._thread = None
