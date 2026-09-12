"""Вычислитель PYTHagor. Фаза 1.1.

Вычисление начинается только после пройденной проверки типов.
Значения рантайма: Monada и Dyada.
"""

from __future__ import annotations

from pythagor.nucleus import checker
from pythagor.nucleus.ast import Atomos, Cosmos, Expr, Harmonia, Tropos
from pythagor.nucleus.values import Value


BINARY_METHODS = {
    "+": "add",
    "-": "sub",
    "*": "mul",
    "<": "lt",
    "<=": "le",
    ">": "gt",
    ">=": "ge",
    "==": "eq",
    "!=": "ne",
    "и": "and_op",
    "или": "or_op",
}


def eval_expr(expr: Expr) -> Value:
    """Вычисляет выражение, предполагая пройденную проверку типов."""
    if isinstance(expr, Atomos):
        return expr.value
    if isinstance(expr, Harmonia):
        left = eval_expr(expr.left)
        right = eval_expr(expr.right)
        return getattr(left, BINARY_METHODS[expr.op])(right)
    if isinstance(expr, Tropos):
        operand = eval_expr(expr.operand)
        if expr.op == "-":
            return operand.neg()
        return operand.not_op()
    raise TypeError(f"неизвестный узел выражения: {type(expr).__name__}")


def run(cosmos: Cosmos) -> Value:
    """Проверяет типы, затем вычисляет. При рассогласовании рантайм не стартует."""
    checker.check(cosmos)
    return eval_expr(cosmos.expr)
