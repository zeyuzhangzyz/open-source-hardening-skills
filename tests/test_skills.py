from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

if not SKILLS_DIR.is_dir():
    raise FileNotFoundError(
        f"Skills directory not found: {SKILLS_DIR}. "
        "Run tests from the repository root: python -m unittest discover -s tests"
    )

REQUIRED_FIELDS = {"name", "description", "allowed-tools"}
EXPECTED_SKILLS = {
    "oss-audit",
    "oss-plan",
    "oss-refactor",
    "oss-tests",
    "oss-ci",
    "oss-docs",
    "oss-review",
    "oss-review-loop",
    "oss-hardening",
    "oss-search",
}
REQUIRED_TOP_LEVEL_FILES = {
    "README.md",
    "README_CN.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
}

FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")


def parse_frontmatter(text: str) -> dict[str, str]:
    normalized = text.replace("\r\n", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0] != "---":
        raise ValueError("missing opening '---'")
    try:
        closing = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing closing '---'") from exc
    data: dict[str, str] = {}
    for line in lines[1:closing]:
        m = FIELD_RE.match(line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


class SkillLayoutTests(unittest.TestCase):
    def test_expected_skill_dirs_exist(self) -> None:
        found = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
        missing = EXPECTED_SKILLS - found
        self.assertFalse(missing, f"Missing skill directories: {sorted(missing)}")

    def test_each_skill_has_skill_md(self) -> None:
        for skill in EXPECTED_SKILLS:
            skill_file = SKILLS_DIR / skill / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"Missing: {skill_file}")

    def test_no_extra_dirs(self) -> None:
        found = {p.name for p in SKILLS_DIR.iterdir() if p.is_dir()}
        extra = found - EXPECTED_SKILLS
        self.assertFalse(extra, f"Unexpected skill directories: {sorted(extra)}")


class FrontmatterTests(unittest.TestCase):
    def _skill_files(self):
        return [SKILLS_DIR / s / "SKILL.md" for s in EXPECTED_SKILLS]

    def test_required_fields_present(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                meta = parse_frontmatter(path.read_text(encoding="utf-8"))
                for field in REQUIRED_FIELDS:
                    self.assertIn(field, meta, f"{path.parent.name}: missing '{field}'")

    def test_name_matches_directory(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                meta = parse_frontmatter(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    meta.get("name"),
                    path.parent.name,
                    f"{path.parent.name}: 'name' field does not match directory name",
                )

    def test_description_not_empty(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                meta = parse_frontmatter(path.read_text(encoding="utf-8"))
                self.assertTrue(
                    meta.get("description", "").strip(),
                    f"{path.parent.name}: 'description' is empty",
                )

    def test_allowed_tools_not_empty(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                meta = parse_frontmatter(path.read_text(encoding="utf-8"))
                self.assertTrue(
                    meta.get("allowed-tools", "").strip(),
                    f"{path.parent.name}: 'allowed-tools' is empty",
                )

    def test_body_not_empty(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
                lines = text.split("\n")
                closing = lines[1:].index("---") + 1
                body = "\n".join(lines[closing + 1:]).strip()
                self.assertTrue(body, f"{path.parent.name}: skill body is empty")


class RepositoryMetadataTests(unittest.TestCase):
    def test_release_files_exist(self) -> None:
        missing = sorted(
            name for name in REQUIRED_TOP_LEVEL_FILES if not (ROOT / name).exists()
        )
        self.assertFalse(missing, f"Missing top-level release files: {missing}")

    def test_readmes_do_not_use_removed_acronym(self) -> None:
        for readme in ("README.md", "README_CN.md"):
            with self.subTest(readme=readme):
                text = (ROOT / readme).read_text(encoding="utf-8")
                self.assertNotIn("FORGE", text, f"{readme}: found removed acronym 'FORGE'")


REQUIRED_SECTIONS = ["## Anti-patterns", "## Self-check", "## Failure Handling", "## Done Criteria"]


class PromptStructureTests(unittest.TestCase):
    def _skill_files(self):
        return [SKILLS_DIR / s / "SKILL.md" for s in EXPECTED_SKILLS]

    def test_required_sections_present(self) -> None:
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                for section in REQUIRED_SECTIONS:
                    self.assertIn(
                        section, text,
                        f"{path.parent.name}: missing '{section}'"
                    )

    def test_section_order(self) -> None:
        """Anti-patterns and Self-check must appear before Failure Handling."""
        for path in self._skill_files():
            with self.subTest(skill=path.parent.name):
                text = path.read_text(encoding="utf-8")
                idx_anti = text.find("## Anti-patterns")
                idx_self = text.find("## Self-check")
                idx_fail = text.find("## Failure Handling")
                self.assertGreater(idx_anti, -1,
                    f"{path.parent.name}: '## Anti-patterns' not found")
                self.assertGreater(idx_self, -1,
                    f"{path.parent.name}: '## Self-check' not found")
                self.assertGreater(idx_fail, -1,
                    f"{path.parent.name}: '## Failure Handling' not found")
                self.assertLess(idx_anti, idx_fail,
                    f"{path.parent.name}: ## Anti-patterns must appear before ## Failure Handling")
                self.assertLess(idx_self, idx_fail,
                    f"{path.parent.name}: ## Self-check must appear before ## Failure Handling")


if __name__ == "__main__":
    unittest.main()
