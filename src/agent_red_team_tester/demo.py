"""Demo: run the full attack catalog against the mock target.

One command, no API key, no network:

    red-team-demo            (or: python -m agent_red_team_tester.demo)

Prints per-category scores, the failures caught (with transcripts),
and the hardening checklist generated from those failures.
"""

from __future__ import annotations

from .conversation import run_red_team
from .report import build_report, render


def main() -> None:
    exchanges = run_red_team()
    report = build_report(exchanges)
    print(f"Ran {len(exchanges)} adversarial cases against the mock target.\n")
    print(render(report))
    print(
        "\nNote: the mock target ships with deliberate weaknesses "
        "(indirect injection, authority impersonation) so the demo "
        "shows real catches. See target.py."
    )


if __name__ == "__main__":
    main()
