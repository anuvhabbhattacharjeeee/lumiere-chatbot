from lumiere.personas import PERSONAS, SUGGESTIONS


def test_all_four_personas_are_available() -> None:
	assert len(PERSONAS) == 4
	assert {"✨ Classic", "🪶 Poetic", "⚡ Straight to the point", "🎈 Playful"} == set(PERSONAS)
	assert all(prompt.startswith("You are Lumière") for prompt in PERSONAS.values())


def test_four_suggestion_prompts_are_available() -> None:
	assert len(SUGGESTIONS) == 4
	assert all(icon and prompt for icon, prompt in SUGGESTIONS)
