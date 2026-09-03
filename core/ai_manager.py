from ai.ollama_provider import OllamaProvider
from ai.gemini_provider import GeminiProvider
from ai.conversation import Conversation
from ai.prompt import SYSTEM_PROMPT


class AIManager:

    def __init__(
        self,
        provider="ollama",
        memory=None,
        memory_intelligence=None
    ):

        self.memory = memory

        self.memory_intelligence = (
            memory_intelligence
        )

        self.conversation = Conversation(
            memory
        )

        if provider == "gemini":

            self.provider = GeminiProvider()

        else:

            self.provider = OllamaProvider()

    # =========================================================
    # ASK
    # =========================================================

    def ask(self, text):

        # -----------------------------------------------------
        # MEMORY INTELLIGENCE
        # -----------------------------------------------------

        if self.memory_intelligence is not None:

            self.memory_intelligence.process(
                text
            )

        # -----------------------------------------------------
        # CONVERSATION
        # -----------------------------------------------------

        self.conversation.add_user(
            text
        )

        # -----------------------------------------------------
        # MEMORY CONTEXT
        # -----------------------------------------------------

        memory_context = ""

        if self.memory_intelligence is not None:

            memory_context = (
                self.memory_intelligence.build_context()
            )

        # -----------------------------------------------------
        # PROMPT
        # -----------------------------------------------------

        prompt = SYSTEM_PROMPT

        if memory_context:

            prompt += (
                "\n\n"
                + memory_context
            )

        prompt += (
            "\n\n"
            + self.conversation.build_prompt()
        )

        # -----------------------------------------------------
        # AI
        # -----------------------------------------------------

        reply = self.provider.generate(
            prompt
        )

        # -----------------------------------------------------
        # SAVE RESPONSE
        # -----------------------------------------------------

        self.conversation.add_ai(
            reply
        )

        return reply