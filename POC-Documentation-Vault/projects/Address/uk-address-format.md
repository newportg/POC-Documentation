# UK Address Format

The project's UPU S42 notes identify these address elements for a UK postal address:

| Element | Example |
|---|---|
| Organization | Acme Corp |
| Department | Marketing |
| Post box | PO Box 123 |
| Sub-building/building | Unit 5, High Street |
| Premise/thoroughfare | 93 Teagues Crescent |
| Double dependent locality | Trench |
| Dependent locality | Telford |
| Locality | Telford |
| Postal code | TF2 6RF |

## Example provider response

```json
{
  "Address": "93 Teagues Crescent<br>Trench<br>Telford<br>TF2 6RF",
  "Address1": "93 Teagues Crescent",
  "Address2": "Trench",
  "Address3": "Telford",
  "Address4": "TF2 6RF",
  "AdministrativeArea": "Shropshire",
  "Locality": "Telford",
  "DependentLocality": "Trench",
  "Thoroughfare": "Teagues Crescent",
  "Premise": "93",
  "PostalCode": "TF2 6RF",
  "CountryName": "United Kingdom",
  "Country": "GB"
}
```

Provider response fields and formatting rules can change. Treat this as an example,
not a canonical address schema.
