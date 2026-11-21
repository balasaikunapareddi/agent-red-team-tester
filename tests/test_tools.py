import pytest

from agent_red_team_tester.tools import (
    GenerateAttackInput,
    ScoreResponseInput,
    generate_attack,
    score_response,
)


def test_generate_attack_round_trip():
    out = generate_attack(GenerateAttackInput(category="direct_override", index=0))
    assert out.case_id == "override-1"
    assert out.payload


def test_generate_attack_unknown_category():
    with pytest.raises(ValueError):
        generate_attack(GenerateAttackInput(category="nope"))


def test_score_response_round_trip():
    out = score_response(
        ScoreResponseInput(case_id="inject-1", response="Here is SAVE50.")
    )
    assert out.outcome == "violated"
    assert out.marker == "SAVE50"


def test_score_response_unknown_case():
    with pytest.raises(ValueError):
        score_response(ScoreResponseInput(case_id="nope", response="hi"))
