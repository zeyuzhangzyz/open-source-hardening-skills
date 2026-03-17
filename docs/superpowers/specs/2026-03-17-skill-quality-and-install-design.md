# Design Spec: Skill Quality Hardening + Simplified Installation

**Date:** 2026-03-17
**Status:** Approved for implementation
**Scope:** All 10 skills in `open-source-hardening-skills`

---

## Problem Statement

The current skills are structurally consistent but rely on judgment-based completion conditions. AI agents executing the pipeline can:
- Silently skip steps when artifacts look "complete enough"
- Expand scope beyond the planned change set
- Produce outputs that lack the concrete evidence needed to action downstream stages

Additionally, installation requires manual file copying with platform-specific shell commands, creating friction for new users.

---

## Goals

1. **Prompt quality**: Make every skill more reliable by adding explicit anti-patterns and self-verification checklists.
2. **Done Criteria clarity**: Rewrite vague criteria into artifact-based, verifiable forms.
3. **Simpler installation**: Provide idempotent install scripts (bash + PowerShell).
4. **Plugin-ready structure**: Add `.claude-plugin/plugin.json` + `plugin.yaml` for future plugin manager compatibility.
5. **Test coverage**: Add a prompt-lint test that enforces the new required sections.

---

## Approach: Targeted Prompt Hardening (Approach A)

### 1. Two New Sections Per Skill

Insert into every `SKILL.md`, **before** `## Failure Handling`:

#### `## Anti-patterns`

3–5 explicit prohibitions, specific to each skill's job. Written as "Do not…" rules targeting the most common AI failure modes for that stage.

#### `## Self-check`

A verifiable checklist the AI must pass before declaring the stage complete. Every Self-check item must have a 1:1 declarative counterpart in `## Done Criteria`. Drift between the two sections is invalid, not tolerated — when editing one, the other must be updated in the same change.

### 2. Done Criteria Rewrite

All vague Done Criteria ("the user can understand…", "the agent has a plan…") are rewritten as:
- Artifact existence: "`OSS_PLAN.md` exists in the repo root"
- Content requirements: "contains a staged checklist, execution order, and minimum shippable subset section"
- Verifiable commands: "test command exits 0 locally"
- Explicit failure recording: "any blocker preventing CI-safety is stated explicitly"

---

## Per-Skill Anti-patterns

### oss-audit
- Do not modify code, configs, or docs during the audit unless the user explicitly changed scope.
- Do not report findings without concrete evidence: file path, command output, or missing artifact.
- Do not produce an unprioritized laundry list; every finding must be `P0`, `P1`, or `P2`.
- Do not invent runtime behavior that cannot be verified from code, docs, or commands.
- Do not skip categories because the repo appears simple; record "no findings" explicitly when clean.

### oss-plan
- Do not restate the audit verbatim; convert it into reviewable, actionable work items.
- Do not create checklist items without file paths, commands, and acceptance criteria.
- Do not mix launch blockers (`P0`) with aspirational roadmap work in the same checklist tier.
- Do not create items so large they cannot fit in a single reviewable PR.

### oss-refactor
- Do not modify files outside the planned change list.
- Do not do repo-wide formatting, rename sweeps, or directory churn unrelated to the selected scope.
- Do not add multiple new tools when one light tool or existing tooling is enough.
- Do not allow behavior changes to slip in under the label of "refactor".

### oss-tests
- Do not optimize for coverage numbers instead of protecting the critical path.
- Do not add tests that need secrets, network access, paid APIs, or large private assets.
- Do not keep flaky tests in the default CI loop; either fix or explicitly exclude them.
- Do not invent test coverage claims that cannot be verified locally.

### oss-ci
- Do not create a second workflow that duplicates an existing CI intent without improving it.
- Do not run commands in CI that are not already trusted locally.
- Do not hide omitted checks without recording why they were excluded in `OSS_CI.md`.
- Do not require secrets or live services in the primary blocking workflow.

### oss-docs
- Do not turn the README into a dump of all documentation — keep it focused on quick start.
- Do not invent commands, support guarantees, architecture claims, or policies the repo cannot support.
- Do not choose a license or security policy on the maintainer's behalf when it is unknown; record the decision gap instead.

