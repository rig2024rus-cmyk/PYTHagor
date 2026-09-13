import pytest

from pythagor.nucleus.ast import Atomos, Cosmos, Harmonia, Tropos
from pythagor.nucleus.types import Arithmos, Dilemma
from pythagor.nucleus.values import Dyada, Monada


def test_atomos_valid_pairs() -> None:
    assert Atomos(Monada(5), Arithmos()).value == Monada(5)
    assert Atomos(Dyada(True), Dilemma()).value == Dyada(True)


def test_atomos_rejects_mismatch() -> None:
    with pytest.raises(TypeError):
        Atomos(Monada(5), Dilemma())
    with pytest.raises(TypeError):
        Atomos(Dyada(True), Arithmos())


def test_harmonia_rejects_unknown_op() -> None:
    a = Atomos(Monada(1), Arithmos())
    with pytest.raises(ValueError):
        Harmonia(a, "%", a)


def test_tropos_rejects_unknown_op() -> None:
    a = Atomos(Monada(1), Arithmos())
    with pytest.raises(ValueError):
        Tropos("!", a)


def test_cosmos_holds_expr() -> None:
    a = Atomos(Monada(1), Arithmos())
    b = Atomos(Monada(2), Arithmos())
    cosmos = Cosmos(Harmonia(a, "+", b))
    assert isinstance(cosmos.statements[0], Harmonia)
