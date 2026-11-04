# Address

Status: Browser and API proof of concept. Live Loqate transport has not been verified
as part of this migration.

Repo: [C:\Source\Repos\poc-address](C:/Source/Repos/poc-address)

This project folder contains Address research and product notes. The runnable app and
its as-built implementation documentation are maintained in the standalone repository.

## Documentation

- [[Poc-Design|POC application design]]
- [[Loqate-api|Loqate API integration]]
- [[UPU-S42|UPU S42 addressing standard]]
- [[ISO-20022|ISO 20022 address schema]]
- [[UK-Address-Format|UK address format]]

# International Addressing Standards — Overview

Comparison of UPU S42 and ISO 20022 for global address management. Source: `outputs/international-addressing.html` (Overview tab).

## Two Standards, Two Purposes

### UPU S42 — Postal Addressing

- **Scope:** Global postal addressing standard
- **Focus:** Logical structure of postal addresses for mail delivery
- **Application:** Postal operations and cross-border mail
- **Flexibility:** Adaptable by any country

### ISO 20022 — Financial Messaging

- **Scope:** Financial transaction data format
- **Focus:** Structured data for financial transactions
- **Application:** Banking, payments, regulatory compliance
- **Coverage:** Only 32 countries

## Key Differences

| Aspect | UPU S42 | ISO 20022 |
|--------|---------|-----------|
| Type | Postal addressing standard | Financial messaging standard |
| Structure | Generic elements + country templates | Highly structured XML tags |
| Adaptability | Flexible, country-specific | Rigid, fixed format |
| Best For | Web applications, mail delivery | Financial operations, compliance |

## Recommendation

UPU S42 is the better choice for most address management scenarios due to its flexibility and wider country coverage. See [[UPU-S42]] and [[ISO-20022]].

## Application

The [app README](C:/Source/Repos/poc-address/README.md) is the setup and validation
contract. Addressing standards and discovery notes remain in this folder; the
implementation truth lives in the app repository.

Last updated: 2026-11-03.