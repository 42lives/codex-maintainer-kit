# OpenAI Academy-Inspired Maintainer Workflow Checklist

This checklist turns AI-assisted project work into a reviewable maintainer loop. It is not a transcript or copy of Academy material; it is a practical workflow template for this project.

## 1. Define the Automation Goal

- What repeated task should be automated?
- Who benefits from the automation?
- What should remain under human review?
- What private data must stay local?

## 2. Prepare Repository Context

- Add or update `README.md`.
- Confirm `LICENSE`, `SECURITY.md`, and `CONTRIBUTING.md` exist.
- Run repository preflight checks.
- Save machine-readable reports when CI or dashboards need them.

## 3. Ask AI for a Bounded Improvement

- Give the current goal.
- Include relevant files or command output.
- Ask for a small, reviewable change.
- Ask the assistant to preserve privacy and avoid unsupported claims.

## 4. Verify the Change

- Run tests.
- Run `repo-check`.
- Read the diff.
- Confirm the user-facing workflow still makes sense.

## 5. Release and Maintain

- Link the change to an issue.
- Close the issue only after verification.
- Publish a release note for user-facing changes.
- Keep the roadmap honest and small.

## Example Loop

```bash
python3 -m codex_maintainer_kit repo-check . --format markdown
python3 -m codex_maintainer_kit readme-score . --format markdown
python3 -m unittest discover
```

## Review Boundaries

- Do not upload private repository content to external services unless the user explicitly opts in.
- Do not claim adoption, stars, or downloads that do not exist.
- Do not copy accepted applications, docs, or third-party wiki pages.
- Keep AI-generated changes tied to concrete maintainer workflows.