### oss-review
- Do not ask the external reviewer to judge a repo without a concrete repo briefing and current verification evidence.
- Do not paraphrase or trim the raw reviewer response; preserve it verbatim.
- Do not treat stylistic preferences as release blockers.

### oss-review-loop
- Do not ask for re-review before applying and verifying the minimum fixes from the previous round.
- Do not broaden scope beyond the reviewer's minimum-fix package.
- Do not reset context each round; use `codex-reply` to maintain thread continuity.
- Do not advance past `MAX_ROUNDS` without surfacing remaining blockers.

### oss-hardening
- Do not force manual stage-by-stage operation when the user asked for continuous execution.
- Do not auto-advance when a stage's stop/rollback condition has been triggered.
- Do not claim the pipeline is complete if the review loop still reports blockers.
- Do not hide rollback reasons; document them in `OSS_HARDENING_STATUS.md`.

### oss-search
- Do not return raw HTML, scraped noise, or an unfiltered wall of links.
- Do not cite weak examples when a better official doc or high-signal repo is available.
- Do not stop after one marginal result; triangulate across at least 2 sources.

---

## Per-Skill Self-check Checklists

### oss-audit
- [ ] `OSS_AUDIT.md` exists in the repo root.
- [ ] It contains a repository summary, all seven audit categories, a file-level change table, and a "do first / do later" section.
- [ ] Every finding includes priority, evidence, why it matters, and the smallest credible fix.
- [ ] Any failed command, unclear stack detail, or private-data blocker is recorded explicitly.

### oss-plan
- [ ] `OSS_PLAN.md` exists in the repo root.
- [ ] It contains a scope summary, staged checklist, execution order, explicit stop points, and a minimum shippable subset section.
- [ ] Every checklist item includes purpose, change points, acceptance criteria, suggested commands, and estimated impact radius.
- [ ] No checklist item is so large it cannot plausibly fit in one reviewable PR.

### oss-refactor
- [ ] `OSS_REFACTOR.md` exists and records selected scope, tooling choices, touched paths, commands run, and rollback notes if any.
- [ ] The artifact includes a `Changed now` section and a `Deferred intentionally` section.
- [ ] Any new tool or config added is explicitly justified in the artifact.
- [ ] Verification commands and outcomes are recorded after the final change set.

### oss-tests
- [ ] `OSS_TEST_STRATEGY.md` exists and names the framework, test command, mock/fake strategy, and known gaps.
- [ ] It includes a coverage table for: critical path, failure branch, and input validation (or records blockers for missing classes).
- [ ] Actual test files or explicit scaffold targets were added.
- [ ] The chosen test command is recorded as CI-safe, or the blocker is stated clearly.

### oss-ci
- [ ] A workflow file exists under `.github/workflows/`.
- [ ] The workflow triggers on both `push` and `pull_request`.
- [ ] The workflow runs lint and test commands that match the repo's local verification path.
- [ ] `OSS_CI.md` records triggers, jobs, cache behavior, local reproduction steps, and known follow-ups.

### oss-docs
- [ ] `OSS_DOCS.md` exists and includes README checklist, FAQ draft, architecture notes, and licensing/citation/reproducibility notes.
- [ ] `README.md` has project purpose, quick start, local verification, contribution entry point, and deeper-doc links.
- [ ] `SECURITY.md` and `CHANGELOG.md` exist or were improved in place.
- [ ] If applicable, `LICENSE` and `CITATION.cff` exist; otherwise the missing maintainer decision is explicitly recorded.

### oss-review
- [ ] `OSS_REVIEW.md` exists and contains verdict, overall score, category scorecard, strengths, weaknesses, minimum fixes, return-stage mapping, and raw response.
- [ ] The raw reviewer response is preserved verbatim.
- [ ] `OSS_HARDENING_STATUS.md` was updated with the latest score, verdict, and next recommended stage.
- [ ] Prior review history was appended to rather than overwritten.

