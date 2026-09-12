import io

from pythagor.hints import HintChannel, HintPhase


def test_hint_channel_delivers_events() -> None:
    stream = io.StringIO()
    channel = HintChannel(stream=stream)
    channel.start()
    channel.push(HintPhase.TYPECHECK, "Проверяю типы.")
    channel.stop()
    assert "[typecheck] Проверяю типы." in stream.getvalue()
