# Skill Quality Hardening + Simplified Installation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Anti-patterns, Self-check, and verifiable Done Criteria to all 10 skills, add idempotent install scripts, and add plugin manifests.

**Architecture:** TDD first — write failing structural tests, then update each skill to make them pass. Install scripts and manifests are pure additions with no test impact. README/CHANGELOG updated last.

**Tech Stack:** Python 3.10+ unittest, Bash, PowerShell, JSON, YAML, Markdown.

**Spec:** `docs/superpowers/specs/2026-03-17-skill-quality-and-install-design.md`

---

## File Map

| Action | Path | Responsibility |
|--------|------|---------------|
| Modify | `tests/test_skills.py` | Add `PromptStructureTests`: section presence + order |
| Modify | `skills/oss-audit/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-plan/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-refactor/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-tests/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-ci/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-docs/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-review/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-review-loop/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-hardening/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Modify | `skills/oss-search/SKILL.md` | Add Anti-patterns, Self-check, rewrite Done Criteria |
| Create | `install.sh` | Idempotent bash installer for macOS/Linux/WSL |
| Create | `install.ps1` | Idempotent PowerShell installer for Windows |
| Create | `.claude-plugin/plugin.json` | Official Claude Code plugin manifest |
| Create | `plugin.yaml` | Companion manifest with per-skill artifact metadata |
| Modify | `README.md` | Update Install section to reference scripts |
| Modify | `README_CN.md` | Keep aligned with English README install changes |
| Modify | `CHANGELOG.md` | Record this hardening pass |

---

## Task 1: Add Failing Structural Tests

**Files:**
- Modify: `tests/test_skills.py`

- [ ] **Step 1: Add PromptStructureTests class**

Open `tests/test_skills.py`. After the `class RepositoryMetadataTests` block (around line 124), add:

```python
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
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
python -m unittest discover -s tests -v
```

Expected: `PromptStructureTests` fails for all 10 skills (missing `## Anti-patterns` and `## Self-check`).

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_skills.py
git commit -m "test: add PromptStructureTests for required sections and order"
```

---

## Task 2: Update oss-audit

**Files:**
- Modify: `skills/oss-audit/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

Find the line `## Failure Handling` and insert this block immediately before it:

```markdown
## Anti-patterns

- Do not modify code, configs, or docs during the audit unless the user explicitly changed scope.
- Do not report findings without concrete evidence: file path, command output, or missing artifact.
- Do not produce an unprioritized laundry list; every finding must be `P0`, `P1`, or `P2`.
- Do not invent runtime behavior that cannot be verified from code, docs, or commands.
- Do not skip categories because the repo appears simple; record "no findings" explicitly when clean.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_AUDIT.md` exists in the repo root.
- [ ] It contains a repository summary, all seven audit categories, a file-level change table, and a "do first / do later" section.
- [ ] Every finding includes priority, evidence, why it matters, and the smallest credible fix.
- [ ] Any failed command, unclear stack detail, or private-data blocker is recorded explicitly.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

Find and replace the entire `## Done Criteria` section with:

```markdown
## Done Criteria

- `OSS_AUDIT.md` exists and contains the repository summary, all seven audit sections, a prioritized file-level change table, and a "do first / do later" summary.
- Every finding in `OSS_AUDIT.md` includes `P0`, `P1`, or `P2`, evidence, impact, and the smallest credible fix.
- Any release-readiness blocker related to licensing, citation, reproducibility, private assets, or failed commands is recorded explicitly.
```

- [ ] **Step 3: Run tests**

```bash
python -m unittest tests/test_skills.py -v
```

Expected: `oss-audit` subtests pass; others still fail.

- [ ] **Step 4: Commit**

