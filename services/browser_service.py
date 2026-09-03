import subprocess
from urllib.parse import quote_plus

from services.base_service import BaseService


class BrowserService(BaseService):

    def start(self):
        return True

    def stop(self):
        return True

    def search(self, text):

        if not text:
            return False

        query = str(text).strip()

        if not query:
            return False

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        try:

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    "",
                    url
                ],
                shell=False
            )

            return True

        except Exception as e:

            print(
                "BrowserService error:",
                e
            )

            return False