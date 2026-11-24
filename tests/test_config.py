from config.settings import DEFAULT_MODEL, get_openrouter_api_key


def test_default_model_is_the_nvidia_nemotron_model() -> None:
    assert DEFAULT_MODEL == "nvidia/nemotron-3-ultra-550b-a55b:free"


def test_api_key_is_optional_and_whitespace_is_ignored(monkeypatch) -> None:
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    assert get_openrouter_api_key() is None

    monkeypatch.setenv("OPENROUTER_API_KEY", "  ")
    assert get_openrouter_api_key() is None

    monkeypatch.setenv("OPENROUTER_API_KEY", " test-key ")
    assert get_openrouter_api_key() == "test-key"