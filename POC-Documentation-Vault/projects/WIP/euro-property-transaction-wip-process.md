# European Property Transaction WIP Process

Status: draft; source specifications contain unresolved conflicts.  
Scope: process, lifecycle states, controls, and recorded country variations for fee-earning
property transaction work. Entity, client, individual, and organization-specific details
are intentionally omitted.

## What WIP means here

In this process, Work in Progress (WIP) is the financial record of authorized,
fee-earning transaction work that has not yet been invoiced and collected. It is not a
general task or staff-capacity tracker.

The process follows an authorized instruction from signing, through fee accrual and
monthly reporting, to billing and payment or loss. The CRM deal stages describe
transaction progress; the WIP record has its own finance lifecycle. They are related,
but are not interchangeable.

## Process at a glance

```text
Instruction authorized and signed
    → Create WIP record
    → Update fee, probability, expected completion, and reporting month
    → Reconcile at month end
    → Lock the reporting period on the 15th of the following month
    → Invoice issued: Billed
    → Payment received: Paid

Work abandoned or instruction withdrawn
    → Lost
```

Recurring fee arrangements may create a WIP line for each reporting period.

## Transaction progress and WIP status

The source material describes an eight-stage deal process, broadly progressing from
origination and pitch through mandate, marketing, bidding, due diligence, exchange, and
completion. A later architecture view maps deal-stage progress to a percentage used in
WIP calculations. That mapping is not fully specified and is a future-state integration
requirement; deal stage alone does not move a WIP record to Billed or Paid.

The stage names differ between source documents. One lists separate Pitch and Mandate
stages and uses Exchange; another combines Pitch and Mandate earlier, calls a later
stage Exclusivity, and labels the instruction stage differently. Reconcile the canonical
stage list and the stage-to-percentage mapping before automating stage gates or accruals.

## WIP finance lifecycle

| State | Meaning and entry event | Required information or rule | Next states |
|---|---|---|---|
| **WIP** | Authorized work is tracked before invoicing. Create the WIP record only after the parent instruction exists and is active and signed. | Reporting month is required and is stored as the first day of that month. Record fee values, probability from 0–100%, expected completion month, and applicable tax rate/currency. | Billed or Lost |
| **Billed** | An invoice has been issued. | Invoice number, invoice due date, and finance-system cross-reference are specified as required. Keep the invoice number once set. A probability below 30% at billing triggers a finance review alert; it does not, by itself, prohibit billing in the documented rule. | Paid or Lost |
| **Paid** | Payment has been received in full. | Record the date paid in full. Invoice number remains required. | Terminal |
| **Lost** | Work is abandoned, the parent instruction is withdrawn/lost, or an invoice is cancelled after billing. | No invoice fields are required for Lost. A parent loss/withdrawal is specified to cascade to related WIP lines. | Terminal |

The intended transitions are `WIP → Billed → Paid`, with `Lost` reachable from WIP
or Billed. The source does not define a transition from Paid to Lost.

### Entry and creation rules

- The parent instruction must exist before its WIP record; the WIP record inherits its
  transaction classification, owning office, currency, and other reporting context.
- WIP entry is described as requiring an active, signed instruction. The source labels
  this gate as inferred, not a fully confirmed rule.
- Warn on a possible duplicate with the same parent instruction, expected completion
  month, and WIP status.
- A recurring monthly or quarterly fee trigger may produce a separate WIP line for each
  period.

### Accrual and probability rules

- Review and update WIP monthly. The owner is expected to update probability and the
  current fee forecast.
- Weighted office-retained pipeline is calculated as:
  `office-retained fee × probability / 100`.
- Probability is editable while the record is WIP and is locked after it leaves WIP.
- Capture the previous probability on change. If a record is billed from below 30%,
  flag it for finance review.
- Warn about mixed or unexpected currencies. Do not sum unlike currencies as if they
  were one amount; reporting must account for currency conversion or separate currency
  totals.

### Billing and loss rules

- At Billed, require the invoice number, invoice due date, and finance-system reference
  as specified by the source.
