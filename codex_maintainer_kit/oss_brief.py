from __future__ import annotations


def build_oss_brief(project: str, repo: str, role: str) -> str:
    return f"""Project: {project}
Repository: {repo}
Role: {role}

Application summary:
I maintain {project}, a local-first open-source toolkit that helps maintainers prepare safer public repositories, triage issues, draft release notes, and document maintainer workflows. The project is designed for solo maintainers and non-professional developers who want practical open-source hygiene without sending repository contents to external services.

Why Codex would help:
Codex would help improve this project by reviewing pull requests, expanding test coverage, generating clearer documentation, identifying edge cases in repository scanning, and helping maintain security-conscious maintainer workflows. I would use Codex to make releases safer and to respond to issues faster.

API credit use:
I would use API credits for optional maintainer automation experiments, such as issue classification, release-note drafting, documentation checks, and privacy-safe prompt generation. Core scanning remains local-first so users can run the tool without uploading private repository data.
"""
