"""Интеграционные тесты Задачи 1.4: если/иначе через реальный текст.

Это те пять сценариев из Шага 8 согласованного плана, которые были
обещаны, но отсутствовали в tests/test_task_1_4.py - там Krisis
проверялся только напрямую через Nomos/Ousia или ручным построением
AST, ни разу не пройдя полный путь lexer -> parser -> checker -> evaluator.
Без них баг "evaluator не обрабатывает Krisis вообще" не был бы пойман
проходящим набором тестов.
"""

import pytest

from pythagor.nucleus.checker import TypeMismatch
from pythagor.nucleus.environment import VariableAlreadyDeclared
from pythagor.nucleus.evaluator import run
from pythagor.nucleus.parser import ParserError, parse
from pythagor.nucleus.values import Monada


def test_krisis_upward_mutation_and_read() -> None:
    """Сквозное присваивание и чтение: если-блок не последний оператор."""
    code = "x: Целое = 1\nесли 1 < 2:\ny: Целое = x + 1\nx = 5\nконец\nx"
    assert run(parse(code)) == Monada(5)


def test_krisis_shadowing_forbidden_through_text() -> None:
    """Запрет затенения проверяется и через реальный текст, не только Nomos напрямую."""
    code = "x: Целое = 1\nесли 1 < 2:\nx: Целое = 2\nконец"
    with pytest.raises(VariableAlreadyDeclared):
        run(parse(code))


def test_krisis_unclosed_block_raises_with_position() -> None:
    """Незакрытый если-блок - понятная ошибка парсера с позицией, не общий EOF."""
    code = "если 1 < 2:\nx: Целое = 1"
    with pytest.raises(ParserError):
        parse(code)


def test_krisis_empty_branch_without_pass_raises() -> None:
    """Пустая ветка без 'пропуск' запрещена."""
    code = "если 1 < 2:\nконец"
    with pytest.raises(ParserError):
        parse(code)


def test_krisis_as_last_statement_raises_type_mismatch() -> None:
    """Krisis/Kenosis как последний оператор программы - явная ошибка (Option A)."""
    code = "если 1 < 2:\nпропуск\nконец"
    with pytest.raises(TypeMismatch):
        run(parse(code))


def test_krisis_false_condition_skips_then_branch() -> None:
    """Ветка then не выполняется, если условие ложно и иначе нет."""
    code = "x: Целое = 1\nесли 1 > 2:\nx = 99\nконец\nx"
    assert run(parse(code)) == Monada(1)


def test_krisis_else_branch_executes() -> None:
    """Ветка else выполняется, когда условие ложно."""
    code = "x: Целое = 1\nесли 1 > 2:\nx = 99\nиначе:\nx = 42\nконец\nx"
    assert run(parse(code)) == Monada(42)


def test_krisis_nested() -> None:
    """Вложенные если корректно входят и выходят из областей видимости."""
    code = "x: Целое = 1\nесли 1 < 2:\nесли 2 < 3:\nx = 7\nконец\nконец\nx"
    assert run(parse(code)) == Monada(7)
