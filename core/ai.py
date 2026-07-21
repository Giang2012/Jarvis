import os

API_KEY = os.getenv("GEMINI_API_KEY")
class AI:

    def chat(self, message):

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=message,
        )

        return response.text