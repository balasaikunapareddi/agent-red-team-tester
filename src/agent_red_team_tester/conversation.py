"""The three-party conversation loop: attacker → target → judge.

Mock mode runs the whole loop in pure Python (deterministic, offline).
Live mode swaps the mock target/attacker for AutoGen agents while
keeping the same judge, so scores stay comparable across modes.
"""

from __future__ import annotations

from dataclasses import dataclass

from .attacker import CatalogAttacker
from .catalog import AttackCase
from .judge import Verdict, score
from .target import MockTarget


@dataclass(frozen=True)
class Exchange:
    case: AttackCase
    response: str
    verdict: Verdict


def run_red_team(
    target: MockTarget | None = None,
    attacker: CatalogAttacker | None = None,
) -> list[Exchange]:
    """Run every catalog case against the target and score each reply."""
    target = target or MockTarget()
    attacker = attacker or CatalogAttacker()
    exchanges: list[Exchange] = []
    for case in attacker.attacks():
        response = target.respond(case.payload)
        exchanges.append(Exchange(case=case, response=response, verdict=score(case, response)))
    return exchanges
