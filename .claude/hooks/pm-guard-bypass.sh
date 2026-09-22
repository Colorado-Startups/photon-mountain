#!/usr/bin/env bash
# Deny the pre-commit escape hatch to Claude, while leaving it to Paul.
#
# PreToolUse hook on Bash. Reads the tool call as JSON on stdin and exits 2 to
# block, which sends the message on stderr back to Claude.
#
# The reasoning: .githooks/pre-commit blocks on an em dash and documents the
# bypass flag as the deliberate override. That override is a human judgment
# call and should stay one. An agent that can bypass the gate whenever the
# gate objects does not really have a gate. So the flag stays available in
# Paul's own terminal, where this hook does not run, and is refused here.
#
# This is a guardrail against the agent taking the easy way out of a doctrine
# check. It is not a security control.
#
# MATCHING IS DELIBERATELY NARROW. The first version of this hook scanned the
# whole command string, and immediately blocked a heredoc that merely *wrote
# documentation mentioning the flag*. A guardrail that fires on prose about
# itself is worse than none, because it trains you to disable it. So the
# matcher now strips heredoc bodies and quoted strings, splits the command on
# shell operators, and only objects when a segment is an actual git
# commit/push invocation carrying the flag as its own argument.

set -uo pipefail

payload="$(cat)"

verdict="$(printf '%s' "$payload" | python3 -c '
import json, re, shlex, sys

BYPASS = {"--no-" + "verify", "--no-" + "verify=true"}

try:
    data = json.load(sys.stdin)
except Exception:
    print("allow"); raise SystemExit

if data.get("tool_name") != "Bash":
    print("allow"); raise SystemExit

cmd = (data.get("tool_input") or {}).get("command") or ""
if not cmd:
    print("allow"); raise SystemExit

# 1. Remove heredoc bodies. Writing a file that talks about the flag is not
#    the same as passing the flag.
cmd = re.sub(r"<<-?\s*[\x27\"]?(\w+)[\x27\"]?.*?^\s*\1\s*$", " ", cmd,
             flags=re.S | re.M)
# A heredoc whose terminator never appears (truncated input) removes the rest.
cmd = re.sub(r"<<-?\s*[\x27\"]?\w+[\x27\"]?.*", " ", cmd, flags=re.S)

# 2. Split on shell separators so each segment is one command.
segments = re.split(r"(?:\|\||&&|[;\n|])", cmd)

for seg in segments:
    seg = seg.strip()
    if not seg:
        continue
    try:
        tokens = shlex.split(seg)
    except ValueError:
        tokens = seg.split()
    if not tokens:
        continue

    # Step past a leading `cd somewhere` or env assignments.
    while tokens and ("=" in tokens[0] and not tokens[0].startswith("-")):
        tokens = tokens[1:]
    if not tokens or tokens[0] != "git":
        continue
    # git [-C path] [--global ...] <subcommand>
    sub = next((t for t in tokens[1:] if not t.startswith("-")), None)
    if sub not in ("commit", "push"):
        continue
    if any(t in BYPASS for t in tokens):
        print("block"); raise SystemExit

print("allow")
' 2>/dev/null)"

# Fail open on a parse problem. Blocking every Bash call because this hook
# could not read its own input would be much worse than missing one bypass.
if [ "${verdict:-allow}" != "block" ]; then
  exit 0
fi

cat >&2 <<'MSG'
Blocked: the pre-commit bypass flag is not available to Claude here.

.githooks/pre-commit blocks on an em dash, which is the one voice rule that
can be enforced mechanically without false positives. Overriding it is a human
judgment call, so that flag is reserved for Paul's own terminal.

Fix the finding instead: replace the em dash with a comma, a semicolon, a
period, or parentheses. If you believe the gate is genuinely wrong, say so and
let Paul make the call.
MSG
exit 2
