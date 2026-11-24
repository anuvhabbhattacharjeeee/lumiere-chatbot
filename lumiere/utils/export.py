"""Markdown conversation transcript formatting."""

from collections.abc import Sequence
from datetime import datetime

from config.settings import APP_NAME


def format_transcript(
	messages: Sequence[dict[str, str]], created_at: datetime | None = None
) -> str:
	"""Format stored chat messages as a downloadable Markdown transcript."""
	timestamp = created_at or datetime.now()
	transcript = f"# {APP_NAME} chat — {timestamp:%Y-%m-%d %H:%M}\n\n"
	entries = []
	for message in messages:
		speaker = "You" if message["role"] == "user" else APP_NAME
		entries.append(f"**{speaker}:** {message['content']}")
	return transcript + "\n\n".join(entries)
