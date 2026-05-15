# Collaborative Verification Protocol

Repo Church verification is designed to be stricter and more collaborative than a simple "tests passed" check.

## Verification Layers

| Layer | Owner | Evidence |
| --- | --- | --- |
| Objective checks | Agent | tests, lint, builds, screenshots, logs, API calls, migrations, observability |
| Requirement checks | Agent | requirement trace matrix and acceptance criteria |
| Workflow checks | Agent plus user when subjective | UAT script results and user journey notes |
| Doctrine checks | Agent plus user for strategic/brand/design changes | Bible alignment audit |
| Ship checks | Agent | ship gate record with rollback |

## UAT Matrix

```markdown
| Story/Requirement | Steps | Expected | Actual | Result | Evidence | Owner | Signoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

## Mutual Approval

Use mutual approval when the agent can verify mechanics but the user must verify product judgment.

Required record:

```markdown
Agent signoff:
User signoff:
Evidence:
Open risks:
Progression decision:
```

## Failures

A failed UAT row must become a gap-closure item unless it is explicitly out of scope. Each failure needs:

- reproduction steps,
- severity,
- owner,
- expected fix or deferral rationale,
- recheck command or manual validation path.
