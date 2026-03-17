# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows a simple maintainer-edited changelog process.

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

---

## [Unreleased - prior]

### Added

- Added a dedicated [CONTRIBUTING.md](CONTRIBUTING.md) guide.
- Added a project changelog for release-facing updates.
- Added metadata tests to ensure release-critical top-level files remain present.

### Changed

- Removed the previous short project alias from public-facing documentation.
- Expanded installation docs with Claude Code setup, first-run initialization, and Windows PowerShell copy commands.
- Clarified repository standards and local verification steps in both `README.md` and `README_CN.md`.
