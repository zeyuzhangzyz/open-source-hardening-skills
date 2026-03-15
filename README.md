# Open Source Hardening Skills

**English** | [中文](README_CN.md)

Open Source Hardening Skills is a skill pack for [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) / Claude Code that hardens any repository - app, library, CLI tool, or research paper codebase - into a readable, testable, maintainable open-source project.

> **Pairs naturally with ARIS.** ARIS runs research autonomously overnight; Open Source Hardening Skills is the next step that gets the resulting code ready for public release.

## Workflow

```text
[ARIS research pipeline]           [Open Source Hardening Skills pipeline]
  /idea-discovery                    /oss-audit        -> scan for gaps
  /auto-review-loop    ------>       /oss-plan         -> make a checklist
  /paper-writing                     /oss-refactor     -> minimal cleanup
  (code exists)                      /oss-tests        -> add CI-safe tests
                                     /oss-ci           -> block bad PRs
                                     /oss-docs         -> polish docs
                                     /oss-review-loop  -> external quality gate
                                     (repo is release-ready)
```

Open Source Hardening Skills also works **standalone** on any existing repository - no ARIS required.

## Skills

| Skill | Trigger | What it does |
|-------|---------|--------------|
| oss-audit | `/oss-audit` | Scans 7 dimensions, outputs a prioritized file-level report (`OSS_AUDIT.md`) |
| oss-plan | `/oss-plan` | Converts audit findings into a PR-ready checklist (`OSS_PLAN.md`) |
| oss-refactor | `/oss-refactor` | Applies the smallest structural changes needed to unlock tests and CI |
| oss-tests | `/oss-tests` | Builds a minimal automated test loop that runs without secrets |
| oss-ci | `/oss-ci` | Adds or improves a GitHub Actions pipeline that blocks broken PRs |
| oss-docs | `/oss-docs` | Polishes README, adds SECURITY.md, CHANGELOG.md, and contribution guidance |
| oss-review | `/oss-review` | One-shot external review via Codex MCP (GPT-5.4) |
| oss-review-loop | `/oss-review-loop` | Iterative review -> fix -> re-review until release-ready (max 4 rounds) |
| oss-hardening | `/oss-hardening` | Orchestrates the full pipeline end-to-end in one command |
| oss-search | `/oss-search` | Searches GitHub and the web for reference repos, CI examples, and best practices - no API keys required |

## Install

### 1. Install and initialize Claude Code

Install Claude Code first, then open it once to finish login and create `~/.claude/`:

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

```bash
cd your-project
claude
```

### 2. Install the skills

macOS / Linux / WSL:

```bash
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
mkdir -p ~/.claude/skills
cp -r open-source-hardening-skills/skills/* ~/.claude/skills/
```

Windows PowerShell:

```powershell
git clone https://github.com/zeyuzhangzyz/open-source-hardening-skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\open-source-hardening-skills\skills\*" "$HOME\.claude\skills\"
```

If the skills do not appear after copying, restart the Claude Code session.

### 3. Optional: set up Codex MCP for review skills

`/oss-review` and `/oss-review-loop` require Codex MCP (same setup as ARIS). The other 8 skills work without it.

```bash
npm install -g @openai/codex
codex setup   # set model to gpt-5.4 when prompted
claude mcp add codex -s user -- codex mcp-server
```

### 4. Run in your target repository

```text
/oss-hardening .
```

## Use with ARIS

Open Source Hardening Skills installs to the same `~/.claude/skills/` directory as ARIS and works alongside ARIS skills without conflicts.

```bash
# After an ARIS research run, harden the resulting code:
/oss-hardening .
```

## Repository Layout

```text
skills/              ARIS-compatible skill files (one subdirectory per skill)
  oss-audit/SKILL.md
  oss-plan/SKILL.md
  ...
tests/               skill validation tests
```

## Project Standards

- [SECURITY.md](SECURITY.md) describes how to report vulnerabilities privately.
- [CHANGELOG.md](CHANGELOG.md) tracks release-facing changes.
- [CONTRIBUTING.md](CONTRIBUTING.md) explains how to edit skills and validate the repo locally.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs the validation suite on every push and pull request.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For the quick version: edit `skills/<name>/SKILL.md`, then run the validation suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

Open a PR when done. Each skill directory name must match the `name` field in the frontmatter.

## Acknowledgements

- **[ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep)** - autonomous ML research skill pack that this project is designed to complement; the skill layout follows ARIS conventions directly.
- **[Claude Code](https://github.com/anthropics/claude-code)** - Anthropic's CLI, the execution backbone.

## License

MIT. See [LICENSE](LICENSE).
