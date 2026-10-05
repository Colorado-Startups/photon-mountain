#!/usr/bin/env bash
# PostToolUse router: run the doctrine gates on a file Claude just wrote.
#
# This hook ROUTES. It does not decide anything. It pulls the file path out of
# the tool call and hands it to the two gates that own the rules:
#
#   .claude/hooks/pm-check-voice.sh   the mechanical voice check
#   .claude/hooks/pm-check-facts.sh   the fact-gate reminder
#
# Keeping the rules out of here is deliberate. A hook that carries the rules
# inside itself cannot be reused by the pre-commit hook or by CI, cannot be
# tested on its own, and turns every rule change into a shell edit.
#
# This is the call site that makes the voice gate FIRE on the agent surface
# rather than WAIT for someone to run /pm-voice-check. It is wired in
# .claude/settings.json under PostToolUse, matcher "Write|Edit".
#
# It never blocks. PostToolUse runs after the write has already happened, so
# blocking would be theatre. Findings go to stderr, where Claude sees them and
# can fix the file before it reaches the pre-commit hook, which does block.
#
# Exit is always 0.

set -uo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

payload="$(cat)"

path="$(printf '%s' "$payload" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print(""); raise SystemExit
ti = data.get("tool_input") or {}
print(ti.get("file_path") or ti.get("notebook_path") or "")
' 2>/dev/null)"

# No path, nothing to check. Never treat a parse problem as a finding.
[ -n "$path" ] || exit 0
[ -r "$path" ] || exit 0

for gate in pm-check-voice.sh pm-check-facts.sh; do
  script="$HOOK_DIR/$gate"
  [ -r "$script" ] || continue
  out="$(bash "$script" "$path" 2>&1)" || true
  # This fires on every single edit, so only real findings are worth saying.
  # Drop the lint's "clean" confirmations and its per-file tallies; a hook
  # that reports success on every write is noise, and noise gets ignored.
  out="$(printf '%s\n' "$out" \
    | grep -vE ': clean$|: [0-9]+ FAIL, [0-9]+ WARN$' || true)"
  if [ -n "$out" ]; then
    printf '%s\n' "$out" >&2
  fi
done

exit 0