- At Paid, require the paid-in-full date and retain the invoice number.
- A WIP record may be marked Lost when work is abandoned. Parent instruction loss or
  withdrawal is intended to mark its child WIP records Lost.
- The source calls for finance review when a line is billed below 30% probability; it
  does not specify whether this review blocks the transition.

## Monthly controls and aging

Each WIP record belongs to a reporting month represented by the first day of that
month. This replaces month-by-month spreadsheet tabs and allows historical periods to
be reported consistently.

- **Month end:** reconcile WIP and receivables and refresh aging reports.
- **Monthly:** remind owners to review and update their WIP records.
- **Stale detection:** a WIP line becomes stale when it remains in WIP after its
  expected completion month plus 30 days.
- **Weekly:** alert the finance operations owner about stale lines, for re-forecasting
  or close-out.
- **Period lock:** lock a reporting month on the 15th of the following month and record
  who locked it and when.
- **Enforcement:** reject writes to fields covered by the lock, including writes through
  APIs or automated flows, not just edits through a user interface.

The precise set of locked fields, the authority and audit procedure for unlocking, and
the handling of a stale record inside a locked period are not specified. These controls
must be agreed before implementation. As written, a stale line may need its forecast or
status updated after the reporting period has already locked.

## Recorded country differences

The supplied design material explicitly records these defaults:

| Country of owning office | VAT default | Recorded distinction |
|---|---:|---|
| France | 20% | Initial market in the rollout sequence |
| Spain | 21% | Added in a subsequent rollout phase |
| United Kingdom | 20% | VAT default is listed; rollout timing is not specified |

The VAT default follows the **owning office**, not the client's location. A cross-border
client therefore does not, on its own, change the default rate. These are the defaults
in the supplied design material, not confirmation of current statutory tax treatment;
Finance and tax owners must validate applicable rates and exceptions before use.

Other recorded variations are operational rather than confirmed country-specific
business rules:

- Currency is inherited from the parent instruction. The source identifies at least
  EUR and GBP in the reporting environment and warns that mixed-currency totals need
  careful treatment.
- Local finance-system routing is selected from the owning office. Country/office
  rollout and ledger integration differ, while consolidated finance integration is
  described as a later phase.
- The documented rollout starts in France, then adds Spain and a further regional
  scope. The United Kingdom's rollout phase is not stated.
- No additional country-specific lifecycle states, invoice requirements, aging
  thresholds, or transition rules were identified in the supplied notes.
- Rules for countries beyond France, Spain, and the United Kingdom are not specified;
  do not infer them from these defaults.

## Open decisions and source conflicts

The source material is a draft and should not be treated as a final operating policy.
Resolve these items with Finance, the process owner, and the relevant country teams:

1. **Canonical transaction stages:** reconcile stage labels and ordering across the
   source materials; confirm whether transaction-stage progress drives any WIP
   calculation and define the mapping.
2. **WIP entry gate:** confirm whether active status plus a signed date is mandatory
   before a WIP record can be created.
3. **Billing reference field:** the newer core table definition does not include the
   finance-system reference on the WIP record, while the billing rules require it at
   Billed. Decide where it is stored.
4. **Period-lock field set:** specify exactly which financial, status, and invoice
   fields become immutable and who may authorize an unlock.
5. **Stale/locked interaction:** define how teams can re-forecast or close out stale
   records after their period locks.
6. **Parent-loss terminology:** define which parent states trigger the Lost cascade
   and confirm consistent handling of withdrawal, completion, and abandonment.
7. **Low-probability billing:** confirm whether a review alert is informational or a
   hard stop.
8. **Country and currency controls:** validate VAT defaults, exceptions, currency
   conversion/reporting, local-system routing, and the United Kingdom rollout.
9. **Recurring fees and calculations:** confirm how monthly or quarterly fee lines are
   generated and how gross fee and foreign-currency totals are derived.

## Source basis

This summary is based on the supplied European WIP workflow, lifecycle, table,
automation, finance-integration, period-locking, rollout, and open-question notes. It
omits organization, entity, client, person, CRM schema, and system-instance details.
Where the source says a requirement is inferred, contradictory, or unresolved, this
document preserves that uncertainty rather than presenting it as agreed policy.
