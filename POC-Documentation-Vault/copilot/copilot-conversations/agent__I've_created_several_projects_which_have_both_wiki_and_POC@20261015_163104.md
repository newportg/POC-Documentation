---
epoch: 1792078264541
mode: agent
backendId: opencode
sessionId: "ses_ebfd15aa3ffex34avJR8tl1fr5"
agentLabel: "Modern app project structure"
usage: '{"usedTokens":52726,"contextWindow":200000,"updatedAt":1792084114733}'
tags:
  - copilot-conversation
---

**user**: I've created several projects which have both wiki and POC applications but they appear dissorganised, can you describe how a modern application project is organised
[Timestamp: 2026/10/15 16:31:04]

**ai**: I looked at your other project folders under `C:\Source\Obsidian\Projects\` to ground this. Here's what I found, then how a modern app project is typically organised.

## Why it feels disorganised

- **One vault per project, each with duplicated boilerplate.** POC-Thirdfort, POC-Enterprise, POC-NorthstarData, POC-poc each carry their own copy of `AGENTS.md`, `CLAUDE.md`, `prompts/translate.md`, and the entire `copilot/skills/` tree (dozens of identical files per vault). Nothing is shared; conventions drift.
- **Mixed concerns inside a vault.** POC-Thirdfort has app code (`POC/lib/cdd-api-client.js`, tests, HTML wizards) sitting alongside wiki notes in the same Obsidian vault. Code and knowledge have different lifecycles, tools, and audiences — mixing them is what makes it feel messy.
- **Flat wiki folders that don't scale.** POC-Enterprise has 47+ wiki files in one directory: SODs, vendor POCs, Entra ID configs, architecture notes all side by side. No taxonomy.
- **Inconsistent shape per project.** POC-Thirdfort has `wiki/ + POC/`, POC-NorthstarData has only `wiki/`, POC-poc is an empty template. No two projects look alike, so there's no muscle memory.
- **The template you started (POC-poc) is the right idea but unpopulated.** Its README describes `/projects/<name>/` with one folder per project — that's the consolidation target you never rolled out.

## How a modern application project is organised

The modern default separates **two things you currently interleave: the application (code) and the knowledge (notes)**. They relate but don't co-live in the same folder tree.

### Layer 1 — One knowledge vault (not one per project)

```text
vault/
├── README.md              # what this system is, how to use it
├── AGENTS.md              # single copy, shared rules
├── raw/                   # inbox — anything captured
├── archive/               # processed raw, permanent record
├── prompts/               # translate.md etc.
└── projects/
    ├── thirdfort/
    │   ├── README.md      # project digest: status, links, decisions
    │   ├── api-notes.md
    │   ├── domain-model.md
    │   └── decisions.md   # ADR-lite: what we chose and why
    ├── enterprise/        # or per-client subfolders
    │   └── ...
    └── northstar-data/
        └── ...
```

Principles:
- **One folder per project, nested subfolders by topic once a project exceeds ~10 notes.** Flat folders of 47 files are the main source of the feeling of disorder.
- **Boilerplate lives once at the root.** AGENTS.md, skills, prompts — shared, not copied.
- **A project README is the index** — status, links to the live repo, key decisions, last-updated. This is what you read first when returning to a project after three weeks.

### Layer 2 — The application repo (one per POC/app)

Whether it's a throwaway POC or production, the modern shape is the same — POCs just have thinner content:

```text
repo/
├── README.md              # what it is, how to run it in <5 min
├── docs/
│   ├── design.md          # architecture, data flow
│   ├── adr/               # decision records: 0001-auth-choice.md ...
│   └── runbook.md         # how to deploy/debug
├── src/                   # application code, one folder per component
├── tests/                 # or colocated next to src
├── infra/                 # IaC: bicep/terraform, one file per resource group
├── config/                # env-specific settings (dev/test/prod)
├── .github/workflows/     # CI: lint, test, deploy
└── .gitignore
```

Modern conventions that matter most:
- **README is the contract** — purpose, prerequisites, one-command run, link back to the vault's project folder. If someone can't run it in five minutes from the README, the project is unowned.
- **Docs-as-code**: design docs and ADRs live in `docs/` in the repo, versioned with the code, not in the wiki. The wiki holds the *thinking* (research, vendor notes, domain exploration); the repo holds the *decisions and build truth*. Link across with a one-line reference in each project README.
- **ADRs as lightweight files** — `docs/adr/0001-use-entra-id.md`, one file per significant decision: context, options, choice, consequence. This is the single biggest payoff for a Solution Architect; it turns tribal knowledge into searchable record.
- **infra/ separate from src/** — your POCs frequently are integration/infra heavy (Zscaler, Prisma, Entra ID, Logic Apps); keeping IaC reviewable separately makes the POC demonstrable and repeatable.
- **One repo per deployable thing.** Don't merge unrelated POCs into a mono-repo unless they ship together. Conversely, don't split one POC into five repos.

### The seam between the two

Each side keeps exactly one pointer to the other:

- Vault project README: `Repo: https://github.com/... | Status: PoC complete 2026-09`
- Repo README: `Design notes: vault/projects/thirdfort/`

