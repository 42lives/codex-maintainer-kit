# Codex Maintainer Kit

Small local tools for open-source maintainers, working professionals, and AI-assisted builders who want safer, clearer project workflows.

This project focuses on practical maintainer chores:

- Check whether a repository is ready to publish publicly.
- Detect risky files and common secret or personal-information patterns.
- Generate issue triage prompts for maintainers.
- Draft release notes from a simple commit list.
- Create an OpenAI Codex for OSS application brief.

It runs locally and does not send repository contents to any external service.

## Why This Exists

Many working professionals and non-professional developers now use AI tools to build small but useful projects. They can publish open-source work, but they often miss basic release hygiene:

- private files accidentally committed,
- missing `README.md` or license,
- unclear issue triage workflow,
- no release note structure,
- no clear maintainer story for contributor tools.

Codex Maintainer Kit gives those builders a lightweight preflight workflow before they publish, share, or maintain a public repository.

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

Generate an issue triage prompt:

```bash
python3 -m codex_maintainer_kit triage-prompt --issue-title "CLI crashes on empty folder"
```

Draft release notes from a commit list:

```bash
python3 -m codex_maintainer_kit release-notes examples/commits.txt
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

### `oss-brief`

Creates a concise application brief that explains how the project supports open-source maintenance and how Codex could help with review, testing, documentation, triage, and security workflows.

## Privacy

This tool is local-first. It does not call OpenAI APIs, GitHub APIs, analytics services, or remote scanners.

## Roadmap

- GitHub Actions workflow for preflight checks.
- JSON schema for report outputs.
- More secret-detector patterns.
- Prompt quality checks for maintainer workflows.
- Contributor-friendly issue labels.
- OpenAI Academy-inspired workflow templates for planning, review, and iteration.

## License

MIT
