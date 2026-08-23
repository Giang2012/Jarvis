from skills.base_skill import BaseSkill


class SystemSkill(BaseSkill):

    name = "SYSTEM"

    def __init__(self, system_service=None):

        self.system = system_service

    def execute(self, text):

        text = text.lower()

        if self.system is None:

            return "System Service chưa sẵn sàng."

        if any(word in text for word in [
            "tắt máy",
            "shutdown",
            "tắt hệ thống"
        ]):

            self.system.shutdown()

            return "Đang tắt máy."

        if any(word in text for word in [
            "khởi động lại",
            "restart",
            "reboot"
        ]):

            self.system.restart()

            return "Đang khởi động lại hệ thống."

        return "Không nhận diện được lệnh hệ thống."