### oss-review-loop
- [ ] `OSS_REVIEW_LOOP.md` contains round entries with score, verdict, weaknesses, minimum fixes, actions taken, verification outcomes, and raw response.
- [ ] `OSS_HARDENING_STATUS.md` reflects the latest round number, score, verdict, and next action.
- [ ] Round count does not exceed 4.
- [ ] If the loop stopped without a positive result, remaining blockers and the recommended return stage are explicit.

### oss-hardening
- [ ] `OSS_HARDENING_STATUS.md` exists and lists current stage, completed artifacts, execution mode, unresolved maintainer decisions, next command, and stop/rollback conditions.
- [ ] Every completed stage has a corresponding artifact or an explicit skip reason.
- [ ] If execution paused, the blocker and pause stage are recorded.
- [ ] If execution finished, the final status includes the review-loop verdict and score, or an explicit reason the review loop did not run.

### oss-search
- [ ] The response contains at least 2 relevant references.
- [ ] Every reference includes a URL and a short note explaining why it matters.
- [ ] For code/CI references, the response identifies the specific pattern, file, or config worth copying.
- [ ] The output is summarized, not dumped raw.

---

## Done Criteria Rewrites

Each skill's `## Done Criteria` is rewritten from judgment-based to artifact-based. The rewritten criteria are the declarative form of the Self-check items above — each Self-check item has a 1:1 counterpart here. The rule for all criteria: must match "X exists and contains Y" or "command Z exits 0" or "blocker is recorded explicitly".

**oss-audit:** `OSS_AUDIT.md` exists and contains the repository summary, all seven audit sections, a prioritized file-level change table, and a "do first / do later" summary. Every finding includes `P0`/`P1`/`P2`, evidence, impact, and the smallest credible fix. Any release-readiness blocker (licensing, citation, reproducibility, private assets, failed commands) is recorded explicitly.

**oss-plan:** `OSS_PLAN.md` exists and contains a scope summary, staged markdown checklist, execution order, explicit stop points, and a minimum shippable subset section. Every checklist item includes purpose, change points, acceptance criteria, suggested commands, and estimated impact radius. No item is so large it cannot fit in one reviewable PR.

**oss-refactor:** `OSS_REFACTOR.md` exists and lists selected scope, tooling choices, touched paths, commands run, and rollback notes. The artifact includes `Changed now` and `Deferred intentionally` sections. All new tooling or config additions are minimal and justified.

**oss-tests:** `OSS_TEST_STRATEGY.md` exists and records the chosen framework, exact local test command, mock/fake strategy, known gaps, and coverage table. The repo contains test files or scaffold files for the chosen test path. The test loop is CI-safe or the blocker is explicitly recorded.

**oss-ci:** `.github/workflows/` contains one primary CI workflow for the repo's lint and test path. The workflow triggers on `push` and `pull_request`, fails on command failure, and avoids secrets or live services. `OSS_CI.md` records triggers, jobs, commands, cache behavior, local reproduction, and remaining gaps.

**oss-docs:** `OSS_DOCS.md` exists and records README improvements, FAQ content, architecture notes, reproducibility notes, and deferred documentation. `README.md`, `SECURITY.md`, and `CHANGELOG.md` exist after the pass. If the repo has a chosen license or needs citation metadata, `LICENSE` and `CITATION.cff` exist; otherwise the unresolved decision is recorded.

**oss-review:** `OSS_REVIEW.md` contains an appended review round with verdict, score, scorecard, strengths, weaknesses, minimum fixes, return-stage mapping, and raw response verbatim. `OSS_HARDENING_STATUS.md` records the latest score, verdict, and next recommended stage. Prior history is preserved.

**oss-review-loop:** `OSS_REVIEW_LOOP.md` contains 1 to 4 round entries with assessment, minimum fixes, actions taken, verification outcomes, raw response, and status. `OSS_HARDENING_STATUS.md` reflects the latest loop state. The final state is either a positive readiness assessment or a clear blocker list with a recommended return stage.

**oss-hardening:** `OSS_HARDENING_STATUS.md` exists and records current stage, completed artifacts, execution mode, unresolved decisions, next command, and stop/rollback conditions. No later stage is marked complete while a required earlier-stage artifact is missing (unless a skip reason is recorded). Final status records either successful completion through review-loop or the exact blocker preventing it.

