from datetime import datetime

from lumiere.utils.export import format_transcript


def test_transcript_formats_timestamp_and_speakers() -> None:
    transcript = format_transcript(
        [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello"},
        ],
        created_at=datetime(2026, 11, 24, 9, 5),
    )

    assert transcript.startswith("# Lumière chat — 2026-11-24 09:05")
    assert "**You:** Hi" in transcript
    assert "**Lumière:** Hello" in transcript