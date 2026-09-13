"""Абстрактное синтаксическое дерево PYTHagor. Фаза 1.3.

Atomos - неделимая частица выражения (литерал).
Onoma - имя, ссылка на переменную.
Harmonia - соединение left и right через бинарный оператор.
Tropos - поворот: унарный минус или булево отрицание.
Horos - определение: объявление переменной с типом.
Thesis - положение: присваивание значения переменной.
Cosmos - корень программы, упорядоченное целое операторов.
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
class Statement:
    """Абстрактный оператор программы."""


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
class Onoma(Expr):
    """Ссылка на переменную по имени."""

    name: str


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
class Horos(Statement):
    """Определение: имя : тип = значение."""

    name: str
    typ: Type
    value: Expr


@dataclass(frozen=True)
class Thesis(Statement):
    """Положение: имя = значение."""

    name: str
    value: Expr


@dataclass(frozen=True)
class Cosmos:
    """Корень программы: упорядоченное целое операторов.

    Принимает кортеж операторов или одиночное выражение
    для совместимости с программами фазы 1.1 и 1.2.
    """

    statements: object

    def __post_init__(self) -> None:
        if isinstance(self.statements, (Expr, Statement)):
            object.__setattr__(self, "statements", (self.statements,))
        else:
            object.__setattr__(self, "statements", tuple(self.statements))

    @property
    def last(self) -> object:
        """Последний оператор программы."""
        return self.statements[-1]


@dataclass(frozen=True)
class Krisis(Statement):
    """Условие (если/иначе). Разделение потока выполнения."""
    condition: Expr
    then_branch: tuple[Statement, ...]
    else_branch: tuple[Statement, ...] | None = None

@dataclass(frozen=True)
class Kenosis(Statement):
    """Пропуск. Намеренно пустой оператор для пустых блоков."""
    pass
