from google import genai

from config.settings import GEMINI_API_KEY


class AIManager:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def ask(self, prompt):

        try:

            response = self.client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            return response.text

        except Exception as e:

            return str(e)