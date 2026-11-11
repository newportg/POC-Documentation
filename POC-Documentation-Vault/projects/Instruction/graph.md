---
type: prd
area: instruction
status: draft
source: 
created: 2026-11-09
---

```mermaid
flowchart TD
    Ad(Address)
    As(Asset)
    Cl(Client)
    Ty(Type)
    InsDet(Details)
    InsTer(Terms)

    Ad --> As
    Ad --> Cl
    As --> Cl
    Cl --> Ty
    Ty --> InsDet
    InsDet --> InsTer

```
