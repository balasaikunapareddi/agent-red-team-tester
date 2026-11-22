"""The three-party conversation loop: attacker → target → judge.

The loop itself lives in ``agent.RedTeamAgent``. This module keeps the
original ``run_red_team()`` entry point (used by the demo, the report
CLI, and the tests) as a thin wrapper around it, and re-exports
``Exchange`` so existing imports keep working.

Mock mode runs the whole loop in pure Python (deterministic, offline).
Live mode swaps the mock target/attacker for AutoGen agents while
keeping the same judge, so scores stay comparable across modes.
"""

from __future__ import annotations

from .agent import Exchange, RedTeamAgent
from .attacker import CatalogAttacker
from .target import MockTarget

__all__ = ["Exchange", "RedTeamAgent", "run_red_team"]


def run_red_team(
    target: MockTarget | None = None,
    attacker: CatalogAttacker | None = None,
) -> list[Exchange]:
    """Run every catalog case against the target and score each reply."""
    return RedTeamAgent(target=target, attacker=attacker).run()
