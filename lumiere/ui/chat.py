"""Hero, welcome, suggestion, and conversation rendering."""

from datetime import datetime
from typing import Any

import streamlit as st

from config.settings import APP_NAME
from lumiere.core.chat_engine import to_langchain_history
from lumiere.personas import SUGGESTIONS


def render_hero(tagline: str) -> None:
	"""Render the Lumière brand header."""
	st.markdown(
		f'<div class="hero"><div class="logo">✨</div><h1>{APP_NAME}</h1>'
		f"<p>{tagline}</p></div>",
		unsafe_allow_html=True,
	)


def render_chat(messages: list[dict[str, str]], chain: Any) -> None:
	"""Render suggestions and history, then stream a submitted user message."""
	if not messages:
		hour = datetime.now().hour
		greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
		st.markdown(
			f"<div class='welcome'><h3>{greeting} 👋</h3>"
			"<span>Pick a spark below, or ask me anything.</span></div>",
			unsafe_allow_html=True,
		)
		columns = st.columns(2)
		for index, (icon, text) in enumerate(SUGGESTIONS):
			if columns[index % 2].button(f"{icon}  {text}", key=f"sug{index}"):
				st.session_state.pending = text
				st.rerun()

	for message in messages:
		avatar = "🧑‍🎤" if message["role"] == "user" else "✨"
		with st.chat_message(message["role"], avatar=avatar):
			st.markdown(message["content"])

	user_input = st.chat_input(f"Whisper something to {APP_NAME}...") or st.session_state.pending
	st.session_state.pending = None
	if not user_input:
		return

	history = to_langchain_history(messages)
	messages.append({"role": "user", "content": user_input})
	with st.chat_message("user", avatar="🧑‍🎤"):
		st.markdown(user_input)

	with st.chat_message("assistant", avatar="✨"):
		try:
			with st.spinner("Lumière is thinking…"):
				stream = chain.stream({"history": history, "input": user_input})
				first_chunk = next(stream, "")

			def response_chunks():
				yield first_chunk
				yield from stream

			reply = st.write_stream(response_chunks())
		except Exception as error:
			reply = f"⚠️ Something went wrong: {error}"
			st.markdown(reply)

	messages.append({"role": "assistant", "content": str(reply)})
	st.rerun()
