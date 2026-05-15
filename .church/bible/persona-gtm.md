---
title: Persona and Go-To-Market Plan
generated: 2026-05-15
status: persona and GTM reference
---

# Persona and Go-To-Market Plan

## Target Persona

| Persona | Pain | Desired outcome | Proof needed |
|---|---|---|---|
| Agent-heavy repo owner | Plans drift, agents lose context, review gates are inconsistent. | Durable, repo-local lifecycle evidence that future agents can resume. | Full self-lifecycle test and validation artifacts. |
| Skill/package author | Skills become long prompts and are hard to validate. | Portable package with concise entrypoints, references, commands, and tests. | Package validator and install smoke check. |
| Technical founder/operator | Strategy and implementation diverge during fast agentic work. | Bible-backed roadmap, moat, requirements, and ship gates. | Meta-Bible and requirement-traced lifecycle records. |

## Product-Market Fit Hypothesis

Repo Church is useful when a team values repeatable agentic execution more than raw one-shot generation speed. The PMF signal is not broad signups in this meta run; it is local proof that the framework can govern itself without collapsing into narrative-only planning.

## Acquisition Plays

| Play | Audience | Asset | Gate |
|---|---|---|---|
| Public self-hosting proof | Agent framework builders | `.church/` meta-Bible and lifecycle test | SR-01 and SR-05 pass |
| Package install trust | skills.sh-compatible users | `npx skills add ./ --list` output | 12 intended skills listed |
| Review-readiness story | repo owners | PR with validation report and ship gate | CodeRabbit/CI plus local checks |

## GTM Timeline

| Phase | Action | Success signal |
|---|---|---|
| P01 | Prove self-lifecycle and meta-Bible locally. | Full lifecycle test and validation report pass. |
| P02 | Turn validation output into README/docs examples. | New user can run first workflow without guessing. |
| P03 | Compare against adjacent agent workflow packages with current sources. | Market claims move from hypothesis to current-source-backed. |
