class IntentRecognizer:

    def detect(self, text):

        text = text.lower()

        if any(word in text for word in ["mở", "chạy", "khởi động"]):
            return "OPEN_APP"

        if any(word in text for word in ["thời tiết", "nhiệt độ"]):
            return "WEATHER"

        if any(word in text for word in ["nhớ", "ghi nhớ"]):
            return "SAVE_MEMORY"

        return "CHAT"