# Application project organisation

The standard shape for a modern application project: two layers that stay separate — the knowledge vault (notes, research, decisions) and the application repo (code, infra, docs-as-code). Each keeps exactly one pointer to the other. This is the target structure for the vault's `/projects/<name>/` folders.
Related: [[cdd-poc-app]] is an example of what this replaces — app code living inside the vault.

## Why the current setup feels disorganised

Observed across the existing POC-* vaults:

- **One vault per project, duplicated boilerplate.** Each vault carries its own `AGENTS.md`, `CLAUDE.md`, `prompts/translate.md` and full `copilot/skills/` tree. Nothing shared, conventions drift.
- **Mixed concerns.** POC-Thirdfort has app code (`POC/lib/`, tests, HTML wizards) alongside wiki notes. Code and knowledge have different lifecycles and tools; interleaving them is the main source of disorder.
- **Flat wiki folders don't scale.** POC-Enterprise has 47+ files in one directory — SODs, vendor POCs, Entra ID configs, architecture notes side by side, no taxonomy.
- **Inconsistent shape per project.** POC-Thirdfort has `wiki/ + POC/`, POC-NorthstarData has only `wiki/`, POC-poc is an empty template. No muscle memory between projects.
- The POC-poc template (`/projects/<name>/` with a README per project) is the right idea but was never rolled out.

## Layer 1 — one knowledge vault

One vault for everything, one folder per project, boilerplate at the root only:

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
    │   └── decisions.md
    ├── enterprise/
    │   └── ...
    └── northstar-data/
        └── ...
