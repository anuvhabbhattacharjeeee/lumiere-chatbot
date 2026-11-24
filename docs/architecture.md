# Architecture

Lumière keeps the Streamlit entry point thin and assigns configuration, model integration, presentation, and export to separate modules.

## Runtime flow

1. `app.py` configures the Streamlit page, loads the stylesheet, initializes session state, and coordinates the application.
2. `config/settings.py` loads `.env` from the repository root and provides non-secret defaults plus the OpenRouter API key accessor.
3. `lumiere/ui/sidebar.py` renders personality, model, and creativity controls, conversation actions, and transcript download. It returns the active settings to the entry point.
4. `lumiere/core/chat_engine.py` converts saved turns to LangChain messages and builds a cached streaming chain using `ChatOpenAI` with OpenRouter's compatible API endpoint.
5. `lumiere/ui/chat.py` renders the Lumière hero, welcome suggestions, history, chat input, and streamed response. Messages remain in Streamlit session state.
6. `lumiere/utils/export.py` turns those stored messages into a timestamped Markdown transcript.
7. `lumiere/ui/styles.py` reads `assets/styles/main.css` and injects it into the page; the stylesheet owns all visual design and animation rules.

## Dependency direction

The entry point imports and composes the modules. UI modules depend on settings/personas and the engine/export helpers; the engine does not import UI modules. This keeps the integration path one-way and avoids circular imports.

## State and secrets

Conversation turns and a pending suggestion are stored in `st.session_state` for the current browser session. API credentials are read from `OPENROUTER_API_KEY`; they are not stored in source files or conversation exports. `.env` and Streamlit secrets files are excluded by `.gitignore`.