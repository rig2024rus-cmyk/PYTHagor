"""Контекст типов PYTHagor. Фаза 1.4.
Nomos - закон, порядок, определяющий, какие переменные объявлены и их типы.
Используется во время статической проверки типов.
Поддерживает стек областей видимости для условий, циклов и функций.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from pythagor.nucleus.types import Type


class UndefinedVariable(Exception):
    """Использование необъявленной переменной."""


class VariableAlreadyDeclared(Exception):
    """Повторное объявление переменной, включая затенение во вложенной области."""


@dataclass
class Nomos:
    """Контекст типов: стек областей видимости имён переменных и их типов."""

    scopes: list[dict[str, Type]] = field(default_factory=lambda: [{}])

    def enter_scope(self) -> None:
        """Входит в новую область видимости (блок условия, цикла, тело функции)."""
        self.scopes.append({})

    def exit_scope(self) -> None:
        """Выходит из текущей области видимости."""
        if len(self.scopes) <= 1:
            raise RuntimeError("Nomos: нельзя выйти из глобальной области видимости")
        self.scopes.pop()

    def declare(self, name: str, typ: Type) -> None:
        """Объявляет переменную. Затенение запрещено во всём стеке."""
        for scope in self.scopes:
            if name in scope:
                raise VariableAlreadyDeclared(f"переменная {name!r} уже объявлена")
        self.scopes[-1][name] = typ

    def lookup(self, name: str) -> Type:
        """Ищет тип переменной от ближайшей области к глобальной."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise UndefinedVariable(f"переменная {name!r} не объявлена")
