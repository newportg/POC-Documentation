# UK Address Format

As described by UPU S42 — uses 9 of 15 elements. Source: `outputs/international-addressing.html` (UK Format tab).

## Address Lines

| # | Field | Example |
|---|-------|---------|
| 1 | Organization | "Acme Corp" |
| 2 | Department | "Marketing" |
| 3 | PostBox | "PO Box 123" |
| 4 | SubBuilding Building | "Unit 5, High Street" |
| 5 | Premise Thoroughfare | "93 Teagues Crescent" |
| 6 | DoubleDependentLocality | "Trench" |
| 7 | DependentLocality | "Telford" |
| 8 | Locality | "Telford" |
| 9 | PostalCode | "TF2 6RF" |

## Example: 93 Teagues Crescent

```json
{
  "Address": "93 Teagues Crescent<br>Trench<br>Telford<br>TF2 6RF",
  "Address1": "93 Teagues Crescent",
  "Address2": "Trench",
  "Address3": "Telford",
  "Address4": "TF2 6RF",
  "DeliveryAddress": "93 Teagues Crescent<br>Trench",
  "DeliveryAddress1": "93 Teagues Crescent",
  "DeliveryAddress2": "Trench",
  "AdministrativeArea": "Shropshire",
  "Locality": "Telford",
  "DependentLocality": "Trench",
  "Thoroughfare": "Teagues Crescent",
  "Premise": "93",
  "PostalCode": "TF2 6RF",
  "CountryName": "United Kingdom",
  "ISO3166-2": "GB",
  "ISO3166-3": "GBR",
  "ISO3166-N": "826",
  "PostalCodePrimary": "TF2 6RF",
  "AVC": "V44-I44-P6-100",
  "AQI": "A",
  "Sequence": "1",
  "MatchRuleLabel": "Rlfnp",
  "HyphenClass": "B",
  "PremiseNumber": "93",
  "Country": "GB"
}
```

Related: [[UPU-S42]], [[Loqate-api]].
