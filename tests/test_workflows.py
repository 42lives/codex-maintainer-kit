import unittest

from codex_maintainer_kit.issue_plan import build_issue_plan
from codex_maintainer_kit.maintainer_report import build_maintainer_report
from codex_maintainer_kit.oss_brief import build_oss_brief
from codex_maintainer_kit.readme_score import score_readme
from codex_maintainer_kit.release_notes import build_release_notes
from codex_maintainer_kit.triage_prompt import build_triage_prompt


class WorkflowTest(unittest.TestCase):
    def test_release_notes_groups_commit_lines(self) -> None:
        notes = build_release_notes(["feat: add scanner", "fix: repair empty input", "docs: update readme"])

        self.assertIn("## Added", notes)
        self.assertIn("## Fixed", notes)
        self.assertIn("## Documentation", notes)

    def test_triage_prompt_contains_issue_context(self) -> None:
        prompt = build_triage_prompt("CLI crashes", "Steps here")

        self.assertIn("CLI crashes", prompt)
        self.assertIn("Steps here", prompt)
        self.assertIn("Do not invent evidence", prompt)

    def test_oss_brief_mentions_codex_use(self) -> None:
        brief = build_oss_brief("Demo", "https://github.com/example/demo", "primary maintainer")

        self.assertIn("Codex", brief)
        self.assertIn("primary maintainer", brief)

    def test_readme_score_rewards_complete_readme(self) -> None:
        report = score_readme("README.md")

        self.assertGreaterEqual(report["percentage"], 75)

    def test_issue_plan_creates_first_three_issues(self) -> None:
        plan = build_issue_plan("Demo")

        self.assertIn("# First Issues for Demo", plan)
        self.assertIn("## 1.", plan)
        self.assertIn("## 3.", plan)

    def test_maintainer_report_links_codex_fit(self) -> None:
        report = build_maintainer_report(".", "Demo", "https://github.com/example/demo")

        self.assertIn("OpenAI Codex Fit", report)
        self.assertIn("README score", report)


if __name__ == "__main__":
    unittest.main()
