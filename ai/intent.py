class IntentRecognizer:

    # =========================================================
    # DETECT
    # =========================================================

    def detect(self, text):

        text = text.lower().strip()

        if not text:
            return "CHAT"

        # =====================================================
        # SYSTEM
        # =====================================================

        if any(
            word in text
            for word in [
                "tắt máy",
                "shutdown",
                "tắt hệ thống",
            ]
        ):
            return "SYSTEM_SHUTDOWN"

        if any(
            word in text
            for word in [
                "khởi động lại",
                "restart",
                "reboot",
            ]
        ):
            return "SYSTEM_RESTART"

        # =====================================================
        # WEATHER
        # =====================================================

        if any(
            word in text
            for word in [
                "thời tiết",
                "nhiệt độ",
                "weather",
                "trời hôm nay",
                "dự báo",
            ]
        ):
            return "WEATHER"

        # =====================================================
        # CLOSE APP
        # =====================================================

        if any(
            word in text
            for word in [
                "đóng",
                "tắt ứng dụng",
                "close",
                "thoát",
            ]
        ):
            return "CLOSE_APP"

        # =====================================================
        # OPEN APP
        # =====================================================

        if any(
            word in text
            for word in [
                "mở",
                "chạy",
                "khởi động",
                "open",
                "launch",
            ]
        ):
            return "OPEN_APP"

        # =====================================================
        # SEARCH
        # =====================================================

        if any(
            word in text
            for word in [
                "tìm",
                "tìm kiếm",
                "search",
                "google",
                "tra cứu",
            ]
        ):
            return "SEARCH"

        # =====================================================
        # CALCULATOR
        # =====================================================

        if any(
            word in text
            for word in [
                "tính",
                "calculator",
                "calculate",
            ]
        ):
            return "CALCULATOR"

        # =====================================================
        # CHAT
        # =====================================================

        return "CHAT"