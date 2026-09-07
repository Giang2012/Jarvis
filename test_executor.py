from dataclasses import dataclass
from ai.executor import Executor

@dataclass
class FakeTask:
    action: str
    target: str = ""

class FakePlanner:
    def __init__(self):
        self.calls = []
    def execute(self, action, target):
        self.calls.append((action, target))
        if action == "FAIL":
            raise RuntimeError("simulated failure")
        return f"OK:{action}:{target}"

def main():
    planner = FakePlanner()
    executor = Executor(planner)
    results = executor.execute([
        FakeTask("open", "notepad"),
        FakeTask("search_web", "python"),
        FakeTask("fail", "demo"),
        FakeTask("close", "notepad"),
    ])
    assert planner.calls == [
        ("OPEN_APP", "notepad"),
        ("SEARCH", "python"),
        ("FAIL", "demo"),
        ("CLOSE_APP", "notepad"),
    ]
    assert results[0] == "OK:OPEN_APP:notepad"
    assert results[1] == "OK:SEARCH:python"
    assert results[2] == "Task FAIL failed: RuntimeError: simulated failure"
    assert results[3] == "OK:CLOSE_APP:notepad"
    assert executor.summary()["total"] == 4
    assert executor.summary()["successful"] == 3
    assert executor.summary()["failed"] == 1
    print("EXECUTOR TEST PASSED")
    print("Summary:", executor.summary())

if __name__ == "__main__":
    main()
