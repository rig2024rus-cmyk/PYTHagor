"""Вычислитель PYTHagor. Фаза 1.3.

Вычисление начинается только после пройденной проверки типов.
Значения рантайма: Monada и Dyada. Значения переменных живут в Ousia.
"""

from __future__ import annotations

from pythagor.nucleus import checker, runtime
from pythagor.nucleus.ast import (
    Atomos,
    Cosmos,
    Expr,
    Harmonia,
    Horos,
    Onoma,
    Thesis,
    Tropos,
)
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


def eval_expr(expr: Expr, ousia: runtime.Ousia) -> Value:
    """Вычисляет выражение в контексте значений ousia."""
    if isinstance(expr, Atomos):
        return expr.value
    if isinstance(expr, Onoma):
        return ousia.lookup(expr.name)
    if isinstance(expr, Harmonia):
        left = eval_expr(expr.left, ousia)
        right = eval_expr(expr.right, ousia)
        return getattr(left, BINARY_METHODS[expr.op])(right)
    if isinstance(expr, Tropos):
        operand = eval_expr(expr.operand, ousia)
        if expr.op == "-":
            return operand.neg()
        return operand.not_op()
    raise TypeError(f"неизвестный узел выражения: {type(expr).__name__}")


def run(cosmos: Cosmos) -> Value:
    """Проверяет типы, затем вычисляет операторы по порядку.

    При рассогласовании типов рантайм не стартует.
    Возвращает значение последнего оператора.
    """
    checker.check(cosmos)
    ousia = runtime.Ousia()
    result: Value | None = None
    for stmt in cosmos.statements:
        if isinstance(stmt, (Horos, Thesis)):
            result = eval_expr(stmt.value, ousia)
            ousia.assign(stmt.name, result)
        elif isinstance(stmt, Expr):
            result = eval_expr(stmt, ousia)
        else:
            raise TypeError(f"неизвестный оператор: {type(stmt).__name__}")
    assert result is not None, "программа без операторов"
    return result
