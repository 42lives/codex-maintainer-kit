# Safe Secret Detector Fixtures

`repo-check` tests common secret and personal-information patterns without committing realistic credentials to the repository.

The test suite uses temporary directories and builds synthetic values at runtime. This keeps the public repository clean while still verifying that the scanner catches:

- OpenAI-style API keys,
- GitHub token shapes,
- private key block headers,
- generic secret assignments,
- email-address-like text,
- phone-number-like text,
- risky generated or private file extensions.

When adding new detector fixtures, keep the same rule: construct matching strings inside tests or test helpers, and avoid storing complete token-looking examples in committed files.

Run the checks locally:

```bash
python3 -m unittest discover
python3 -m codex_maintainer_kit repo-check . --format markdown
```
