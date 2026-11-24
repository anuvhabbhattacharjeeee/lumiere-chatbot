"""Streamlit entry point for the Lumiere chatbot."""

import streamlit as st

from config.settings import APP_NAME, OPENROUTER_MODEL, TAGLINE, get_openrouter_api_key
from lumiere.core.chat_engine import build_chain
from lumiere.personas import PERSONAS
from lumiere.ui.chat import render_chat, render_hero
from lumiere.ui.sidebar import render_sidebar
from lumiere.ui.styles import load_styles


def main() -> None:
    """Configure the page and connect the chatbot modules."""
    st.set_page_config(page_title=APP_NAME, page_icon="✨", layout="centered")
    load_styles()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "pending" not in st.session_state:
        st.session_state.pending = None

    settings = render_sidebar(st.session_state.messages)
    api_key = get_openrouter_api_key()
    if not api_key:
        st.error("OPENROUTER_API_KEY not found. Add it to a `.env` file next to app.py.")
        st.stop()

    chain = build_chain(
        model=settings.model_name or OPENROUTER_MODEL,
        temperature=settings.temperature,
        api_key=api_key,
        system_prompt=PERSONAS[settings.persona],
    )

    render_hero(TAGLINE)
    render_chat(st.session_state.messages, chain)


if __name__ == "__main__":
    main()
