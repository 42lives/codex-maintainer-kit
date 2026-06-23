from __future__ import annotations

from pathlib import Path
from typing import Union


CHECKS = [
    ("Project title", lambda text: text.lstrip().startswith("# "), "Start README.md with a clear project title."),
    ("Purpose", lambda text: _has_any(text, ["why this exists", "purpose", "overview"]), "Explain who the project helps and why it exists."),
    ("Installation", lambda text: _has_any(text, ["installation", "install"]), "Add installation or setup steps."),
    ("Usage", lambda text: _has_any(text, ["usage", "quickstart", "examples"]), "Show at least one command or user workflow."),
    ("Commands or API", lambda text: _has_any(text, ["commands", "api", "cli"]), "Document the main commands or API surface."),
    ("Privacy or security", lambda text: _has_any(text, ["privacy", "security", "local-first"]), "State how the project handles private data or security risks."),
    ("Roadmap", lambda text: "roadmap" in text.lower(), "Add a small roadmap so contributors know what comes next."),
    ("License", lambda text: "license" in text.lower(), "Mention the project license."),
]


PathInput = Union[str, Path]


def score_readme(path: PathInput) -> dict[str, object]:
    readme_path = Path(path).expanduser().resolve()
    if readme_path.is_dir():
        readme_path = readme_path / "README.md"

    if not readme_path.exists():
        return {
            "score": 0,
            "max_score": len(CHECKS),
            "percentage": 0,
            "checks": [
                {
                    "name": "README.md exists",
                    "passed": False,
                    "recommendation": "Create README.md before publishing the repository.",
                }
            ],
        }

    text = readme_path.read_text(encoding="utf-8", errors="ignore")
    checks = []
    passed_count = 0
    for name, predicate, recommendation in CHECKS:
        passed = bool(predicate(text))
        if passed:
            passed_count += 1
        checks.append({"name": name, "passed": passed, "recommendation": "" if passed else recommendation})

    percentage = round((passed_count / len(CHECKS)) * 100)
    return {"score": passed_count, "max_score": len(CHECKS), "percentage": percentage, "checks": checks}


def render_readme_score(report: dict[str, object], output_format: str = "text") -> str:
    checks = report["checks"]
    assert isinstance(checks, list)

    if output_format == "markdown":
        lines = [
            "# README Score",
            "",
            f"Score: {report['score']}/{report['max_score']} ({report['percentage']}%)",
            "",
            "## Checks",
            "",
        ]
        for check in checks:
            mark = "PASS" if check["passed"] else "TODO"
            lines.append(f"- {mark}: {check['name']}")
            if check["recommendation"]:
                lines.append(f"  - Recommendation: {check['recommendation']}")
        return "\n".join(lines) + "\n"

    lines = [f"README Score: {report['score']}/{report['max_score']} ({report['percentage']}%)", ""]
    for check in checks:
        mark = "PASS" if check["passed"] else "TODO"
        lines.append(f"[{mark}] {check['name']}")
        if check["recommendation"]:
            lines.append(f"  Recommendation: {check['recommendation']}")
    return "\n".join(lines) + "\n"


def _has_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)
