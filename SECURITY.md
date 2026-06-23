# Security Policy

Codex Maintainer Kit is a local-first scanner and maintainer workflow helper. It should not send repository contents to external services.

## Reporting a Vulnerability

Please open a GitHub issue with a minimal reproduction that does not include real secrets or private data.

If you find a detector bypass, include:

- the detector that missed the case,
- a sanitized example,
- expected severity,
- suggested remediation language.

## Handling Test Secrets

Tests must construct fake secret strings at runtime instead of committing realistic secret-looking values directly into source files.
