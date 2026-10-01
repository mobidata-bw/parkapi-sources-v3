# Contipark

Contipark provides a JSON REST API (`/v1/carparks`) with static parking site data across Germany. Access
requires a certificate (`PARK_API_CONTIPARK_CERT_PATH`). The response contains a `data` list, where
each entry is one parking site. The API models only static data.

Ignored entries:



Static values:

* `has_realtime_data` is always `False` (the API does not offer realtime data yet)

| Field                  | Type            | Cardinality | Mapping | Comment |
|------------------------|-----------------|-------------|---------|---------|
| id["value"]            | string          | 1           | uid     |         |
| type["value"]          | ParkingSiteType | 1           | type    |         |
| namePublicDE["value"]  | string          | 1           | name    |         |
| namePublicEN["value"]  | string          | 1           |         |         |
| gates                  |                 | ?           |         |         |
| operations             |                 | 1           |         |         |
| station                |                 | 1           |         |         |
| bahnPark               |                 | +           |         |         |
| openingHours           |                 | +           |         |         |
| parkingSpots           |                 | *           |         |         |
| chargingStations       |                 | 1           |         |         |
| tags                   |                 | ?           |         |         |
| consumerManagement     |                 |             |         |         |
| static_data_updated_at |                 |             |         |         |

