# Contributing

Thanks for helping improve Open Source Hardening Skills.

## What to Edit

- Skill behavior lives in `skills/<name>/SKILL.md`.
- User-facing repository docs live in `README.md`, `README_CN.md`, `SECURITY.md`, and `CHANGELOG.md`.
- CI validation lives in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Local Validation

Run the test suite from the repository root before opening a PR:

```bash
python -m unittest discover -s tests -v
```

The tests validate:

- the expected skill directories exist
- every skill contains required frontmatter
- release metadata files are present

## Contribution Guidelines

- Keep the skill directory name identical to the `name` field in frontmatter.
- Prefer small, reviewable prompt changes over broad rewrites.
- Keep English and Chinese README updates aligned when the change affects onboarding or public usage.
- Do not invent capabilities, support policies, or security guarantees the project does not actually provide.
- If you change user-facing behavior, update `CHANGELOG.md` in the same PR.

## Pull Requests

- Explain what changed and why.
- Include the validation command you ran.
- Link related issues, discussions, or reference repositories when relevant.

## Security

For vulnerabilities, do not open a public issue. Follow the private reporting process in [SECURITY.md](SECURITY.md).
