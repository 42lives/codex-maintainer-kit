from __future__ import annotations

import argparse
import json
from pathlib import Path

from .issue_plan import build_issue_plan
from .maintainer_report import build_maintainer_report
from .oss_brief import build_oss_brief
from .readme_score import render_readme_score, score_readme
from .release_notes import build_release_notes
from .repo_check import scan_repository
from .schemas import load_schema
from .triage_prompt import build_triage_prompt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="codex-maintainer-kit",
        description="Local-first OSS maintainer preflight and workflow tools.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    repo_check = subparsers.add_parser("repo-check", help="Scan a repository before public release.")
    repo_check.add_argument("path", type=Path, help="Repository path to scan.")
    repo_check.add_argument("--format", choices=["text", "markdown", "json"], default="text")
    repo_check.add_argument("--output", type=Path, help="Optional output file.")
    repo_check.add_argument(
        "--fail-on",
        choices=["none", "low", "medium", "high"],
        default="high",
        help="Exit with status 1 when findings at this severity or higher exist. Defaults to high.",
    )

    triage = subparsers.add_parser("triage-prompt", help="Generate an issue triage prompt.")
    triage.add_argument("--issue-title", required=True)
    triage.add_argument("--issue-body", default="")

    release = subparsers.add_parser("release-notes", help="Draft release notes from commit lines.")
    release.add_argument("commits_file", type=Path)

    readme_score = subparsers.add_parser("readme-score", help="Score README readiness for a public repository.")
    readme_score.add_argument("path", type=Path, help="Repository path or README.md path.")
    readme_score.add_argument("--format", choices=["text", "markdown", "json"], default="text")

    issues = subparsers.add_parser("issue-plan", help="Draft first public roadmap issues.")
    issues.add_argument("--project", default="Codex Maintainer Kit")

    report = subparsers.add_parser("maintainer-report", help="Summarize public maintainer readiness.")
    report.add_argument("path", type=Path)
    report.add_argument("--project", required=True)
    report.add_argument("--repo", required=True)

    schema = subparsers.add_parser("schema", help="Print a machine-readable output schema.")
    schema.add_argument("name", choices=["repo-check-report"])

    brief = subparsers.add_parser("oss-brief", help="Create an OpenAI Codex for OSS application brief.")
    brief.add_argument("--project", required=True)
    brief.add_argument("--repo", required=True)
    brief.add_argument("--role", default="primary maintainer")

    args = parser.parse_args(argv)

    if args.command == "repo-check":
        report = scan_repository(args.path)
        rendered = _render_repo_report(report, args.format)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        else:
            print(rendered)
        return 1 if _should_fail_repo_check(report, args.fail_on) else 0

    if args.command == "triage-prompt":
        print(build_triage_prompt(args.issue_title, args.issue_body))
        return 0

    if args.command == "release-notes":
        commits = args.commits_file.read_text(encoding="utf-8").splitlines()
        print(build_release_notes(commits))
        return 0

    if args.command == "readme-score":
        report = score_readme(args.path)
        if args.format == "json":
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(render_readme_score(report, args.format))
        return 0 if report["percentage"] >= 75 else 1

    if args.command == "issue-plan":
        print(build_issue_plan(args.project))
        return 0

    if args.command == "maintainer-report":
        print(build_maintainer_report(args.path, args.project, args.repo))
        return 0

    if args.command == "schema":
        print(load_schema(f"{args.name}.schema.json"))
        return 0

    if args.command == "oss-brief":
        print(build_oss_brief(args.project, args.repo, args.role))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _render_repo_report(report: dict[str, object], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    findings = report["findings"]
    summary = report["summary"]
    assert isinstance(findings, list)
    assert isinstance(summary, dict)

    if output_format == "markdown":
        lines = [
            "# Repository Preflight Report",
            "",
            f"- High: {summary['high']}",
            f"- Medium: {summary['medium']}",
            f"- Low: {summary['low']}",
            "",
            "## Findings",
            "",
        ]
        if not findings:
            lines.append("No findings.")
        for finding in findings:
            lines.extend(
                [
                    f"### {finding['severity'].upper()}: {finding['title']}",
                    "",
                    f"- Path: `{finding['path']}`",
                    f"- Detail: {finding['detail']}",
                    f"- Recommendation: {finding['recommendation']}",
                    "",
                ]
            )
        return "\n".join(lines).rstrip() + "\n"

    lines = [
        "Repository Preflight Report",
        f"High: {summary['high']}  Medium: {summary['medium']}  Low: {summary['low']}",
        "",
    ]
    if not findings:
        lines.append("No findings.")
    for finding in findings:
        lines.append(
            f"[{finding['severity'].upper()}] {finding['title']} ({finding['path']}): "
            f"{finding['detail']} Recommendation: {finding['recommendation']}"
        )
    return "\n".join(lines) + "\n"


def _should_fail_repo_check(report: dict[str, object], fail_on: str) -> bool:
    if fail_on == "none":
        return False

    summary = report["summary"]
    assert isinstance(summary, dict)
    severity_order = {
        "low": ("low", "medium", "high"),
        "medium": ("medium", "high"),
        "high": ("high",),
    }
    return any(summary[severity] > 0 for severity in severity_order[fail_on])
