import pytest

from pythagor.nucleus.ast import Harmonia
from pythagor.nucleus.checker import TypeMismatch, check
from pythagor.nucleus.environment import UndefinedVariable, VariableAlreadyDeclared
from pythagor.nucleus.evaluator import run
from pythagor.nucleus.parser import ParserError, parse
from pythagor.nucleus.types import Dilemma
from pythagor.nucleus.values import Dyada, Monada


def test_precedence_mul_over_add() -> None:
    assert run(parse("2 + 3 * 4")) == Monada(14)


def test_parentheses_change_precedence() -> None:
    assert run(parse("(2 + 3) * 4")) == Monada(20)


def test_unary_minus() -> None:
    assert run(parse("-2 + 3")) == Monada(1)
    assert run(parse("--2")) == Monada(2)


def test_not_with_parentheses() -> None:
    assert run(parse("не (1 < 2)")) == Dyada(False)


def test_and_binds_tighter_than_or() -> None:
    assert run(parse("1 < 2 или 3 < 4 и 5 > 6")) == Dyada(True)


def test_comparison_above_addition() -> None:
    cosmos = parse("1 + 2 < 4")
    assert isinstance(cosmos.statements[0], Harmonia)
    assert cosmos.statements[0].op == "<"
    assert run(cosmos) == Dyada(True)


def test_full_pipeline_type_and_value() -> None:
    cosmos = parse("2 + 3 * 4 < 20 и не (5 > 3)")
    assert check(cosmos) == Dilemma()
    assert run(cosmos) == Dyada(False)


def test_parser_error_missing_operand() -> None:
    with pytest.raises(ParserError):
        parse("2 +")


def test_parser_error_unexpected_token() -> None:
    with pytest.raises(ParserError):
        parse("2 3")


def test_parser_error_unclosed_paren() -> None:
    with pytest.raises(ParserError):
        parse("(2")


def test_error_has_position() -> None:
    with pytest.raises(ParserError) as exc_info:
        parse("2 +\n* 3")
    assert exc_info.value.line == 1
    assert exc_info.value.column == 4


def test_declaration_and_usage() -> None:
    cosmos = parse("x: Целое = 5\nx + 1")
    assert run(cosmos) == Monada(6)


def test_assignment_to_declared_variable() -> None:
    cosmos = parse("x: Целое = 5\nx = 10\nx + 1")
    assert run(cosmos) == Monada(11)


def test_undefined_variable_in_expression() -> None:
    with pytest.raises(UndefinedVariable):
        run(parse("x + 1"))


def test_undefined_variable_in_assignment() -> None:
    with pytest.raises(UndefinedVariable):
        run(parse("x = 1"))


def test_type_mismatch_in_assignment() -> None:
    with pytest.raises(TypeMismatch):
        run(parse("x: Целое = 5\nx = 1 < 2"))


def test_duplicate_declaration() -> None:
    with pytest.raises(VariableAlreadyDeclared):
        run(parse("x: Целое = 5\nx: Целое = 10"))


def test_unknown_type_name() -> None:
    with pytest.raises(ParserError) as exc_info:
        parse("x: Натуральное = 5")
    assert "Натуральное" in str(exc_info.value)


def test_multiple_statements_pipeline() -> None:
    text = "x: Целое = 5\ny: Целое = x + 1\nx + y < 20"
    cosmos = parse(text)
    assert check(cosmos) == Dilemma()
    assert run(cosmos) == Dyada(True)
