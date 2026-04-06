---
name: oss-review-loop
description: Autonomous multi-round open-source review loop. Repeatedly reviews a repository via Codex MCP, applies the minimum hardening fixes, and re-reviews until the repository or paper-code release is ready or max rounds are reached. Use when the user says "review until it passes", "open source review loop", "maintainer review loop", or wants the oss-hardening pipeline to end with an external quality gate and iterative fixes.
argument-hint: [repo-path-or-scope]
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Skill, mcp__codex__codex, mcp__codex__codex-reply
---

# OSS Review Loop

Autonomously iterate: review -> implement the minimum hardening fixes -> re-review, until the external reviewer gives a positive release-readiness assessment or `MAX_ROUNDS` is reached.

## Context: $ARGUMENTS

## Tool Dispatch (priority order)

1. **Official Codex MCP tools** (preferred): call `mcp__codex__codex` for round 1 and `mcp__codex__codex-reply` for rounds 2+. These are the canonical entry points — always try them first.
2. **Codex skill helpers**: if the Codex MCP tools are unavailable or return an error, invoke the `codex:rescue` skill as a fallback to delegate the review task through the Codex CLI runtime.
3. **Manual fallback**: if neither is reachable, record the failure in `OSS_REVIEW_LOOP.md`, surface the blocker to the user, and suggest they verify their Codex MCP setup.

Never skip step 1 and jump to a fallback. Always attempt the official tool first.

## Constants

- MAX_ROUNDS = 4
- POSITIVE_THRESHOLD: score >= 7/10, or verdict contains `ready` or `almost`
- REVIEW_DOC = `OSS_REVIEW_LOOP.md` in the project root
- REVIEWER_MODEL = `gpt-5.4`. Use a currently available Codex model; prefer `gpt-5.4`, `gpt-5.3-codex`, or `gpt-5.2-codex`.

## Input Contract

- Primary input: the repository plus any hardening artifacts that already exist:
  - `OSS_AUDIT.md`
  - `OSS_PLAN.md`
  - `OSS_REFACTOR.md`
  - `OSS_TEST_STRATEGY.md`
  - `OSS_CI.md`
  - `OSS_DOCS.md`
  - `OSS_HARDENING_STATUS.md`
  - `OSS_REVIEW.md` if a one-shot review already happened
- Optional input: explicit release target, contributor audience, support expectations, or constraints like "no new deps".
- Default: if artifacts are partial, review the current repo state and fix the highest-leverage open-source gaps first.

## Output Contract

Create or update `OSS_REVIEW_LOOP.md` as a cumulative log. Each round must include:

1. Overall score
2. Verdict: `ready`, `almost`, or `not ready`
3. Ranked weaknesses
4. Minimum fixes requested by the reviewer
5. Actions taken this round
6. Verification commands and outcomes
7. Full raw reviewer response, preserved verbatim

Also update `OSS_HARDENING_STATUS.md` after every round with:

- current review-loop round
- latest score
- latest verdict
- next recommended stage or command

## Non-goals

- Do not chase cosmetic perfection if the repository is already releasable.
- Do not hide failing checks, weak docs, or missing automation to get a better score.
- Do not broaden the scope beyond the minimum fixes that materially improve release readiness.

## Workflow

### Initialization

1. Read `README*`, `CONTRIBUTING.md`, package/build manifests, CI workflows, tests, and the `OSS_*.md` hardening artifacts.
2. Identify current strengths, known gaps, license or citation status, and available local verification commands.
3. Initialize round counter = 1.
4. Create or update `OSS_REVIEW_LOOP.md` with a header and timestamp.

### Loop (repeat up to MAX_ROUNDS)

#### Phase A: Review via official Codex MCP tools

**Round 1** — call `mcp__codex__codex` directly (the official tool, not a Bash wrapper):

```text
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round 1/MAX_ROUNDS of open-source review loop]

    Repository briefing:
    [purpose, setup commands, verification commands, hardening artifacts, known gaps]

    Please act as a senior open-source maintainer reviewing this repository for public release readiness.

    Evaluate:
    1. Onboarding and usability
    2. Correctness and user safety
    3. Maintainability and structure
    4. Testability and automation
    5. CI and release hygiene
    6. Documentation, licensing, and contributor clarity
    7. Security and responsible maintenance

    Then provide:
    1. Overall score 1-10
    2. Overall verdict: Ready / Almost / Not Ready
    3. Remaining critical weaknesses ranked by severity
    4. For each weakness, specify the MINIMUM fix
    5. For each fix, specify the best return stage: audit / plan / refactor / tests / ci / docs

    Be direct and practical. Focus on the smallest fix package that materially improves open-source quality.
```

Save the returned `threadId` immediately after round 1 — it is required for all subsequent rounds.

**Round 2+** — call `mcp__codex__codex-reply` with the saved `threadId` to maintain conversation context. Do NOT create a new thread for each round.

If `mcp__codex__codex` is unreachable, fall back per the Tool Dispatch priority order above.

#### Phase B: Parse Assessment

Save the full raw response verbatim for the round log. Then extract:

- overall score
- verdict
- ranked weaknesses
- minimum fixes
- return stage for each fix

Stop condition:

- If score >= 7 and verdict contains `ready` or `almost`, stop the loop and document final state.

#### Phase C: Implement Fixes

Apply the minimum fixes in priority order. Use the recommended return stage to guide how you respond:

