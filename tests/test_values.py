import pytest

from pythagor.nucleus.values import Dyada, Monada


def test_monada_arithmetic() -> None:
    assert Monada(2).add(Monada(3)) == Monada(5)
    assert Monada(10).sub(Monada(4)) == Monada(6)
    assert Monada(3).mul(Monada(4)) == Monada(12)
    assert Monada(7).neg() == Monada(-7)


def test_monada_comparisons() -> None:
    assert Monada(3).lt(Monada(5)) == Dyada(True)
    assert Monada(5).le(Monada(5)) == Dyada(True)
    assert Monada(7).gt(Monada(3)) == Dyada(True)
    assert Monada(3).ge(Monada(3)) == Dyada(True)
    assert Monada(4).eq(Monada(4)) == Dyada(True)
    assert Monada(4).ne(Monada(5)) == Dyada(True)


def test_dyada_logic() -> None:
    assert Dyada(True).and_op(Dyada(False)) == Dyada(False)
    assert Dyada(True).or_op(Dyada(False)) == Dyada(True)
    assert Dyada(True).not_op() == Dyada(False)
    assert Dyada(False).not_op() == Dyada(True)


def test_type_mismatch_raises() -> None:
    with pytest.raises(TypeError):
        Monada(2).add(Dyada(True))
    with pytest.raises(TypeError):
        Dyada(True).and_op(Monada(3))
