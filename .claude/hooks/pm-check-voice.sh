#!/usr/bin/env bash
# Photon Mountain voice gate, in one place.
#
# This script is the single definition of the mechanical voice check. Its call
# sites, as actually wired:
#
#   1. The Claude Code harness, on every Write or Edit, via the PostToolUse
#      entry in .claude/settings.json, which routes through pm-on-edit.sh.
#      FIRES automatically.
#   2. .githooks/pre-commit, on staged files. FIRES on every commit, once the
#      clone has run `git config core.hooksPath .githooks`.
#   3. .github/workflows/voice-check.yml, on files changed in a pull request.
#      FIRES on every pull request.
#
#   The /pm-voice-check slash command also calls it, but that one WAITS for
#   someone to invoke it. It is not a gate; it is a convenience.
#
# If you change the wiring, change this comment in the same edit. A header that
# claims a call site the settings file does not wire is a defect, not a
# documentation lag: it tells the next reader a check is firing when it is not.
# Check .claude/settings.json, not this comment.
#
# CI deliberately shells out to this script instead of reimplementing the check
# in YAML, so the gate cannot drift between a laptop, a web edit, and a cloud
# agent. That has been verified: a CI run and the local pre-commit hook
# produced byte-identical findings on the same files and line numbers.
#
# Usage:
#   bash pm-check-voice.sh FILE [FILE ...]
#   bash pm-check-voice.sh --self-test
#
# Exit codes:
#   0  no FAIL finding: clean, warnings only, or the check could not run.
#      Could-not-run fails open and says so on stderr.
#   1  at least one FAIL finding, as graded by voice_lint.py
#
# This script grades nothing. voice_lint.py decides every grade, and the
# "Built-in checks" table in its docstring lists them; its --self-test holds
# that table to the code. As of 2026-10-08 the FAIL checks are em-dash and
# spaced-en-dash. unattributed-figure, ai-tell, hedge-word and sentence-length
# warn. voice_lint.py is vendored from Git Crafter (its first lines name the
# source and commit), so a regrade happens there and needs no edit here.
#
# Exit 1 is normalized. A crash inside voice_lint.py also exits 1, but prints
# no FAIL finding, so it would otherwise look like a doctrine violation. This
# script returns 1 only when the lint exited 1 and printed a FAIL finding, so
# every caller can route on the exit code without parsing the output.
#
# The caller decides what exit 1 means. The pre-commit hook blocks on it and
# shows warnings as advisory. CI notes it in the job summary. See
# .githooks/pre-commit and .github/workflows/voice-check.yml. The pre-commit
# hook's own --self-test holds that routing to account through real commits,
# so a change to the exit codes here fails that test, not just this one.

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LINT="$REPO_ROOT/04_tools/voice_lint.py"
EXEMPT_FILE="$REPO_ROOT/04_tools/voice_exempt.txt"

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

# Exemptions live in 04_tools/voice_exempt.txt, as data. The patterns are shell
# globs relative to the repo root. A missing file means nothing is exempt,
# which fails safe: the gate over-checks rather than under-checks.
read_exempt_patterns() {
  [ -r "$EXEMPT_FILE" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|'#'*) continue ;;
    esac
    printf '%s\n' "$line"
  done < "$EXEMPT_FILE"
}

is_exempt() {
  local rel="$1" pattern
  while IFS= read -r pattern; do
    [ -z "$pattern" ] && continue
    # shellcheck disable=SC2254
    case "$rel" in
      $pattern) return 0 ;;
    esac
  done <<EOF
$(read_exempt_patterns)
EOF
  return 1
}

run_check() {
  if [ "$#" -eq 0 ]; then
    return 0
  fi

  # Fail open on an infrastructure problem. "Could not verify" is not the same
  # as "verified and red", and a missing interpreter should never look like a
  # doctrine violation.
  if ! command -v python3 >/dev/null 2>&1; then
    echo "pm-check-voice: python3 not found; skipping the voice check." >&2
    return 0
  fi
  if [ ! -r "$LINT" ]; then
    echo "pm-check-voice: $LINT not found or unreadable; skipping." >&2
    return 0
  fi

  local targets=() f rel
  for f in "$@"; do
    rel="${f#"$REPO_ROOT"/}"
    if is_prose "$f" && ! is_exempt "$rel" && [ -r "$f" ]; then
      targets+=("$f")
    fi
  done

  if [ "${#targets[@]}" -eq 0 ]; then
    return 0
  fi

  local output status
  output="$(python3 "$LINT" "${targets[@]}" 2>&1)"
  status=$?

  if [ "$status" -eq 2 ]; then
    echo "pm-check-voice: voice_lint.py could not read a file; skipping." >&2
    echo "$output" >&2
    return 0
  fi

  # Always show findings. The caller decides whether they block.
  if [ -n "$output" ]; then
    echo "$output"
  fi

  if [ "$status" -eq 0 ]; then
    return 0
  fi
  if [ "$status" -eq 1 ] && printf '%s\n' "$output" | grep -qE ':[0-9]+: FAIL \['; then
    return 1
  fi
  # Non-zero with no FAIL finding is a crash, not a verdict. Fail open, loudly.
  echo "pm-check-voice: voice_lint.py exited $status without a FAIL finding;" \
       "could not verify, skipping." >&2
  return 0
}

