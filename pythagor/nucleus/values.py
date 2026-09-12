"""Значения рантайма PYTHagor. Фаза 1.1.

Monada - неделимая единица количества (целое число).
Dyada - двойственность истина/ложь (булево значение).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Value:
    """Абстрактное значение рантайма PYTHagor."""


@dataclass(frozen=True)
class Monada(Value):
    """Целое число. Поле n хранит значение."""

    n: int

    def add(self, other: Monada) -> Monada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.add ожидает Monada")
        return Monada(self.n + other.n)

    def sub(self, other: Monada) -> Monada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.sub ожидает Monada")
        return Monada(self.n - other.n)

    def mul(self, other: Monada) -> Monada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.mul ожидает Monada")
        return Monada(self.n * other.n)

    def neg(self) -> Monada:
        return Monada(-self.n)

    def lt(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.lt ожидает Monada")
        return Dyada(self.n < other.n)

    def le(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.le ожидает Monada")
        return Dyada(self.n <= other.n)

    def gt(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.gt ожидает Monada")
        return Dyada(self.n > other.n)

    def ge(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.ge ожидает Monada")
        return Dyada(self.n >= other.n)

    def eq(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.eq ожидает Monada")
        return Dyada(self.n == other.n)

    def ne(self, other: Monada) -> Dyada:
        if not isinstance(other, Monada):
            raise TypeError("Monada.ne ожидает Monada")
        return Dyada(self.n != other.n)


@dataclass(frozen=True)
class Dyada(Value):
    """Булево значение. Поле b хранит значение."""

    b: bool

    def and_op(self, other: Dyada) -> Dyada:
        if not isinstance(other, Dyada):
            raise TypeError("Dyada.and_op ожидает Dyada")
        return Dyada(self.b and other.b)

    def or_op(self, other: Dyada) -> Dyada:
        if not isinstance(other, Dyada):
            raise TypeError("Dyada.or_op ожидает Dyada")
        return Dyada(self.b or other.b)

    def not_op(self) -> Dyada:
        return Dyada(not self.b)