No content duplication — the vault links to the repo, the repo links back. Archive POCs by marking status in the vault README and leaving the repo read-only; never move code into the vault.

## Recommended next step for your setup

1. Keep **one** vault (the POC-poc structure is already right): `projects/<name>/` per project, shared root boilerplate, delete the per-vault skill copies as you retire each vault.
2. Move app code out of vault `POC/` folders into standalone git repos (your Thirdfort wizards and API client are already a coherent app).
3. Adopt the `docs/ + src/ + infra/` shape even for throwaway POCs — it costs nothing and means every POC is demoable the same way.

Want me to capture this as a wiki entry (e.g. `wiki/application-project-organisation.md`), or draft the consolidated `projects/` structure with a migration list of which existing vault content goes where?
[Timestamp: 2026/10/15 16:31:04]

**user**: yes capture it
[Timestamp: 2026/10/15 16:34:19]

**ai**: Captured to `wiki/application-project-organisation.md`. It contains:

- **Why it feels disorganised** — the observed issues across your POC-* vaults (duplicated boilerplate, mixed code/notes, flat wiki folders, inconsistent shapes)
- **Layer 1** — the single-vault structure with `projects/<name>/`
- **Layer 2** — the standard app repo layout (`README`, `docs/`, `src/`, `tests/`, `infra/`, `config/`)
- **The seam** — one pointer each way between vault and repo
- **Migration steps** — the three concrete moves

It follows your wiki conventions: terse, kebab-case filename, one topic, related links to [[cdd-poc-app]] as the "before" example, and it notes uncertainty explicitly.

One thing I couldn't do: the hard rule says "commit after meaningful changes", but the environment reports this folder is **not a git repo** (despite the README claiming it is), so no commit was made. If you run `git init` here (or the repo lives elsewhere), I can commit — or you can, with a message like `wiki: add application project organisation entry`.
[Timestamp: 2026/10/15 16:34:19]

**user**: how does this structure compensate for drift. where the documentation or the code doesnt represent the other
[Timestamp: 2026/10/15 16:42:41]

**ai**: Good question — and the honest answer is: **structure alone compensates for nothing**. Drift is proportional to duplicated truth, and no arrangement makes two copies of the same fact agree. What this design does is three narrower things: remove most duplication so there's little left to drift, make the remainder falsifiable rather than silently wrong, and mark what can't be verified as dated/uncertain instead of asserting it as current.

## Where drift comes from, and what meets it

**1. Code vs its own docs (inside the repo)**

This is where drift is most damaging and where the structure fights hardest:

- **docs/ versioned with the code** — a behaviour change and its doc change land in the same PR. Review becomes the drift gate: "code changed, docs didn't" is visible at the moment it happens, not months later. (Enabled by structure, but enforced by discipline — see the caveat below.)
- **The README is falsifiable.** "Runs in five minutes, one command" is a testable claim, re-tested by every fresh clone. When it stops working, drift is *proven*, not suspected. Most doc rot is undetectable precisely because nothing ever tests the doc.
- **Executable documentation** — your CDD POC already does this well: `cdd-api-client.test.js` (60 assertions) and the mock transport, which you yourself described as "executable documentation of the contract". Tests and contract simulators can't drift silently — CI goes red. Same for the OpenAPI file: contract tests verify the implementation against `internal-cdd-api-openapi.yaml` rather than trusting the yaml to describe reality.
- **ADRs are append-only.** Never edited, only superseded (`0002 supersedes 0001`). The decision record therefore cannot disagree with history — later thinking appears as new truth next to old truth, with the succession explicit, instead of quietly overwriting it.

**2. Vault vs repo (cross-layer)**

