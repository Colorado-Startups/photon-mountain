# Security

## What is here

This repository holds written doctrine, corridor research, and three Python scripts that render an infographic and two maps. There is no server, no database, no authentication, and no deployed service. It processes no personal data and holds no credentials.

That keeps the real attack surface small. The two things worth attention are supply chain and accidental disclosure.

## Reporting something

Email **paul@coloradostartups.org**. Please do not open a public issue for a suspected credential leak.

If you found a secret committed to this repository, say so directly and do not include the value in your message. It will be treated as compromised and rotated regardless of whether it turns out to have been live.

There is no bounty. This is a small civic project.

## What is in place

- **Secret scanning.** `gitleaks` runs on every pull request and weekly, from `.github/workflows/secret-scan.yml`. It uses the gitleaks binary rather than the Action wrapper, because that wrapper requires a license key for organization-owned repositories. The pre-commit hook also scans staged changes when gitleaks is installed locally, as an earlier warning.
- **Pinned actions.** Every GitHub Action is pinned to a full commit SHA, not a tag, so a retagged upstream release cannot change what runs. Dependabot keeps the pins current, which is the reason that config exists.
- **Least-privilege workflows.** Every workflow declares `permissions: contents: read`. None needs write access.
- **No third-party dependencies in the gates.** `voice_lint.py`, `brand_tokens.py`, and `marker_parity.py` are standard library only. Only the two deliverable build scripts pull in matplotlib and reportlab, pinned in `requirements.txt`.
- **`local/` is gitignored** and is where anything operational or private belongs.

## Known gaps, stated plainly

- **Branch protection is not available.** GitHub offers rulesets and required status checks on private repositories only at paid tiers. This repository is private on a Free organization, so CI reports but cannot block, and `CODEOWNERS` is advisory. The local pre-commit hook is the only enforcing gate today. This is a deliberate, recorded tradeoff, and it resolves when the repo goes public at PT-9, which turns all of it on for free.
- **GitHub secret scanning and push protection are off.** They are free on public repositories, not on private ones at this tier. They turn on at PT-9 as well. Until then the gitleaks workflow is the only scanner.
- **Client-side hooks are bypassable by design.** `--no-verify` exists and is documented. That is correct for a client-side hook; the answer is a server-side gate, which arrives at PT-9.

## A note on the brand

`TRADEMARKS.md` covers brand misuse, which is a different problem from a security vulnerability. Someone passing off material as Photon Mountain's, or attaching the mark to claims the corridor has not verified, is a trademark and honesty matter. Report it to the same address.
