"""PYTHagor: основной интеллектуальный агент. Фаза 0: каркас."""

from __future__ import annotations

from pythagor.hints import HintChannel, HintPhase


class FunAndMental:
    def __init__(self) -> None:
        self.hints = HintChannel()

    def run(self) -> None:
        self.hints.start()
        print("PYTHagor. Агент fun_and_mental. Фаза 0: каркас.")
        print("Распознавание намерений появится в фазе 3.")
        try:
            while True:
                try:
                    user = input("Ты: ").strip()
                except EOFError:
                    break
                if user in {"выход", "exit", "quit"}:
                    break
                self.hints.push(HintPhase.INTENT, "Распознаю цель запроса.")
                print(f"Агент: запрос принят: {user}")
        finally:
            self.hints.stop()
            print("Агент: завершение работы.")


if __name__ == "__main__":
    FunAndMental().run()
