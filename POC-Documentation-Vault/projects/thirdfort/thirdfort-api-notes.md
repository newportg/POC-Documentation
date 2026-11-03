# Thirdfort API notes

What the upstream Thirdfort API offers, reduced to the facts that matter for designing our own interface on top of it.

Source: <https://thirdfort.stoplight.io/docs/api/b2edb775739e6-thirdfort-api> (canonical: <https://docs.thirdfort.com/docs/api>). Content pulled 2026-10-15 from the Stoplight backing API (project `cHJqOjM2MzI5`, branch `master`; the tree lists 74 documentation nodes among 110 total nodes). See [[#Appendix - refreshing these facts]].

Related: [[internal-cdd-api]], [[cdd-kyc-domain-model]], [[cdd-journey-state-model]]

## Environments and versions

| | Base URL |
|---|---|
| v2 sandbox | `https://sandbox.api.thirdfort.io/v2` |
| v2 production | `https://api-v2.thirdfort.io/v2` |
| v3 sandbox | `https://sandbox.api.thirdfort.io/v3` |
| v3 production | `https://api-v2.thirdfort.io/v3` |

- Two live versions with different scope. **v3 only covers title documents** (Checks, Documents, Titles). Everything else — transactions, checks (KYB/document), tenants, users, inboxes, events, companies — exists only in **v2**.
- No deprecation or sunset notice for v2 anywhere in the docs. Assume both must be integrated and that our own API must not leak this split to callers.
- Sandbox is functionally complete: real webhooks, real SMS (so don't use random phone numbers), mock verification data sources.

## Authentication

- Bearer JWT signed RS256 with our own 2048-bit RSA key. We keep the private half; Thirdfort gets the public half plus an email for the m2m account, and returns a `kid`.
- Claims: `aud`, `exp` (= `iat` + 3600s), `iat`, `iss`, `sub` (both = m2m email). `aud` documented as `https://sandbox.api.thirdfort.io/v2/` and `https://api.thirdfort.io/v2/` — **v2 only**; no v3 audience is documented, and there is no documented mechanism for rotating the key. Both are open questions for Thirdfort.
- Practical consequence: a token minter must exist, with jittered refresh well inside the 3600s window. This is the single point of failure for the whole integration.
- **Context headers** are how resources get scoped. Mutually exclusive, `team-id` wins over `tenant-id`:
  - `tenant-id` — create under a partner tenant (access for everyone in it).
  - `user-id` — impersonate a stub user (attributes the request to a named individual).
  - `team-id` — direct-integration teams.

## Tenancy model

- **Tenant** = the business (law firm, agent) that bought Thirdfort. Its name is shown to the consumer in the SMS invite. Created with `POST /v2/tenants` (`{name}`); cannot be updated by API.
- **User** = an individual at the company. For partner integrations we create **stub** users (`type: "stub"`, roles `["app:web","transactions:user"]`), which can only be impersonated, not logged into. `POST /v2/users`.
- **Consumer** = the subject of the check, who uses the Thirdfort mobile app.
- Partner integrations **must** map our customer → tenant and our user → stub user. Without it Thirdfort communicates with the consumer on behalf of us (the partner) instead of the tenant/user we represent — which is both a UX and an audit problem.
- Commercial model matters to the design: *reseller* (we bill the firm) vs *platform partner* (Thirdfort bills the firm directly). Reseller requires us to derive which check actually completed in order to bill (see [[#Billing and entitlement signals]]).

## Checks, transactions and tasks

Thirdfort's resource graph:

```
transaction (v2)          check (v2)              check (v3)
  request.tasks[]           request.reports[]       request.documents[]
  actor (consumer PII)      request.data{company}   request.data{address|title_numbers}
  → reports → PDF           → reports → PDF         → documents (PDF)
```

- A **transaction** is the container for an ID/AML/Source of Funds journey for one consumer. `type: "v2"`, required `ref` and `request`, `name` shown to the consumer, `ref` is ours.
- A **check** covers document verification (`type: "document"`) and Know-Your-Business (`type: "company"`); v3 uses `type: "title"`.
- Tasks are declared at creation and are **not additive**: you cannot bolt a new task onto an existing transaction. Adding a check later means a new transaction/check.
- One or more tasks per transaction; status is per report, aggregated per resource.

### Task catalogue

| Product | Tasks |
|---|---|
| Enhanced NFC ID | `report:identity` (with `opts.nfc: "preferred"`), `report:footprint`, `report:peps` |
| Original ID | same three, without the `nfc` option |
| Lite screening | `report:footprint`, `report:peps` (no app involvement) |
| Standalone screening | `report:screening:lite` (needs DOB, last name, ISO3 country) |
| Proof of address | `documents:poa` |
| Proof of ownership | `documents:poo` (transferor, borrower, lessor only) |
| Source of Funds | `report:bank-statement`, `report:bank-summary`, `report:sof-v1`, optional `documents:bank-statement` |
| Ongoing monitoring | `opts.monitored: true` on `report:peps` (individuals) or `company:sanctions` (companies) |
| International address verification | `opts.consent: true` on `report:footprint` (needed only for a listed set of non-UK countries) |
| Document verification | `POST /v2/checks` with `type: "document"`, report `identity:lite`, then `POST /v2/checks/{check}/documents` |
| KYB | `company:summary` + `company:sanctions` always; plus `company:ubo`, `company:annual-accounts`, `company:annual-return`, `company:articles-association`, `company:beneficial-check`, `company:register-check`, `company:register-extract`, `company:register-report`, `company:shareholders` by jurisdiction |
| Title documents (v3) | `title:plan-freehold`, `title:register-freehold`, `title:plan-leasehold`, `title:register-leasehold` |

Giftor variation: `request.actor.type: "giftor"` switches the SoF questionnaire to the giftor flow.

## Statuses and enums

- Transaction status: `open`, `closed`, `aborted` (`deleted` also appears in the model enum).
- Check status: `open`, `closed` (v3 adds `deleted`).
- Report status: `closed`, `complete`, `error`, `expired`, `rejected`, `unobtainable`. Only `closed`/`complete` mean completed — everything else means "not done", not "failed the applicant".
- Report result: `clear`, `consider`, `fail`. This is the compliance signal; it is separate from status.
- Events: `transaction`, `transaction:report`, `transaction:pdf`, `transaction:changes`, `transaction:share`, `check:report`, `check:pdf`, `check:changes`, `subscription:notification`.
- Per-task completion also surfaces as `metadata.tasks.{type}.{status, completed_at}`.

Two status traps worth encoding into our model:

1. `transaction: closed` means *the PDF is ready*, not *the client passed*. A human decision is still ours to make.
2. An Enhanced NFC check that fails chip read, liveness, or "no passport" silently degrades to an Original ID journey — the NFC breakdown comes back `unobtainable`. The identity report carries the evidence: `breakdown.document` non-empty ⇒ Original ID completed; absent ⇒ Enhanced NFC completed.

## Notifications

Two supported mechanisms, configured per transaction/check at creation:

- **HTTP webhook** — `metadata.notify = {type: "http", data: {hmac_key, method, uri}}`. Methods POST/PUT/PATCH/DELETE (DELETE carries no payload). Payload envelope:

  ```json
	{ 
		"event": "transaction:report", 
		"timestamp": "...", 
		"type": "notify",
		"payload": { 
			"id": "...", 
			"resource": "reports", 
			"status": "closed",
			"uri": "/v2/transactions/{id}/reports/{id}", 
			"data": { 
				"type": "peps" 
			} 
		} 
	}
  ```
  Signature: `X-Signature` header = HMAC-SHA256 of the **raw** body, keyed by the base64 `hmac_key`; verify constant-time before parsing. Keys are per-request, our choice.
- **Polling inbox** — `metadata.notify = {type: "inbox", data: {id}}`; create with `POST /v2/inboxes`, read with `GET /v2/inboxes/{id}/messages` (unacknowledged by default, `?acknowledged=true` for read, **204** when empty), acknowledge with `PATCH /v2/inboxes/{inboxId}/messages/{msgId}` body `{"acknowledged": true}` only.

Gaps that shape our design:

- **No documented retry policy, delivery guarantee, ordering guarantee, or replay.** A webhook receiver must therefore treat delivery as at-most-once and reconcile by re-reading the resource.
- No documented rate limits or `429` semantics.
- Polling has no documented interval; messages must be de-duplicated by `id`.
- Inbox acknowledgement is the only upstream read-receipt. We must acknowledge to avoid re-processing.

## Retrieval

| Need | Call |
|---|---|
| Transaction JSON (+ `_embed=reports`) | `GET /v2/transactions/{id}?_embed=reports` |
| Transaction PDF | same, `Accept: application/pdf` (`406` if negotiation fails) |
| Extra uploaded documents | same report URL, `Accept: application/zip` |
| One report | `GET /v2/transactions/{t}/reports/{r}` |
| Normalised summary | `GET /v2/transactions/{id}/_summary` |
| KYB check JSON/PDF | `GET /v2/checks/{id}` (`Accept: application/pdf` for the PDF) |
| One KYB report | `GET /v2/checks/{c}/reports/{r}` |

- `_summary` returns `pii{address,dob,document,name}` plus per-report `{status, result, data}` for `address`, `document`, `facial_similarity`, `identity`, `peps`, `nfc`. It is the cheapest single call for a normalised view — but its shape varies by check type.
- Additional app-uploaded documents are **not** in the PDF; they arrive as a separate ZIP, signalled by report type `documents:other` (event `transaction:report`).

## Mutating operations

| Action | Upstream |
|---|---|
| Abort a journey | `PATCH /v2/transactions/{t}` `{"status":"aborted"}` — stops SMS, blocks further tasks, prevents PDF if not already generated, **cannot be reopened**, auto-disables monitoring |
| Disable monitoring (individual) | `PATCH /v2/transactions/{t}` `{"changes":{"tasks":[{"type":"report:peps","opts":{"monitored":false}}]}}` |
| Disable monitoring (company) | `PATCH /v2/checks/{c}` `{"changes":{"reports":[{"type":"company:sanctions","opts":{"monitored":false}}]}}` |
| Whitelist screening hits | `POST /v2/transactions/{t}/reports/{r}/hits` or `POST /v2/checks/{c}/reports/{r}/hits`, body `{"dismissals":[{"id":"...","reason":"Irrelevant"}]}` → `202` |
| Share a report with a colleague | `POST /v2/transactions/{t}/events` `{"event":"transaction:share","payload":{"to":{"uid":"..."} \| {"email":"..."}}}` |
| Accept/reject a share | `PATCH /v2/events/{e}` `{"status":"accepted"\|"rejected"}`; list via `GET /v2/events` |
| Company lookup before KYB | `GET /v2/companies?jurisdiction=..&_q=name:X\|number:Y` |
| Title number search (v3) | `POST /v3/titles/_search`; then `GET /v3/titles/{title}/availability` |

Note the asymmetry: only status **or** changes per PATCH, and monitoring can be turned off but never on after creation if it was created off.

## Billing and entitlement signals

These matter if we bill, and they are all derived from report payloads:

- ID checks are charged **per completed check**; SoF is charged **per property transaction** (grouped by identical `ref`). Use a consistent, prefixed `ref` — a matter/case/file reference.
- Original ID vs Enhanced NFC (completed, not initiated): `breakdown.document` present on the `identity` report ⇒ Original ID.
- SoF completed if any of `bank:statement`, `bank:summary`, `sof:v1`, `documents:bank-statement` is present with `status: closed`. Consumer skipping everything ⇒ no charge.
- International address verification is not chargeable if `footprint.breakdown.data.address.country == "GBR"`.

## Constraints and gotchas

- **Title documents** are HMLR-bound: 06:30–23:00 GMT on workdays only; out-of-hours checks close the next business day. Order only titles whose availability is `IMMEDIATE`; `referred_to_documents` are not downloadable.
- **v3 document generation is slow** — sandbox returns **HTTP 400** for roughly 3–4 minutes while a document is being generated. A 400 there is not a client error and must be retried with backoff.
- Mobile number is mandatory for anything that uses the app; validated with libphonenumber. 23 country codes are flagged as unreliable for SMS delivery and warrant a UI warning.
- Uploaded documents: PDF/JPEG/PNG only, 32 kb–10 mb, max 64 mpx; validated synchronously for blur, cut-off and document presence.
- Ongoing monitoring runs 12 months and auto-renews; a `subscription:notification` arrives about a month before renewal and should prompt the user to continue or stop.
- Error bodies come in two shapes: `{"message": "..."}` and a richer `{message,name,code,status,error{reason,trace,type,details[]}}`. Codes seen: 400, 401, 403, 404, 405, 406, 409, 422, 500, 503.

## Not present upstream

Confirmed absent from both specs and the guides — each absence is a gap our layer must fill:

- Idempotency keys, ETags/optimistic concurrency, `Retry-After`, pagination on any collection, rate-limit headers, bulk/batch endpoints.
- Any notion of a compliance decision, a reviewer, or an approval — Thirdfort returns evidence and results, never "accepted"/"rejected".
- Any mapping to our matter/case identity beyond the free-text `ref`.
- Re-issuing an invite (no resend SMS/invite endpoint).
- Partial task addition to an existing transaction.
- Deletion of a tenant or transaction.

## Inconsistencies found in the published specs

Worth knowing before we code against them:

- v3 `POST /checks` path schema (`request.documents[]`, flat `data.address`) disagrees with the prose guide and the unused `CREATE_CHECK` component (`request.data.title_numbers|address`, `request.reports[]`, `metadata.notify`).
- `Check.request` requires `data` and `reports` while v3 examples return `documents[]`; `pdf` examples use `documents_id`/`type: title` against a schema of `document_id`/`type: check:pdf`.
- A `CHECKS_LIST` schema and a `CREATE_CHECK` requestBody exist in v3 but are not wired to any path — there is no v3 list endpoint.
- `GET /v3/documents/{document}` is the only v3 operation with an explicit `security` block.
- v2's `PATCH /v2/events/{event}` declares no 2xx response.
- The docs link a Thirdfort Notion "API Hub" for UI/UX guidance; it was not read for these notes.

## Appendix - refreshing these facts

The docs are a Stoplight-rendered SPA, so the HTML is empty. Pull the data instead:

```powershell
# table of contents (all 74 doc nodes)
curl.exe -s -H 'Accept: application/json' `
 'https://stoplight.io/api/v1/projects/cHJqOjM2MzI5/table-of-contents' -o toc.json

# a single doc node
curl.exe -s -H 'Accept: application/json' `
 'https://stoplight.io/api/v1/projects/cHJqOjM2MzI5/nodes/<slug>?branch=master'

# the OpenAPI specs (v2 project 5606820 / v3 project 1593468 for mocks)
curl.exe -s 'https://stoplight.io/api/v1/projects/thirdfort/api/nodes/reference/api.v2.yaml?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle'
curl.exe -s 'https://stoplight.io/api/v1/projects/thirdfort/api/nodes/reference/api.v3.yaml?fromExportButton=true&snapshotType=http_service&deref=optimizedBundle'
```

Project id for the docs is `cHJqOjM2MzI5` (base64 of `prj:36329`), workspace `thirdfort`, project slug `api`; the numeric ids in the mock URLs (5606820 v2, 1593468 v3) are mock-server ids, not project ids.
