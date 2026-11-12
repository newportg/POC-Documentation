# Instruction types and information requirements

This reference consolidates the previous Instruction wiki with the current
`poc_Instruction` product requirements. It distinguishes the shared record type
from the service line that supplies the specialised work record.

## Two classifications

### Shared record type

Every `poc_Instruction` has exactly one value for `poc_instructiontype`:

| Record type | Meaning | Typical service lines |
|---|---|---|
| **Mandate** | An ongoing or recurring appointment to act. | Capital Advisory, Property Management, Investor Advisory |
| **Engagement** | A scoped professional-services engagement. | OSS, Development, Building Consultancy, Workplace, ESG |
| **Instruction** | A directive to act on a defined matter or transaction. | Capital Markets, Valuations, Leasing, Residential Sales, Residential Lettings |

These are finance-layer classifications. They are not the same as the
service-line process stage called “Instruction”.

### Service-line type

Each record must populate exactly one service-line parent lookup, selected by
`poc_serviceline`. The parent lookup must agree with the selected service line.

| Service line | Parent record | Shared type | What it covers |
|---|---|---|---|
| Capital Markets | `poc_Deal` | Instruction | Investment acquisitions, disposals, capital raising, and transactions |
| OSS | `poc_Engagement` | Engagement | Corporate occupier advisory, workplace strategy, location search, and lease negotiation |
| Valuations | `poc_ValuationInstruction` | Instruction | RICS-regulated valuations |
| Leasing | `poc_Lease` | Instruction | Commercial landlord and tenant representation |
| Residential Sales | `poc_SalesInstruction` | Instruction | Marketing and selling a residential property |
| Residential Lettings | `poc_LettingsInstruction` | Instruction | Letting a residential property, with optional management |
| Property Management | `poc_PropertyMandate` | Mandate | Lease administration, service charges, maintenance, rent collection |
| Capital Advisory | `poc_DebtMandate` | Mandate | Debt and structured finance |
| Investor Advisory | `poc_InvestorMandate` | Mandate | Investment strategy, sourcing, and portfolio reporting |
| Development | `poc_DevelopmentProject` | Engagement | Feasibility, planning strategy, and development management |
| Building Consultancy | `poc_BuildingSurvey` | Engagement | Surveys, dilapidations, monitoring, and technical due diligence |
| Workplace Consulting | `poc_WorkplaceAssessment` | Engagement | Space utilisation, design, and change management |
| ESG Consultancy | `poc_ESGAssessment` | Engagement | Energy audits, CRREM analysis, net-zero pathways, and certification |

The source material says “twelve service lines” but lists thirteen parent
lookups. Residential Lettings also lacks a fully defined target table in one
source. This mapping must be approved before implementation.

## Common information required for every Instruction

The following fields belong on the shared `poc_Instruction` record unless the
approved schema says otherwise:

- Stable identifier: `poc_instructionid`.
- Generated reference: `poc_name`, proposed format `INS-{SEQNUM:6}`.
- Shared record type: `poc_instructiontype`.
- Service line: `poc_serviceline`.
- Exactly one matching service-line parent lookup.
- Brand/Group client account: `poc_clientaccountid`.
- Owning office/business unit: `poc_owningoffice`.
- Start date: `poc_startdate`.
- Status: Active, Completed, On Hold, or Withdrawn.
- Optional primary contact: `poc_primarycontactid`.
- Optional primary property: `poc_propertyid`.
- Legal Entity account for contracting and invoicing, when known:
  `poc_legalentityaccountid`.
- Optional signed date, end date, expected revenue, comments, and finance
  references.
- Termination reason when status is Withdrawn.
- Creation/update timestamps and attributable change history.

The client account identifies the relationship owner. It must not be confused
with the Legal Entity account used for the fee letter or invoice.

## Type-specific information requirements

### Capital Markets — `poc_Deal`

Required or expected information:

- Deal or transaction reference and the linked `poc_Deal`.
- Brand/Group client and contracting Legal Entity.
- Transaction type: acquisition, disposal, capital raising, or other approved
  transaction classification.
- Owning office, service line, start date, status, and expected revenue.
- Primary property or portfolio association where applicable.
- Transaction parties, jurisdictions, and cross-border context.
- Mandate or signed date when the approved Capital Markets gate requires it.
- KYC, conflict, and intercompany billing evidence as process controls.

The Capital Markets process uses Instruction as stage S3 after Origination and
Pitch/Mandate. The stage and compliance gates are not substitutes for the
shared Instruction fields.

### OSS — `poc_Engagement`

Required or expected information:

- Engagement reference and linked `poc_Engagement`.
- Brand/Group client and Legal Entity.
- Occupier or workplace advisory scope.
- Relevant properties, locations, lease events, or search criteria.
- Responsible office, lead adviser, start date, status, and commercial terms.
- Expected revenue and any agreed milestones or deliverables.

### Valuations — `poc_ValuationInstruction`

Required information:

- Instructing Account: `poc_accountid`.
- Optional or required contact and property, according to the valuation case.
- Valuation purpose: Secured Lending, Fund Reporting, Acquisition, Disposal,
  Insurance, Tax, or Financial Statements.
- Valuation basis: Market Value, Market Rent, Fair Value, DRC, or
  Reinstatement.
- Instruction date: `poc_instructiondate`.
- Report due date: `poc_reportduedate`.
- Assigned valuer: `poc_valuer`.
- Required conflict-checked flag: `poc_conflictchecked`.

Typically also required or captured:

- Inspection date and report-issued date.
- Reviewer and fee.
- Market value, market rent, yield applied, and special assumptions.
- Status and process stage from Received through Issued.

