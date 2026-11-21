"""Live mode: the same three roles as AutoGen agents.

Attacker / target / judge is a three-party conversation, which is
AutoGen's native shape: AssistantAgents with distinct system prompts
exchanging messages under a team runtime. Live mode uses Gemini
through AutoGen's OpenAI-compatible client (GEMINI_API_KEY required).

Mock mode never imports this module's AutoGen path — the import is
guarded so the test suite runs offline with no key and no network.
The deterministic judge (judge.py) scores live replies too, so mock
and live results stay comparable.
"""

from __future__ import annotations

import os

from .prompts import ATTACKER_SYSTEM_PROMPT, JUDGE_SYSTEM_PROMPT, TARGET_SYSTEM_PROMPT

try:  # guarded: mock mode must work without AutoGen installed
    from autogen_agentchat.agents import AssistantAgent
    from autogen_ext.models.openai import OpenAIChatCompletionClient

    AUTOGEN_AVAILABLE = True
except ImportError:  # pragma: no cover
    AUTOGEN_AVAILABLE = False


def _gemini_client() -> "OpenAIChatCompletionClient":
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("live mode requires GEMINI_API_KEY")
    return OpenAIChatCompletionClient(
        model=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"),
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "gemini",
        },
    )


def build_agents() -> dict[str, "AssistantAgent"]:
    """Build the attacker / target / judge AutoGen agents (live mode)."""
    if not AUTOGEN_AVAILABLE:
        raise RuntimeError("autogen-agentchat is not installed; live mode unavailable")
    client = _gemini_client()
    return {
        "attacker": AssistantAgent(
            "attacker", model_client=client, system_message=ATTACKER_SYSTEM_PROMPT
        ),
        "target": AssistantAgent(
            "target", model_client=client, system_message=TARGET_SYSTEM_PROMPT
        ),
        "judge": AssistantAgent(
            "judge", model_client=client, system_message=JUDGE_SYSTEM_PROMPT
        ),
    }
