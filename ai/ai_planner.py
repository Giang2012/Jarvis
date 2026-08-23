
import json
import re

from ai.task import Task
from ai.plan import Plan


class AIPlanner:

    ALLOWED_ACTIONS = {
        "OPEN_APP",
        "CLOSE_APP",
        "SEARCH",
        "CALCULATOR",
        "WEATHER",
        "SYSTEM_SHUTDOWN",
        "SYSTEM_RESTART",
    }

    def __init__(self, ai_manager):

        self.ai = ai_manager

    def build(self, text):

        prompt = f"""
You are JARVIS task planner.

Convert the user's request into JSON.

Allowed actions:
OPEN_APP
CLOSE_APP
SEARCH
CALCULATOR
WEATHER
SYSTEM_SHUTDOWN
SYSTEM_RESTART

Return ONLY valid JSON.

Format:
{{
    "tasks": [
        {{
            "action": "ACTION",
            "target": "TARGET"
        }}
    ]
}}

User request:
{text}
"""

        response = self.ai.provider.generate(prompt)

        return self.parse(response)

    def parse(self, response):

        try:

            match = re.search(
                r'\{.*\}',
                response,
                re.DOTALL
            )

            if not match:
                return None

            data = json.loads(
                match.group()
            )

            plan = Plan()

            for item in data.get(
                "tasks",
                []
            ):

                action = item.get(
                    "action",
                    ""
                ).upper()

                target = item.get(
                    "target",
                    ""
                )

                if action not in self.ALLOWED_ACTIONS:
                    continue

                plan.add(
                    Task(
                        action=action,
                        target=target
                    )
                )

            return plan

        except Exception as e:

            print(
                "[AI PLANNER ERROR]",
                e
            )

            return None

