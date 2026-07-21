import requests


class ChatBot:
    def __init__(self):
        self.url = "http://127.0.0.1:11434/api/generate"
        self.model = "qwen2.5:3b"

    def ask(self, prompt):
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.url, json=data, timeout=60)

        if response.status_code != 200:
            return "Không thể kết nối tới Ollama."

        result = response.json()
        return result["response"]