"""
Copyright 2024 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from unittest.mock import Mock

import pytest
from openpyxl.reader.excel import load_workbook
from parkapi_sources.converters import DummyBikePushConverter

from tests.converters.helper import get_data_path, validate_static_parking_site_inputs


@pytest.fixture
def dummy_bike_push_converter(mocked_config_helper: Mock) -> DummyBikePushConverter:
    return DummyBikePushConverter(config_helper=mocked_config_helper)


class DummyBikePushConverterTest:
    @staticmethod
    def test_get_static_parking_sites(dummy_bike_push_converter: DummyBikePushConverter):
        workbook = load_workbook(filename=str(get_data_path('dummy_bike.xlsx').absolute()))

        static_parking_site_inputs, import_parking_site_exceptions = dummy_bike_push_converter.handle_xlsx(workbook)

        assert len(static_parking_site_inputs) == 3
        assert len(import_parking_site_exceptions) == 0

        validate_static_parking_site_inputs(static_parking_site_inputs)
