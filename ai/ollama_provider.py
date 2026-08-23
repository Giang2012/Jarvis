import requests
from ai.provider import AIProvider


class OllamaProvider(AIProvider):

    def __init__(
        self,
        url="http://localhost:11434/api/generate",
        model="llama3.2:3b"
    ):
        self.url = url
        self.model = model

    def generate(self, prompt: str):

        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:

            response = requests.post(
                self.url,
                json=data,
                timeout=60
            )

            if response.status_code != 200:
                print(
                    "[OLLAMA ERROR]",
                    response.status_code,
                    response.text
                )

                return "Không thể kết nối tới Ollama."

            result = response.json()

            return result.get(
                "response",
                ""
            )

        except Exception as e:

            print(
                "[OLLAMA ERROR]",
                e
            )

            return "JARVIS không thể kết nối tới AI."
