# Contipark

Contipark provides a JSON REST API (`/v1/carparks`) with static parking site data across Germany. Access
requires a certificate (`PARK_API_CONTIPARK_CERT_PATH`). The response contains a `data` list, where
each entry is one parking site. The API models only static data.

Static values:

* `has_realtime_data` is always `False` (the API does not offer realtime data yet)

## Properties

| Field                         | Type                                | Cardinality | Mapping                | Comment |
|-------------------------------|-------------------------------------|-------------|------------------------|---------|
| id["value"]                   | string                              | 1           | uid                    |         |
| type["value"]                 | [ParkingSiteType](#ParkingSiteType) | 1           | type                   |         |
| namePublicDE["value"]         | string                              | 1           | name                   |         |
| namePublicEN["value"]         | string                              | 1           |                        |         |
| gates                         | list                                |             |                        |         |
| dimensions["height"]["value"] | Number                              | 1           | max_height             |         |
| dimensions["width"]["value"]  | NUmber                              | 1           | max_width              |         |
| operations                    |                                     |             |                        |         |
| station                       |                                     |             |                        |         |
| bahnPark                      |                                     |             |                        |         |
| openingHours                  |                                     |             |                        |         |
| parkingSpots                  |                                     |             |                        |         |
| chargingStations              |                                     |             |                        |         |
| tags                          |                                     |             |                        |         |
| consumerManagement            |                                     |             |                        |         |
| static_data_updated_at        | str(date-time)                      | 1           | static_data_updated_at |         |




### ParkingSiteType

| Key | Mapping: type             |
|-----|---------------------------|
| PD  | CAR_PARK                  |
| PH  | CAR_PARK                  |
| PP  | OFF_STREET_PARKING_GROUND |
| TG  | UNDERGROUND               |

