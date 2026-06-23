from __future__ import annotations


CATEGORIES = {
    "Added": ("add", "feat", "new", "create", "introduce"),
    "Fixed": ("fix", "bug", "repair", "resolve"),
    "Security": ("security", "secret", "token", "privacy", "vulnerability"),
    "Documentation": ("doc", "readme", "guide", "example"),
    "Changed": ("change", "refactor", "update", "improve"),
}

CONVENTIONAL_COMMIT_CATEGORIES = {
    "feat": "Added",
    "fix": "Fixed",
    "docs": "Documentation",
    "doc": "Documentation",
    "security": "Security",
    "sec": "Security",
    "refactor": "Changed",
    "perf": "Changed",
    "chore": "Changed",
}


def build_release_notes(commit_lines: list[str]) -> str:
    buckets = {name: [] for name in CATEGORIES}
    buckets["Other"] = []

    for raw_line in commit_lines:
        line = raw_line.strip()
        if not line:
            continue
        category = _category_for(line)
        buckets[category].append(_clean_commit_line(line))

    output = ["# Release Notes", ""]
    for category, entries in buckets.items():
        if entries:
            output.extend([f"## {category}", ""])
            output.extend(f"- {entry}" for entry in entries)
            output.append("")
    if len(output) == 2:
        output.append("No commit lines provided.")
    return "\n".join(output).rstrip() + "\n"


def _category_for(line: str) -> str:
    lowered = line.lower()
    prefix = lowered.split(":", 1)[0].split("(", 1)[0].strip()
    if prefix in CONVENTIONAL_COMMIT_CATEGORIES:
        return CONVENTIONAL_COMMIT_CATEGORIES[prefix]
    for category, keywords in CATEGORIES.items():
        if any(keyword in lowered for keyword in keywords):
            return category
    return "Other"


def _clean_commit_line(line: str) -> str:
    parts = line.split(maxsplit=1)
    if parts and len(parts[0]) in {7, 8, 9, 10, 11, 12} and all(c in "0123456789abcdef" for c in parts[0].lower()):
        return parts[1] if len(parts) > 1 else line
    return line
