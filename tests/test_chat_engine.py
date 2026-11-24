import pytest
from langchain_core.messages import AIMessage, HumanMessage

from lumiere.core.chat_engine import create_prompt, to_langchain_history


def test_history_conversion_preserves_roles_and_order() -> None:
	history = to_langchain_history(
		[
			{"role": "user", "content": "Hello"},
			{"role": "assistant", "content": "Welcome"},
		]
	)

	assert isinstance(history[0], HumanMessage)
	assert isinstance(history[1], AIMessage)
	assert [message.content for message in history] == ["Hello", "Welcome"]


def test_history_conversion_rejects_unknown_roles() -> None:
	with pytest.raises(ValueError, match="Unsupported conversation role"):
		to_langchain_history([{"role": "system", "content": "No"}])


def test_prompt_includes_system_history_and_current_input() -> None:
	prompt = create_prompt("Be concise.")
	formatted = prompt.format_messages(history=[], input="Hello")

	assert formatted[0].content == "Be concise."
	assert formatted[-1].content == "Hello"
