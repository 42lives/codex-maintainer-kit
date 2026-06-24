# CI Preflight Gate

`repo-check` can act as a lightweight release gate in GitHub Actions or any local script.

The `--fail-on` option controls when the command exits with status `1`:

- `none`: never fail from findings,
- `low`: fail on low, medium, or high findings,
- `medium`: fail on medium or high findings,
- `high`: fail only on high findings.

Example:

```bash
python3 -m codex_maintainer_kit repo-check . --fail-on medium
```

This is useful for small public repositories that want a simple rule before publishing: do not merge if the repository contains likely private files, personal information, or missing public-repo basics.