### Leasing — `poc_Lease`

Required or expected information:

- Linked lease record and client/Legal Entity.
- Landlord or tenant role and the relevant property.
- Representation type and lease objective.
- Lease term, rent, key dates, and renewal or break events where applicable.
- Responsible handler, office, start date, status, scope, and fee terms.

The source material does not define a complete `poc_Lease` field list in the
previous wiki. The lease-specific contract requires confirmation.

### Residential Sales — `poc_SalesInstruction`

Required information:

- Vendor account: `poc_vendoraccountid`.
- Vendor contact: `poc_vendorcontactid`.
- Residential property: `poc_respropertyid`.
- Sales variant: Sole Agency, Joint Sole Agency, Multi Agency, Private Treaty,
  Auction, or Tender.
- Instruction date: `poc_instructiondate`.
- Asking price: `poc_askingprice`.
- Commission percentage: `poc_commissionpercent`.
- Negotiator: `poc_negotiator`.
- Office: `poc_officebu`.

Also capture when applicable:

- Instruction expiry, guide-price range, achieved price, and minimum
  commission.
- Marketing launch, under-offer, exchange, and completion dates.
- Instruction stage and status, including Fallen Through where supported.
- Viewing and offer counts.

### Residential Lettings — `poc_LettingsInstruction`

Required information:

- Landlord account: `poc_landlordaccountid`.
- Landlord contact: `poc_landlordcontactid`.
- Residential property: `poc_respropertyid`.
- Lettings variant: Sole Agency, Joint, Multi, Let Only, Let & Manage, or Full
  Management.
- Instruction date: `poc_instructiondate`.
- Weekly rent: `poc_weeklyrent`.
- Commission percentage: `poc_commissionpercent`.
- Negotiator: `poc_negotiator`.

Also capture when applicable:

- Instruction expiry, monthly/annual calculated rent, and management fee
  percentage for managed variants.
- Minimum tenancy term and furnishing.
- Marketing launch, let-agreed, and tenancy-start dates.
- Tenant after let-agreed, status, stage, and notes.

### Property Management — `poc_PropertyMandate`

Required or expected information:

- Linked property-management mandate.
- Client/Brand account and Legal Entity.
- Property or portfolio covered by the mandate.
- Scope: lease administration, service charges, maintenance, rent collection,
  or other approved services.
- Management term, start date, responsible office, handler, status, and fee
  basis.
- Property portfolio links through `poc_DealProperty` where more than one
  property is covered.

### Capital Advisory — `poc_DebtMandate`

Required or expected information:

- Linked debt mandate.
- Borrower/client and Legal Entity.
- Lender or financing counterparty.
- Loan amount, debt product, funding purpose, and financing conditions.
- Relevant property or development, jurisdictions, and transaction dates.
- Responsible office, adviser, start date, status, scope, and fee terms.

### Investor Advisory — `poc_InvestorMandate`

Required or expected information:

- Linked investor mandate.
- Institutional investor/client and Legal Entity.
- Investment strategy, mandate scope, geography, and asset class.
- Portfolio or property associations.
- Sourcing, reporting, or portfolio-management deliverables.
- Responsible office, adviser, start date, status, and fee terms.

### Development — `poc_DevelopmentProject`

Required or expected information:

- Linked development project.
- Client/developer and Legal Entity.
- Development site or property portfolio.
- Feasibility, planning, development-management, or delivery scope.
- Programme milestones, planning status, responsible office, start date,
  status, and commercial terms.

### Building Consultancy — `poc_BuildingSurvey`

Required or expected information:

- Linked building survey or consultancy record.
- Client/Legal Entity and subject property.
- Survey, dilapidations, project-monitoring, or technical due-diligence scope.
- Inspection requirements, deliverables, report deadline, and assumptions.
- Assigned surveyor, reviewer where required, office, start date, status, and
  fee.

### Workplace Consulting — `poc_WorkplaceAssessment`

Required or expected information:

- Linked workplace assessment.
- Client/Legal Entity and relevant sites.
- Scope such as utilisation, workplace design, location strategy, or change
  management.
- Required outputs, milestones, responsible adviser, office, start date,
  status, and fee terms.

### ESG Consultancy — `poc_ESGAssessment`

Required or expected information:

- Linked ESG assessment.
- Client/Legal Entity and relevant property or portfolio.
- Scope such as energy audit, CRREM analysis, net-zero pathway, or
  certification.
- Assets, reporting boundary, target dates, assumptions, responsible
  consultant, office, status, and fee terms.

## Cross-cutting information

An Instruction may cover multiple properties. Store one optional primary
property on `poc_propertyid`, and use the `poc_DealProperty` junction for the
complete portfolio and its history.

WIP records reference `poc_WIP.poc_instructionid`. WIP must obtain service-line
context through the Instruction rather than carrying separate service-line
parent lookups.

Instruction status, process stage, KYC/AML, conflict checks, authority to act,
and audit history are control information in addition to the matter payload.
They must not be omitted merely because the specialised service-line table
contains the commercial details.

## Source and unresolved decisions

This reference is based on the previous Instruction wiki and the current
Instruction PRD. Before implementation, confirm:

1. The authoritative list and count of service lines and parent lookups.
2. Whether Mandate, Engagement, and Instruction are mutually exclusive
   business types or labels with different lifecycle rules.
3. The final field list where the Core and older CRM definitions conflict.
4. The timing of Legal Entity, signed-date, Active-status, and WIP-entry
   requirements.
5. Status transitions, withdrawal cascades, and historical snapshot rules.
