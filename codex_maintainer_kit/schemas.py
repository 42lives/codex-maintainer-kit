from __future__ import annotations

from pathlib import Path


SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(name: str) -> str:
    schema_path = SCHEMA_DIR / name
    return schema_path.read_text(encoding="utf-8")
