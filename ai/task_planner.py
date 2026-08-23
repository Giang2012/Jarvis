from ai.ai_manager import AIManager


class TaskPlanner:

    def __init__(self):
        self.ai = AIManager(provider="gemini")

    def build_plan(self, text):

        prompt = f"""
Bạn là AI Planner.

Hãy chia yêu cầu dưới đây thành các bước.

Chỉ trả về JSON.

Ví dụ:

[
    {{
        "action":"OPEN_APP",
        "target":"chrome"
    }},
    {{
        "action":"SEARCH",
        "target":"Python"
    }}
]

Yêu cầu:

{text}
"""

        return self.ai.ask(prompt)