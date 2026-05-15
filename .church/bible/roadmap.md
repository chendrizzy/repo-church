---
title: Optimized Roadmap
generated: 2026-05-15
status: roadmap reference
---

# Optimized Roadmap

| Phase | Objective | Requirement IDs | Existing components | New components | Required specs/ADRs | Exit gate |
|---|---|---|---|---|---|---|
| P01 | Prove Repo Church can self-host its full lifecycle. | SR-01, SR-02, SR-03, SR-04, SR-05 | CLI, tests, commands, agents, Bible templates | Meta-Bible, lifecycle artifacts, E2E test | `.church/specs/meta-lifecycle-spec.md` | Full lifecycle reaches `refresh/PASS`; validation suite passes. |
| P02 | Convert self-hosting proof into public onboarding examples. | SR-04, SR-05 | README, docs | First-run walkthrough and troubleshooting | Future docs spec | User can reproduce first workflow without hidden assumptions. |
| P03 | Refresh market claims with current competitor research. | SR-03 | Market watchlist | Current-source competitor matrix | Future research spec | Claims upgraded from hypothesis to current-source-backed. |

## Phase Details

### P01: Self-Hosted Lifecycle Proof

- Goal: make Repo Church govern itself through the entire intended process with evidence, not narrative.
- Tasks:
  - Fill the meta-Bible with requirement IDs and local evidence.
  - Import a completed moat and render it.
  - Record each lifecycle gate with evidence artifacts.
  - Add a regression test that performs the full lifecycle on a temp repo.
  - Validate package, tests, install surface, and Bible packet.
- Flags:
  - AI/eval: no model behavior changed; framework output quality is tested through command contracts.
  - Security: no secrets/auth/data migrations.
  - Design: docs/UX command surfaces affected.
  - GTM: market claims remain category-level unless current sources are added.
- Dependencies: prior quality-gate hardening commit, meta-Bible scaffold, CLI validation.
- Exit criteria: `.church/state.json` active workflow is `refresh/PASS`, UAT ledger passes, ship gate passes, and PR validation is green or pending external review only.

### P02: Public Onboarding

- Goal: make the self-hosting flow repeatable for a new repo owner.
- Exit criteria: README/docs include a minimal first-run path and failure-mode explanations.

### P03: Market Refresh

- Goal: replace category-level hypotheses with current competitor and platform evidence.
- Exit criteria: market watchlist cites current primary or direct observation sources.