- **One source of truth per fact.** The seam is one line each way; the vault *links* to the repo rather than restating what the repo contains. There is deliberately almost no cross-layer content that could drift. This is the load-bearing rule: every time you copy a fact into the vault instead of linking, you've created a future drift site.
- **Division of staleness.** The two layers fail differently on purpose. Repo docs rot *loudly* (CI, review, broken README). Vault notes are snapshots of *thinking* — research, vendor exploration, domain analysis — and they don't claim to be build truth, so they don't "drift", they *age*, and the capture date shows it. The damage comes only from notes that masquerade as current facts, which leads to:
- **Uncertainty is logged, not guessed** — already a hard rule in your AGENTS.md. `thirdfort-api-notes` is the sharp case: Thirdfort's API behaviour is upstream and changes without telling you; *neither layer* detects that. What compensates is the note carrying capture date, source, and explicit open questions — so a stale fact reads as "true as of September, unverified since" rather than as current truth.
- **Status + last-updated on the project README** makes a stale project visible from the index, before you trust it.
- **Archive freezes both halves at once** — repo read-only, vault status is the last word. Post-archive drift is impossible by definition.

**3. What the structure does *not* compensate for**

State this plainly because it's the real risk:

- A note that was **wrong when written** — nothing detects that except someone revisiting it.
- **Upstream/vendor changes** — invisible to both layers.
- And the big one: **all of it is discipline until enforced**. The same structure with no PR review, no CI, no dated notes gives you zero drift protection. The structure's job is to make each safeguard cheap and each failure visible — it can't skip the enforcement.

