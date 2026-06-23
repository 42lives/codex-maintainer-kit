from __future__ import annotations


def build_triage_prompt(issue_title: str, issue_body: str = "") -> str:
    body_section = issue_body.strip() or "(No issue body provided.)"
    return f"""You are helping triage an open-source issue.

Issue title:
{issue_title}

Issue body:
{body_section}

Return a maintainer-ready triage note with:
1. probable category: bug, feature request, documentation, question, security, or maintenance
2. severity: low, medium, high, or urgent
3. missing information needed from the reporter
4. likely files or areas to inspect
5. reproduction checklist
6. recommended labels
7. concise maintainer response draft

Do not invent evidence. Mark uncertain claims as assumptions.
"""
