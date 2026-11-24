# Lumière Chatbot

Lumière is a refined Streamlit chat experience for curious conversations. It combines four assistant personalities, OpenRouter model access, and a softly animated interface with streaming responses and downloadable Markdown transcripts.

## Features

- Four personalities: Classic, Poetic, Straight to the point, and Playful
- Streaming responses through LangChain and OpenRouter
- NVIDIA Nemotron as the default model, with a configurable model field
- Adjustable creativity, conversation history, and starter prompts
- Sidebar conversation statistics, reset action, and Markdown export
- Animated aurora background, glowing hero, welcome card, and responsive chat styling

## Screenshots

Screenshots are not included yet. Add desktop and mobile captures under `assets/images/` when available.

## Project Structure

```text
.
├── app.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── lumiere/
│   ├── personas.py
│   ├── core/chat_engine.py
│   ├── ui/chat.py
│   ├── ui/sidebar.py
│   ├── ui/styles.py
│   └── utils/export.py
├── assets/styles/main.css
├── docs/architecture.md
├── tests/
└── requirements.txt
```

## Installation

Python 3.10 or later is required. From the repository root, create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

For development and tests, install the optional development dependencies instead of the requirements file:

```powershell
python -m pip install -e ".[dev]"
```

## Environment Variables

Copy `.env.example` to `.env` and add your OpenRouter key:

```dotenv
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=nvidia/nemotron-3-ultra-550b-a55b:free
```

`OPENROUTER_API_KEY` is required. `OPENROUTER_MODEL` is optional; the application defaults to NVIDIA Nemotron when it is omitted. Never commit `.env` or paste a real key into source code.

## Run

From the repository root, run:

```powershell
streamlit run app.py
```

## Tests

```powershell
python -m pytest
```

## Technologies

Python, Streamlit, LangChain Core, LangChain OpenAI, OpenRouter, and python-dotenv.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting a pull request. Please add tests for behavior changes and keep credentials out of commits.

## License

No license has been selected for this repository yet. Reuse and redistribution rights remain unspecified until the repository owner adds a license.