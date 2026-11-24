"""Load the application stylesheet from the shared assets directory."""

from pathlib import Path

import streamlit as st


STYLESHEET_PATH = Path(__file__).resolve().parents[2] / "assets" / "styles" / "main.css"


def load_styles() -> None:
	"""Inject the project's CSS into the current Streamlit page."""
	try:
		stylesheet = STYLESHEET_PATH.read_text(encoding="utf-8")
	except OSError as error:
		st.error(f"Unable to load application styles: {error}")
		return
	st.markdown(f"<style>{stylesheet}</style>", unsafe_allow_html=True)