# --------------------------------------------------------------- self-test --
# Seeds a known-bad sample and a known-clean sample, and fails if either
# behaves wrong. Also asserts the exempt list has not rotted.
self_test() {
  local ok=0 tmp
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN

  printf '# Bad\n\nA line with an em dash %s here.\n' "$(printf '\xe2\x80\x94')" > "$tmp/bad.md"
  printf '# Clean\n\nThis line is plain and direct.\n' > "$tmp/clean.md"
  printf '# Warn\n\nThis line is arguably fine.\n' > "$tmp/warn.md"
  printf '# Crash\n\nNot UTF-8: \xff\xfe\n' > "$tmp/crash.md"
  printf 'not prose\n' > "$tmp/thing.py"

  run_check "$tmp/bad.md" >/dev/null 2>&1
  if [ "$?" -eq 1 ]; then
    echo "self-test: known-bad sample flagged: OK"
  else
    ok=1; echo "self-test: known-bad sample NOT flagged: FAIL"
  fi

  run_check "$tmp/clean.md" >/dev/null 2>&1
  if [ "$?" -eq 0 ]; then
    echo "self-test: known-clean sample passes: OK"
  else
    ok=1; echo "self-test: known-clean sample raised a finding: FAIL"
  fi

  # A warning is advisory. It must print and still exit 0.
  local warn_out
  warn_out="$(run_check "$tmp/warn.md" 2>/dev/null)"
  if [ "$?" -eq 0 ] && printf '%s\n' "$warn_out" | grep -qE ':[0-9]+: WARN \['; then
    echo "self-test: warning-only sample prints and exits 0: OK"
  else
    ok=1; echo "self-test: warning-only sample did not print and exit 0: FAIL"
  fi

  # A crash in the lint exits 1 with no FAIL finding. That is could-not-verify,
  # so it must fail open rather than read as a doctrine violation.
  run_check "$tmp/crash.md" >/dev/null 2>&1
  if [ "$?" -eq 0 ]; then
    echo "self-test: a lint crash fails open: OK"
  else
    ok=1; echo "self-test: a lint crash blocked like a FAIL: FAIL"
  fi

  run_check "$tmp/thing.py" >/dev/null 2>&1
  if [ "$?" -eq 0 ]; then
    echo "self-test: non-prose skipped: OK"
  else
    ok=1; echo "self-test: non-prose was not skipped: FAIL"
  fi

  run_check >/dev/null 2>&1
  if [ "$?" -eq 0 ]; then
    echo "self-test: no arguments is a no-op: OK"
  else
    ok=1; echo "self-test: no arguments did not exit 0: FAIL"
  fi

  # --- exempt list contract -------------------------------------------------
  # Every pattern must still match at least one real file. A pattern that
  # matches nothing is a renamed path, and a dead exemption that still reads
  # like policy is exactly how an exempt list rots.
  local pattern dead=0 count=0
  while IFS= read -r pattern; do
    [ -z "$pattern" ] && continue
    count=$((count + 1))
    # shellcheck disable=SC2086
    if ! compgen -G "$REPO_ROOT/$pattern" >/dev/null 2>&1; then
      ok=1; dead=$((dead + 1))
      echo "self-test: exempt pattern matches nothing: $pattern: FAIL"
    fi
  done <<EOF
$(read_exempt_patterns)
EOF
  if [ "$dead" -eq 0 ] && [ "$count" -gt 0 ]; then
    echo "self-test: all $count exempt patterns still match a real file: OK"
  elif [ "$count" -eq 0 ]; then
    echo "self-test: no exempt patterns loaded from $EXEMPT_FILE: FAIL"; ok=1
  fi

  # An exempt file must actually be skipped, and a non-exempt one checked.
  if is_exempt "01_doctrine/voice.md" && ! is_exempt "02_substance/README.md"; then
    echo "self-test: exemption applies to the listed path and not others: OK"
  else
    ok=1; echo "self-test: exemption matching is wrong: FAIL"
  fi

  if [ "$ok" -eq 0 ]; then
    echo "self-test: PASS"
  else
    echo "self-test: FAIL"
  fi
  return "$ok"
}

if [ "${1:-}" = "--self-test" ]; then
  self_test
  exit $?
fi

run_check "$@"
exit $?
