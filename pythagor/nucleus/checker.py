"""Статическая проверка типов PYTHagor. Фаза 1.3.

Проверка идёт до вычисления: если типы не согласованы,
рантайм не запускается. Сообщение объясняет причину
и указывает место рассогласования.
"""

from __future__ import annotations

from pythagor.nucleus import environment
from pythagor.nucleus.ast import (
    ARITHMETIC_OPS,
    COMPARISON_OPS,
    LOGIC_BIN_OPS,
    Atomos,
    Cosmos,
    Expr,
    Harmonia,
    Horos,
    Onoma,
    Statement,
    Thesis,
    Tropos,
)
from pythagor.nucleus.types import Arithmos, Dilemma, Type


class TypeMismatch(Exception):
    """Рассогласование типов. Выражение не вычисляется."""


def _expect(actual: Type, expected: Type, where: str) -> None:
    if actual != expected:
        raise TypeMismatch(
            f"{where}: ожидался тип {expected.language_name}, "
            f"получен {actual.language_name}"
        )


def infer(expr: Expr, nomos: environment.Nomos) -> Type:
    """Выводит статический тип выражения в контексте nomos."""
    if isinstance(expr, Atomos):
        return expr.typ
    if isinstance(expr, Onoma):
        return nomos.lookup(expr.name)
    if isinstance(expr, Harmonia):
        left = infer(expr.left, nomos)
        right = infer(expr.right, nomos)
        if expr.op in ARITHMETIC_OPS:
            _expect(left, Arithmos(), f"левый операнд '{expr.op}'")
            _expect(right, Arithmos(), f"правый операнд '{expr.op}'")
            return Arithmos()
        if expr.op in COMPARISON_OPS:
            _expect(left, Arithmos(), f"левый операнд '{expr.op}'")
            _expect(right, Arithmos(), f"правый операнд '{expr.op}'")
            return Dilemma()
        if expr.op in LOGIC_BIN_OPS:
            _expect(left, Dilemma(), f"левый операнд '{expr.op}'")
            _expect(right, Dilemma(), f"правый операнд '{expr.op}'")
            return Dilemma()
        raise TypeMismatch(f"неизвестный бинарный оператор '{expr.op}'")
    if isinstance(expr, Tropos):
        if expr.op == "-":
            _expect(infer(expr.operand, nomos), Arithmos(), "операнд унарного '-'")
            return Arithmos()
        if expr.op == "не":
            _expect(infer(expr.operand, nomos), Dilemma(), "операнд 'не'")
            return Dilemma()
        raise TypeMismatch(f"неизвестный унарный оператор '{expr.op}'")
    raise TypeMismatch(f"неизвестный узел выражения: {type(expr).__name__}")


def check_statement(stmt: Statement, nomos: environment.Nomos) -> Type:
    """Проверяет оператор, обновляет nomos, возвращает тип результата."""
    if isinstance(stmt, Horos):
        value_type = infer(stmt.value, nomos)
        _expect(value_type, stmt.typ, f"значение переменной '{stmt.name}'")
        nomos.declare(stmt.name, stmt.typ)
        return stmt.typ
    if isinstance(stmt, Thesis):
        value_type = infer(stmt.value, nomos)
        var_type = nomos.lookup(stmt.name)
        _expect(value_type, var_type, f"присваивание переменной '{stmt.name}'")
        return var_type
    if isinstance(stmt, Expr):
        return infer(stmt, nomos)
    raise TypeMismatch(f"неизвестный оператор: {type(stmt).__name__}")


def check(cosmos: Cosmos) -> Type:
    """Проверяет программу и возвращает тип последнего оператора."""
    nomos = environment.Nomos()
    result_type: Type | None = None
    for stmt in cosmos.statements:
        result_type = check_statement(stmt, nomos)
    assert result_type is not None, "программа без операторов"
    return result_type
