---
type: prd
area: instruction
status: draft
source: POC-EuroWIP-Vault/wiki/wip-instruction-model.md and related WIP specifications
created: 2026-11-05
---

# Instruction — Product Requirements Document

## Summary

Instruction is the shared finance-layer record for a mandate, engagement, or
instruction. It represents the authorised business engagement between a client
relationship and the legal entity that is party to the contract. It provides the
common parent for WIP and billing records across service lines.

The Instruction connects to exactly one service-line record, selected by its
service line. WIP records reference the Instruction rather than carrying their own
service-line-specific parent lookups. The model therefore gives Finance a consistent
parent while retaining service-line context in CRM.

This PRD uses the Core Shared Tables definition of `kf_Instruction` as the working
baseline. The source material identifies it as authoritative, but also records
unresolved conflicts that must be decided before implementation.

## Problem

Finance needs a consistent record for the signed or otherwise authorised work that
underlies WIP, billing, and revenue reporting. If each service line creates its own
finance parent, WIP must understand each CRM table and reporting becomes fragmented.
If the parent record does not distinguish the relationship-owning client from the
contracting invoice entity, relationship reporting and billing can use the wrong
organization.

The source model defines `kf_Instruction`, but its field set and automation
requirements conflict with older definitions. This PRD turns the current Core model
into product requirements while preserving those conflicts for approval.

## Goals

- Provide one stable finance parent for each service-line engagement.
- Support Mandate, Engagement, and Instruction record types.
- Identify both the Brand/Group relationship owner and the contracting Legal Entity.
- Link the record to the correct service-line parent and enforce the single-parent
  rule.
- Capture dates, ownership, status, and finance references needed to create and
  manage WIP.
- Preserve auditable history and distinguish source CRM facts from finance-process
  data.
- Support portfolio work without limiting an Instruction to one property.

## Non-goals

- Replacing service-line CRM records, their business-process flows, or deal lifecycle.
- Tracking monthly WIP values, invoices, payments, probability, or period locks;
  those belong to `kf_WIP`.
- Defining the full Account, Contact, Property, or service-line data models.
- Performing KYC, AML screening, client verification, or compliance decisions.
- Replacing the SharePoint WIP migration or Finance ERP integration plan.
- Deciding unresolved source conflicts without the relevant business and data owners.

## Users and responsibilities

| User or system | Need |
|---|---|
| Case handler / service-line user | Create and maintain an Instruction associated with the right client, legal entity, and service-line record. |
| Finance user | Use the Instruction as the parent for WIP and billing, with correct invoice entity and office context. |
| Relationship / reporting user | Attribute work to the Brand/Group client without confusing it with the invoice entity. |
| Integrating systems | Retrieve and update an Instruction using a stable identifier and an explicit schema. |
| Operations / administrator | Correct data, manage lifecycle status, and investigate changes through audit history. |

## Core concepts

| Concept | Meaning |
|---|---|
| **Instruction** | Shared finance-layer parent representing a mandate, engagement, or instruction. |
| **Instruction type** | Required classification: `Mandate`, `Engagement`, or `Instruction`. |
| **Client account** | Brand/Group account that owns the relationship and supports relationship reporting. |
| **Legal Entity account** | Contracting entity shown on the fee letter and invoice. |
| **Service-line parent** | The CRM record for the service line associated with this Instruction. Exactly one is populated, as selected by service line. |
| **WIP** | Finance child record(s) attached to the Instruction; WIP details are specified separately. |
| **Instruction-property link** | Association between an Instruction and one or more properties, using the universal `kf_DealProperty` junction in the source model. |

## Users and primary journey

### Create and activate an Instruction

1. A user or authorized system creates an Instruction with a type, service line,
   Brand/Group client, owning office, and start date.
2. The system links the Instruction to the matching service-line parent and rejects
   a record with no parent, multiple parents, or a parent inconsistent with the
   selected service line.
3. The user selects a Legal Entity account when known. For a Mandate, the source says
   the Legal Entity must exist by the Capital Markets Mandate stage (S3).
4. The user records the signed date when the mandate is signed and sets the
   Instruction status to Active when work is authorized.
5. Once the source-defined WIP entry conditions are met, a WIP record can reference
   this Instruction. The exact universal gate remains to be confirmed.

### Update or close an Instruction

1. An authorized user updates the Instruction's dates, accounts, service-line link,
   finance references, or status.
2. The system validates conditional fields and records an auditable change.
3. If an Instruction is withdrawn, any impact on its WIP children is handled by the
   approved cascade rule; the detailed rule is unresolved in the source.
4. Historical WIP and process records remain interpretable after changes to the
   Instruction.

## Functional requirements

Priority: **Must** is required for the initial usable release; **Should** is
important but may follow; **Could** is a future enhancement.

### Identity and data

