import pytest

from pythagor.nucleus.ast import Atomos, Cosmos, Harmonia, Tropos
from pythagor.nucleus.checker import TypeMismatch, check
from pythagor.nucleus.evaluator import run
from pythagor.nucleus.types import Arithmos, Dilemma
from pythagor.nucleus.values import Dyada, Monada


def lit(n: int) -> Atomos:
    return Atomos(Monada(n), Arithmos())


def boo(b: bool) -> Atomos:
    return Atomos(Dyada(b), Dilemma())


def test_arithmetic_and_comparison() -> None:
    expr = Harmonia(Harmonia(lit(2), "+", Harmonia(lit(3), "*", lit(4))), "<", lit(20))
    cosmos = Cosmos(expr)
    assert check(cosmos) == Dilemma()
    assert run(cosmos) == Dyada(True)


def test_unary_minus() -> None:
    cosmos = Cosmos(Tropos("-", Harmonia(lit(2), "+", lit(3))))
    assert check(cosmos) == Arithmos()
    assert run(cosmos) == Monada(-5)


def test_logic_operators() -> None:
    expr = Harmonia(Harmonia(boo(True), "и", boo(False)), "или", Tropos("не", boo(False)))
    cosmos = Cosmos(expr)
    assert check(cosmos) == Dilemma()
    assert run(cosmos) == Dyada(True)


def test_mismatch_blocks_runtime() -> None:
    with pytest.raises(TypeMismatch):
        run(Cosmos(Harmonia(lit(2), "и", boo(True))))
    with pytest.raises(TypeMismatch):
        run(Cosmos(Harmonia(lit(2), "+", boo(True))))


def test_unary_minus_on_bool_blocked() -> None:
    with pytest.raises(TypeMismatch):
        run(Cosmos(Tropos("-", boo(True))))
