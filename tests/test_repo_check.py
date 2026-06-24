import tempfile
import unittest
from pathlib import Path

from codex_maintainer_kit.repo_check import scan_repository


def write_public_repo_basics(root: Path) -> None:
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")


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
            write_public_repo_basics(root)
            fake_key = "sk-" + "testsecretvalue1234567890"
            (root / ".env").write_text(f"OPENAI_API_KEY='{fake_key}'\n", encoding="utf-8")

            report = scan_repository(root)

        self.assertGreaterEqual(report["summary"]["high"], 1)
        self.assertTrue(any(finding["title"] == "Risky file for public repositories" for finding in report["findings"]))
        self.assertTrue(any(finding["title"] == "OpenAI-style API key" for finding in report["findings"]))

    def test_repo_check_detects_sanitized_secret_fixture_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_public_repo_basics(root)
            fake_github_token = "ghp_" + ("A" * 20)
            fake_private_key = "-----BEGIN " + "RSA PRIVATE KEY-----\nplaceholder\n"
            fake_password_assignment = "password" + "='not-a-real-secret'\n"
            (root / "sample.txt").write_text(
                "\n".join([fake_github_token, fake_private_key, fake_password_assignment]),
                encoding="utf-8",
            )

            report = scan_repository(root)

        titles = {finding["title"] for finding in report["findings"]}
        self.assertIn("GitHub token", titles)
        self.assertIn("Private key block", titles)
        self.assertIn("Generic secret assignment", titles)

    def test_repo_check_detects_personal_information_fixtures(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_public_repo_basics(root)
            fake_email = "person" + "@" + "example.test"
            fake_phone = "010" + "-1234-5678"
            (root / "notes.md").write_text(f"{fake_email}\n{fake_phone}\n", encoding="utf-8")

            report = scan_repository(root)

        titles = {finding["title"] for finding in report["findings"]}
        self.assertIn("Email address", titles)
        self.assertIn("Phone-like number", titles)

    def test_repo_check_detects_risky_generated_file_suffixes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            write_public_repo_basics(root)
            (root / "export.csv").write_text("name,value\n", encoding="utf-8")
            (root / "private.pem").write_text("placeholder\n", encoding="utf-8")

            report = scan_repository(root)

        by_path = {finding["path"]: finding for finding in report["findings"]}
        self.assertEqual(by_path["export.csv"]["severity"], "medium")
        self.assertEqual(by_path["private.pem"]["severity"], "high")


if __name__ == "__main__":
    unittest.main()
