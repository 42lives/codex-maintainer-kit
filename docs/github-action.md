# GitHub Action

Codex Maintainer Kit can be used as a reusable GitHub Action for public-repository preflight checks.

The action is designed for small open-source maintainers who want a lightweight CI gate before publishing or merging changes.

## Basic Usage

```yaml
name: Repository Preflight

on:
  pull_request:
  push:
    branches: [main]

jobs:
  repo-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: 42lives/codex-maintainer-kit@v0.6.0
        with:
          path: "."
          fail-on: high
          format: markdown
          output: repo-check-report.md
      - uses: actions/upload-artifact@v4
        with:
          name: repo-check-report
          path: repo-check-report.md
```

## Inputs

- `path`: repository path to scan. Default: `.`
- `fail-on`: severity threshold that should fail CI. Use `none`, `low`, `medium`, or `high`. Default: `high`
- `format`: `markdown`, `json`, or `text`. Default: `markdown`
- `output`: report file path. Default: `repo-check-report.md`

## Suggested Thresholds

- `high`: good default for public repos with sample CSVs, fixtures, or example emails.
- `medium`: stricter mode for mature repos that want to block missing docs or possible personal data.
- `low`: strictest mode for release gates.
- `none`: report-only mode.

## Privacy Boundary

The action runs locally in GitHub Actions. It does not call OpenAI APIs, GitHub APIs, analytics services, or remote scanners.
