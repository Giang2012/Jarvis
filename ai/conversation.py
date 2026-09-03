class Conversation:

    def __init__(self, memory=None):

        self.memory = memory

        # Fallback để Conversation vẫn có thể
        # hoạt động độc lập nếu cần.
        self.history = []

    # =========================================================
    # USER
    # =========================================================

    def add_user(self, text):

        if self.memory is not None:

            self.memory.remember(
                "user",
                text
            )

            return

        self.history.append({
            "role": "user",
            "content": text
        })

    # =========================================================
    # AI
    # =========================================================

    def add_ai(self, text):

        if self.memory is not None:

            self.memory.remember(
                "assistant",
                text
            )

            return

        self.history.append({
            "role": "assistant",
            "content": text
        })

    # =========================================================
    # HISTORY
    # =========================================================

    def get_history(self):

        if self.memory is not None:

            return self.memory.history()

        return self.history

    # =========================================================
    # PROMPT
    # =========================================================

    def build_prompt(self):

        prompt = ""

        for msg in self.get_history():

            role = msg.get(
                "role",
                ""
            )

            # MemoryManager dùng "text"
            # Conversation cũ dùng "content"
            content = msg.get(
                "text",
                msg.get("content", "")
            )

            prompt += (
                f"{role}: {content}\n"
            )

        return prompt