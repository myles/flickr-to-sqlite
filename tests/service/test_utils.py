import datetime
import pytest
from flickr_to_sqlite.service import utils


@pytest.mark.parametrize(
    "timestamp, expected_result",
    [
        ("", None),
        (None, None),
        (" 2022-03-14 12:34:56 ", datetime.datetime(2022, 3, 14, 12, 34, 56)),
        ("2022-03-14 12:34:56", datetime.datetime(2022, 3, 14, 12, 34, 56)),
        ("2022-03-14 12:34", None),
    ],
)
def test_transform_timestamp(timestamp, expected_result):
    result = utils.transform_timestamp(timestamp)
    assert result == expected_result


def test_transform_invalid_timestamp():
    # Test with an invalid timestamp
    invalid_timestamp = "2022-03-14 12:34"
    with pytest.raises(ValueError):
        utils.transform_timestamp(invalid_timestamp)


@pytest.mark.parametrize(
    "timestamp, expected_result",
    [
        ("", None),
        (None, None),
        ("1647317696", datetime.datetime(2022, 3, 14, 12, 34, 56)),
        ("1647317696.123456", datetime.datetime(2022, 3, 14, 12, 34, 56, 123456)),
        ("-1647317696", datetime.datetime(1910, 10, 8, 11, 25, 4)),
    ],
)
def test_transform_epoch_timestamp(timestamp, expected_result):
    result = transform_epoch_timestamp(timestamp)
    assert result == expected_result


def test_transform_invalid_epoch_timestamp():
    # Test with an invalid timestamp
    invalid_timestamp = "2022-03-14 12:34"
    with pytest.raises(ValueError):
        transform_epoch_timestamp(invalid_timestamp)
