"""
JARVIS Backend Smoke Test
-------------------------
Chay:
    python test_backend.py

Muc tieu:
- Kiem tra import cac backend module.
- Kiem tra IntentRecognizer.
- Kiem tra Reasoner -> Plan.
- Kiem tra Executor -> Planner routing.
- Kiem tra multi-step command.
- Kiem tra Executor bat loi ma khong lam crash pipeline.
- Co the chay ma khong mo app, tat may, chup man hinh hay goi Ollama.

Khong can pytest.
"""

from __future__ import annotations

import importlib
import sys
import traceback


PASS = 0
FAIL = 0
SKIP = 0


def check(name, fn):
    global PASS, FAIL, SKIP
    try:
        result = fn()
        if result is False:
            raise AssertionError("check returned False")
        print(f"[PASS] {name}")
        PASS += 1
        return True
    except SkipTest as exc:
        print(f"[SKIP] {name} -> {exc}")
        SKIP += 1
        return True
    except Exception as exc:
        print(f"[FAIL] {name} -> {type(exc).__name__}: {exc}")
        FAIL += 1
        if "--traceback" in sys.argv:
            traceback.print_exc()
        return False


class SkipTest(Exception):
    pass


def test_imports():
    modules = [
        "ai.intent",
        "ai.reasoner",
        "ai.plan",
        "ai.task",
        "ai.executor",
        "ai.planner",
        "core.brain",
    ]

    errors = []

    for module_name in modules:
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            errors.append(f"{module_name}: {type(exc).__name__}: {exc}")

    if errors:
        raise AssertionError("Backend import errors:\n  " + "\n  ".join(errors))


def test_intent():
    from ai.intent import IntentRecognizer

    recognizer = IntentRecognizer()

    cases = {
        "tính 25*8": "CALCULATOR",
        "mở chrome": "OPEN_APP",
        "đóng chrome": "CLOSE_APP",
        "tìm kiếm black hole": "SEARCH",
        "thời tiết hôm nay": "WEATHER",
        "giải thích cho tôi black hole là gì": "CHAT",
        "khởi động lại máy": "SYSTEM_RESTART",
        "tắt máy": "SYSTEM_SHUTDOWN",
    }

    for text, expected in cases.items():
        actual = recognizer.detect(text)
        assert actual == expected, (
            f"Intent sai cho {text!r}: "
            f"expected={expected!r}, actual={actual!r}"
        )


def test_reasoner_basic():
    from ai.reasoner import Reasoner

    reasoner = Reasoner()

    cases = {
        "mở chrome": ("OPEN_APP", "chrome"),
        "đóng chrome": ("CLOSE_APP", "chrome"),
        "tìm kiếm black hole": ("SEARCH", "black hole"),
        "tính 25*8": ("CALCULATOR", "tính 25*8"),
        "giải thích cho tôi black hole là gì": (
            "CHAT",
            "giải thích cho tôi black hole là gì",
        ),
    }

    for text, (expected_action, expected_target) in cases.items():
        plan = reasoner.build(text)
        tasks = list(plan)

        assert len(tasks) == 1, f"{text!r}: expected 1 task, got {len(tasks)}"
        task = tasks[0]

        assert task.action == expected_action, (
            f"{text!r}: expected action {expected_action!r}, "
            f"got {task.action!r}"
        )
        assert task.target == expected_target, (
            f"{text!r}: expected target {expected_target!r}, "
            f"got {task.target!r}"
        )


def test_reasoner_multistep():
    from ai.reasoner import Reasoner

    reasoner = Reasoner()

    plan = reasoner.build(
        "mở chrome rồi tìm kiếm black hole rồi tính 25*8"
    )
    tasks = list(plan)

    assert len(tasks) == 3, f"expected 3 tasks, got {len(tasks)}"

    expected = [
        ("OPEN_APP", "chrome"),
        ("SEARCH", "black hole"),
        ("CALCULATOR", "tính 25*8"),
    ]

    actual = [(task.action, task.target) for task in tasks]
    assert actual == expected, f"multistep mismatch: {actual!r}"


