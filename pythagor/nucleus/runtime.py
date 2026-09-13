"""Контекст значений PYTHagor. Фаза 1.4.
Ousia - сущность, бытие, где живут реальные значения.
Используется во время вычисления.
Поддерживает стек областей видимости для условий, циклов и функций.
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
    """Контекст значений: стек областей видимости имён переменных и их значений."""
    scopes: list[dict[str, Value]] = field(default_factory=lambda: [{}])

    def enter_scope(self) -> None:
        """Входит в новую область видимости (блок условия, цикла, тело функции)."""
        self.scopes.append({})

    def exit_scope(self) -> None:
        """Выходит из текущей области видимости."""
        if len(self.scopes) <= 1:
            raise RuntimeError("Ousia: нельзя выйти из глобальной области видимости")
        self.scopes.pop()

    def declare(self, name: str, value: Value) -> None:
        """Создаёт новую переменную в текущей (верхней) области видимости.
        Используется при выполнении Horos (объявления).
        """
        self.scopes[-1][name] = value

    def assign(self, name: str, value: Value) -> None:
        """Присваивает значение переменной. Ищет по стеку сверху вниз."""
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise UndefinedRuntimeVariable(
            f"переменная {name!r} не имеет значения в рантайме"
        )

    def lookup(self, name: str) -> Value:
        """Ищет значение переменной от ближайшей области к глобальной."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise UndefinedRuntimeVariable(
            f"переменная {name!r} не имеет значения в рантайме"
        )