```

Rules:

- One folder per project; nest by topic once a project exceeds ~10 notes.
- Boilerplate (AGENTS.md, skills, prompts) lives once at the vault root, shared across projects.
- A project README is the index: status, links to the live repo, key decisions, last-updated. Read this first when returning to a project after three weeks.

### Vault folders and workflow

The vault root README is a brief entry point. This document defines the structure and
workflow; [[projects]] is the index linking to each project README.

- `/raw` — capture inbox for notes, PDFs, screenshots, and links.
- `/wiki` — organized notes and navigation pages, including the project index.
- `/projects/<name>/` — active project notes, with one README per project.
- `/archive` — processed raw material retained as a permanent record.
- `/prompts` — shared prompts used by vault workflows.

For the capture-to-wiki workflow: add material to `/raw`, process it using
[[prompts/translate]], update the relevant wiki or project notes, then move processed
raw material to `/archive`. Preserve raw and archived material according to the vault
rules in `AGENTS.md`; never overwrite an existing wiki entry without reading and
merging it first. The vault is version-controlled so changes remain reviewable.

## Layer 2 — one application repo per deployable thing

Same shape for a throwaway POC and for production — POCs just have thinner content:

```text
repo/
├── README.md              # what it is, how to run it in <5 min
├── docs/
│   ├── design.md          # architecture, data flow
│   ├── adr/               # 0001-auth-choice.md, ...
│   └── runbook.md         # deploy/debug
├── src/                   # app code, one folder per component
├── tests/                 # or colocated next to src
├── infra/                 # IaC: bicep/terraform
├── config/                # env-specific settings (dev/test/prod)
├── .github/workflows/     # CI: lint, test, deploy
└── .gitignore
```

Conventions that matter most:

- **README is the contract** — purpose, prerequisites, one-command run, link back to the vault project folder. If it can't run in five minutes from the README, the project is unowned.
- **Docs-as-code** — design docs and ADRs live in `docs/` in the repo, versioned with the code. The vault holds the *thinking* (research, vendor notes, domain exploration); the repo holds the *decisions and build truth*.
- **ADRs are lightweight files** — `docs/adr/0001-use-entra-id.md`, one per significant decision: context, options, choice, consequence. Biggest payoff for solution work; turns tribal knowledge into searchable record.
- **infra/ separate from src/** — POC work is often integration/infra heavy (Zscaler, Prisma, Entra ID, Logic Apps); keeping IaC reviewable separately makes the POC demonstrable and repeatable.
- **One repo per deployable thing.** Don't merge unrelated POCs into a mono-repo; don't split one POC into five repos.

## Repo topology — where the code lives

Total is **N+1**: the vault itself is one git repo; every deployable thing is its own repo, outside the vault:

```text
C:\Source\
├── Obsidian\Projects\<vault>\    ← 1 repo: notes, research, decisions
│   └── projects\<name>\          → Repo: <url>   (pointer only)
└── Repos\<app>\                  ← N repos: one per app/POC
```

- **Not one repo for all projects.** Unrelated POCs have independent lifecycles (archive one without freezing others), independent CI (a Logic App change shouldn't block an unrelated app's build), independent sharing (per-engagement audiences), and failure/clone isolation. Partition repos by **what ships together**; partition vault folders by **what you think about together**. The boundaries needn't match — the seam links them.
- **Monorepo only when things genuinely ship together** — e.g. the CDD wizard and its API client are one repo (tested and deployed as one); a separately deployed API for the same engagement is a second repo, not a folder.
- **Mapping vault folder ↔ repo is not 1:1:** 1:1 is the norm; 1:0 for notes-only work (POC-Enterprise: 47 SOD notes, most with no code — just `Repo:` URLs); 1:N for one engagement with several deployables (app + shared infra).
- Code physically inside the vault (`POC-Thirdfort-Vault\POC\`) is the anti-pattern this replaces — never move code into the vault.

## The seam

One pointer each way, no content duplication:

- Vault project README: `Repo: <url> | Status: PoC complete <date>`
- Repo README: `Design notes: vault/projects/<name>/`

Archive a POC by marking status in the vault README and leaving the repo read-only. Never move code into the vault.

## Documentation ownership

Nothing is repeated between `projects/<name>/` and `repo/docs/` — each document has one home; the other side links to it in a line. Ownership test: *would a code change force this to change?* → repo/docs (versioned with code, enforced by PR/CI). *Does it change because the engagement or thinking changed?* → vault (dated evidence, own timeline).

| Content | Home |
|---|---|
| Architecture as built, API contract, runbook, ADRs | `repo/docs/` |
| Research, vendor facts, domain exploration, options rejected in discovery, meeting notes | `vault/projects/<name>/` |
| External artifacts (SODs, PDFs, screenshots) | `vault/archive/` (frozen — never drifts) |
| Status, `Repo:` URL, index | vault project README |

Flow is one-directional: exploration in the vault narrows to a decision → decision recorded once as an ADR in the repo → vault links to the ADR rather than restating it. The vault never describes the architecture (points at `design.md`); the repo never records engagement context (points back at the vault).

Accepted echo: one or two sentences of "what this is" on each README — pointer-scale, low-churn. Beyond a sentence it's a copy, and a copy is a future drift site (see Drift).

## PRDs

A PRD is normative — it says what *should* be built — so it migrates rather than belonging to one layer:

- **Draft** — vault `projects/<name>/`, dated like any thinking note; negotiated on the engagement's timeline (e.g. `internal-cdd-process-prd.md`, status "draft for review" — correct placement while unratified).
- **Ratified** — moves (never copies) to `repo/docs/prd.md`. It's now the contract code is judged against, so it must sit where drift is detected: a behaviour PR that doesn't touch it is flagged in review, and its acceptance criteria become tests (goals → `cdd-api-client.test.js` assertions = requirements as executable documentation). A criterion nobody can write a failing test for was never a criterion.
- **Superseded** — prior versions stay in git history; a deliberate scope pivot gets an ADR (`0005-scope-pivot-supersedes-prd-v2`), never a silent edit. The vault keeps the *why* behind the pivot, linked.

Rules: post-ratification the vault keeps only discovery material + a `PRD: <url>` pointer — two editable copies of the contract is a drift site in the most important document. If stakeholders edit the PRD outside git (Word/SharePoint), that file is the artifact: archive the signed version like an SOD, don't maintain a working copy beside it. Notes-only engagements (1:0, no repo) keep the PRD in the vault — no code, nothing to enforce against.

For POCs the PRD is one page — problem, success criteria, non-goals — and the success criteria are the point: what result proves or kills the hypothesis. Kept in `docs/` even for throwaway POCs: a POC without falsifiable criteria can't fail, and what can't fail proved nothing.

## Drift

Structure alone doesn't prevent drift — drift is proportional to duplicated truth, and no structure makes two copies agree. This design compensates by minimising duplication and making what remains falsifiable:

- **One source of truth per fact.** The vault links to the repo instead of restating it; the seam is one line each way, so there's almost nothing cross-layer that can drift. Every fact copied into the vault instead of linked is a future drift site.
- **Repo docs rot loudly.** Code + doc changes land in the same PR (review flags "code changed, docs didn't"); the README's "runs in five minutes" claim is re-tested by every fresh clone; tests, mock-as-contract simulators and OpenAPI contract tests verify claims in CI — e.g. `cdd-api-client.test.js` and the mock transport as executable documentation of the contract.
- **ADRs are append-only** — never edited, only superseded (`0002 supersedes 0001`), so the decision record can't disagree with history; later thinking sits next to old truth with the succession explicit.
- **Vault notes age, they don't drift.** They are dated snapshots of thinking, not build truth. Vendor/upstream facts (e.g. Thirdfort API behaviour) are invisible to both layers when they change; the compensation is capture date + source + open questions on the note (log uncertainty rather than guess — AGENTS.md rule), so stale facts read as "true as of <date>" rather than current.
- **Status + last-updated** on the project README makes a stale project visible from the index.
- **Archive freezes both halves at once** — repo read-only, vault status is the last word.

Not compensated: a note that was wrong when written, upstream changes while nobody looks, and any of the above without enforcement. The structure makes each safeguard cheap and each failure visible — it can't skip the discipline (PR review, CI, dated notes).

## Migration steps

1. Keep one vault (the POC-poc structure); populate `projects/<name>/` per project; retire per-vault skill copies and other duplicated boilerplate as each old vault is absorbed.
2. Move app code out of vault `POC/` folders into standalone git repos (e.g. the Thirdfort wizards and API client are already a coherent app).
3. Adopt `docs/ + src/ + infra/` even for throwaway POCs — costs nothing, makes every POC demoable the same way.
