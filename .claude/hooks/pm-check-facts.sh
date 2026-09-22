#!/usr/bin/env bash
# Photon Mountain fact-gate reminder.
#
# This is a prompt, not a check. The real fact gate is the pm-fact-guardrails
# skill, which searches before it asserts, and no script can do that. What
# this hook does is notice when an edit touches a file that carries
# current-status claims, and say so, so the gate does not get skipped by
# forgetting rather than by decision.
#
# It never blocks. It writes to stderr and exits 0, always.
#
# Usage:  bash pm-check-facts.sh FILE [FILE ...]

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

[ "$#" -eq 0 ] && exit 0

# Paths whose contents make dated claims about the corridor.
carries_claims() {
  case "$1" in
    02_substance/*) return 0 ;;
    03_deliverables/maps/MAP_NOTES.md) return 0 ;;
    03_deliverables/maps/*.geojson|03_deliverables/maps/*.kml) return 0 ;;
    01_doctrine/brand_identity.md) return 0 ;;
    *) return 1 ;;
  esac
}

flagged=()
for f in "$@"; do
  rel="${f#"$REPO_ROOT"/}"
  if carries_claims "$rel"; then
    flagged+=("$rel")
  fi
done

[ "${#flagged[@]}" -eq 0 ] && exit 0

{
  echo
  echo "pm-check-facts: these files carry current-status claims:"
  for f in "${flagged[@]}"; do
    echo "    $f"
  done
  echo
  echo "Before this ships anywhere external, run pm-fact-guardrails on it and"
  echo "re-search every status claim. The three clocks have to stay apart:"
  echo "what operates today, what opens in 2026, and what is on the horizon."
  echo "NLR is \"formerly NREL\" on first reference. Association figures are"
  echo "the association's figures."
  echo
} >&2

exit 0
