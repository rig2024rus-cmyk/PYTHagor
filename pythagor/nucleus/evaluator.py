"""Вычислитель PYTHagor. Фаза 1.4.
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
    Kenosis,
    Krisis,
    Onoma,
    Statement,
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

def run_statement(stmt: Statement, ousia: runtime.Ousia) -> Value | None:
    """Выполняет оператор, обновляет ousia, возвращает значение результата."""
    if isinstance(stmt, Horos):
        value = eval_expr(stmt.value, ousia)
        ousia.declare(stmt.name, value)
        return value
    if isinstance(stmt, Thesis):
        value = eval_expr(stmt.value, ousia)
        ousia.assign(stmt.name, value)
        return value
    if isinstance(stmt, Krisis):
        condition = eval_expr(stmt.condition, ousia)
        branch = stmt.then_branch if condition.b else stmt.else_branch
        if branch is not None:
            ousia.enter_scope()
            try:
                for s in branch:
                    run_statement(s, ousia)
            finally:
                ousia.exit_scope()
        return None
    if isinstance(stmt, Kenosis):
        return None
    if isinstance(stmt, Expr):
        return eval_expr(stmt, ousia)
    raise TypeError(f"неизвестный оператор: {type(stmt).__name__}")


def run(cosmos: Cosmos) -> Value:
    """Проверяет типы, затем вычисляет операторы по порядку.
    При рассогласовании типов рантайм не стартует.
    Возвращает значение последнего оператора.
    """
    checker.check(cosmos)
    ousia = runtime.Ousia()
    result: Value | None = None
    for stmt in cosmos.statements:
        result = run_statement(stmt, ousia)
    assert result is not None, "программа без операторов"
    return result
