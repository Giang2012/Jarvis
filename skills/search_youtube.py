import webbrowser
import urllib.parse


def run(query):

    text = urllib.parse.quote(query)

    webbrowser.open(
        f"https://www.youtube.com/results?search_query={text}"
    )

    return f"Đang tìm '{query}' trên YouTube."