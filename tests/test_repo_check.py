import tempfile
import unittest
from pathlib import Path

from codex_maintainer_kit.repo_check import scan_repository


class RepoCheckTest(unittest.TestCase):
    def test_repo_check_detects_missing_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            report = scan_repository(Path(tmpdir))

        self.assertEqual(report["summary"]["medium"], 2)
        titles = {finding["title"] for finding in report["findings"]}
        self.assertIn("Missing public repository file", titles)

    def test_repo_check_detects_secret_like_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            fake_key = "sk-" + "testsecretvalue1234567890"
            (root / ".env").write_text(f"OPENAI_API_KEY='{fake_key}'\n", encoding="utf-8")

            report = scan_repository(root)

        self.assertGreaterEqual(report["summary"]["high"], 1)
        self.assertTrue(any(finding["title"] == "Risky file for public repositories" for finding in report["findings"]))
        self.assertTrue(any(finding["title"] == "OpenAI-style API key" for finding in report["findings"]))


if __name__ == "__main__":
    unittest.main()
