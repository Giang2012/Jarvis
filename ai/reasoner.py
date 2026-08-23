from ai.plan import Plan
from ai.task import Task


class Reasoner:

    def build(self, text):

        text = text.lower().strip()

        plan = Plan()

        # =========================
        # MULTI COMMAND
        # =========================

        parts = []

        for separator in [
            " rồi ",
            " sau đó ",
            " và "
        ]:
            if separator in text:
                parts = [
                    part.strip()
                    for part in text.split(separator)
                    if part.strip()
                ]
                break

        if not parts:
            parts = [text]

        # =========================
        # BUILD TASKS
        # =========================

        for part in parts:

            # OPEN APP
            if any(word in part for word in [
                "mở",
                "chạy",
                "khởi động",
                "open",
                "launch"
            ]):

                plan.add(
                    Task(
                        action="OPEN_APP",
                        target=part
                    )
                )

            # CLOSE APP
            elif any(word in part for word in [
                "đóng",
                "tắt ứng dụng",
                "close",
                "thoát"
            ]):

                plan.add(
                    Task(
                        action="CLOSE_APP",
                        target=part
                    )
                )

            # SEARCH
            elif any(word in part for word in [
                "tìm",
                "tìm kiếm",
                "search",
                "google",
                "tra cứu"
            ]):

                plan.add(
                    Task(
                        action="SEARCH",
                        target=part
                    )
                )

            # SYSTEM
            elif any(word in part for word in [
                "tắt máy",
                "shutdown",
                "tắt hệ thống",
                "khởi động lại",
                "restart",
                "reboot"
            ]):

                plan.add(
                    Task(
                        action="SYSTEM",
                        target=part
                    )
                )

            # CALCULATOR
            elif any(word in part for word in [
                "tính",
                "calculate",
                "calculator"
            ]):

                plan.add(
                    Task(
                        action="CALCULATOR",
                        target=part
                    )
                )

            # UNKNOWN → CHAT
            else:

                plan.add(
                    Task(
                        action="CHAT",
                        target=part
                    )
                )

        return plan