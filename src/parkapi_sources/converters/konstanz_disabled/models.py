"""
Copyright 2025 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from shapely import GeometryType, Point
from validataclass.dataclasses import validataclass
from validataclass.exceptions import ValidationError
from validataclass.validators import DataclassValidator, EnumValidator, IntegerValidator, StringValidator

from parkapi_sources.models import (
    GeojsonBaseFeatureInput,
    ParkingAudience,
    ParkingSpotRestrictionInput,
    PurposeType,
    StaticParkingSpotInput,
)
from parkapi_sources.models.enums import ParkingSiteOrientation, ParkingSpotType
from parkapi_sources.util import generate_point, round_7d
from parkapi_sources.validators import GeoJSONGeometryValidator


class InvalidKonstanzCountError(ValidationError):
    code = 'invalid_konstanz_count'


class KonstanzCountValidator(IntegerValidator):
    def validate(self, input_data: Any, **kwargs: Any) -> int:
        self._ensure_type(input_data, [str])

        input_data = input_data.split(' ')
        if len(input_data) != 2:
            raise InvalidKonstanzCountError()
        try:
            return int(input_data[0])
        except ValueError as e:
            raise InvalidKonstanzCountError() from e


class KonstanzDisabledParkingSpotTypeInput(Enum):
    OFF_STREET_PARKING_GROUND = 'OFF_STREET_PARKING_GROUND'
    ON_STREET = 'ON_STREET'

    def to_parking_site_type_input(self) -> ParkingSpotType:
        return {
            self.OFF_STREET_PARKING_GROUND: ParkingSpotType.OFF_STREET_PARKING_GROUND,
            self.ON_STREET: ParkingSpotType.CAR_PARK,
        }.get(self, ParkingSpotType.OTHER)

class Orientierung(Enum):
    PARALLEL = 'längs'
    PERPENDICULAR = 'quer'
    DIAGONAL = 'schräg'

    # TODO: Should be ParkingSpotTypeOrientation, but first check whether it works like this and whether the datamodel adaption should be implemented separately
    def to_parking_site_orientation_type(self) -> ParkingSiteOrientation:
        return {
            self.PARALLEL: ParkingSiteOrientation.PARALLEL,
            self.PERPENDICULAR: ParkingSiteOrientation.PERPENDICULAR,
            self.DIAGONAL: ParkingSiteOrientation.DIAGONAL,
        }.get(self)

@validataclass
class KonstanzDisabledPropertiesInput:
    OBJECTID: int = IntegerValidator()
    Name: str = StringValidator()
    adress: str = StringValidator()
    Stadtteil: str = StringValidator()
    type: KonstanzDisabledParkingSpotTypeInput = EnumValidator(KonstanzDisabledParkingSpotTypeInput)
    Anordnung: Orientierung = EnumValidator(Orientierung)
    description: str = StringValidator()
    GlobalID: str = StringValidator()


@validataclass
class KonstanzDisabledFeatureInput(GeojsonBaseFeatureInput):
    properties: KonstanzDisabledPropertiesInput = DataclassValidator(KonstanzDisabledPropertiesInput)
    geometry: Point = GeoJSONGeometryValidator(allowed_geometry_types=[GeometryType.POINT])

    def to_static_parking_spot_inputs(self) -> list[StaticParkingSpotInput]:
        static_parking_spot_inputs = []
        for i in range(self.properties.Informatio):
            lat, lon = generate_point(
                lat=round_7d(self.geometry.y),
                lon=round_7d(self.geometry.x),
                number=i,
                max_number=self.properties.Informatio,
            )

            static_parking_spot_inputs.append(
                StaticParkingSpotInput(
                    uid=f'{self.properties.GlobalID}',
                    name=f'{self.properties.Name}-{self.properties.Stadtteil}',
                    purpose=PurposeType.CAR,
                    address=self.properties.adress
                    description=self.properties.description,
                    static_data_updated_at=datetime.now(tz=timezone.utc),
                    lat=lat,
                    lon=lon,
                    has_realtime_data=False,
                    restrictions=[ParkingSpotRestrictionInput(type=ParkingAudience.DISABLED)],
                ),
            )

        return static_parking_spot_inputs
