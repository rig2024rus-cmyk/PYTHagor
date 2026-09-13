import pytest

from pythagor.nucleus.ast import Atomos, Kenosis, Krisis
from pythagor.nucleus.environment import Nomos, VariableAlreadyDeclared
from pythagor.nucleus.evaluator import run
from pythagor.nucleus.lexer import Lexer, TokenType
from pythagor.nucleus.parser import parse
from pythagor.nucleus.runtime import Ousia
from pythagor.nucleus.types import Arithmos, Dilemma
from pythagor.nucleus.values import Dyada, Monada


def test_crlf_line_endings() -> None:
    code = "x: Целое = 5\r\ny: Целое = x + 1\r\ny"
    assert run(parse(code)) == Monada(6)


def test_new_keywords_tokens() -> None:
    tokens = Lexer("если иначе конец пропуск").tokenize()
    assert [t.typ for t in tokens[:-1]] == [
        TokenType.IF,
        TokenType.ELSE,
        TokenType.END,
        TokenType.PASS,
    ]


def test_shadowing_forbidden_in_nomos() -> None:
    nomos = Nomos()
    nomos.declare("x", Arithmos())
    nomos.enter_scope()
    with pytest.raises(VariableAlreadyDeclared):
        nomos.declare("x", Arithmos())


def test_nomos_lookup_through_stack() -> None:
    nomos = Nomos()
    nomos.declare("x", Arithmos())
    nomos.enter_scope()
    assert nomos.lookup("x") == Arithmos()
    nomos.exit_scope()
    assert nomos.lookup("x") == Arithmos()


def test_ousia_lookup_through_stack() -> None:
    ousia = Ousia()
    ousia.declare("x", Monada(1))
    ousia.enter_scope()
    assert ousia.lookup("x") == Monada(1)


def test_ousia_assign_through_stack() -> None:
    ousia = Ousia()
    ousia.declare("x", Monada(1))
    ousia.enter_scope()
    ousia.assign("x", Monada(5))
    ousia.exit_scope()
    assert ousia.lookup("x") == Monada(5)


def test_exit_scope_from_global_forbidden() -> None:
    nomos = Nomos()
    with pytest.raises(RuntimeError):
        nomos.exit_scope()
    ousia = Ousia()
    with pytest.raises(RuntimeError):
        ousia.exit_scope()


def test_krisis_node_holds_branches() -> None:
    cond = Atomos(Dyada(True), Dilemma())
    then_branch = (Kenosis(),)
    else_branch = (Kenosis(),)
    krisis = Krisis(cond, then_branch, else_branch)
    assert krisis.condition == cond
    assert krisis.then_branch == then_branch
    assert krisis.else_branch == else_branch


def test_krisis_else_branch_optional() -> None:
    krisis = Krisis(Atomos(Dyada(False), Dilemma()), (Kenosis(),))
    assert krisis.else_branch is None


def test_paren_newline_suppressed() -> None:
    assert run(parse("(2 +\n3) * 2")) == Monada(10)