| ID | Priority | Requirement |
|---|---|---|
| INS-1 | Must | Every Instruction has a stable unique identifier (`kf_instructionid`) and a system-generated reference (`kf_name`, proposed format `INS-{SEQNUM:6}`). |
| INS-2 | Must | Every Instruction has exactly one required type: Mandate, Engagement, or Instruction. |
| INS-3 | Must | Every Instruction has a required service line, client account, owning office, status, and start date. |
| INS-4 | Must | `kf_clientaccountid` identifies the Brand/Group relationship owner and is not substituted for the legal invoice entity. |
| INS-5 | Must | `kf_legalentityaccountid`, when populated, must reference an Account classified as Legal Entity. For a Mandate it must be present by the applicable mandate/billing gate; the exact universal timing requires approval. |
| INS-6 | Must | The Instruction may reference a primary contact and a primary property. Neither is used as a substitute for the client account or service-line parent. |
| INS-7 | Must | The record supports optional signed and end dates, expected revenue, termination reason, comments, and finance cross-reference fields defined by the approved schema. |
| INS-8 | Must | A termination reason is required when the Instruction status is Withdrawn. |
| INS-9 | Must | The system records creation and update timestamps and retains an auditable history of authorized changes. |
| INS-10 | Should | Search and retrieval support the stable ID, generated reference, client, legal entity, service line, type, status, and available external finance references. |

### Service-line relationship

| ID | Priority | Requirement |
|---|---|---|
| INS-11 | Must | Exactly one service-line parent lookup is populated on each Instruction, and the populated lookup must agree with `kf_serviceline`. |
| INS-12 | Must | The service-line parent relationship is one-to-one from the service-line record's perspective. The Instruction is the shared finance parent; it does not replace the CRM parent. |
| INS-13 | Must | A service-line parent cannot be silently changed to a different service line. An authorized correction must preserve audit history and any WIP references. |
| INS-14 | Must | The initial schema and validation rules must use an approved list of service-line lookups and service-line values. The source lists 13 lookup targets while describing coverage as twelve service lines; this count and mapping must be reconciled before build. |
| INS-15 | Should | The model supports rollout of additional service lines by adding an approved parent relationship without adding service-line-specific parent fields to `kf_WIP`. |

The Core source lists these parent lookup targets: Deal, Engagement, Valuation
Instruction, Lease, Property Mandate, Development Project, Debt Mandate, Building
Survey, Workplace Assessment, Investor Mandate, Sales Instruction, Lettings
Instruction, and ESG Assessment. The source notes that Residential Lettings has no
target table defined, despite listing `kf_lettingsinstructionid`.

### Lifecycle and WIP relationship

| ID | Priority | Requirement |
|---|---|---|
| INS-16 | Must | The Instruction status supports Active, Completed, On Hold, and Withdrawn. Party/record status is distinct from legal standing of the client. |
| INS-17 | Must | WIP records reference the Instruction through `kf_WIP.kf_instructionid`; the Instruction can have many WIP records. |
| INS-18 | Must | WIP does not carry direct lookups to service-line CRM records. Service-line context is reached through the Instruction. |
| INS-19 | Must | Changes to an Instruction do not silently rewrite historical WIP snapshots or process evidence. |
| INS-20 | Should | An approved lifecycle rule defines whether Completed or Withdrawn Instructions can be edited, reactivated, or used to create additional WIP. |
| INS-21 | Should | If a parent Instruction is withdrawn, the system applies the approved and idempotent disposition to its WIP children and records the outcome. |

The requirement that WIP entry requires an Active Instruction and a populated
`kf_signeddate` is an inference in the source material, not an approved baseline
rule. It must not be enforced as a universal hard block until the business owner
confirms it.

### Properties and portfolio work

| ID | Priority | Requirement |
|---|---|---|
| INS-22 | Must | `kf_propertyid` supports an optional primary property reference. |
| INS-23 | Must | An Instruction that covers multiple properties can associate them through the universal `kf_DealProperty` junction; a single property lookup must not be treated as the complete portfolio. |
| INS-24 | Should | Property associations carry status and dates sufficient to preserve additions, removals, and historical context. |

### Security, privacy, and operations

| ID | Priority | Requirement |
|---|---|---|
| INS-25 | Must | Access to Instructions is scoped by the required owning office and follows approved role-based permissions. |
| INS-26 | Must | Legal entity, registration, and finance references are exposed only to authorized callers and retained only for approved business purposes. |
| INS-27 | Must | Create, update, status changes, and relationship corrections are attributable and auditable. |
| INS-28 | Should | Integration and automation failures are visible to support users and do not leave a success-shaped partial Instruction. |

## Data model baseline

The working Core Shared Tables schema includes:

- `kf_instructionid` — GUID primary key.
- `kf_name` — generated reference, `INS-{SEQNUM:6}`.
- `kf_instructiontype` — Mandate / Engagement / Instruction.
- `kf_serviceline` — global choice; selects the service-line parent lookup.
- `kf_clientaccountid` — required Brand/Group Account.
- `kf_legalentityaccountid` — Account filtered to Legal Entity.
- `kf_primarycontactid` — optional Contact.
- `kf_propertyid` — optional primary Property.
- `kf_owningoffice` — required Business Unit.
- `kf_instructionstatus` — Active / Completed / On Hold / Withdrawn.
- `kf_startdate` — required; `kf_signeddate` and `kf_enddate` optional in the table definition.
- `kf_expectedrevenue` — optional.
- `kf_terminationreason` — conditionally required for Withdrawn.
- `kf_comments` — optional multi-line text.
- `kf_fin_localsystemref`, `kf_fin_localsystemname`, and `kf_fin_projectid` — finance-system references.
- One service-line-specific parent lookup, as selected by service line.

