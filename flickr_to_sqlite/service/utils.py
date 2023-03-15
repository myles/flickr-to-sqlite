import datetime
from typing import Optional

import pytz


def transform_timestamp(value: Optional[str]) -> Optional[datetime.datetime]:
    """
    Transform a Flickr's string formatted timestamp into a Python datetime
    object.
    """
    if value is None:
        return None

    if value.strip() == "":
        return None

    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)


def transform_epoch_timestamp(
    value: Optional[str],
) -> Optional[datetime.datetime]:
    """
    Transform a Flickr's epoch string formatted timestamp into a Python
    datetime object.
    """
    if value is None:
        return None

    if value.strip() == "":
        return None

    return datetime.datetime.fromtimestamp(float(value), tz=pytz.UTC)
