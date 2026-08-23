from skills.base_skill import BaseSkill


class OpenAppSkill(BaseSkill):

    name = "OPEN_APP"

    APPS = {
        "chrome": "start chrome",
        "google chrome": "start chrome",

        "edge": "start msedge",
        "microsoft edge": "start msedge",

        "notepad": "notepad",
        "word": "start winword",
        "excel": "start excel",

        "paint": "mspaint",
        "cmd": "cmd",

        "calculator": "calc",

        "vscode": "code",
        "vs code": "code",
        "visual studio code": "code",

        "explorer": "explorer",
        "file explorer": "explorer",
    }

    def __init__(self, app_service=None):

        self.app = app_service

    def execute(self, text):

        text = text.lower().strip()

        # tìm app trong câu lệnh
        for name, command in self.APPS.items():

            if name in text:

                if self.app is not None:

                    success = self.app.open(command)

                else:

                    success = False

                if success:

                    return f"Đã mở {name}."

                return f"Không thể mở {name}."

        return "Tôi không nhận diện được ứng dụng cần mở."