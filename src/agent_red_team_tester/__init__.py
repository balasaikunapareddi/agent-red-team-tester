"""agent-red-team-tester: red-team other agents before your users do."""

from .catalog import CATALOG, CATEGORIES, AttackCase
from .conversation import Exchange, run_red_team
from .judge import HELD, PARTIAL, VIOLATED, Verdict, score
from .report import Report, build_report, render
from .target import MockTarget

__all__ = [
    "CATALOG",
    "CATEGORIES",
    "AttackCase",
    "Exchange",
    "run_red_team",
    "HELD",
    "PARTIAL",
    "VIOLATED",
    "Verdict",
    "score",
    "Report",
    "build_report",
    "render",
    "MockTarget",
]

__version__ = "0.1.0"
