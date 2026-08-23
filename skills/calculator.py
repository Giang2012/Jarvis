import ast
import operator

from skills.base_skill import BaseSkill


class CalculatorSkill(BaseSkill):

    name = "CALCULATOR"

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def execute(self, text):

        expression = text.lower()

        prefixes = [
            "tính",
            "calculate",
            "calculator"
        ]

        for prefix in prefixes:

            if expression.startswith(prefix):

                expression = expression[
                    len(prefix):
                ].strip()

                break

        if not expression:

            return "Bạn muốn tôi tính gì?"

        try:

            tree = ast.parse(
                expression,
                mode="eval"
            )

            result = self._evaluate(
                tree.body
            )

            return str(result)

        except Exception:

            return "Biểu thức không hợp lệ."

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float)
            ):

                return node.value

            raise ValueError

        if isinstance(node, ast.BinOp):

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError

            return operation(
                left,
                right
            )

        if isinstance(node, ast.UnaryOp):

            value = self._evaluate(
                node.operand
            )

            operation = self.OPERATORS.get(
                type(node.op)
            )

            if operation is None:

                raise ValueError

            return operation(value)

        raise ValueError