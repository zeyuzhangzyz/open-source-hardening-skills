---
name: oss-search
description: Search GitHub and the web for reference repositories, code patterns, CI examples, and open-source best practices. No API keys required. Use when the user says "find similar repos", "search GitHub", "look up best practices", or when oss-audit / oss-refactor needs external reference material.
argument-hint: [query or topic]
allowed-tools: WebFetch
---

# OSS Search

Search GitHub and the web for reference material to support the hardening pipeline. All searches use direct URL construction — no API keys required.

## Context: $ARGUMENTS

## Input Contract

- Input: a search query, topic, technology name, or specific GitHub repo pattern.
- Common callers: `/oss-audit` (find reference repos), `/oss-refactor` (find patterns), `/oss-ci` (find CI examples).
- Default: search GitHub repositories relevant to the current project's stack.

## Output Contract

Return a short annotated list of findings relevant to the caller's need:

- For repo search: repo name, star count if visible, brief description, and why it is relevant.
- For code/CI pattern search: the pattern or snippet, source URL, and how to apply it.
- For best practices: concise summary with source URL.

Do not return raw HTML or a wall of links. Summarize what is useful.

## Search Recipes

### Find similar open-source repositories

```
web_fetch("https://www.google.com/search?q=site:github.com+{topic}+{language}")
web_fetch("https://github.com/search?q={topic}&type=repositories&sort=stars")
```

### Search GitHub for code patterns (CI, tests, configs)

```
# Find CI workflow examples for a specific stack
web_fetch("https://www.google.com/search?q=site:github.com+.github/workflows+{stack}+example")

# Find test patterns
web_fetch("https://www.google.com/search?q=site:github.com+{framework}+test+example")

# Find specific config files (pyproject.toml, Makefile, etc.)
web_fetch("https://www.google.com/search?q=site:github.com+{config-file}+{stack}")
```

### Search GitHub issues and discussions for known problems

```
web_fetch("https://www.google.com/search?q=site:github.com+issues+{error-or-topic}")
```

### Find documentation and best practices

```
# General best practices
web_fetch("https://duckduckgo.com/html/?q={topic}+best+practices+open+source")

# Stack Overflow for specific technical questions
web_fetch("https://www.google.com/search?q=site:stackoverflow.com+{question}")

# Official docs
web_fetch("https://duckduckgo.com/html/?q={tool}+documentation+site:{tool-domain}")
```

### DuckDuckGo bang shortcuts (fast, no tracking)

```
# Search GitHub directly
web_fetch("https://duckduckgo.com/html/?q=!gh+{query}")

# Search Stack Overflow
web_fetch("https://duckduckgo.com/html/?q=!so+{question}")

# Search npm
web_fetch("https://duckduckgo.com/html/?q=!npm+{package}")
```

## Workflow

### Step 1: Identify what to search for

From the calling context, determine the type of search needed:

- **Audit context**: find repos with similar stacks to compare structure, docs, and CI.
- **Refactor context**: find idiomatic patterns for the repo's language and toolchain.
- **CI context**: find minimal working CI workflow examples for the stack.
- **Docs context**: find README and CONTRIBUTING templates for similar projects.

### Step 2: Run 2–3 targeted searches

Start with the narrowest query. Broaden only if the first results are not useful.

Prefer:
- `site:github.com` for code/repo examples
- `site:stackoverflow.com` for technical how-to questions
- DuckDuckGo `!gh` bang for quick GitHub-scoped searches

### Step 3: Summarize findings

Extract the actionable parts. For each result:

- State what it demonstrates that is relevant to the current hardening task.
- Note any patterns worth copying (file path, config structure, CI step).
- Skip results that are off-topic or low quality.

## Failure Handling

- If a search URL returns no useful results, try a broader query or a different engine.
- If `web_fetch` is rate-limited or blocked, wait briefly and retry once with DuckDuckGo instead of Google.
- If no relevant examples are found after 3 attempts, state that clearly and suggest the user check manually.

## Done Criteria

- At least 2–3 relevant references are found and summarized.
- Each reference has a URL and a brief note on what it contributes to the current task.
- The output is short enough to act on without further filtering.
