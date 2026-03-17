---
name: oss-hardening
description: Orchestrate an end-to-end open-source hardening pass for a repository. Use when the user wants to turn a loose codebase or paper-code release into a readable, testable, maintainable open-source project and wants audit, plan, refactor, tests, CI, and docs to run as one continuous workflow unless a blocker appears.
argument-hint: [repo-path-or-scope]
allowed-tools: Read, Grep, Glob, Write, Skill
---

# OSS Hardening

Run a staged hardening pipeline in one continuous pass by default:

1. `/oss-audit`
2. `/oss-plan`
3. `/oss-refactor`
4. `/oss-tests`
5. `/oss-ci`
6. `/oss-docs`
7. `/oss-review-loop`

Default behavior:

- execute `audit -> plan -> refactor -> tests -> ci -> docs -> review-loop` in one invocation
- carry artifacts forward automatically between stages
- only pause when a real blocker, rollback condition, or user-requested stop point appears

Do not force the user to manually re-issue every stage command unless they explicitly ask for stage-by-stage control.

## Context: $ARGUMENTS

## Input Contract

- Input: repository path or scope, user constraints, optional stop point, whether the repo is product code or paper code, and any "continuous" or "manual" preference.
- Default: if no stop point is given, run the full pipeline continuously from audit to docs.

## Output Contract

Create or update `OSS_HARDENING_STATUS.md` with:

- current stage
- completed artifacts
- whether execution auto-continued or paused
- latest external review-loop score and verdict if review ran
- unresolved maintainer decisions such as license choice or missing citation path
- next recommended command
- explicit stop/rollback conditions

If the workflow pauses, give the user a short "where we are / what comes next" summary. If the workflow finishes continuously, give one end-to-end summary plus any blockers left deferred.

## Stage Order

### 1. Audit

Run `/oss-audit` first, then continue directly to `/oss-plan` if no blocker is found.

Stop here if:

- there is no reproducible local run command yet
- the repo appears abandoned or generated
- the scope is too unclear to change safely
- the repo depends on private data or checkpoints with no public-safe sample path yet

### 2. Plan

Run `/oss-plan` once the audit has concrete `P0/P1/P2` findings, then continue directly to `/oss-refactor` when the plan is actionable.

Stop here if:

- the plan still contains unresolved "discover first" tasks
- one checklist item is too large to review safely

### 3. Refactor

Run `/oss-refactor` only for the smallest structural changes needed to unlock tests and CI, then continue directly to `/oss-tests` when behavior remains stable.

Rollback or pause if:

- behavior changes unexpectedly
- the refactor starts expanding beyond the planned file set
- new tooling creates more maintenance burden than value

### 4. Tests

Run `/oss-tests` after the structure is stable enough to test, then continue directly to `/oss-ci` when the local test command is trustworthy.

Stop here if:

- the only available tests are flaky or rely on live services
- external dependencies still need seams or mocks

### 5. CI

Run `/oss-ci` only after local lint and test commands are trustworthy, then continue directly to `/oss-docs` once CI reflects the intended local workflow.

Rollback or pause if:

- the workflow requires secrets
- the workflow duplicates an existing pipeline without improving it

### 6. Docs

Run `/oss-docs` so the documentation reflects the final behavior and commands, then continue directly to `/oss-review-loop` if all prior stages passed cleanly.

Stop here if:

- the implementation state is still changing daily
- support, license, citation, or security ownership is unknown and needs maintainer input

### 7. Review Loop

Run `/oss-review-loop` after docs so the pipeline ends with an external Codex quality gate and up to four rounds of iterative fixes.

If the loop returns:

- `ready`: finish the hardening pass
- `almost`: either stop with explicit remaining gaps or do one targeted follow-up pass and rerun review
- `not ready`: return to the highest-leverage recommended stage (`audit`, `plan`, `refactor`, `tests`, `ci`, or `docs`)

`/oss-review` remains useful as a one-shot checkpoint when the user wants a single external pass without the full loop.

## Non-goals

- Do not merge all six stages into one opaque report.
- Do not require manual stage-by-stage interaction unless the user asks for it.
- Do not push through later stages when earlier artifacts are incomplete.
- Do not hide rollback reasons; document them in `OSS_HARDENING_STATUS.md`.

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

## Failure Handling

- If a later stage reveals a new foundational issue, return to `/oss-audit` or `/oss-plan` and record why.
- If the user only wants one stage, honor that and update the status file accordingly.
- If the repo already has mature tests or CI, skip duplicate work and focus on the missing stages.
- In continuous mode, pause only on blockers; otherwise auto-advance to the next stage.
- If `/oss-review-loop` fails the repo after max rounds, record the recommended return stage and do not claim the pipeline is complete.

## Done Criteria

- `OSS_HARDENING_STATUS.md` exists and records current stage, completed artifacts, execution mode, unresolved decisions, next command, and stop/rollback conditions.
- No later stage is marked complete while a required earlier-stage artifact is missing, unless a skip reason is recorded.
- The final status records either successful completion through review-loop or the exact blocker that prevented completion.
