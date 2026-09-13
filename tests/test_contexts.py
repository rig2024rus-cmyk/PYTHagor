import pytest

from pythagor.nucleus.environment import (
    Nomos,
    UndefinedVariable,
    VariableAlreadyDeclared,
)
from pythagor.nucleus.runtime import Ousia, UndefinedRuntimeVariable
from pythagor.nucleus.types import Arithmos, Dilemma
from pythagor.nucleus.values import Dyada, Monada


def test_nomos_declare_and_lookup() -> None:
    nomos = Nomos()
    nomos.declare("x", Arithmos())
    assert nomos.lookup("x") == Arithmos()


def test_nomos_rejects_duplicate() -> None:
    nomos = Nomos()
    nomos.declare("x", Arithmos())
    with pytest.raises(VariableAlreadyDeclared):
        nomos.declare("x", Dilemma())


def test_nomos_rejects_undefined() -> None:
    nomos = Nomos()
    with pytest.raises(UndefinedVariable):
        nomos.lookup("y")


def test_ousia_assign_and_lookup() -> None:
    ousia = Ousia()
    ousia.declare("x", Monada(5))
    assert ousia.lookup("x") == Monada(5)


def test_ousia_overwrites() -> None:
    ousia = Ousia()
    ousia.declare("x", Monada(5))
    ousia.assign("x", Monada(10))
    assert ousia.lookup("x") == Monada(10)


def test_ousia_rejects_undefined() -> None:
    ousia = Ousia()
    with pytest.raises(UndefinedRuntimeVariable):
        ousia.lookup("y")