The full field-level contract, option values, validation timing, and localization
rules require approval before API or Dataverse implementation.

## Integrations and dependencies

| Dependency | Instruction use |
|---|---|
| Account | Brand/Group client and filtered Legal Entity invoice account. |
| Contact | Optional primary contact. |
| Business Unit | Required owning office; supports security scope and downstream finance defaults. |
| Service-line CRM tables | Exactly one parent relationship selected by service line. Capital Markets is the initial live pipeline in the source rollout. |
| Property / `kf_DealProperty` | Optional primary property and multi-property portfolio association. |
| `kf_WIP` | One Instruction to many WIP records; WIP retrieves service-line context through Instruction. |
| Finance / ERP | Local system name, local system reference, and finance project ID are carried for current/manual or future integrated use. ERP automation is deferred to Phase 7 in the source rollout. |

## Scope and rollout

- **Foundation / Phase 0:** build the shared Instruction schema and its core Account,
  Business Unit, and property relationships, subject to confirmation of activation
  timing. The source marks Instruction as MVP but omits it from the explicit
  activation tables.
- **Phase 1:** support Paris Capital Markets and its Deal relationship; make the
  Instruction usable as the parent for WIP and support the SharePoint WIP cutover.
- **Later phases:** activate other service-line parent lookups as their CRM solutions
  and workflows become available.
- **Phase 7:** enable the consolidated Finance ERP integration. Until then, source
  material indicates that finance references may be maintained manually.

## Acceptance criteria

1. A user can create and retrieve an Instruction using its stable ID and generated
   reference.
2. Required fields, type/status values, Legal Entity filtering, and conditional
   termination reason are validated consistently through supported interfaces.
3. A saved Instruction has exactly one service-line parent matching its service line,
   using the approved relationship map.
4. Finance users can distinguish the Brand/Group relationship owner from the Legal
   Entity used for contracting and invoicing.
5. An Instruction can have multiple WIP children, and each WIP record reaches
   service-line context only through the Instruction.
6. Portfolio property associations can be represented without losing the primary
   property reference.
7. Authorized edits and lifecycle changes are auditable; previous process/WIP
   records remain interpretable.
8. The agreed MVP activation phase, WIP-entry gate, withdrawal cascade, and source
   schema are documented and approved before production release.

## Open decisions and source conflicts

These are decisions, not assumptions:

1. **Schema version:** The Core Shared Tables definition is treated as authoritative,
   but an older definition includes `kf_transactiontype`, `kf_sector`,
   `kf_negotiatorid`, and `kf_currency`, while the Core definition omits them.
   WIP's classification-population requirements rely on some of this context.
   Confirm the final Instruction fields and each WIP field's authoritative source.
2. **Parent mapping and count:** The source says twelve service lines but lists
   thirteen parent lookups. It also lists a Lettings lookup without a target table.
   Approve the actual service-line values, lookup targets, and rollout mapping.
3. **Status:** Confirm the Core statuses (Active / Completed / On Hold / Withdrawn)
   and their transitions, including whether reactivation is allowed.
4. **Mandate gates:** Confirm whether an Active status and signed date are hard
   requirements for WIP creation, and when the Legal Entity must be present outside
   the described Capital Markets S3 gate.
5. **Withdrawal cascade:** Confirm whether withdrawal sets all child WIP records to
   Lost, what happens to billed or paid records, and how the cascade is audited.
6. **Activation phase:** Instruction is marked MVP but omitted from the explicit
   Phase 0/1 activation table. Confirm the activation phase and update the programme
   list.
7. **Finance references:** Confirm the source of local system defaults, whether the
   local reference belongs on Instruction or WIP, and when `kf_fin_projectid` is
   populated.
8. **Historical data:** Decide whether full field-level history, attributed audit
   events, or process-specific snapshots are required for client, legal entity,
   parent, and property relationship changes.
9. **Concurrency and uniqueness:** Confirm whether a service-line parent can have
   only one Instruction and how duplicates are handled during migration and create.
10. **Term definitions:** Confirm whether Mandate / Engagement / Instruction are
    mutually exclusive business record types or labels that have different
    lifecycle and commercial requirements.

## Related

- [[README|Instruction project overview]]
- [[../WIP/README|WIP project]]
- [[../Party/company-model|Company Party — Domain Model]]
- Source: `POC-EuroWIP-Vault/wiki/wip-instruction-model.md`
- Source: `POC-EuroWIP-Vault/wiki/wip-mandate-components.md`
- Source: `POC-EuroWIP-Vault/wiki/wip-open-questions.md`
