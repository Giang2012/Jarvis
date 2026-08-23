from dataclasses import dataclass


@dataclass
class Task:

    action: str

    target: str = ""

    data: dict | None = None