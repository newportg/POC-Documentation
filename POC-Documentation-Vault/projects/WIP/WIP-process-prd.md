# Work In Progress (WIP) Process — PRD

Status: draft for review. Owner: TBD. Date: 2026-11-02.

## Summary

The Work In Progress (WIP) process governs work after it is accepted and before it is
finished. It makes each active item visible, gives it a clear owner and outcome, and
helps work move through a small set of explicit states instead of accumulating unseen
in queues or being treated as complete before it is ready.

WIP means work that has started but has not met its agreed completion criteria. The
process is intended to make work flow and blockers visible; it does not prescribe a
specific project-management tool, delivery method, or team cadence.

## Problem

When work is started without clear ownership, priority, or completion criteria, teams
can take on more than they can finish. Partially completed tasks become difficult to
track, blocked work can remain unnoticed, and stakeholders may mistake activity for
progress.

## Goals

- Make accepted and active work visible in one agreed place.
- Give each active item a named owner, clear outcome, and current status.
- Limit starting new work when existing work is blocked or unfinished.
- Make blockers, dependencies, and decisions visible so they can be addressed.
- Define how work is reviewed and what qualifies as complete.
- Use flow information to improve the process rather than judge individuals.

## Non-goals

- Mandating a particular tool, framework, meeting schedule, or estimation method.
- Defining organization-wide priorities, staffing, or service-level commitments.
- Treating the number of tasks completed as a measure of individual performance.
- Setting numerical WIP limits before the team and its capacity are understood.

## Users and responsibilities

| Role | Responsibility |
|---|---|
| Requester | Describes the requested outcome and provides necessary context. |
| Team or work coordinator | Reviews incoming work, clarifies priority, and helps resolve capacity conflicts. |
| Owner | Moves an accepted item forward, updates its status, and raises blockers. |
| Reviewer or approver | Checks the result against the agreed completion criteria when review is required. |

One person may perform more than one role. Every active item must have one clearly
identified owner, even when several people contribute.

## Process

```text
Requested → Ready → In Progress → Review → Done
                           ↘ Blocked ↗
```

1. **Request** — Record the outcome needed, requester, context, and any known deadline
   or dependency.
2. **Triage** — Decide whether to accept, defer, reject, or request clarification. Make
   priority and capacity trade-offs visible.
3. **Ready** — Confirm the item is understood well enough to start: an owner is
   available, the expected outcome is clear, and required inputs are known.
4. **In Progress** — The owner begins the work and keeps its status current. Before
   starting another item, the team checks its active WIP and agreed limits.
5. **Blocked** — Record what is preventing progress, who can help, and the next action.
   The owner or coordinator follows up; blocked work remains visible and is not counted
   as complete.
6. **Review** — Where review is needed, a reviewer checks the result against the
   completion criteria and either accepts it or returns it with specific follow-up work.
7. **Done** — Close the item only when its agreed outcome and completion criteria are
   met. Record the result and notify relevant stakeholders.

## Work item requirements

An accepted item should identify:

- The outcome or problem to address.
- The requester and one accountable owner.
- Its priority or relative order, as agreed by the team.
- Completion criteria that make “done” observable.
- Known dependencies, risks, and required review.

If an item is too large to complete or review as one unit, split it into smaller
outcomes that can each be tracked and completed independently.

## WIP policy

WIP is the set of items that have started and are not yet done. The team should agree
how it counts active work, including work in review and blocked work, before applying
a limit.

When an agreed WIP limit is reached, the default response is to help finish, review, or
unblock existing work before pulling in more. Exceptions should be explicit, with a
reason and an owner for revisiting the decision. Numerical limits are intentionally
left open until the team, work type, and capacity are known.

## Success measures

Establish a baseline before setting numerical targets:

| Measure | What it indicates | Target |
|---|---|---|
| Active items with an owner and completion criteria | Whether WIP is sufficiently defined | Agree after baseline |
| Age of unfinished and blocked items | Where work is waiting or stalled | Agree after baseline |
| Cycle time from start to done | How long started work takes to complete | Agree after baseline |
| Work completed compared with work started | Whether the team is finishing at a sustainable rate | Improve from baseline |
| Items reopened after being marked done | Whether completion criteria and review are effective | Agree after baseline |

Use these measures to identify system bottlenecks and improve flow, not to rank
individuals.

## Acceptance criteria

The process is ready to adopt when:

- The team agrees on its workflow states and what entry and exit mean for each.
- A work item template captures the minimum information defined above.
- The team agrees how to identify active WIP and how to handle a reached limit.
- Blocked work has a visible reason, next action, and responsible person.
- “Done” is based on agreed criteria rather than effort spent or status age.
- Baselines and owners for reviewing flow measures are agreed.

## Assumptions and open questions

- WIP means **Work In Progress** in this document.
- This is a general workflow proposal; the team, work type, existing tool, and current
  process have not been specified.
- Which work types should use this process, and what work is exempt?
- Who makes final priority and acceptance decisions?
- Should review be required for every item or only specified work types?
- How should urgent work enter without silently displacing committed work?
- What WIP counting rules and limits fit the team's actual capacity?
- What baseline period and targets should be used for the success measures?