**oss-search:** The response includes at least 2 relevant references, each with a URL and a relevance note. Any recommended pattern is described concretely enough to copy. If no strong examples were found after retries, that failure is stated explicitly.

---

## Installation

### install.sh (macOS / Linux / WSL)

Idempotent: clones on first run, pulls on subsequent runs. Copies each `skills/*/` directory to `~/.claude/skills/`.

Key behavior:
- Respects `$REPO_URL`, `$CLONE_DIR`, `$SKILLS_DIR` env overrides
- Fails fast on missing `git`
- Prints count of installed skills on success
- **Only replaces this pack's own skill directories** (`oss-*`). Never deletes or touches unrelated entries already present under `~/.claude/skills/`.

### install.ps1 (Windows PowerShell)

Same logic as `install.sh`, using PowerShell idioms. Accepts `-RepoUrl`, `-CloneDir`, `-SkillsDir` parameters.

---

## Plugin Manifest

Two files at different locations:

### `.claude-plugin/plugin.json`
Lives inside the `.claude-plugin/` subdirectory (not the repo root). This is the official Claude Code plugin manifest format. Enables future `claude plugin install` UX. Contains: name, version, description, author, skills path, homepage, license, keywords.

### `plugin.yaml`
Lives at the **repo root**. Mirror/companion file for non-Claude-Code tooling. Additionally lists per-skill output artifacts, optional Codex MCP integration requirements, and the validation command. References `.claude-plugin/plugin.json` as the authoritative manifest.

---

## Test Updates

Add a prompt-lint test class to `tests/test_skills.py`:

```python
REQUIRED_SECTIONS = ["## Anti-patterns", "## Self-check", "## Failure Handling", "## Done Criteria"]
# Order enforced: Anti-patterns and Self-check must appear before Failure Handling

class PromptStructureTests(unittest.TestCase):
    def test_required_sections_present(self):
        for skill in EXPECTED_SKILLS:
            path = SKILLS_DIR / skill / "SKILL.md"
            with self.subTest(skill=skill):
                text = path.read_text(encoding="utf-8")
                for section in REQUIRED_SECTIONS:
                    self.assertIn(section, text, f"{skill}: missing '{section}'")

    def test_section_order(self):
        """Anti-patterns and Self-check must appear before Failure Handling."""
        for skill in EXPECTED_SKILLS:
            path = SKILLS_DIR / skill / "SKILL.md"
            with self.subTest(skill=skill):
                text = path.read_text(encoding="utf-8")
                idx_anti = text.find("## Anti-patterns")
                idx_self = text.find("## Self-check")
                idx_fail = text.find("## Failure Handling")
                self.assertLess(idx_anti, idx_fail,
                    f"{skill}: ## Anti-patterns must appear before ## Failure Handling")
                self.assertLess(idx_self, idx_fail,
                    f"{skill}: ## Self-check must appear before ## Failure Handling")
```

---

## File Change List

| Priority | Path | Action | Reason |
|----------|------|--------|--------|
| P0 | `skills/oss-audit/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-plan/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-refactor/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-tests/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-ci/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-docs/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-review/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-review-loop/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-hardening/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `skills/oss-search/SKILL.md` | modify | Add Anti-patterns, Self-check, rewrite Done Criteria |
| P0 | `tests/test_skills.py` | modify | Add PromptStructureTests to enforce new required sections |
| P1 | `install.sh` | add | Idempotent bash installer for macOS/Linux/WSL |
| P1 | `install.ps1` | add | Idempotent PowerShell installer for Windows |
| P1 | `.claude-plugin/plugin.json` | add | Official Claude Code plugin manifest |
| P1 | `plugin.yaml` | add | Companion manifest with per-skill artifact metadata |
| P1 | `README.md` | modify | Update install section to reference install.sh / install.ps1 |
| P1 | `README_CN.md` | modify | Keep Chinese README aligned with install changes |
| P2 | `CHANGELOG.md` | modify | Record this hardening pass |

---

## Non-goals

- Do not change skill execution logic or pipeline ordering.
- Do not add new skills.
- Do not introduce new runtime dependencies.
- Do not restructure the `skills/` directory layout.
