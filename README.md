# Codex Maintainer Kit

Local-first maintainer automation for open-source maintainers, working professionals, and AI-assisted builders who want safer, clearer project workflows.

This project focuses on practical maintainer automation:

- Check whether a repository is ready to publish publicly.
- Detect risky files and common secret or personal-information patterns.
- Score README readiness for first-time open-source users.
- Generate issue triage prompts for maintainers.
- Draft release notes from a simple commit list.
- Draft first roadmap issues for a new public repository.
- Generate a maintainer readiness report.
- Create an OpenAI Codex for OSS application brief.

It runs locally and does not send repository contents to any external service.

## Why This Exists

Many working professionals and non-professional developers now use AI tools to build small but useful projects. They can publish open-source work, but they often miss basic release hygiene:

- private files accidentally committed,
- missing `README.md` or license,
- unclear issue triage workflow,
- no release note structure,
- no clear maintainer story for contributor tools.

Codex Maintainer Kit gives those builders a lightweight automation workflow before they publish, share, or maintain a public repository.

## Installation

No external dependencies are required.

```bash
python3 -m codex_maintainer_kit --help
```

## Usage

Run a public-release readiness check:

```bash
python3 -m codex_maintainer_kit repo-check .
```

Write the report to Markdown:

```bash
python3 -m codex_maintainer_kit repo-check . --format markdown --output preflight-report.md
```

Write the report as JSON for CI or dashboards:

```bash
python3 -m codex_maintainer_kit repo-check . --format json
```

Print the report schema:

```bash
python3 -m codex_maintainer_kit schema repo-check-report
```

Generate an issue triage prompt:

```bash
python3 -m codex_maintainer_kit triage-prompt --issue-title "CLI crashes on empty folder"
```

Draft release notes from a commit list:

```bash
python3 -m codex_maintainer_kit release-notes examples/commits.txt
```

Score README readiness:

```bash
python3 -m codex_maintainer_kit readme-score . --format markdown
```

Draft first public roadmap issues:

```bash
python3 -m codex_maintainer_kit issue-plan --project "Codex Maintainer Kit"
```

Generate a maintainer readiness report:

```bash
python3 -m codex_maintainer_kit maintainer-report . \
  --project "Codex Maintainer Kit" \
  --repo "https://github.com/42lives/codex-maintainer-kit"
```

Example readiness output:

```text
README score: 8/8 (100%)
Preflight high findings: 0
Preflight medium findings: 0
Preflight low findings: 0
```

Create a short application brief for OpenAI Codex for OSS:

```bash
python3 -m codex_maintainer_kit oss-brief \
  --project "Codex Maintainer Kit" \
  --repo "https://github.com/example/codex-maintainer-kit" \
  --role "primary maintainer"
```

## Commands

### `repo-check`

Scans a repository path and reports:

- missing public-repo basics,
- risky file names and extensions,
- likely secrets,
- likely personal information,
- large files that may not belong in a small public repository.

JSON output follows [`schemas/repo-check-report.schema.json`](schemas/repo-check-report.schema.json).
The detector fixture approach is documented in [`docs/safe-secret-fixtures.md`](docs/safe-secret-fixtures.md).

### `triage-prompt`

Creates a maintainer-friendly prompt for issue triage. The generated text asks an AI assistant to classify severity, reproduction steps, affected files, and next maintainer actions.

### `release-notes`

Turns a plain commit list into structured release note sections:

- Added
- Changed
- Fixed
- Security
- Documentation
- Other

### `readme-score`

Scores whether `README.md` explains the project clearly enough for a public open-source repository.

### `issue-plan`

Drafts the first three roadmap issues so the repository shows an active maintainer path instead of a blank project page.

### `maintainer-report`

Summarizes public-readiness, README score, preflight results, and how Codex fits the maintainer workflow.

### `schema`

Prints JSON schemas for machine-readable outputs.

### `oss-brief`

Creates a concise application brief that explains how the project supports open-source maintenance and how Codex could help with review, testing, documentation, triage, and security workflows.

## Privacy

This tool is local-first. It does not call OpenAI APIs, GitHub APIs, analytics services, or remote scanners.

## Maintainer Workflow

Use the [OpenAI Academy-inspired maintainer workflow checklist](docs/academy-workflow-checklist.md) to turn AI-assisted automation work into a reviewable loop: define the repeated task, prepare repository context, ask for a bounded improvement, verify the change, and release it.

## Related Projects

These companion projects support the same local-first automation direction:

- [promptops-toolkit](https://github.com/42lives/promptops-toolkit): prompt linting and inventory tools for reusable AI workflows
- [llm-wiki-upgrader](https://github.com/42lives/llm-wiki-upgrader): turns rough LLM notes into reviewable wiki pages

## Roadmap

- GitHub Actions workflow for automated preflight checks.
- JSON schema for report outputs.
- More secret-detector patterns.
- More safe detector fixtures for common public-repo mistakes.
- Prompt quality checks for maintainer workflows.
- Contributor-friendly issue labels.
- OpenAI Academy-inspired workflow templates for planning, review, and iteration.
- Optional GitHub API integration after the local-first workflow is stable.

## License

MIT
