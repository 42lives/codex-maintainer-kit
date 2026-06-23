from __future__ import annotations

from pathlib import Path
from typing import Union

from .readme_score import score_readme
from .repo_check import scan_repository


PathInput = Union[str, Path]


def build_maintainer_report(path: PathInput, project: str, repo_url: str) -> str:
    root = Path(path).expanduser().resolve()
    preflight = scan_repository(root)
    readme = score_readme(root)
    summary = preflight["summary"]
    assert isinstance(summary, dict)

    lines = [
        f"# Maintainer Readiness Report: {project}",
        "",
        f"Repository: {repo_url}",
        "",
        "## Positioning",
        "",
        (
            "This project is aimed at working professionals, solo maintainers, and non-professional "
            "developers who use AI tools to prepare practical projects for public open-source release."
        ),
        "",
        "## Current Readiness",
        "",
        f"- README score: {readme['score']}/{readme['max_score']} ({readme['percentage']}%)",
        f"- Preflight high findings: {summary['high']}",
        f"- Preflight medium findings: {summary['medium']}",
        f"- Preflight low findings: {summary['low']}",
        "",
        "## OpenAI Codex Fit",
        "",
        "- Pull request review: Codex can help review small maintainer changes and detect edge cases.",
        "- Issue triage: Codex can classify bug reports, missing reproduction steps, and documentation requests.",
        "- Release workflow: Codex can draft release notes from commit lists and maintainer summaries.",
        "- Security hygiene: Codex can help expand safe scanner patterns and remediation guidance.",
        "",
        "## Next Maintainer Actions",
        "",
        "1. Publish the repository publicly.",
        "2. Create the first release tag.",
        "3. Open the first three roadmap issues.",
        "4. Ask real users or peers for feedback instead of artificial stars.",
        "5. Review the OpenAI application form before submitting.",
    ]
    return "\n".join(lines) + "\n"
