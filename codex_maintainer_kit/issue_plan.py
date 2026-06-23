from __future__ import annotations


DEFAULT_ISSUES = [
    {
        "title": "Add JSON output schema for repository preflight reports",
        "labels": ["enhancement", "good first issue"],
        "body": "Define a stable JSON schema for repo-check output so other tools can consume preflight results.",
    },
    {
        "title": "Expand safe secret detector fixtures",
        "labels": ["security", "tests"],
        "body": "Add sanitized fixtures for common token patterns without committing realistic secrets.",
    },
    {
        "title": "Add OpenAI Academy workflow checklist template",
        "labels": ["documentation", "workflow"],
        "body": "Create a maintainer checklist for planning, review, iteration, and release workflows.",
    },
]


def build_issue_plan(project: str = "Codex Maintainer Kit") -> str:
    lines = [f"# First Issues for {project}", ""]
    for index, issue in enumerate(DEFAULT_ISSUES, start=1):
        labels = ", ".join(issue["labels"])
        lines.extend(
            [
                f"## {index}. {issue['title']}",
                "",
                f"Labels: {labels}",
                "",
                issue["body"],
                "",
                "Maintainer value:",
                "- Makes the project easier to verify, contribute to, or safely reuse.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
