# Repository Preflight Report

- High: 0
- Medium: 7
- Low: 0

## Findings

This companion repository intentionally uses sample email-like text and CSV fixtures, so `repo-check` reports medium review items rather than failing the default high-severity CI gate.

Representative findings:

- Sample email-like text should be reviewed before publishing.
- CSV fixtures should be checked to confirm they are synthetic.
- Public examples should remain free of real account exports, tokens, or customer data.

Recommended action:

- Use `--fail-on high` for fixture-heavy starter repositories.
- Use `--fail-on medium` for stricter release repositories after sample data policy is clear.
