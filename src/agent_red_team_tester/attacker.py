"""The attacker: produces adversarial messages from the catalog.

Mock mode: yields the catalog payloads verbatim (deterministic).
Live mode (AutoGen): an LLM attacker agent generates fresh variants
per category — see autogen_agents.py. The catalog remains the ground
truth for scoring either way.
"""

from __future__ import annotations

from .catalog import CATALOG, AttackCase


class CatalogAttacker:
    """Deterministic attacker: replays the catalog, optionally filtered."""

    def __init__(self, categories: tuple[str, ...] | None = None) -> None:
        self.categories = categories

    def attacks(self) -> list[AttackCase]:
        if self.categories is None:
            return list(CATALOG)
        return [c for c in CATALOG if c.category in self.categories]
