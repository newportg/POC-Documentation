# poc-party Project Plan

Status: approved by the user on 2026-11-05.

## Purpose

Create a standalone, static browser proof of concept for reusable Party records,
covering individuals, companies, and groups. Demonstrate identity and group
membership concepts from the Party PRD without implying production controls.

## Project organization

- Application repository: `C:\Source\Repos\poc-party`
- Knowledge-vault project:
  `C:\Source\Obsidian\Projects\POC-Documentation\POC-Documentation-Vault\projects\Party`
- Keep code and build-truth docs in the application repo; keep discovery and domain
  thinking in the vault.
- Include a README, implementation design documentation, source, tests, and a
  `.gitignore`. Keep a one-line pointer between repo and vault.

## Scope

### In scope

- Plain HTML, CSS, and browser-native JavaScript; no build step, backend, datastore
  service, sign-in, or cloud resource.
- Visual styling aligned with `C:\Source\Repos\poc-asset`: dark background and
  surfaces, indigo/purple gradient accent, rounded panels, tabs, badges, and
  responsive behavior.
- Fictional sample Party data with `individual`, `company`, and `group` types.
- Party list/search with type and status filters; readable Party details.
- Lightweight create/edit interactions with validation.
- Explicit group membership with optional role and effective dates. Groups contain
  individual and/or company Parties; invalid membership is rejected visibly.
- Matter participation references as context-specific roles, not intrinsic Party
  attributes.
- Browser-local persistence with reset-to-sample-data; communicate that the storage
  is local to this browser.
- Clear demo-only notice: authorization, audit, retention, identity matching, and
  compliance controls are not implemented.
- README with run instructions and vault pointer; `docs/design.md` with the
  implemented model and limitations.
- Focused, dependency-free tests for domain validation and membership behavior.

### Out of scope

- Production APIs, authentication, authorization, cloud services, or shared storage.
- Automatic duplicate merging, KYC/AML screening, verification, or compliance
  decisions.
- Real personal data or external lookups.
- Implementing a production audit, retention, or privacy regime.

## Acceptance criteria

1. The app opens from its static HTML entry point without installation or build.
2. The interface follows poc-asset's visual language and works at mobile widths.
3. Users can search/filter Parties, open details, and create/edit supported types.
4. Group membership explicitly links only valid individual/company Parties, with
   optional roles/dates and validation feedback.
5. Participation roles are attached to matter references, not Party identity.
6. Demo changes persist in browser storage and can be reset.
7. Fictional data and the absence of production security/compliance guarantees are
   clearly communicated.
8. README and docs link back to the Party vault project.
9. Focused validation passes; unrelated files and the poc-asset repository are not
   modified.

## References

- `POC-Documentation-Vault\projects\Party\party-prd.md`
- `POC-Documentation-Vault\projects\Party\individual-model.md`
- `POC-Documentation-Vault\projects\Party\company-model.md`
- `POC-Documentation-Vault\wiki\application-project-organisation.md`
- `C:\Source\Repos\poc-asset`