class RecordingPlanner:
    """Fake planner: records routing without touching Windows."""

    def __init__(self):
        self.calls = []

    def execute(self, action, target):
        self.calls.append((action, target))
        return f"OK:{action}:{target}"


class FailingPlanner:
    def execute(self, action, target):
        raise RuntimeError("intentional smoke-test failure")


def test_executor_routing():
    from ai.executor import Executor
    from ai.plan import Plan
    from ai.task import Task

    planner = RecordingPlanner()
    executor = Executor(planner)

    plan = Plan()
    plan.add(Task("OPEN_APP", "chrome"))
    plan.add(Task("SEARCH", "black hole"))
    plan.add(Task("CALCULATOR", "tính 25*8"))

    results = executor.execute(plan)

    expected_calls = [
        ("OPEN_APP", "chrome"),
        ("SEARCH", "black hole"),
        ("CALCULATOR", "tính 25*8"),
    ]

    assert planner.calls == expected_calls, (
        f"planner routing mismatch: {planner.calls!r}"
    )

    assert results == [
        "OK:OPEN_APP:chrome",
        "OK:SEARCH:black hole",
        "OK:CALCULATOR:tính 25*8",
    ]


def test_executor_error_handling():
    from ai.executor import Executor
    from ai.plan import Plan
    from ai.task import Task

    executor = Executor(FailingPlanner())

    plan = Plan()
    plan.add(Task("OPEN_APP", "this-is-not-really-opened"))

    results = executor.execute(plan)

    assert len(results) == 1
    assert "Task OPEN_APP failed:" in str(results[0])
    assert "intentional smoke-test failure" in str(results[0])


def test_reasoner_executor_integration():
    from ai.reasoner import Reasoner
    from ai.executor import Executor

    reasoner = Reasoner()
    planner = RecordingPlanner()
    executor = Executor(planner)

    plan = reasoner.build("mở chrome rồi tìm black hole")
    results = executor.execute(plan)

    assert planner.calls == [
        ("OPEN_APP", "chrome"),
        ("SEARCH", "black hole"),
    ]

    assert results == [
        "OK:OPEN_APP:chrome",
        "OK:SEARCH:black hole",
    ]


def test_empty_input_contract():
    from ai.reasoner import Reasoner

    plan = Reasoner().build("")
    assert len(list(plan)) == 0


def test_brain_process_contract():
    """
    Contract-only check.

    Khong tao Brain() vi constructor hien tai khoi dong services,
    screen observer va AI manager. Smoke test backend khong nen tu y
    mo app, truy cap man hinh hoac goi Ollama.
    """
    module = importlib.import_module("core.brain")
    Brain = getattr(module, "Brain", None)

    assert Brain is not None
    assert callable(getattr(Brain, "process", None))
    assert callable(getattr(Brain, "shutdown", None))


def main():
    print("=" * 62)
    print(" JARVIS BACKEND SMOKE TEST")
    print("=" * 62)

    checks = [
        ("Backend imports", test_imports),
        ("Intent recognition", test_intent),
        ("Reasoner basic planning", test_reasoner_basic),
        ("Reasoner multi-step planning", test_reasoner_multistep),
        ("Executor routing", test_executor_routing),
        ("Executor error handling", test_executor_error_handling),
        ("Reasoner -> Executor integration", test_reasoner_executor_integration),
        ("Empty input contract", test_empty_input_contract),
        ("Brain process contract", test_brain_process_contract),
    ]

    for name, fn in checks:
        check(name, fn)

    print()
    print("=" * 62)
    print(f"RESULT: PASS={PASS} FAIL={FAIL} SKIP={SKIP}")
    print("=" * 62)

    if FAIL:
        print("BACKEND SMOKE TEST: FAIL")
        return 1

    print("BACKEND SMOKE TEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
