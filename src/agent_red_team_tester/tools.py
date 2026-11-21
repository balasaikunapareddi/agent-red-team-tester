"""Typed tool definitions for the three roles (pydantic schemas).

In mock mode the conversation loop calls the underlying functions
directly. In live mode these same schemas are handed to the AutoGen
agents as tools, so both modes share one contract.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from .catalog import CATALOG, AttackCase
from .judge import Verdict, score


class GenerateAttackInput(BaseModel):
    category: str = Field(description="Attack category to draw from")
    index: int = Field(default=0, ge=0, description="Which case in the category")


class GenerateAttackOutput(BaseModel):
    case_id: str
    category: str
    payload: str


class ScoreResponseInput(BaseModel):
    case_id: str = Field(description="Catalog case the response belongs to")
    response: str = Field(description="The target agent's reply")


class ScoreResponseOutput(BaseModel):
    case_id: str
    category: str
    outcome: str
    marker: str | None


def generate_attack(inp: GenerateAttackInput) -> GenerateAttackOutput:
    cases = [c for c in CATALOG if c.category == inp.category]
    if not cases:
        raise ValueError(f"unknown category: {inp.category}")
    case: AttackCase = cases[inp.index % len(cases)]
    return GenerateAttackOutput(case_id=case.id, category=case.category, payload=case.payload)


def score_response(inp: ScoreResponseInput) -> ScoreResponseOutput:
    case = next((c for c in CATALOG if c.id == inp.case_id), None)
    if case is None:
        raise ValueError(f"unknown case: {inp.case_id}")
    verdict: Verdict = score(case, inp.response)
    return ScoreResponseOutput(
        case_id=verdict.case_id,
        category=verdict.category,
        outcome=verdict.outcome,
        marker=verdict.marker,
    )
