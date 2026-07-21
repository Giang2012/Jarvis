from datetime import datetime


def write(text):

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(
        "logs/jarvis.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"[{now}] {text}\n"
        )