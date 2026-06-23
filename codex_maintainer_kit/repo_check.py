from __future__ import annotations

import re
from pathlib import Path

MAX_SCAN_BYTES = 512_000
LARGE_FILE_BYTES = 5_000_000

RISKY_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "credentials.json",
    "cookies.txt",
}

RISKY_SUFFIXES = {
    ".key",
    ".pem",
    ".p12",
    ".pfx",
    ".sqlite",
    ".db",
    ".xlsx",
    ".xls",
    ".csv",
    ".log",
}

SECRET_PATTERNS = [
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Generic secret assignment", re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\s*=\s*['\"][^'\"]{8,}['\"]")),
]

PERSONAL_PATTERNS = [
    ("Email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("Phone-like number", re.compile(r"\b(?:\+?\d{1,3}[-. ]?)?(?:\d{2,4}[-. ]){2}\d{3,4}\b")),
]

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache"}


def scan_repository(path: Path) -> dict[str, object]:
    root = path.expanduser().resolve()
    findings: list[dict[str, str]] = []

    if not root.exists():
        return _report(
            [
                _finding(
                    "high",
                    str(path),
                    "Path does not exist",
                    "The requested repository path was not found.",
                    "Run the command against an existing project directory.",
                )
            ]
        )

    _check_required_files(root, findings)

    for file_path in _iter_files(root):
        rel = str(file_path.relative_to(root))
        _check_file_metadata(file_path, rel, findings)
        _check_file_contents(file_path, rel, findings)

    return _report(findings)


def _check_required_files(root: Path, findings: list[dict[str, str]]) -> None:
    required = {
        "README.md": "Add a README with purpose, installation, and usage examples.",
        "LICENSE": "Add a license so users know how they can use the project.",
    }
    for filename, recommendation in required.items():
        if not (root / filename).exists():
            findings.append(
                _finding(
                    "medium",
                    filename,
                    "Missing public repository file",
                    f"{filename} is expected in a public open-source repository.",
                    recommendation,
                )
            )


def _iter_files(root: Path):
    for file_path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in file_path.parts):
            continue
        if file_path.is_file():
            yield file_path


def _check_file_metadata(file_path: Path, rel: str, findings: list[dict[str, str]]) -> None:
    lower_name = file_path.name.lower()
    suffix = file_path.suffix.lower()

    if lower_name in RISKY_NAMES or suffix in RISKY_SUFFIXES:
        findings.append(
            _finding(
                "high" if suffix in {".key", ".pem", ".p12", ".pfx"} or lower_name.startswith(".env") else "medium",
                rel,
                "Risky file for public repositories",
                f"{file_path.name} often contains private data or generated artifacts.",
                "Remove it, replace it with a sanitized example, or add it to .gitignore.",
            )
        )

    try:
        size = file_path.stat().st_size
    except OSError:
        return

    if size > LARGE_FILE_BYTES:
        findings.append(
            _finding(
                "low",
                rel,
                "Large file",
                f"File size is {size} bytes.",
                "Confirm this belongs in the repository or use release assets/storage instead.",
            )
        )


def _check_file_contents(file_path: Path, rel: str, findings: list[dict[str, str]]) -> None:
    try:
        raw = file_path.read_bytes()
    except OSError:
        return

    if b"\x00" in raw[:4096]:
        return

    text = raw[:MAX_SCAN_BYTES].decode("utf-8", errors="ignore")
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(
                _finding(
                    "high",
                    rel,
                    label,
                    "A secret-like pattern was found.",
                    "Rotate the secret if real, remove it from history, and commit a safe example instead.",
                )
            )

    for label, pattern in PERSONAL_PATTERNS:
        if pattern.search(text):
            findings.append(
                _finding(
                    "medium",
                    rel,
                    label,
                    "A personal-information-like pattern was found.",
                    "Review and replace personal data with examples before publishing.",
                )
            )


def _finding(severity: str, path: str, title: str, detail: str, recommendation: str) -> dict[str, str]:
    return {
        "severity": severity,
        "path": path,
        "title": title,
        "detail": detail,
        "recommendation": recommendation,
    }


def _report(findings: list[dict[str, str]]) -> dict[str, object]:
    summary = {"high": 0, "medium": 0, "low": 0}
    for finding in findings:
        summary[finding["severity"]] += 1
    return {"summary": summary, "findings": findings}
