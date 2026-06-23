# Contributing

Thanks for considering a contribution.

This project is intentionally small and local-first. Good contributions usually improve:

- safer repository scanning,
- clearer maintainer workflows,
- better documentation,
- test coverage,
- beginner-friendly CLI behavior.

## Development

Run the test suite:

```bash
python3 -m unittest discover
```

Try the CLI locally:

```bash
python3 -m codex_maintainer_kit --help
python3 -m codex_maintainer_kit repo-check .
```

## Pull Request Checklist

- Keep the change focused.
- Add or update tests for behavior changes.
- Avoid external dependencies unless clearly necessary.
- Do not add real secrets, personal data, private logs, or private repository content.
- Update the README when user-facing behavior changes.
