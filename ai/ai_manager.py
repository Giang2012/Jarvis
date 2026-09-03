from ai.ollama_provider import OllamaProvider
from ai.gemini_provider import GeminiProvider
from ai.conversation import Conversation
from ai.prompt import SYSTEM_PROMPT


class AIManager:

    def __init__(
        self,
        provider="ollama",
        memory=None
    ):

        self.memory = memory

        self.conversation = Conversation()

        if provider == "gemini":
            self.provider = GeminiProvider()
        else:
            self.provider = OllamaProvider()

    # =========================================================
    # BUILD MEMORY CONTEXT
    # =========================================================

    def _build_memory_context(self):

        if self.memory is None:
            return ""

        lines = []

        # -----------------------------------------------------
        # USER
        # -----------------------------------------------------

        name = self.memory.get_user("name")

        if name:
            lines.append(
                f"User name: {name}"
            )

        # -----------------------------------------------------
        # PROJECT
        # -----------------------------------------------------

        projects = getattr(
            self.memory.project,
            "projects",
            {}
        )

        if projects:

            for project, status in projects.items():

                lines.append(
                    f"Project: {project} - {status}"
                )

        # -----------------------------------------------------
        # LONG MEMORY
        # -----------------------------------------------------

        try:

            long_memory = self.memory.load()

            if long_memory:

                for key, value in long_memory.items():

                    lines.append(
                        f"{key}: {value}"
                    )

        except Exception:

            pass

        # -----------------------------------------------------
        # SHORT MEMORY
        # -----------------------------------------------------

        try:

            history = self.memory.history()

            if history:

                lines.append(
                    "Recent conversation:"
                )

                for message in history[-10:]:

                    role = message.get(
                        "role",
                        ""
                    )

                    text = message.get(
                        "text",
                        ""
                    )

                    lines.append(
                        f"{role}: {text}"
                    )

        except Exception:

            pass

        if not lines:
            return ""

        return (
            "\n\n"
            "===== JARVIS MEMORY =====\n"
            + "\n".join(lines)
            + "\n===== END MEMORY =====\n"
        )

    # =========================================================
    # ASK
    # =========================================================

    def ask(self, text):

        text = text.strip()

        if not text:
            return ""

        # -----------------------------------------------------
        # SAVE USER MESSAGE
        # -----------------------------------------------------

        if self.memory is not None:

            self.memory.remember(
                "user",
                text
            )

        self.conversation.add_user(
            text
        )

        # -----------------------------------------------------
        # MEMORY
        # -----------------------------------------------------

        memory_context = (
            self._build_memory_context()
        )

        # -----------------------------------------------------
        # PROMPT
        # -----------------------------------------------------

        prompt = (
            SYSTEM_PROMPT
            + memory_context
            + "\n"
            + self.conversation.build_prompt()
        )

        # -----------------------------------------------------
        # AI
        # -----------------------------------------------------

        reply = self.provider.generate(
            prompt
        )

        # -----------------------------------------------------
        # SAVE AI RESPONSE
        # -----------------------------------------------------

        if self.memory is not None:

            self.memory.remember(
                "assistant",
                reply
            )

        self.conversation.add_ai(
            reply
        )

        return reply