from gui.engine.scene import Scene

from gui.objects.ai_object import AIObject
from gui.objects.chrome_object import ChromeObject

from gui.workspace.workspace_manager import WorkspaceManager


class MainScene(Scene):

    def __init__(self):

        super().__init__()

        # Workspace
        self.workspace = WorkspaceManager()

        # AI
        self.ai = AIObject()

        # Tăng kích thước AI Core
        self.ai.transform.setScale(1.55)

        self.add(self.ai)

        # Chrome
        self.chrome = ChromeObject()

        self.workspace.add(self.chrome)

        self.chrome.launch()

    # ----------------------------

    def update(self):

        super().update()

        self.workspace.update()

    # ----------------------------

    def render(self, painter):

        # ==========================================
        # CENTER AI CORE
        # ==========================================

        device = painter.device()

        if device is not None:

            width = device.width()
            height = device.height()

            # Chính giữa màn hình
            self.ai.transform.setPosition(
                width / 2,
                height / 2
            )

        # ==========================================
        # RENDER SCENE
        # ==========================================

        super().render(painter)

        # ==========================================
        # WORKSPACE
        # ==========================================

        self.workspace.render(painter)