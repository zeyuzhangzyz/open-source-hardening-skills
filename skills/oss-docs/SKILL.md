---
name: oss-docs
description: Improve the repository's open-source documentation and metadata. Use when the user says "improve docs", "make this repo easier to adopt", "fix the README", or wants README polish plus SECURITY.md, CHANGELOG.md, FAQ, architecture notes, and paper-release metadata.
argument-hint: [repo-path-or-doc-scope]
allowed-tools: Read, Grep, Glob, Write, Edit
---

# OSS Docs

Make the repository easier to discover, adopt, and maintain without turning the README into a wall of text.

## Context: $ARGUMENTS

## Input Contract

- Primary input: current `README*`, docs folder, contribution guidance, and the final code/test/CI state.
- Optional input: target audience, supported platforms, support window, and release process.
- Default: if no doc scope is given, cover onboarding plus maintenance metadata.

## Output Contract

Produce:

1. `OSS_DOCS.md` with:
   - README improvement checklist
   - FAQ draft
   - architecture explanation recommendations
   - licensing, citation, and reproducibility notes
   - docs still intentionally deferred
2. Requested document changes in-place.
3. Add `SECURITY.md` if missing.
4. Add `CHANGELOG.md` if missing.
5. Add or improve `LICENSE` if the repository already has a chosen license. If license selection is still undecided, record that as a maintainer decision instead of inventing legal terms.
6. If the repository accompanies a paper, benchmark, dataset, or model release, add `CITATION.cff` or explicit citation instructions.

If the repository already has `SECURITY.md`, `CHANGELOG.md`, `LICENSE`, or `CITATION.cff`, improve the existing file instead of creating duplicates.

The README checklist must cover at least:

- what the project does
- quick start
- how to verify locally
- how to cite or reproduce results if applicable
- contribution entry point
- where deeper docs live

## Non-goals

- Do not duplicate detailed docs inside the README.
- Do not invent guarantees, support policies, or architecture details that the code cannot support.
- Do not create a long doc set that the repository will not maintain.

## Workflow

### Step 1: Keep the README short and useful

- Ensure the README answers: what is this, why does it exist, how do I run it, how do I verify it, where do I learn more.
- Move depth into `docs/` instead of expanding the README endlessly.

### Step 2: Fill open-source metadata gaps

- `SECURITY.md`: reporting channel, supported versions if known, what to include in a report.
- `CHANGELOG.md`: lightweight "Keep a Changelog" style skeleton is enough if no release history exists yet.
- `LICENSE`: required for a real open-source release. If the license has not been chosen yet, surface that gap explicitly instead of guessing.
- `CITATION.cff`: add when the repo backs a paper, benchmark, dataset, or model release.
- FAQ: installation pitfalls, common failure modes, and contributor questions.
- Architecture note: short overview of major modules and data/control flow.
- Reproduction note: external data/model dependencies, expected artifacts, and the smallest public-safe way to validate claims.

### Step 3: Align docs with reality

- Verify commands against the current repo state.
- Link to real files and workflows that exist now.
- Remove stale instructions rather than preserving them for nostalgia.

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

## Failure Handling

- If behavior is uncertain, write an open question instead of making up documentation.
- If the repo is too early for a full architecture document, add a lightweight module map and defer the rest.
- If support or security policy is unknown, provide a maintainer-editable template and call out the placeholders.
- If license choice is unknown, do not choose one on the user's behalf; mark it as a release blocker or explicit maintainer decision.

## Done Criteria

- `OSS_DOCS.md` exists and records README improvements, FAQ content, architecture notes, reproducibility notes, and deferred documentation.
- `README.md`, `SECURITY.md`, and `CHANGELOG.md` exist after the pass, either newly added or updated in place.
- If the repo has a chosen license or needs citation metadata, `LICENSE` and `CITATION.cff` exist; otherwise the unresolved maintainer decision is recorded.
