# LOQATE API Integration

Reference implementation for address verification. Source: `outputs/international-addressing.html` (LOQATE API tab).

## Find API (Interactive Search)

```
GET https://api.addressy.com/Capture/Interactive/Find/v1.20/json6.ws
    ?Key=YOUR_API_KEY
    &Text=tf26rf
    &Countries=GB
    &Limit=100
```
### Request 

```
curl --request GET \
  --url 'https://api.addressy.com/Capture/Interactive/Find/v1.20/json6.ws?Key=API-KEY&Text=tf26rf'
```
### Response 

```json
{
	"Items":[
		{
			"Id":"gb-rm|ZWsIBaEBbtdL8wmKn2Iy",
			"Type":"Postcode",
			"Text":"TF2 6RF",
			"Highlight":"0-3,4-7",
			"Description":"Telford - 54 Addresses"
		}
	]
}
```


### Subsequent Request

feed id from previous response into the Container request parameter 

```
curl --request GET \
  --url 'https://api.addressy.com/Capture/Interactive/Find/v1.20/json6.ws?Key=API-KEY&Text=tf26rf&Container=gb-rm%7CZWsIBaEBbtdL8wmKn2Iy'
```

### Response

```json
{
	"Items":[
		{
			"Id":"GB|RM|B|24490745|ENG",
			"Type":"Address",
			"Text":"41 Teagues Crescent",
			"Highlight":"",
			"Description":"Trench Telford TF2 6RF"
		},
		{
			"Id":"GB|RM|B|24490746|ENG",
			"Type":"Address",
			"Text":"41A Teagues Crescent",
			"Highlight":"",
			"Description":"Trench Telford TF2 6RF"
			},
			...
		}
	]
}
```
## Recursive Find Flow

Search: `"tf26rf"` → Postcode Container → `Container: gb-rm|xxx` → 54 Addresses



## Verify API Request (Detail API)

Endpoint used by the app: `POST https://api.addressy.com/Cleansing/International/Batch/v1.20/json6.ws`

```
curl --request POST \
  --url https://api.addressy.com/Cleansing/International/Batch/v1.10/json6.ws \
  --header 'Content-Type: application/json' \
  --data '{
  "Key": "...",
  "GeoCode": true,
  "Options": {
    "Process": "Verify",
    "Enhance": false
  },
  "Addresses": [
    {
      "Department": "",
      "PostalCode": "EC2M 7NH",
      "Country": "United Kingdom",
      "Address": "1 Liverpool Street"
    }
  ],
  "Options": {
    "Process": "Verify",
    "Enhance": false,
    "ServerOptions": {
      "OutputAddressFormat": "YES"
    }
  }
}
```

### Response

```json
{
    "AQI": "A",
    "AVC": "V44-I44-P6-100",
    "Address": "1 Liverpool Street<br>London<br>EC2M 7NH",
    "Address1": "1 Liverpool Street",
    "Address2": "London",
    "Address3": "EC2M 7NH",
    "AddressFormat": "Premise Thoroughfare<br>Locality<br>PostalCode",
    "AdministrativeArea": "London",
    "Country": "GB",
    "CountryName": "United Kingdom",
    "DeliveryAddress": "1 Liverpool Street",
    "DeliveryAddress1": "1 Liverpool Street",
    "DeliveryAddressFormat": "Premise Thoroughfare",
    "GeoAccuracy": "I4",
    "GeoDistance": "0.0",
    "HyphenClass": "B",
    "ID": "GB|RM|B|52840932|ENG",
    "ISO3166-2": "GB",
    "ISO3166-3": "GBR",
    "ISO3166-N": "826",
    "Latitude": "51.517670",
    "Locality": "London",
    "Longitude": "-0.084339",
    "MatchRuleLabel": "Rlh",
    "PostalCode": "EC2M 7NH",
    "PostalCodePrimary": "EC2M 7NH",
    "Premise": "1",
    "PremiseNumber": "1",
    "Sequence": "1",
    "Thoroughfare": "Liverpool Street"
  }
```


