"""Абстрактное синтаксическое дерево PYTHagor. Фаза 1.1.

Atomos - неделимая частица выражения (литерал).
Harmonia - соединение left и right через бинарный оператор.
Tropos - поворот: унарный минус или булево отрицание.
Cosmos - корень программы, упорядоченное целое выражений.
"""

from __future__ import annotations

from dataclasses import dataclass

from pythagor.nucleus.types import Arithmos, Dilemma, Type
from pythagor.nucleus.values import Monada, Dyada, Value


ARITHMETIC_OPS = frozenset({"+", "-", "*"})
COMPARISON_OPS = frozenset({"<", ">", "<=", ">=", "==", "!="})
LOGIC_BIN_OPS = frozenset({"и", "или"})
BINARY_OPS = ARITHMETIC_OPS | COMPARISON_OPS | LOGIC_BIN_OPS
UNARY_OPS = frozenset({"-", "не"})


@dataclass(frozen=True)
class Expr:
    """Абстрактный узел выражения."""


@dataclass(frozen=True)
class Atomos(Expr):
    """Литерал. Хранит значение и его статический тип."""

    value: Value
    typ: Type

    def __post_init__(self) -> None:
        if isinstance(self.value, Monada) and not isinstance(self.typ, Arithmos):
            raise TypeError("Atomos: Monada требует тип Arithmos")
        if isinstance(self.value, Dyada) and not isinstance(self.typ, Dilemma):
            raise TypeError("Atomos: Dyada требует тип Dilemma")


@dataclass(frozen=True)
class Harmonia(Expr):
    """Бинарная операция: left op right."""

    left: Expr
    op: str
    right: Expr

    def __post_init__(self) -> None:
        if self.op not in BINARY_OPS:
            raise ValueError(f"Harmonia: неизвестный бинарный оператор {self.op!r}")


@dataclass(frozen=True)
class Tropos(Expr):
    """Унарная операция: op operand."""

    op: str
    operand: Expr

    def __post_init__(self) -> None:
        if self.op not in UNARY_OPS:
            raise ValueError(f"Tropos: неизвестный унарный оператор {self.op!r}")


@dataclass(frozen=True)
class Cosmos:
    """Корень программы."""

    expr: Expr
