#!/usr/bin/env bash
# Photon Mountain voice gate, in one place.
#
# This script is the single definition of the mechanical voice check. It has
# three callers, and they must all get the same answer:
#
#   1. The Claude Code harness, via .claude/settings.json (PreToolUse).
#   2. .githooks/pre-commit, on staged files.
#   3. .github/workflows/voice-check.yml, on files changed in a pull request.
#
# CI deliberately shells out to this script instead of reimplementing the
# check in YAML, so the gate cannot drift between a laptop, a web edit, and a
# cloud agent.
#
# Usage:   bash pm-check-voice.sh FILE [FILE ...]
#
# Exit codes:
#   0  nothing to say, or only warnings
#   1  at least one FAIL finding (an em dash, or an unattributed figure)
#   2  could not run the check at all
#
# The caller decides what a non-zero exit means. The pre-commit hook blocks on
# an em dash but only warns on an unattributed figure, because the figure rule
# is a heuristic by voice_lint.py's own description. See .githooks/pre-commit.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LINT="$REPO_ROOT/04_tools/voice_lint.py"

# Content types the voice lint understands. Everything else is skipped, so a
# caller can hand this script an unfiltered changed-file list.
#
# Lowercasing uses tr, not ${var,,}: this has to run under the bash 3.2 that
# ships with macOS, where the parameter-expansion form is a syntax error.
is_prose() {
  case "$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')" in
    *.md|*.mdx|*.txt) return 0 ;;
    *) return 1 ;;
  esac
}

# Files that quote banned constructions on purpose. The voice doctrine itself
# has to be able to show an em dash in order to forbid one.
is_exempt() {
  case "$1" in
    01_doctrine/voice.md|\
    01_doctrine/why_and_how_guide.md|\
    .claude/skills/*|\
    LICENSE|LICENSES/*) return 0 ;;
    *) return 1 ;;
  esac
}

if [ "$#" -eq 0 ]; then
  exit 0
fi

# Fail open on an infrastructure problem. "Could not verify" is not the same
# as "verified and red", and a missing interpreter should never look like a
# doctrine violation.
if ! command -v python3 >/dev/null 2>&1; then
  echo "pm-check-voice: python3 not found; skipping the voice check." >&2
  exit 0
fi
if [ ! -r "$LINT" ]; then
  echo "pm-check-voice: $LINT not found or unreadable; skipping." >&2
  exit 0
fi

targets=()
for f in "$@"; do
  rel="${f#"$REPO_ROOT"/}"
  if is_prose "$f" && ! is_exempt "$rel" && [ -r "$f" ]; then
    targets+=("$f")
  fi
done

if [ "${#targets[@]}" -eq 0 ]; then
  exit 0
fi

output="$(python3 "$LINT" "${targets[@]}" 2>&1)"
status=$?

if [ "$status" -eq 2 ]; then
  echo "pm-check-voice: voice_lint.py could not read a file; skipping." >&2
  echo "$output" >&2
  exit 0
fi

# Always show findings. The caller decides whether they block.
if [ -n "$output" ]; then
  echo "$output"
fi

exit "$status"
