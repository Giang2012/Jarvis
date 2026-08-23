import webbrowser
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

        url = (
            "https://www.google.com/search?q="
            + quote_plus(text)
        )

        try:

            return webbrowser.open(url)

        except Exception:

            return False