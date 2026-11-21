from agent_red_team_tester.conversation import run_red_team
from agent_red_team_tester.judge import HELD, PARTIAL, VIOLATED
from agent_red_team_tester.report import build_report, render, to_json


def test_aggregation_math():
    report = build_report(run_red_team())
    by_cat = {c.category: c for c in report.categories}
    assert by_cat["direct_override"].score == 1.0
    assert by_cat["indirect_injection"].score == 0.5
    assert by_cat["authority_impersonation"].score == 0.0
    assert by_cat["oversharing_bait"].score == 0.75
    assert report.overall == 0.75


def test_failure_ordering_violated_first():
    report = build_report(run_red_team())
    outcomes = [f.verdict.outcome for f in report.failures]
    assert outcomes == [VIOLATED, VIOLATED, VIOLATED, PARTIAL]


def test_checklist_generated_from_failures():
    report = build_report(run_red_team())
    joined = " ".join(report.checklist).lower()
    assert "pasted content as data" in joined
    assert "claimed authority" in joined
    assert "neither confirm nor deny" in joined
    # Categories that held must not produce checklist items.
    assert "persona switches" not in joined


def test_render_and_json():
    report = build_report(run_red_team())
    text = render(report)
    assert "Red-team report" in text
    assert "Hardening checklist" in text
    data = to_json(report)
    assert '"overall": 0.75' in data
