---
title: Design Doctrine
generated: 2026-05-15
status: design reference
---

# Design Doctrine

## Product Experience Promise

Repo Church should feel like a disciplined operator console for agentic work: dense, explicit, evidence-first, and portable. The experience is not decorative; its quality comes from making the next correct action hard to miss and making unsupported progress hard to record.

## Design Non-Negotiables

| ID | Doctrine | Practical rule | Evidence |
|---|---|---|---|
| DD-01 | Dense but scannable | Commands and reports use tables for evidence, owners, blockers, and rechecks. | `commands/*.md`, `gate-taxonomy.md` |
| DD-02 | No invisible pass | Every PASS has visible evidence and lifecycle state. | `church.py`, `.church/state.json` |
| DD-03 | Portable language | Avoid agent-vendor-only assumptions unless a profile declares compatibility. | `AGENTS.md`, `.claude-plugin/plugin.json` |
| DD-04 | Human review surfaces | Render Bible/validation HTML when useful; keep markdown canonical. | `repo_bible.py render-html` |
| DD-05 | Progressive disclosure | Keep SKILL entrypoints concise and push detail to references, commands, agents, and CLI reports. | `skills/church/SKILL.md`, `skills/repo-bible/SKILL.md` |

## Core Surfaces

| Surface | User job | Must not do |
|---|---|---|
| `SKILL.md` | Route intent and load minimal context. | Become a monolithic procedure dump. |
| `commands/*.md` | Provide staged operator workflow and output shape. | Omit evidence/recheck/signoff fields. |
| `agents/*.md` | Provide specialist contracts. | Return unverifiable summaries. |
| `.church/bible/*.md` | Govern requirements, roadmap, moat, and validation. | Leave placeholders in controlling artifacts. |
| CLI reports | Offload inventory, sources, validation, context, and ledgers. | Pretend mechanical output is strategy judgment. |
