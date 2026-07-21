import webbrowser
import urllib.parse


def run(query):

    text = urllib.parse.quote(query)

    webbrowser.open(
        f"https://www.google.com/search?q={text}"
    )

    return f"Đang tìm '{query}' trên Google."