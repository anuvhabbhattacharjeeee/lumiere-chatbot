"""LangChain and OpenRouter integration for chat responses."""

from collections.abc import Mapping, Sequence

import streamlit as st
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

from config.settings import OPENROUTER_BASE_URL

ChatRecord = Mapping[str, str]


def to_langchain_history(messages: Sequence[ChatRecord]) -> list[BaseMessage]:
	"""Convert stored user/assistant records into LangChain messages."""
	converted: list[BaseMessage] = []
	for message in messages:
		role = message.get("role")
		content = message.get("content", "")
		if role == "user":
			converted.append(HumanMessage(content=content))
		elif role == "assistant":
			converted.append(AIMessage(content=content))
		else:
			raise ValueError(f"Unsupported conversation role: {role!r}")
	return converted


def create_prompt(system_prompt: str) -> ChatPromptTemplate:
	"""Create the prompt template used for one conversation turn."""
	return ChatPromptTemplate.from_messages(
		[("system", system_prompt), MessagesPlaceholder("history"), ("human", "{input}")]
	)


@st.cache_resource(show_spinner=False)
def build_chain(
	model: str, temperature: float, api_key: str, system_prompt: str
) -> Runnable:
	"""Build and cache a streaming OpenRouter chat chain."""
	llm = ChatOpenAI(
		model=model,
		temperature=temperature,
		api_key=api_key,
		base_url=OPENROUTER_BASE_URL,
		streaming=True,
	)
	return create_prompt(system_prompt) | llm | StrOutputParser()