```bash
git add skills/oss-audit/SKILL.md
git commit -m "feat(oss-audit): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 3: Update oss-plan

**Files:**
- Modify: `skills/oss-plan/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not restate the audit verbatim; convert it into reviewable, actionable work items.
- Do not create checklist items without file paths, commands, and acceptance criteria.
- Do not mix launch blockers (`P0`) with aspirational roadmap work in the same checklist tier.
- Do not create items so large they cannot fit in a single reviewable PR.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_PLAN.md` exists in the repo root.
- [ ] It contains a scope summary, staged checklist, execution order, explicit stop points, and a minimum shippable subset section.
- [ ] Every checklist item includes purpose, change points, acceptance criteria, suggested commands, and estimated impact radius.
- [ ] No checklist item is so large it cannot plausibly fit in one reviewable PR.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_PLAN.md` exists and contains a scope summary, staged markdown checklist, execution order, explicit stop points, and a minimum shippable subset section.
- Every checklist item includes purpose, change points, acceptance criteria, suggested commands, and estimated impact radius.
- No item is so large it cannot fit in one reviewable PR.
```

- [ ] **Step 3: Run tests**

```bash
python -m unittest tests/test_skills.py -v
```

Expected: `oss-plan` subtests pass.

- [ ] **Step 4: Commit**

```bash
git add skills/oss-plan/SKILL.md
git commit -m "feat(oss-plan): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 4: Update oss-refactor

**Files:**
- Modify: `skills/oss-refactor/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not modify files outside the planned change list.
- Do not do repo-wide formatting, rename sweeps, or directory churn unrelated to the selected scope.
- Do not add multiple new tools when one light tool or existing tooling is enough.
- Do not allow behavior changes to slip in under the label of "refactor".

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_REFACTOR.md` exists and records selected scope, tooling choices, touched paths, commands run, and rollback notes if any.
- [ ] The artifact includes a `Changed now` section and a `Deferred intentionally` section.
- [ ] Any new tool or config added is explicitly justified in the artifact.
- [ ] Verification commands and outcomes are recorded after the final change set.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_REFACTOR.md` exists and lists selected scope, tooling choices, touched paths, commands run, and rollback notes.
- The artifact includes a `Changed now` section and a `Deferred intentionally` section.
- All new tooling or config additions are minimal and explicitly justified.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-refactor/SKILL.md
git commit -m "feat(oss-refactor): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 5: Update oss-tests

**Files:**
- Modify: `skills/oss-tests/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not optimize for coverage numbers instead of protecting the critical path.
- Do not add tests that need secrets, network access, paid APIs, or large private assets.
- Do not keep flaky tests in the default CI loop; either fix or explicitly exclude them.
- Do not invent test coverage claims that cannot be verified locally.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_TEST_STRATEGY.md` exists and names the framework, test command, mock/fake strategy, and known gaps.
- [ ] It includes a coverage table for: critical path, failure branch, and input validation (or records blockers for missing classes).
- [ ] Actual test files or explicit scaffold targets were added.
- [ ] The chosen test command is recorded as CI-safe, or the blocker is stated clearly.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_TEST_STRATEGY.md` exists and records the chosen framework, exact local test command, mock/fake strategy, known gaps, and coverage table.
- The repo contains test files or scaffold files for the chosen test path.
- The test loop is CI-safe or the blocker preventing that is explicitly recorded.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-tests/SKILL.md
git commit -m "feat(oss-tests): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 6: Update oss-ci