The bottom line: drift ∝ duplication. Minimise duplication (link, don't copy), make claims testable (runnable README, CI, contract tests, append-only ADRs), and label the untestable as dated evidence rather than fact.

I've appended a **Drift** section capturing this to [[application-project-organisation]].Done — the **Drift** section is now in [[application-project-organisation]] between "The seam" and "Migration steps", covering:

- **Duplication is the root cause** — link, don't copy; the one-line seam is the load-bearing rule
- **Falsifiable repo docs** — same-PR doc changes, runnable README re-tested per clone, tests/contract simulators as executable documentation (referencing your `cdd-api-client.test.js` and mock transport pattern)
- **Append-only ADRs** — supersession beats editing, so decisions can't silently contradict history
- **Vault notes age rather than drift** — dated snapshots of thinking, with capture date + open questions for upstream facts like Thirdfort's API
- **The honest limits** — wrong-when-written notes, upstream changes while nobody looks, and the fact that all of it is discipline until enforced in PR review and CI
[Timestamp: 2026/10/15 16:42:41]

**user**: so where does the repo exist within the structure, is it one repo for ALL projects ? or multiple repos
[Timestamp: 2026/10/15 17:26:40]

**ai**: Multiple repos — specifically **N+1: the vault is one repo, and every deployable thing gets its own repo.** The vault repo is the knowledge layer (its README already says "the whole folder is a git repo"); application repos are separate and live *outside* the vault entirely.

## Where they live

```text
C:\Source\
├── Obsidian\
│   └── Projects\
│       └── <vault>\              ← 1 repo: notes, research, decisions
│           └── projects\
│               ├── thirdfort\    → Repo: https://github.com/…/cdd-journey-wizard
│               └── northstar\    → Repo: https://github.com/…/northstar-mapping
└── Repos\                        ← N repos: one per app/POC
    ├── cdd-journey-wizard\
    ├── northstar-mapping\
    └── …
```

The code root is a different root from the vault — nothing under `Repos\` is inside the Obsidian vault, and nothing under `projects\` is code. The only thing connecting them is the URL line in each README. (Your current `POC-Thirdfort\POC-Thirdfort-Vault\POC\` — code physically inside the vault — is the anti-pattern this replaces.)

## Why not one repo for all projects

Unrelated POCs fail every monorepo test:

- **Independent lifecycles** — a completed POC gets archived while three others are active; in one repo, archiving one thing means either freezing all of it or inventing per-subtree archive rules.
- **Independent CI** — a change to a Logic App POC shouldn't trigger, block, or wait on the tests of an unrelated app.
- **Independent audiences** — repos get shared with clients, reviewers, or other teams per engagement. One mega-repo forces either over-exposure or constant permission gymnastics.
- **Failure isolation and clone cost** — one broken build, one secrets leak, one bloated history affects everything.

One repo per deployable thing = the unit at which you deploy, review, share, and archive independently. When those four are shared, that's the *only* time a monorepo is correct — e.g. the CDD journey wizard and its API client belong in **one** repo (they ship and are tested together), while a separately-deployed API for the same engagement would be a **second** repo, not a folder in the first.

## The mapping is deliberately not 1:1

A vault project folder ↔ repo count can be:

- **1 : 1** — the norm. One POC, one repo.
- **1 : 0** — notes-only work. POC-Enterprise is mostly this: 47 SOD/engagement notes, many with no code at all — just `Repo:` URLs where code exists.
- **1 : N** — one engagement, several deployables (e.g. an app repo and a shared platform/infra repo).

So the rule to remember: **repos are partitioned by what ships together, vault folders by what you think about together.** They're allowed to have different boundaries — the seam links them.

---

I've added a **Repo topology** section to [[application-project-organisation]] capturing this:The wiki entry now has the **Repo topology** section between "Layer 2" and "The seam", covering the N+1 rule, the disk layout, why no mega-repo, the monorepo exception, and the non-1:1 mapping (1:1 / 1:0 / 1:N).

Summary of the answer: **N+1 repos** — one vault repo for all knowledge, plus one repo per thing that ships together. Code lives at a sibling root outside the vault (`C:\Source\Repos\<app>\` in the sketch), connected only by the `Repo:` URL line in the vault project's README and the `Design notes:` line back. Repo boundaries follow *what deploys together*; vault folder boundaries follow *what you think about together* — different questions, linked by the seam, never merged.
[Timestamp: 2026/10/15 17:26:40]

**user**: so do you avoid repeating the documentation between the vault/project/<name> and the repo/docs
[Timestamp: 2026/10/15 17:46:09]

**ai**: Yes — by default nothing is repeated. Each document has exactly **one home**, and the other side points at it. The seam is a link, not a copy. But "which home" needs a sharper rule than "design goes in the repo", so:

## The ownership test

Ask two questions about any document:

1. **Would a code change force this to change?** → it belongs in `repo/docs/`. If it can rot because code moved on, it must be versioned next to the code so the same PR catches it.
2. **Does it change because the engagement, research, or your thinking changed?** → it belongs in `vault/projects/<name>/`. It has no reason to follow code changes, so co-locating it with code would just make it *look* authoritative while going stale quietly.

| Content | Home | Why |
|---|---|---|
| Architecture as built, API contract, runbook, ADRs | `repo/docs/` | Must change in the same PR as the code; CI/review can enforce it |
| Research, vendor facts, domain exploration, meeting notes, options you rejected during discovery | `vault/projects/<name>/` | Thinking has its own timeline; it's dated evidence, not build truth |
| External artifacts (SODs, PDFs, screenshots) | `vault/archive/` | Frozen snapshots — they don't drift because they never change |
| Status, `Repo:` URL, index | vault project README | The "returning after three weeks" surface |

## The flow is one-directional

Exploration lives in the vault and *funnels forward* into a decision; the decision is recorded once, as an ADR in the repo; the vault links to it. Concretely:

- Vault note: "we compared X vs Y, Z won, see `docs/adr/0003`" — one line, no restatement of the ADR's content.
- The vault **never describes the architecture** — it points at `design.md`. The moment you paste an architecture description into the vault, you've created a second copy that will drift the next time the repo refactors.
- The repo **never records engagement context** — client background, why the POC exists, what was captured in meetings — that's vault material, referenced from `docs/design.md` in a sentence.

## The one accepted echo

Each side's README carries a sentence or two of "what this is" — pointer-scale, low-churn (a name and a purpose rarely change, so even if the two sentences disagree slightly the damage is nil). That's the entire permitted overlap. Beyond a sentence, it's a copy, and a copy is a future drift site — the Drift section's rule: *every fact copied instead of linked is where the structure fails*.

The result: `vault/projects/<name>/` is much thinner than it first sounds — an index README, dated thinking notes, maybe a decisions list that's mostly links, and the captured raw material. The heavy documentation (design, ADRs, runbook, contract) lives with the code where it's enforced.

I've added this as a **Documentation ownership** section to [[application-project-organisation]], right after the seam:Added — the **Documentation ownership** section now sits between "The seam" and "Drift" in [[application-project-organisation]], containing:

- **The ownership test** — code-change-forces-it → `repo/docs/`; engagement/thinking-changes-it → vault
- **The four-way table** — build truth (repo), thinking notes (vault), frozen artifacts (`vault/archive/`), status/index (project README)
- **One-directional flow** — exploration → decision recorded once as an ADR → linked, never restated; vault never describes architecture, repo never records engagement context
- **The accepted echo** — one or two sentences of "what this is" per README is the only permitted overlap; anything beyond a sentence is a copy and a future drift site

So the direct answer to your question stands: yes, the vault project folder and `repo/docs/` never repeat content — the vault folder ends up thin (index + dated thinking + links), and all enforced, code-adjacent documentation lives with the repo where PRs and CI keep it honest.
[Timestamp: 2026/10/15 17:46:09]

**user**: so where do  PRD's exist within this structure
[Timestamp: 2026/10/15 18:04:36]

**ai**: A PRD doesn't map statically to either layer — it **migrates**. It's a normative document (says what *should* exist, not what does or did), and it changes role when it gets signed off. The structure handles it with a small lifecycle:

## The PRD lifecycle

**1. Draft — vault, `projects/<name>/`**
While the PRD is being negotiated — stakeholder asks, competing scope options, problem framing — it's thinking. It evolves on the engagement's timeline, predates any repo, and is dated like any other note. This is where your `internal-cdd-process-prd.md` lives right now, correctly: its status is *"draft for review"*.

**2. Ratified — moves (never copies) to `repo/docs/prd.md`**
The moment it becomes the agreed baseline for "done", it stops being dated evidence and becomes a contract that code is judged against. Two reasons it must be next to the code:

- **It only drifts detectably there.** A behaviour PR that doesn't touch the PRD is flagged in review — the same same-PR gate as `design.md`. Left in the vault, nothing forces them together: vault notes are allowed to age quietly, and a contract can't be allowed to age quietly.
- **Its acceptance criteria become tests.** This is the traceability that makes a PRD actually work: goal → test assertion. Your PRD's goals are already embodied in `cdd-api-client.test.js` — requirements as executable documentation, the same mechanism as the runnable README. A criterion nobody can write a failing test for was never a criterion.

**3. Superseded — git history + ADR**
Old versions live in git history, untouched. A deliberate scope pivot ("goals changed because X") gets an ADR — `0005-scope-pivot-supersedes-prd-v2` — not a silent edit to section 4. The vault keeps the *why* behind the pivot, linked to the ADR.

## The rules that keep it honest

- **Move, don't copy.** After ratification the vault keeps only discovery material (interviews, raw asks, rejected scope) and a `PRD: <url>` pointer. The moment both copies are editable, you've built a drift site out of your most important document.
- **If the PRD is edited outside git** (Word/SharePoint with business stakeholders), *that* file is the artifact — archive the signed version (like the SODs in `vault/archive/`) and don't maintain a second working copy. One source of truth, wherever it lives.
- **1:0 projects:** if no repo ever materialises (notes-only engagement), the PRD stays in the vault — the repo rule exists for enforcement against code, and there's no code to enforce against.

## The POC special case

Most POC PRDs are one page: **problem, success criteria, non-goals**. The success criteria are the whole point — *what result proves the hypothesis, what result kills it*. Even a throwaway POC keeps this in `docs/` (or a README section), because a POC without falsifiable success criteria can't fail, and a thing that can't fail proved nothing. Same principle as the "runs in five minutes" README.

Adding this to the wiki as a **PRDs** section between Documentation ownership and Drift:Captured — the **PRDs** section is now in [[application-project-organisation]], between "Documentation ownership" and "Drift".

The short answer to your question: **PRDs move through the structure rather than living in one place** —

1. **Draft** → vault `projects/<name>/` (thinking, dated, negotiated on the engagement timeline — where your `internal-cdd-process-prd.md` correctly sits today)
2. **Ratified** → `repo/docs/prd.md` (the contract, enforced by the same-PR review gate, criteria traced into tests)
3. **Superseded** → git history + an ADR for scope pivots, never a silent edit

The load-bearing rules: *move, never copy* after ratification (two editable copies of the contract is a drift site in your most important document), treat an externally-edited PRD as a single artifact you archive rather than duplicate, and for POCs keep it to one page where the success criteria are falsifiable — because a POC that can't fail proved nothing.

One practical note for your current Thirdfort material: when the CDD wizard graduates from vault `POC/` into a real repo, the PRD should move with it into that repo's `docs/`, leaving the vault note as discovery material + pointer.
[Timestamp: 2026/10/15 18:04:36]