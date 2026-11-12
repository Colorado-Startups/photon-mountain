# Security

## What is here

This repository holds written doctrine, corridor research, and a few Python scripts that render an infographic and maps. There is no server, no database, no authentication, and no deployed service. It processes no personal data and holds no credentials.

That keeps the real attack surface small. The two things worth attention are supply chain and accidental disclosure.

## Reporting something

**Use GitHub's private reporting first:** [report a vulnerability](https://github.com/Colorado-Startups/photon-mountain/security/advisories/new). Only you and the maintainers see the report.

Or email **paul@coloradostartups.org**. Either way, please do not open a public issue for a suspected credential leak.

If you found a secret committed to this repository, say so directly and do not include the value in your message. It will be treated as compromised and rotated regardless of whether it turns out to have been live.

There is no bounty. This is a small civic project. A first reply within seven days is our goal.

## What is in place

- **Two secret scanners.** GitHub's secret scanning and push protection run on the repository, and push protection blocks a recognized credential before it lands. `gitleaks` also runs over every commit on each pull request, on each push to `main`, and weekly, from `.github/workflows/secret-scan.yml`. It uses the gitleaks binary, pinned by version and SHA-256, because the Action wrapper requires a license key for organization-owned repositories. The pre-commit hook scans staged changes too when gitleaks is installed locally.
- **Required checks on `main`.** `main` takes changes only through a pull request, never a direct or force push. A pull request merges only when `voice-check`, `secret scan` and `DCO` pass.
- **Pinned actions.** Every GitHub Action is pinned to a full commit SHA, and the repository's Actions settings require it, so a retagged upstream release cannot change what runs. Dependabot keeps the pins current.
- **Least-privilege workflows.** Every workflow declares `permissions: contents: read`. None needs write access, and the repository holds no Actions secrets.
- **Outside pull requests wait.** Workflows on a pull request from a fork run only after a maintainer approves them, and a fork's workflows never receive secrets.
- **Dependabot alerts and security updates** are on.
- **No third-party dependencies in the gates.** `voice_lint.py`, `brand_tokens.py`, and `marker_parity.py` are standard library only. Only the deliverable build scripts pull in matplotlib and reportlab, pinned in `requirements.txt`.
- **`local/` is gitignored** and is where anything operational or private belongs.

## Known gaps, stated plainly

- **No required human approval.** Maintainer pull requests come from the same account that merges them, and GitHub does not let an author approve their own pull request. The required checks and the maintainer's review are the gate. Outside contributors cannot merge.
- **CI runs the pull request's own copy of the gates.** A pull request could weaken a gate script and then pass it. Any pull request that touches `.github/`, `.claude/`, `.githooks/` or `04_tools/` is reviewed for exactly that before it merges.
- **Client-side hooks are bypassable by design.** `--no-verify` exists and is documented. The required checks on the pull request are the server-side answer.

## A note on the brand

Nothing about the brand is reserved, so anyone may use the name and the Summit Sun mark. A false claim made under the name is a fact matter, not a security vulnerability. Report it as a fact correction, or to the same address.
