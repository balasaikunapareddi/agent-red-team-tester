.PHONY: test demo report

test:
	.venv/bin/python -m pytest -q

demo:
	.venv/bin/red-team-demo

report:
	.venv/bin/red-team-report
