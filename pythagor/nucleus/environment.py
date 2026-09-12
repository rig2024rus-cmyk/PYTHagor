"""Контекст типов PYTHagor. Фаза 1.3.

Nomos - закон, порядок, определяющий, какие переменные объявлены и их типы.
Используется во время статической проверки типов.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pythagor.nucleus.types import Type


class UndefinedVariable(Exception):
    """Использование необъявленной переменной."""


class VariableAlreadyDeclared(Exception):
    """Повторное объявление переменной."""


@dataclass
class Nomos:
    """Контекст типов: отображение имён переменных на их типы."""

    bindings: dict[str, Type] = field(default_factory=dict)

    def declare(self, name: str, typ: Type) -> None:
        """Объявляет переменную. Если уже объявлена, бросает ошибку."""
        if name in self.bindings:
            raise VariableAlreadyDeclared(f"переменная {name!r} уже объявлена")
        self.bindings[name] = typ

    def lookup(self, name: str) -> Type:
        """Ищет тип переменной. Если не найдена, бросает ошибку."""
        if name not in self.bindings:
            raise UndefinedVariable(f"переменная {name!r} не объявлена")
        return self.bindings[name]