**Files:**
- Modify: `skills/oss-ci/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not create a second workflow that duplicates an existing CI intent without improving it.
- Do not run commands in CI that are not already trusted locally.
- Do not hide omitted checks without recording why they were excluded in `OSS_CI.md`.
- Do not require secrets or live services in the primary blocking workflow.

## Self-check

Before declaring this stage complete, verify:

- [ ] A workflow file exists under `.github/workflows/`.
- [ ] The workflow triggers on both `push` and `pull_request`.
- [ ] The workflow runs lint and test commands that match the repo's local verification path.
- [ ] `OSS_CI.md` records triggers, jobs, cache behavior, local reproduction steps, and known follow-ups.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `.github/workflows/` contains one primary CI workflow for the repo's lint and test path.
- The workflow triggers on `push` and `pull_request`, fails on command failure, and avoids secrets or live services.
- `OSS_CI.md` records triggers, jobs, commands, cache behavior, local reproduction, and remaining gaps.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-ci/SKILL.md
git commit -m "feat(oss-ci): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 7: Update oss-docs

**Files:**
- Modify: `skills/oss-docs/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not turn the README into a dump of all documentation — keep it focused on quick start.
- Do not invent commands, support guarantees, architecture claims, or policies the repo cannot support.
- Do not choose a license or security policy on the maintainer's behalf when it is unknown; record the decision gap instead.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_DOCS.md` exists and includes README checklist, FAQ draft, architecture notes, and licensing/citation/reproducibility notes.
- [ ] `README.md` has project purpose, quick start, local verification, contribution entry point, and deeper-doc links.
- [ ] `SECURITY.md` and `CHANGELOG.md` exist or were improved in place.
- [ ] If applicable, `LICENSE` and `CITATION.cff` exist; otherwise the missing maintainer decision is explicitly recorded.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_DOCS.md` exists and records README improvements, FAQ content, architecture notes, reproducibility notes, and deferred documentation.
- `README.md`, `SECURITY.md`, and `CHANGELOG.md` exist after the pass, either newly added or updated in place.
- If the repo has a chosen license or needs citation metadata, `LICENSE` and `CITATION.cff` exist; otherwise the unresolved maintainer decision is recorded.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-docs/SKILL.md
git commit -m "feat(oss-docs): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 8: Update oss-review

**Files:**
- Modify: `skills/oss-review/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not ask the external reviewer to judge a repo without a concrete repo briefing and current verification evidence.
- Do not paraphrase or trim the raw reviewer response; preserve it verbatim.
- Do not treat stylistic preferences as release blockers.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_REVIEW.md` exists and contains verdict, overall score, category scorecard, strengths, weaknesses, minimum fixes, return-stage mapping, and raw response.
- [ ] The raw reviewer response is preserved verbatim.
- [ ] `OSS_HARDENING_STATUS.md` was updated with the latest score, verdict, and next recommended stage.
- [ ] Prior review history was appended to rather than overwritten.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_REVIEW.md` contains an appended review round with verdict, score, scorecard, strengths, weaknesses, minimum fixes, return-stage mapping, and raw response verbatim.
- `OSS_HARDENING_STATUS.md` records the latest external review score, verdict, and next recommended stage.
- Prior review history remains intact.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-review/SKILL.md
git commit -m "feat(oss-review): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 9: Update oss-review-loop

**Files:**
- Modify: `skills/oss-review-loop/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

Note: `oss-review-loop/SKILL.md` has `## Key Rules` instead of a standard `## Failure Handling`. Read the file first and find the correct insertion point — insert before whatever section comes after the main loop description. If `## Failure Handling` is absent but `## Key Rules` exists, insert before `## Key Rules`.

```markdown
## Anti-patterns

- Do not ask for re-review before applying and verifying the minimum fixes from the previous round.
- Do not broaden scope beyond the reviewer's minimum-fix package.
- Do not reset context each round; use `mcp__codex__codex-reply` with the saved `threadId` to maintain thread continuity.
- Do not advance past `MAX_ROUNDS` without surfacing remaining blockers.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_REVIEW_LOOP.md` contains round entries with score, verdict, weaknesses, minimum fixes, actions taken, verification outcomes, and raw response.
- [ ] `OSS_HARDENING_STATUS.md` reflects the latest round number, score, verdict, and next action.
- [ ] Round count does not exceed 4.
- [ ] If the loop stopped without a positive result, remaining blockers and the recommended return stage are explicit.

```

- [ ] **Step 2: Add `## Failure Handling` section if absent, then `## Done Criteria`**

If `## Failure Handling` is absent in `oss-review-loop/SKILL.md`, add it before `## Done Criteria`:

```markdown
## Failure Handling

- If the external reviewer is unreachable, record the failure in `OSS_REVIEW_LOOP.md` and surface to the user.
- If a round's minimum fixes cannot all be applied in one session, apply the highest-leverage fixes and document deferred items explicitly.
- If the loop reaches `MAX_ROUNDS` without a positive verdict, stop, list remaining blockers, and recommend a return stage.
```

Replace or add `## Done Criteria`:

```markdown
## Done Criteria

- `OSS_REVIEW_LOOP.md` contains 1 to 4 round entries with assessment, minimum fixes, actions taken, verification outcomes, raw response, and status.
- `OSS_HARDENING_STATUS.md` reflects the latest loop state.
- The final state is either a positive readiness assessment or a clear blocker list with a recommended return stage.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-review-loop/SKILL.md
git commit -m "feat(oss-review-loop): add Anti-patterns, Self-check, Failure Handling, rewrite Done Criteria"
```

---

## Task 10: Update oss-hardening

**Files:**
- Modify: `skills/oss-hardening/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not force manual stage-by-stage operation when the user asked for continuous execution.
- Do not auto-advance when a stage's stop/rollback condition has been triggered.
- Do not claim the pipeline is complete if the review loop still reports blockers.
- Do not hide rollback reasons; document them in `OSS_HARDENING_STATUS.md`.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_HARDENING_STATUS.md` exists and lists current stage, completed artifacts, execution mode, unresolved maintainer decisions, next command, and stop/rollback conditions.
- [ ] Every completed stage has a corresponding artifact or an explicit skip reason.
- [ ] If execution paused, the blocker and pause stage are recorded.
- [ ] If execution finished, the final status includes the review-loop verdict and score, or an explicit reason the review loop did not run.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- `OSS_HARDENING_STATUS.md` exists and records current stage, completed artifacts, execution mode, unresolved decisions, next command, and stop/rollback conditions.
- No later stage is marked complete while a required earlier-stage artifact is missing, unless a skip reason is recorded.
- The final status records either successful completion through review-loop or the exact blocker that prevented completion.
```

- [ ] **Step 3: Run tests, Step 4: Commit**

```bash
python -m unittest tests/test_skills.py -v
git add skills/oss-hardening/SKILL.md
git commit -m "feat(oss-hardening): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 11: Update oss-search

**Files:**
- Modify: `skills/oss-search/SKILL.md`

- [ ] **Step 1: Insert Anti-patterns + Self-check before `## Failure Handling`**

```markdown
## Anti-patterns

- Do not return raw HTML, scraped noise, or an unfiltered wall of links.
- Do not cite weak examples when a better official doc or high-signal repo is available.
- Do not stop after one marginal result; triangulate across at least 2 sources.

## Self-check

Before declaring this stage complete, verify:

- [ ] The response contains at least 2 relevant references.
- [ ] Every reference includes a URL and a short note explaining why it matters.
- [ ] For code/CI references, the response identifies the specific pattern, file, or config worth copying.
- [ ] The output is summarized, not dumped raw.

```

- [ ] **Step 2: Replace `## Done Criteria` section**

```markdown
## Done Criteria

- The response includes at least 2 relevant references, each with a URL and a relevance note.
- Any recommended pattern is described concretely enough to copy into the current task.
- If no strong examples were found after retries, that failure is stated explicitly.
```

- [ ] **Step 3: Run full test suite to confirm all pass**

```bash
python -m unittest discover -s tests -v
```

Expected: **ALL tests pass.** If any fail, fix before proceeding.

- [ ] **Step 4: Commit**

```bash
git add skills/oss-search/SKILL.md
git commit -m "feat(oss-search): add Anti-patterns, Self-check, rewrite Done Criteria"
```

---

## Task 12: Add Install Scripts

**Files:**
- Create: `install.sh`
- Create: `install.ps1`

- [ ] **Step 1: Create `install.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/zeyuzhangzyz/open-source-hardening-skills.git}"
CLONE_DIR="${CLONE_DIR:-$HOME/.claude/repos/open-source-hardening-skills}"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

require_cmd git

if [ -d "$CLONE_DIR/.git" ]; then
  git -C "$CLONE_DIR" remote set-url origin "$REPO_URL"
  git -C "$CLONE_DIR" pull --ff-only
else
  mkdir -p "$(dirname "$CLONE_DIR")"
  git clone "$REPO_URL" "$CLONE_DIR"
fi

mkdir -p "$SKILLS_DIR"

for skill_dir in "$CLONE_DIR"/skills/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  target_dir="$SKILLS_DIR/$skill_name"
  rm -rf "$target_dir"
  cp -R "$skill_dir" "$target_dir"
done

installed_count="$(find "$CLONE_DIR/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"

echo "Installed $installed_count skills to $SKILLS_DIR"
echo "Restart Claude Code or run /reload if the skills do not appear immediately."
```

