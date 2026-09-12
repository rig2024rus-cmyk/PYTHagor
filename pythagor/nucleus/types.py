"""Статические типы PYTHagor. Фаза 1.1.

Arithmos - тип целых чисел, на уровне языка Целое.
Dilemma - тип булевых значений, на уровне языка Булево.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Type:
    """Абстрактный статический тип PYTHagor."""

    @property
    def language_name(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class Arithmos(Type):
    """Тип целых чисел."""

    @property
    def language_name(self) -> str:
        return "Целое"


@dataclass(frozen=True)
class Dilemma(Type):
    """Тип булевых значений."""

    @property
    def language_name(self) -> str:
        return "Булево"
