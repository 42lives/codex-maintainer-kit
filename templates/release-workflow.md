# Release Workflow

Use this lightweight release loop for small open-source projects.

1. Run tests.
2. Run repository preflight.
3. Review generated files and sample data.
4. Update docs and examples.
5. Close shipped issues with a short verification note.
6. Create a versioned release with verification commands.
7. Check CI after push.

Example:

```bash
python3 -m unittest discover
python3 -m codex_maintainer_kit repo-check . --fail-on medium --format markdown
```