Important: the loop only removes/replaces directories that came from this pack's `skills/` directory. It never clears the entire `$SKILLS_DIR`.

- [ ] **Step 2: Create `install.ps1`**

```powershell
param(
  [string]$RepoUrl = "https://github.com/zeyuzhangzyz/open-source-hardening-skills.git",
  [string]$CloneDir = "$HOME\.claude\repos\open-source-hardening-skills",
  [string]$SkillsDir = "$HOME\.claude\skills"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Missing required command: git"
}

$gitDir = Join-Path $CloneDir ".git"

if (Test-Path $gitDir) {
  & git -C $CloneDir remote set-url origin $RepoUrl | Out-Host
  & git -C $CloneDir pull --ff-only | Out-Host
} else {
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $CloneDir) | Out-Null
  & git clone $RepoUrl $CloneDir | Out-Host
}

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

Get-ChildItem -Path (Join-Path $CloneDir "skills") -Directory | ForEach-Object {
  $targetDir = Join-Path $SkillsDir $_.Name
  if (Test-Path $targetDir) {
    Remove-Item -Recurse -Force $targetDir
  }
  Copy-Item -Recurse -Force $_.FullName $targetDir
}

$installedCount = (Get-ChildItem -Path (Join-Path $CloneDir "skills") -Directory).Count
Write-Host "Installed $installedCount skills to $SkillsDir"
Write-Host "Restart Claude Code or run /reload if the skills do not appear immediately."
```

- [ ] **Step 3: Make install.sh executable and commit**

```bash
chmod +x install.sh
git add install.sh install.ps1
git commit -m "feat: add idempotent install.sh and install.ps1"
```

---

## Task 13: Add Plugin Manifests

**Files:**
- Create: `.claude-plugin/plugin.json`
- Create: `plugin.yaml`

- [ ] **Step 1: Create `.claude-plugin/plugin.json`**

Create directory `.claude-plugin/` and add `plugin.json`:

```json
{
  "name": "open-source-hardening-skills",
  "version": "0.2.0",
  "description": "Open-source hardening skill pack for Claude Code: audit, plan, refactor, tests, CI, docs, review, review-loop, hardening orchestration, and reference search.",
  "author": {
    "name": "zeyuzhangzyz"
  },
  "homepage": "https://github.com/zeyuzhangzyz/open-source-hardening-skills",
  "repository": "https://github.com/zeyuzhangzyz/open-source-hardening-skills",
  "license": "MIT",
  "keywords": [
    "claude-code",
    "skills",
    "open-source",
    "hardening",
    "ci",
    "tests",
    "docs",
    "security"
  ],
  "skills": "./skills/"
}
```

- [ ] **Step 2: Create `plugin.yaml`**

At the repo root:

```yaml
schema_version: 1
kind: claude-code-plugin-mirror
name: open-source-hardening-skills
version: "0.2.0"
description: Open-source hardening skill pack for Claude Code.
author:
  name: zeyuzhangzyz
homepage: https://github.com/zeyuzhangzyz/open-source-hardening-skills
repository: https://github.com/zeyuzhangzyz/open-source-hardening-skills
license: MIT
keywords:
  - claude-code
  - skills
  - open-source
  - hardening
  - ci
  - tests
  - docs
  - security
claude_code:
  manifest: .claude-plugin/plugin.json
  skills: ./skills/
  standalone_install_dir: ~/.claude/skills
skills:
  - name: oss-audit
    path: skills/oss-audit/SKILL.md
    outputs: [OSS_AUDIT.md]
  - name: oss-plan
    path: skills/oss-plan/SKILL.md
    outputs: [OSS_PLAN.md]
  - name: oss-refactor
    path: skills/oss-refactor/SKILL.md
    outputs: [OSS_REFACTOR.md]
  - name: oss-tests
    path: skills/oss-tests/SKILL.md
    outputs: [OSS_TEST_STRATEGY.md]
  - name: oss-ci
    path: skills/oss-ci/SKILL.md
    outputs: [OSS_CI.md]
  - name: oss-docs
    path: skills/oss-docs/SKILL.md
    outputs: [OSS_DOCS.md]
  - name: oss-review
    path: skills/oss-review/SKILL.md
    outputs: [OSS_REVIEW.md, OSS_HARDENING_STATUS.md]
  - name: oss-review-loop
    path: skills/oss-review-loop/SKILL.md
    outputs: [OSS_REVIEW_LOOP.md, OSS_HARDENING_STATUS.md]
  - name: oss-hardening
    path: skills/oss-hardening/SKILL.md
    outputs: [OSS_HARDENING_STATUS.md]
  - name: oss-search
    path: skills/oss-search/SKILL.md
optional_integrations:
  - name: codex-mcp
    required_for:
      - oss-review
      - oss-review-loop
validation:
  command: python -m unittest discover -s tests -v
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/plugin.json plugin.yaml
git commit -m "feat: add .claude-plugin/plugin.json and plugin.yaml manifests"
```

