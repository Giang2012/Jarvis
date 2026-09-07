import re
import unicodedata


class WakeWord:
    """
    Wake word detector for ORION.

    Primary wake words:
        ORION
        Hey ORION
        OK ORION

    Common STT variations are supported,
    but unrelated Vietnamese phrases are not.
    """

    def __init__(self):
        self.aliases = [
            # Primary
            "hey orion",
            "okay orion",
            "ok orion",
            "orion",

            # Common STT variations
            "hey o ri on",
            "o ri on",
            "ori on",
            "ô ri ôn",
            "ô ri on",
            "ôriôn",
            "orion",
        ]

    def _normalize(self, text):
        text = text.lower().strip()

        text = unicodedata.normalize(
            "NFD",
            text
        )

        text = "".join(
            char
            for char in text
            if unicodedata.category(char) != "Mn"
        )

        text = text.replace("đ", "d")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def extract_command(self, text):
        if not text:
            return None

        normalized = self._normalize(text)

        aliases = sorted(
            self.aliases,
            key=lambda x: len(self._normalize(x)),
            reverse=True,
        )

        for alias in aliases:
            alias_normalized = self._normalize(alias)

            # Wake word đứng một mình
            if normalized == alias_normalized:
                return "xin chào"

            # Wake word + command
            if normalized.startswith(
                alias_normalized + " "
            ):
                command = normalized[
                    len(alias_normalized):
                ].strip()

                return command or "xin chào"

        return None