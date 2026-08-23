import subprocess

from skills.base_skill import BaseSkill


class CloseAppSkill(BaseSkill):

    name = "CLOSE_APP"

    APPS = {
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",

        "edge": "msedge.exe",

        "notepad": "notepad.exe",

        "paint": "mspaint.exe",

        "cmd": "cmd.exe",

        "vscode": "Code.exe",
        "vs code": "Code.exe",

        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
    }

    def execute(self, text):

        text = text.lower().strip()

        for name, process in self.APPS.items():

            if name in text:

                result = subprocess.run(
                    [
                        "taskkill",
                        "/F",
                        "/IM",
                        process
                    ],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:

                    return f"Đã đóng {name}."

                return f"{name} hiện không chạy."

        return "Tôi không nhận diện được ứng dụng cần đóng."