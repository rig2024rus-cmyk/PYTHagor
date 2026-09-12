"""Контекст значений PYTHagor. Фаза 1.3.

Ousia - сущность, бытие, где живут реальные значения.
Используется во время вычисления.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pythagor.nucleus.values import Value


class UndefinedRuntimeVariable(Exception):
    """Попытка получить значение необъявленной переменной в рантайме.

    В нормальной работе это не должно происходить: checker проверяет
    объявление переменных до запуска рантайма. Эта ошибка - защита
    от внутренних несогласованностей.
    """


@dataclass
class Ousia:
    """Контекст значений: отображение имён переменных на их значения."""

    bindings: dict[str, Value] = field(default_factory=dict)

    def assign(self, name: str, value: Value) -> None:
        """Присваивает значение переменной. Может перезаписывать."""
        self.bindings[name] = value

    def lookup(self, name: str) -> Value:
        """Ищет значение переменной. Если не найдена, бросает ошибку."""
        if name not in self.bindings:
            raise UndefinedRuntimeVariable(
                f"переменная {name!r} не имеет значения в рантайме"
            )
        return self.bindings[name]
