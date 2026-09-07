from __future__ import annotations

import ast
import math
import operator
import re
import unicodedata
from typing import Any


class CalculatorSkill:
    """Safe calculator for natural Vietnamese/English math commands."""

    name = "CALCULATOR"

    _BIN_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _UNARY_OPS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    _WORD_REPLACEMENTS = (
        (r"\bnhan\b", "*"),
        (r"\bx\b", "*"),
        (r"\bchia\b", "/"),
        (r"\bcong\b", "+"),
        (r"\btru\b", "-"),
        (r"\bmu\b", "^"),
        (r"\bluy thua\b", "^"),
        (r"\bphay\b", "."),
        (r"\bphan tram\b", "%"),
    )

    def _normalize(self, text: str) -> str:
        text = unicodedata.normalize("NFD", str(text).lower())
        text = "".join(c for c in text if unicodedata.category(c) != "Mn")
        text = text.replace("đ", "d")

        # Remove common conversational wrappers.
        text = re.sub(
            r"\b("
            r"hay|cho toi|cho mình|cho minh|giup toi|giup minh|"
            r"tinh|tinh giup|calculate|what is|what's|bao nhieu|"
            r"ket qua|bang|la bao nhieu"
            r")\b",
            " ",
            text,
        )

        for pattern, replacement in self._WORD_REPLACEMENTS:
            text = re.sub(pattern, replacement, text)

        # Vietnamese decimal/comma and spoken multiplication forms.
        text = text.replace("×", "*").replace("÷", "/")
        text = re.sub(r"(?<=\d),(?=\d)", ".", text)
        text = re.sub(r"\s+", " ", text).strip()

        # '^' means exponent in user speech, but Python AST needs '**'.
        text = text.replace("^", "**")

        # Keep only calculator-relevant characters.
        text = re.sub(r"[^0-9+\-*/%().\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _eval(self, node: ast.AST) -> float | int:
        if isinstance(node, ast.Expression):
            return self._eval(node.body)

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if not math.isfinite(float(node.value)):
                raise ValueError("Số không hợp lệ.")
            return node.value

        if isinstance(node, ast.UnaryOp) and type(node.op) in self._UNARY_OPS:
            return self._UNARY_OPS[type(node.op)](self._eval(node.operand))

        if isinstance(node, ast.BinOp) and type(node.op) in self._BIN_OPS:
            left = self._eval(node.left)
            right = self._eval(node.right)

            if isinstance(node.op, ast.Pow) and abs(float(right)) > 100:
                raise ValueError("Số mũ quá lớn.")

            value = self._BIN_OPS[type(node.op)](left, right)
            if isinstance(value, float) and not math.isfinite(value):
                raise ValueError("Kết quả không hợp lệ.")
            return value

        raise ValueError("Biểu thức không hợp lệ.")

    def _format(self, value: Any) -> str:
        if isinstance(value, float):
            if value.is_integer():
                return str(int(value))
            return f"{value:.12g}"
        return str(value)

    def execute(self, text: str) -> str:
        expression = self._normalize(text)
        if not expression:
            return "Biểu thức không hợp lệ."

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._eval(tree)
            return self._format(result)
        except ZeroDivisionError:
            return "Không thể chia cho 0."
        except (SyntaxError, ValueError, TypeError, OverflowError):
            return "Biểu thức không hợp lệ."
