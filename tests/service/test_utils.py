import datetime

import pytest
import pytz

from flickr_to_sqlite.service import utils


@pytest.mark.parametrize(
    "timestamp, expected_result",
    [
        ("", None),
        (None, None),
        (
            "2022-03-14 12:34:56",
            datetime.datetime(2022, 3, 14, 12, 34, 56, tzinfo=pytz.UTC),
        ),
    ],
)
def test_transform_timestamp(timestamp, expected_result):
    result = utils.transform_timestamp(timestamp)
    assert result == expected_result


def test_transform_timestamp__invalid():
    # Test with an invalid timestamp
    invalid_timestamp = "2022-03-14 12:34"
    with pytest.raises(ValueError):
        utils.transform_timestamp(invalid_timestamp)


@pytest.mark.parametrize(
    "timestamp, expected_result",
    [
        ("", None),
        (None, None),
        (
            "1647317696",
            datetime.datetime(2022, 3, 15, 4, 14, 56, tzinfo=pytz.UTC),
        ),
        (
            "1647317696.123456",
            datetime.datetime(2022, 3, 15, 4, 14, 56, 123456, tzinfo=pytz.UTC),
        ),
        (
            "-1647317696",
            datetime.datetime(1917, 10, 19, 19, 45, 4, tzinfo=pytz.UTC),
        ),
    ],
)
def test_transform_epoch_timestamp(timestamp, expected_result):
    result = utils.transform_epoch_timestamp(timestamp)
    assert result == expected_result


def test_transform_epoch_timestamp__invalid():
    # Test with an invalid timestamp
    invalid_timestamp = "2022-03-14 12:34"
    with pytest.raises(ValueError):
        utils.transform_epoch_timestamp(invalid_timestamp)
