---
name: oss-refactor
description: Apply careful structure and style hardening to a repository without unnecessary churn. Use when the user says "refactor for maintainability", "set up linting/formatting/types", "clean up this repo", or wants the minimum structural changes needed to make a project easier to maintain.
argument-hint: [scope-or-plan-item]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# OSS Refactor

Harden structure and style with the smallest credible set of changes. Preserve behavior, avoid vanity renames, and prefer extension of existing tooling over toolchain replacement.

## Context: $ARGUMENTS

## Input Contract

- Primary input: `OSS_PLAN.md` or a selected subset of plan items.
- Secondary input: current repo manifests and existing formatter/linter/type-check configuration.
- Default: if no explicit scope is given, work on the highest-priority refactor items from `OSS_PLAN.md`.

## Output Contract

Produce:

1. The requested code/config changes.
2. Minimal tooling configuration additions or updates.
3. `OSS_REFACTOR.md` summarizing:
   - selected scope
   - tooling choices and why
   - touched paths
   - commands run
   - rollback notes if any change should be reconsidered

The final summary in `OSS_REFACTOR.md` must include "Changed now" vs "Deferred intentionally".

## Non-goals

- Do not rename files, functions, or modules just for style consistency.
- Do not reformat the entire repository if only a few files changed.
- Do not introduce multiple new tools when one lightweight tool is enough.
- Do not alter public behavior unless the plan explicitly calls for it.

## Tool Selection Rules

Prefer existing repo choices first. If the repo has nothing yet, choose the lightest credible option:

- Python:
  - Format/lint: prefer `ruff format` + `ruff check`.
  - Type check: add `mypy` only if the repo already has meaningful annotations or the plan explicitly asks for it.
  - If no external deps are acceptable, document the recommendation and limit code changes to structure only.
- TypeScript:
  - Format: `prettier`.
  - Lint: `eslint`.
  - Type check: `tsc --noEmit`.
- JavaScript:
  - Reuse existing package scripts; avoid bolting on TypeScript just for hardening.
- Go:
  - `gofmt`, `go vet`, `go test`.
- Rust:
  - `cargo fmt --check`, `cargo clippy`, `cargo test`.
- Shell:
  - Prefer existing script style.
  - If no toolchain exists, use `bash -n` or `sh -n` validation before adding extra tools.

## Workflow

### Step 1: Confirm the minimum viable scope

- Read the relevant audit and plan items.
- Identify the exact files and boundaries touched by the refactor.
- If the request is vague, limit work to the smallest set that unlocks tests or CI.

### Step 2: Detect current toolchain

- Reuse existing manifests, scripts, config files, and editor conventions.
- Extend existing commands before inventing new top-level entry points.

### Step 3: Apply structural hardening

Examples of valid refactor targets:

- isolate side effects behind small functions
- split a monolithic script into one tiny reusable module plus a thin CLI
- centralize duplicated config/constants
- add explicit exit codes and error messages
- introduce a minimal formatter/linter config

Examples of invalid churn:

- wholesale file moves with no reliability gain
- blanket rename campaigns
- repo-wide style rewrites unrelated to changed code

### Step 4: Verify locally

- Run the narrowest relevant commands after every meaningful change.
- Prefer touched-file formatting/linting when possible.
- Record commands and outcomes in `OSS_REFACTOR.md`.

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

## Failure Handling

- If tooling installation is heavy or conflicts with the repo, stop after documenting the recommendation and keep code changes minimal.
- If a proposed refactor changes behavior, pause and either add tests first or roll back to the last safe structure.
- If hidden scope appears, update `OSS_REFACTOR.md` and hand control back to `/oss-plan` instead of expanding silently.

## Done Criteria

- `OSS_REFACTOR.md` exists and lists selected scope, tooling choices, touched paths, commands run, and rollback notes.
- The artifact includes a `Changed now` section and a `Deferred intentionally` section.
- All new tooling or config additions are minimal and explicitly justified.
