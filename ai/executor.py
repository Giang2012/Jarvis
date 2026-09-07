from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass
class ExecutionResult:
    action: str
    target: str
    success: bool
    result: Any = None
    error: str | None = None
    elapsed_ms: float = 0.0

    def to_text(self) -> str:
        if self.success:
            return "" if self.result is None else str(self.result)
        return f"Task {self.action} failed: {self.error}"


class Executor:
    """Reliable execution layer between Brain/Reasoner and Planner."""

    _ALIASES = {
        "OPEN": "OPEN_APP",
        "CLOSE": "CLOSE_APP",
        "SEARCH_WEB": "SEARCH",
        "SCREEN": "VISION",
    }

    def __init__(self, planner, continue_on_error: bool = True):
        self.planner = planner
        self.continue_on_error = bool(continue_on_error)
        self.last_results: list[ExecutionResult] = []

    @classmethod
    def _normalize_action(cls, action: Any) -> str:
        value = str(action or "").strip().upper()
        return cls._ALIASES.get(value, value)

    @staticmethod
    def _normalize_target(target: Any) -> str:
        return str(target or "").strip()

    @staticmethod
    def _is_task_like(task: Any) -> bool:
        return hasattr(task, "action") and hasattr(task, "target")

    def execute(self, plan: Iterable[Any] | None) -> list[str]:
        """Execute every task in order while preserving Brain's list[str] API."""
        self.last_results = []
        if plan is None:
            return []

        for task in plan:
            if not self._is_task_like(task):
                result = ExecutionResult("UNKNOWN", "", False, error="Invalid task object.")
                self.last_results.append(result)
                if not self.continue_on_error:
                    break
                continue

            action = self._normalize_action(task.action)
            target = self._normalize_target(task.target)

            if not action:
                result = ExecutionResult("UNKNOWN", target, False, error="Task action is empty.")
                self.last_results.append(result)
                if not self.continue_on_error:
                    break
                continue

            started = time.perf_counter()
            try:
                value = self.planner.execute(action, target)
                result = ExecutionResult(
                    action=action,
                    target=target,
                    success=True,
                    result=value,
                    elapsed_ms=(time.perf_counter() - started) * 1000.0,
                )
                self.last_results.append(result)
            except Exception as exc:
                result = ExecutionResult(
                    action=action,
                    target=target,
                    success=False,
                    error=f"{type(exc).__name__}: {exc}",
                    elapsed_ms=(time.perf_counter() - started) * 1000.0,
                )
                self.last_results.append(result)
                if not self.continue_on_error:
                    break

        return [item.to_text() for item in self.last_results]

    def execute_one(self, task) -> str:
        results = self.execute([task])
        return results[0] if results else ""

    def summary(self) -> dict[str, Any]:
        total = len(self.last_results)
        successful = sum(1 for item in self.last_results if item.success)
        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "elapsed_ms": round(sum(item.elapsed_ms for item in self.last_results), 2),
        }