- `audit`: revisit the repo assumptions and update `OSS_AUDIT.md` and `OSS_PLAN.md` only as needed
- `plan`: tighten scope, ordering, or acceptance criteria in `OSS_PLAN.md`
- `refactor`: apply the smallest structural or tooling change that unlocks maintainability
- `tests`: add or repair CI-safe tests, fixtures, and local verification commands
- `ci`: update or add the minimal workflow needed to enforce checks
- `docs`: tighten README, FAQ, architecture notes, `SECURITY.md`, `CHANGELOG.md`, `LICENSE`, or citation guidance

Rules for implementation:

- Prefer the smallest change set that addresses the reviewer concern
- Reuse the existing `oss-*` stage artifacts instead of inventing a parallel process
- If a fix clearly belongs to another stage skill, follow that stage's contract and update its artifact

#### Phase D: Verify

After implementing fixes:

- run the narrowest relevant local verification commands
- record success or failure
- if a command fails, fix the highest-leverage issue before asking for re-review

Typical verification sources:

- commands documented in `README*`
- commands recorded in `OSS_TEST_STRATEGY.md`
- commands recorded in `OSS_CI.md`
- repository-native scripts such as `npm test`, `python -m unittest`, `pytest`, `cargo test`, `go test ./...`

#### Phase E: Document Round

Append to `OSS_REVIEW_LOOP.md`:

```markdown
## Round N (timestamp)

### Assessment
- Score: X/10
- Verdict: ready / almost / not ready
- Key weaknesses: [bullet list]

### Minimum Fixes Requested
- [fix 1] -> return stage: tests
- [fix 2] -> return stage: docs

### Actions Taken
- [what was changed]

### Verification
- [command] -> [pass/fail]

### Reviewer Raw Response

<details>
<summary>Click to expand full reviewer response</summary>

[paste the complete raw response verbatim]

</details>

### Status
- [continuing to round N+1 / stopping]
```

Update `OSS_HARDENING_STATUS.md` with:

- current round
- latest score
- latest verdict
- current loop status

Increment round counter -> back to Phase A.

### Termination

When the loop ends:

1. Write a final summary to `OSS_REVIEW_LOOP.md`
2. Update `OSS_HARDENING_STATUS.md`
3. If stopped at max rounds without a positive assessment:
   - list the remaining blockers
   - estimate which stage should be revisited next
   - say whether the repo is close to release or still materially blocked

## Anti-patterns

- Do not bypass the official `mcp__codex__codex` / `mcp__codex__codex-reply` tools by shelling out to `codex` directly in Bash — the MCP tools handle authentication, threading, and config automatically.
- Do not ask for re-review before applying and verifying the minimum fixes from the previous round.
- Do not broaden scope beyond the reviewer's minimum-fix package.
- Do not reset context each round; use `mcp__codex__codex-reply` with the saved `threadId` to maintain thread continuity.
- Do not create a new `mcp__codex__codex` thread for rounds 2+; always use `mcp__codex__codex-reply`.
- Do not advance past `MAX_ROUNDS` without surfacing remaining blockers.

## Self-check

Before declaring this stage complete, verify:

- [ ] `OSS_REVIEW_LOOP.md` contains round entries with score, verdict, weaknesses, minimum fixes, actions taken, verification outcomes, and raw response.
- [ ] `OSS_HARDENING_STATUS.md` reflects the latest round number, score, verdict, and next action.
- [ ] Round count does not exceed 4.
- [ ] If the loop stopped without a positive result, remaining blockers and the recommended return stage are explicit.

## Key Rules

- ALWAYS call the official `mcp__codex__codex` / `mcp__codex__codex-reply` tools first; only fall back to `codex:rescue` if the MCP endpoint is unreachable
- ALWAYS use `config: {"model_reasoning_effort": "xhigh"}`
- Save `threadId` from the round 1 `mcp__codex__codex` call and reuse it with `mcp__codex__codex-reply` for all subsequent rounds — never create a new thread mid-loop
- Preserve the full raw reviewer response
- Ask for minimum fixes, not an aspirational rewrite
- Fix issues before re-reviewing; do not just promise changes
- Treat broken setup, missing tests, missing CI, weak docs, missing license or citation path, irreproducible claims, and unsafe release posture as higher severity than polish
- Keep the log self-contained

## Prompt Template for Round 2+ (official `mcp__codex__codex-reply` tool)

Always use the official `mcp__codex__codex-reply` tool for rounds 2+. This preserves thread context and avoids redundant briefings.

```text
mcp__codex__codex-reply:
  threadId: [saved from round 1 mcp__codex__codex call]
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N update]

    Since your last review, we have:
    1. [Action 1]: [result]
    2. [Action 2]: [result]
    3. [Action 3]: [result]

    Updated verification status:
    [commands and outcomes]

    Please re-score and re-assess.
    Same format: Score, Verdict, Remaining Weaknesses, Minimum Fixes, Return Stage for each fix.
```

## Failure Handling

- If `mcp__codex__codex` is unreachable, retry once. If still unavailable, fall back to `codex:rescue` skill. If neither works, record the failure in `OSS_REVIEW_LOOP.md` with the error details and surface the blocker to the user with setup instructions.
- If the reviewer returns a truncated response, use `mcp__codex__codex-reply` on the same thread to request completion.
- If a round's minimum fixes cannot all be applied in one session, apply the highest-leverage fixes and document deferred items explicitly.
- If the loop reaches `MAX_ROUNDS` without a positive verdict, stop, list remaining blockers, and recommend a return stage.

## Done Criteria

- `OSS_REVIEW_LOOP.md` contains 1 to 4 round entries with assessment, minimum fixes, actions taken, verification outcomes, raw response, and status.
- `OSS_HARDENING_STATUS.md` reflects the latest loop state.
- The final state is either a positive readiness assessment or a clear blocker list with a recommended return stage.
