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

# Only replace this pack's own skill directories — never touch unrelated entries
for skill_dir in "$CLONE_DIR"/skills/oss-*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  target_dir="$SKILLS_DIR/$skill_name"
  rm -rf "$target_dir"
  cp -R "$skill_dir" "$target_dir"
done

installed_count="$(find "$CLONE_DIR/skills" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"

echo "Installed $installed_count skills to $SKILLS_DIR"
echo "Restart Claude Code or run /reload if the skills do not appear immediately."
