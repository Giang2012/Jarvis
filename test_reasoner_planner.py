from ai.reasoner import Reasoner
from ai.planner import Planner


class FakeSkill:
    def __init__(self, name):
        self.name = name
        self.calls = []

    def execute(self, command):
        self.calls.append(command)
        return f"EXECUTED:{command}"


class FakeRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill):
        self.skills[skill.name.upper()] = skill

    def find(self, name):
        return self.skills.get(name.upper())


def test_reasoner_multi_step():
    reasoner = Reasoner()
    plan = reasoner.build("mở chrome rồi tìm Python rồi chụp màn hình")

    tasks = list(plan)

    assert [task.action for task in tasks] == [
        "OPEN_APP",
        "SEARCH",
        "SCREENSHOT",
    ]
    assert tasks[0].target == "chrome"
    assert tasks[1].target == "python"


def test_reasoner_chat():
    plan = Reasoner().build("xin chào ORION")
    tasks = list(plan)

    assert len(tasks) == 1
    assert tasks[0].action == "CHAT"


def test_planner_routing():
    planner = Planner.__new__(Planner)
    planner.registry = FakeRegistry()

    search = FakeSkill("SEARCH")
    planner.registry.register(search)

    result = planner.execute("SEARCH", "python")

    assert result == "EXECUTED:python"
    assert search.calls == ["python"]


def test_planner_missing_skill():
    planner = Planner.__new__(Planner)
    planner.registry = FakeRegistry()

    result = planner.execute("NOT_REGISTERED", "demo")

    assert result == "No skill registered for action: NOT_REGISTERED"


def main():
    test_reasoner_multi_step()
    test_reasoner_chat()
    test_planner_routing()
    test_planner_missing_skill()
    print("REASONER + PLANNER TEST PASSED")


if __name__ == "__main__":
    main()
