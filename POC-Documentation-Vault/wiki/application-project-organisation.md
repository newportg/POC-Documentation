# Application project organisation

A standard shape for application projects: keep the knowledge vault (research, context, and exploration) separate from application repositories (code, infrastructure, and documentation that must evolve with the code). Each side points to the other; neither keeps a second copy of the other’s content.

This is the target structure for the vault’s `/projects/<name>/` folders. [[cdd-poc-app]] is an example of the arrangement this replaces: application code living inside the vault.

## Why the current setup feels disorganised

Observed across the existing POC-* vaults:

- **One vault per project, duplicated boilerplate.** Each vault carries its own `AGENTS.md`, `CLAUDE.md`, `prompts/translate.md`, and `copilot/skills/` tree. Nothing is shared, so conventions drift.
- **Mixed concerns.** POC-Thirdfort has app code (`POC/lib/`, tests, HTML wizards) alongside wiki notes. Code and knowledge have different lifecycles and tools; interleaving them makes both harder to manage.
- **Flat wiki folders don't scale.** POC-Enterprise has 47+ files in one directory—SODs, vendor POCs, Entra ID configs, and architecture notes side by side.
- **Inconsistent shape per project.** POC-Thirdfort has `wiki/ + POC/`, POC-NorthstarData has only `wiki/`, and POC-poc is an empty template. There is no consistent structure to return to.
- The POC-poc template (`/projects/<name>/` with a README per project) is the right starting point, but was never rolled out.

## Layer 1 — one knowledge vault

One vault for shared knowledge, with one folder per project and shared boilerplate at the root:

```text
vault/
├── README.md
├── AGENTS.md
├── raw/
├── archive/
├── prompts/
└── projects/
    ├── thirdfort/
    │   ├── README.md
    │   ├── api-research.md
    │   ├── domain-exploration.md
    │   └── open-questions.md
    ├── enterprise/
    │   └── ...
    └── northstar-data/
        └── ...
```

Rules:

- Use one folder per project; nest by topic once a project has roughly 10 notes.
- Keep shared boilerplate (`AGENTS.md`, skills, prompts) at the vault root.
- Make the project README the index: status, repo link, links to relevant research and repo-owned decisions, and last-updated date. Summarize context there, but link to ADRs rather than copying their decisions.

### Vault folders and workflow

The vault root README is a brief entry point. This document defines the structure and workflow; [[projects]] is the index linking to each project README.

- `/raw` — capture inbox for notes, PDFs, screenshots, and links.
- `/wiki` — organized notes and navigation pages, including the project index.
- `/projects/<name>/` — active project research and engagement notes.
- `/archive` — processed raw material retained as a permanent record.
- `/prompts` — shared prompts used by vault workflows.

For the capture-to-wiki workflow, add material to `/raw`, process it using [[prompts/translate]], update the relevant wiki or project notes, then move processed material to `/archive`. Follow the vault rules in `AGENTS.md`: preserve raw and archived material, and read and merge an existing wiki entry rather than overwriting it. The vault is version-controlled so changes remain reviewable.

## Layer 2 — one application repo per deployable thing

Use the same basic shape for a throwaway POC and production; POCs simply have thinner content:

```text
repo/
├── README.md
├── docs/
│   ├── design.md
│   ├── adr/
│   ├── prd.md
│   └── runbook.md
├── src/
├── tests/
├── infra/
├── config/
├── .github/workflows/
└── .gitignore
```

Conventions that matter most:

- **README is the contract:** purpose, prerequisites, how to run it, and a link to the vault project folder. Aim for a fresh clone to run in under five minutes.
- **Docs-as-code:** design docs, API contracts, runbooks, ratified PRDs, and ADRs live in the repo and are versioned with the code. The vault holds research and engagement context; the repo holds the current product requirements and build truth.
- **ADRs are lightweight records:** one file per significant decision, such as `docs/adr/0001-use-entra-id.md`, covering context, options, choice, and consequences.
- **Keep `infra/` separate from `src/`:** this makes infrastructure-as-code reviewable and POCs easier to reproduce.
- **One repo per deployable thing:** don't merge unrelated POCs into a monorepo or split one deployable POC across several repos.

## Writing repo documentation in Obsidian

Repo-owned documentation is still Markdown, so it can be written in Obsidian. Open the application repo folder as an Obsidian vault and edit its `docs/` there; the files remain in the application repo and are versioned with the code. If using Obsidian settings or plugins in that repo, decide deliberately which shared configuration belongs in Git and keep machine-specific workspace state out.

The main knowledge vault and an application repo are separate Obsidian vaults. You can switch between them in Obsidian or open them in separate Obsidian windows. Obsidian does not combine independent folders into one vault view. If having all notes and repo documentation in a single Obsidian file tree is essential, this separate-vault arrangement may not fit; don't solve that by copying repo documentation into the knowledge vault, since that creates two sources of truth.

## Repo topology — where the code lives

