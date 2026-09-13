"""Параллельные строковые подсказки PYTHagor. Фаза 0."""

from __future__ import annotations

import queue
import sys
import threading
from dataclasses import dataclass
from enum import Enum
from typing import IO


class HintPhase(Enum):
    INTENT = "intent"
    PARSE = "parse"
    SEMANTICS = "semantics"
    TYPECHECK = "typecheck"
    TESTS = "tests"
    PROOF = "proof"
    REPAIR = "repair"
    CURATOR = "curator"


@dataclass(frozen=True)
class HintEvent:
    phase: HintPhase
    text: str
    replace_id: str | None = None
    priority: int = 0


class HintChannel:
    """Канал подсказок: события уходят в очередь и выводятся параллельно."""

    def __init__(self, stream: IO[str] | None = None) -> None:
        self._queue: queue.Queue[HintEvent | None] = queue.Queue()
        self._stop = threading.Event()
        self._stream = stream if stream is not None else sys.stderr
        self._thread = threading.Thread(target=self._worker, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def emit(self, event: HintEvent) -> None:
        self._queue.put(event)

    def push(
        self,
        phase: HintPhase,
        text: str,
        replace_id: str | None = None,
        priority: int = 0,
    ) -> None:
        self.emit(HintEvent(phase=phase, text=text, replace_id=replace_id, priority=priority))

    def stop(self) -> None:
        self._stop.set()
        self._queue.put(None)
        self._thread.join(timeout=1.0)

    def _worker(self) -> None:
        while not self._stop.is_set():
            item = self._queue.get()
            if item is None:
                break
            line = f"[{item.phase.value}] {item.text}"
            self._stream.write(line + "\n")
            self._stream.flush()
