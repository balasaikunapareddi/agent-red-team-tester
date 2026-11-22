"""The red-team agent: attacker → target → judge, one case at a time.

This module is the agent's front door. ``RedTeamAgent`` owns the loop:

1. **attack** — the attacker produces an adversarial message from the
   catalog (``catalog.py``). Mock mode: ``CatalogAttacker``
   (``attacker.py``) replays catalog payloads verbatim. Live mode: an
   AutoGen attacker agent generates fresh variants (``autogen_agents.py``).
2. **respond** — the target agent under test replies. Mock mode:
   ``MockTarget`` (``target.py``), a deterministic support agent with
   documented weaknesses. Live mode: an AutoGen ``AssistantAgent``.
3. **judge** — the deterministic judge (``judge.py``) scores each reply
   held / partial / violated against the case's rubric and records the
   exact marker that decided it.

System prompts for all three roles live in ``prompts.py``
(``ATTACKER_SYSTEM_PROMPT``, ``TARGET_SYSTEM_PROMPT``,
``JUDGE_SYSTEM_PROMPT``) — behavior only. Everything checkable (the
attack catalog, the target's rules, the judge's rubric) lives in code,
so mock-mode results are deterministic and reproducible offline.
"""

from __future__ import annotations

from dataclasses import dataclass

from .attacker import CatalogAttacker
from .catalog import AttackCase
from .judge import Verdict, score
from .target import MockTarget


@dataclass(frozen=True)
class Exchange:
    """One red-team exchange: an attack case, the target's reply, the verdict."""

    case: AttackCase
    response: str
    verdict: Verdict


class RedTeamAgent:
    """Red-team agent: runs adversarial cases against a target and judges replies.

    Args:
        target: The agent under test. Defaults to ``MockTarget`` (mock
            mode). In live mode this is an AutoGen target agent built by
            ``autogen_agents.build_agents()``.
        attacker: Source of attack cases. Defaults to ``CatalogAttacker``
            replaying the full catalog; pass
            ``CatalogAttacker(categories=(...))`` to filter.

    The judge is always the deterministic scorer in ``judge.py`` — the
    same rubric scores mock and live replies, so results stay
    comparable across modes.

    Usage::

        agent = RedTeamAgent()
        exchanges = agent.run()          # every catalog case
        one = agent.run_case(case)       # a single case
    """

    def __init__(
        self,
        target: MockTarget | None = None,
        attacker: CatalogAttacker | None = None,
    ) -> None:
        self.target = target or MockTarget()
        self.attacker = attacker or CatalogAttacker()

    def run_case(self, case: AttackCase) -> Exchange:
        """Run one attack case: attacker payload → target reply → verdict."""
        response = self.target.respond(case.payload)
        return Exchange(case=case, response=response, verdict=score(case, response))

    def run(self) -> list[Exchange]:
        """Run every attack case against the target and score each reply."""
        return [self.run_case(case) for case in self.attacker.attacks()]