---

## Task 14: Update README.md and README_CN.md

**Files:**
- Modify: `README.md`
- Modify: `README_CN.md`

- [ ] **Step 1: Update `README.md` Install section**

Replace the "### 2. Install the skills" block with a simpler one-liner approach that references the scripts:

```markdown
### 2. Install the skills

**macOS / Linux / WSL (one-liner):**

```bash
curl -fsSL https://raw.githubusercontent.com/zeyuzhangzyz/open-source-hardening-skills/main/install.sh | bash
```

Or clone and run manually:

```bash
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
cd open-source-hardening-skills
bash install.sh
```

**Windows PowerShell (one-liner):**

```powershell
irm https://raw.githubusercontent.com/zeyuzhangzyz/open-source-hardening-skills/main/install.ps1 | iex
```

Or clone and run manually:

```powershell
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
cd open-source-hardening-skills
.\install.ps1
```

The install scripts are idempotent: re-running them updates the skills to the latest version. They only replace this pack's own `oss-*` skill directories and never touch other skills you may have installed.
```

- [ ] **Step 2: Update `README_CN.md` Install section**

Apply the equivalent changes in Chinese. Translate the new install instructions, keeping them aligned with the English version.

- [ ] **Step 3: Commit**

```bash
git add README.md README_CN.md
git commit -m "docs: update install section with one-liner scripts"
```

---

## Task 15: Update CHANGELOG.md

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Read current CHANGELOG.md to understand format**

- [ ] **Step 2: Prepend a new entry at the top**

Add at the top (after the title/header):

```markdown
## [Unreleased]

### Added
- `## Anti-patterns` section in all 10 skills: explicit prohibitions for the most common AI failure modes per stage.
- `## Self-check` section in all 10 skills: verifiable completion checklist that mirrors Done Criteria.
- `install.sh`: idempotent bash installer for macOS/Linux/WSL.
- `install.ps1`: idempotent PowerShell installer for Windows.
- `.claude-plugin/plugin.json`: official Claude Code plugin manifest.
- `plugin.yaml`: companion manifest with per-skill artifact metadata.

### Changed
- `## Done Criteria` rewritten in all 10 skills: from judgment-based to artifact-based verifiable criteria.
- `tests/test_skills.py`: added `PromptStructureTests` enforcing section presence and ordering.
- `README.md`, `README_CN.md`: updated install section with one-liner curl/irm commands.
```

- [ ] **Step 3: Run full test suite one final time**

```bash
python -m unittest discover -s tests -v
```

Expected: **ALL tests pass.**

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for skill quality hardening pass"
```

---

## Final Verification

- [ ] Run full test suite: `python -m unittest discover -s tests -v` → all pass
- [ ] Confirm 10 skills all have `## Anti-patterns`, `## Self-check`, `## Failure Handling`, `## Done Criteria` in correct order
- [ ] Confirm `install.sh` and `install.ps1` exist at repo root
- [ ] Confirm `.claude-plugin/plugin.json` and `plugin.yaml` exist
- [ ] Confirm `README.md` install section references the one-liner scripts
