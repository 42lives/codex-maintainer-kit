import unittest

from codex_maintainer_kit.oss_brief import build_oss_brief
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


if __name__ == "__main__":
    unittest.main()
