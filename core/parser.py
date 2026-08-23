from dataclasses import dataclass

from core.intent import Intent


@dataclass
class Command:

    intent: Intent

    target: str = ""

    raw: str = ""


class Parser:

    def parse(self, text):

        text = text.strip()

        lower = text.lower()

        if lower.startswith("mở "):

            return Command(
                Intent.OPEN,
                text[3:].strip(),
                text
            )

        if lower.startswith("đóng "):

            return Command(
                Intent.CLOSE,
                text[5:].strip(),
                text
            )

        if lower.startswith("tìm "):

            return Command(
                Intent.SEARCH,
                text[4:].strip(),
                text
            )

        return Command(
            Intent.CHAT,
            text,
            text
        )