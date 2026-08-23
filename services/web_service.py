import webbrowser


class WebService:

    def search(self, query):

        webbrowser.open(

            "https://www.google.com/search?q="

            + query

        )

        return True