The standard topology is **N+1**: one Git repo for the knowledge vault, plus one repo outside it for each deployable thing.

```text
C:\Source\
├── Obsidian\Projects\<vault>\    ← vault Git repo
│   └── projects\<name>\          → pointer to repo
└── Repos\<app>\                  ← app Git repo
```

- **Not one repo for all projects.** Unrelated POCs have independent lifecycles, CI, audiences, and clone histories. Partition repos by **what ships together**; partition vault folders by **what you think about together**. Those boundaries need not match.
- **Use a monorepo only when things genuinely ship together.** For example, a CDD wizard and its API client belong together if they are tested and deployed as one. A separately deployed API is a separate repo.
- **Vault folder ↔ repo is not always 1:1:** 1:1 is the norm; 1:0 for notes-only work (such as POC-Enterprise, where most SOD notes have no code); and 1:N when an engagement has several deployables.
- Keep application code out of the vault. `POC-Thirdfort-Vault\POC\` is the anti-pattern this structure replaces.

## The seam

Use one pointer each way; don't duplicate content:

- Vault project README: `Repo: <URL> | Status: <status and date>`
- Repo README: a link to the vault project folder, such as `Knowledge notes: <vault project URL or agreed local link>`

Archive a POC by marking its status in the vault README and making the repo read-only when appropriate. Do not move code into the vault.

## Documentation ownership

Each document has one home. Use this test: *Would a change to the running product or its supported behavior require this document to change?* If so, it belongs in `repo/docs/`. *Does it change because research, engagement context, or understanding changed?* If so, it belongs in the vault.

| Content | Home |
|---|---|
| Architecture as built, API contract, runbook, ADRs, ratified PRD | `repo/docs/` |
| Research, vendor facts, domain exploration, rejected discovery options, meeting notes | `vault/projects/<name>/` |
| External artifacts (SODs, PDFs, screenshots) | `vault/archive/` |
| Status, repo link, project index, links to repo decisions | Vault project README |

A domain model in the vault is exploratory; the implemented model or API contract belongs in the repo. Exploration may lead to a decision, which is recorded once as an ADR in the repo. The vault links to that ADR rather than restating the decision. The repo links back to the vault for engagement context.

One or two low-churn sentences describing the project may appear in both READMEs. Beyond that, link to the other source rather than copying it.

## PRDs

A PRD is normative: it says what should be built.

- **Draft:** Keep it in `vault/projects/<name>/`, dated like other thinking notes, while it is being discussed and negotiated.
- **Ratified:** Move it—not copy it—to `repo/docs/prd.md`. It is now the contract for the product. Map acceptance criteria to tests or another explicit verification method; changes to requirements should update the PRD.
- **Superseded:** Keep prior versions in Git history. Record a deliberate scope change in an ADR; keep the discovery context in the vault and link to that ADR.

After ratification, the vault keeps discovery material and a `PRD: <repo link>` pointer, not an editable copy. If stakeholders edit the PRD outside Git (for example, in Word or SharePoint), treat the signed file as the artifact and archive it like an SOD; do not keep a competing working copy. Notes-only engagements with no repo keep their PRD in the vault.

For POCs, keep the PRD short: problem, success criteria, and non-goals. State how each criterion will be verified—by test, demo, inspection, or another suitable method—so the hypothesis can be meaningfully evaluated.

## Drift

Structure reduces drift but cannot eliminate it. The aim is one source of truth per fact and visible checks where the two layers meet:

- **Link rather than restate.** Every copied fact is a potential drift site.
- **Review repo docs with behavior changes.** When a code change affects documented behavior, the PR should update the relevant docs or explain why no update is needed. Use tests, contract checks, and CI to verify specific claims; a README or PR checklist alone does not guarantee documentation stays current.
- **Keep ADRs append-only.** Supersede a decision with a new ADR (for example, `0002 supersedes 0001`) rather than silently rewriting its history.
- **Date vault research.** Notes are records of what was understood at a point in time, not current build truth. Include capture date, source, and open questions for facts that may change, such as vendor API behavior.
- **Show project freshness.** Keep status and last-updated on the project README.
- **Archive deliberately.** Mark the project archived in the vault and make the corresponding repo read-only when appropriate.

This structure cannot prevent an initially incorrect note, an unnoticed upstream change, or failures to follow review and CI practices. It makes ownership clearer and drift easier to detect; it does not replace those practices.

## Migration steps

1. Keep one shared vault and populate `projects/<name>/` for each project. Retire duplicated per-vault boilerplate as projects are absorbed.
2. Move application code out of vault `POC/` folders into standalone repos. Keep code and build-truth docs together in each repo.
3. Adopt `docs/ + src/ + infra/` where appropriate, even for throwaway POCs, so they are reviewable and reproducible.
4. For repo-owned Markdown, use Obsidian by opening the app repo as a vault. Keep vault research and repo documentation separate; link between them rather than copying.