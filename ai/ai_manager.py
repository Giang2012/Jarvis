from ai.ollama_provider import OllamaProvider
from ai.gemini_provider import GeminiProvider
from ai.conversation import Conversation
from ai.prompt import SYSTEM_PROMPT


class AIManager:

    def __init__(self, provider="ollama"):
        self.conversation = Conversation()

        if provider == "gemini":
            self.provider = GeminiProvider()
        else:
            self.provider = OllamaProvider()

    def ask(self, text):
        self.conversation.add_user(text)

        prompt = SYSTEM_PROMPT + "\n" + self.conversation.build_prompt()

        reply = self.provider.generate(prompt)

        self.conversation.add_ai(reply)

        return reply