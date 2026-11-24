"""Sidebar controls and conversation-level actions."""

from dataclasses import dataclass
from html import escape
from typing import Sequence

import streamlit as st

from config.settings import (
	APP_NAME,
	DEFAULT_TEMPERATURE,
	MAX_TEMPERATURE,
	MIN_TEMPERATURE,
	OPENROUTER_MODEL,
	TEMPERATURE_STEP,
)
from lumiere.personas import PERSONAS
from lumiere.utils.export import format_transcript


@dataclass(frozen=True)
class SidebarSettings:
	"""Settings selected for the active conversation."""

	persona: str
	temperature: float
	model_name: str


def render_sidebar(messages: Sequence[dict[str, str]]) -> SidebarSettings:
	"""Render sidebar settings and return the active selections."""
	with st.sidebar:
		st.markdown(f"<div class='side-title'>✨ {APP_NAME}</div>", unsafe_allow_html=True)
		persona = st.selectbox("Personality", list(PERSONAS.keys()))
		temperature = st.slider(
			"Creativity",
			MIN_TEMPERATURE,
			MAX_TEMPERATURE,
			DEFAULT_TEMPERATURE,
			TEMPERATURE_STEP,
		)
		model_name = st.text_input("Model (OpenRouter)", value=OPENROUTER_MODEL).strip()
		display_model = escape((model_name or OPENROUTER_MODEL).split("/")[-1][:22])
		st.markdown(
			f"<span class='stat'>💬 {len(messages)} messages</span>"
			f"<span class='stat'>🤖 {display_model}</span>",
			unsafe_allow_html=True,
		)
		st.divider()
		if st.button("🗑️ New conversation"):
			st.session_state.messages = []
			st.session_state.pending = None
			st.rerun()
		if messages:
			st.download_button(
				"⬇️ Save conversation",
				format_transcript(messages),
				file_name="lumiere_chat.md",
				mime="text/markdown",
			)

	return SidebarSettings(persona, temperature, model_name)
