"""
Copyright 2024 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from datetime import datetime, timezone
from typing import Any

from openpyxl.cell import Cell

from parkapi_sources.converters.base_converter.push import NormalizedXlsxConverter
from parkapi_sources.models import SourceInfo
from parkapi_sources.models.enums import ParkingSiteType, PurposeType, SupervisionType


class DummyBikePushConverter(NormalizedXlsxConverter):
    source_info = SourceInfo(
        uid='dummy_bike',
        name='Dummy Abstellenanlage',
        public_url='https://www.dummy-bike.de',
        has_realtime_data=False,
    )

    purpose_mapping: dict[str, PurposeType] = {
        'Fahrradparken': 'BIKE',
        'Schließfach': 'ITEM',
    }

    supervision_type_mapping: dict[str, SupervisionType] = {
        'Ja': 'YES',
        'Nein': 'NO',
        'Video': 'VIDEO',
        'Bewacht': 'ATTENDED',
    }

    type_mapping: dict[str, ParkingSiteType] = {
        'Fahrradparken allgemein': 'GENERIC_BIKE',
        'Vorderradhalter': 'WALL_LOOPS',
        'Vorderradhalter mit Sicherung': 'SAFE_WALL_LOOPS',
        'Anlehnbügel': 'STANDS',
        'Schließfächer': 'LOCKERS',
        'Zweistock-Abstellanlage': 'TWO_TIER',
        'Parkhaus': 'CAR_PARK',
        'Parkdeck': 'BUILDING',
        'andere': 'OTHER',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # For some reason, Dummy Bike decided to change the titles
        dummy_bike_header_rows: dict[str, str] = {
            'Einfahrtshöhe': 'max_height',
            'Zweck der Anlage': 'purpose',
            'Überdacht?': 'is_covered',
            'Überwacht?': 'supervision_type',
            'Ortsbezug': 'related_location',
            'Webseite Fotos': 'photo_url',
            'Gebührenpflichtig?': 'has_fee',
            'Existieren Echtzeit-Daten?': 'has_realtime_data',
        }

        dummy_bike_remove_header_rows: dict[str, str] = {
            'Anzahl Carsharing-Parkplätze': 'capacity_carsharing',
            'Anzahl Frauenparkplätze': 'capacity_woman',
            'Anzahl Behindertenparkplätze': 'capacity_disabled',
        }

        self.header_row = {
            **{
                key: value
                for key, value in super().header_row.items()
                if value not in dummy_bike_header_rows.values() and value not in dummy_bike_remove_header_rows.values()
            },
            **dummy_bike_header_rows,
        }

    def map_row_to_parking_site_dict(self, mapping: dict[str, int], row: list[Cell]) -> dict[str, Any]:
        parking_site_dict: dict[str, str] = {}

        for field in mapping.keys():
            parking_site_dict[field] = row[mapping[field]].value

        parking_site_dict['purpose'] = self.purpose_mapping.get(parking_site_dict.get('purpose'))
        parking_site_dict['type'] = self.type_mapping.get(parking_site_dict.get('type'))
        parking_site_dict['supervision_type'] = self.supervision_type_mapping.get(parking_site_dict.get('supervision_type'))
        parking_site_dict['static_data_updated_at'] = datetime.now(tz=timezone.utc).isoformat()

        return parking_site_dict
