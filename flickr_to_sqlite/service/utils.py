import datetime
from typing import Optional


def transform_timestamp(value: Optional[str]) -> Optional[datetime.datetime]:
    """
    Transform a Flickr's string formatted timestamp into a Python datetime
    object.
    """
    # If the value is an empty string or None then we just want to return
    # early.
    if value in (None, ""):
        return None

    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def transform_epoch_timestamp(
    value: Optional[str],
) -> Optional[datetime.datetime]:
    """
    Transform a Flickr's epoch string formatted timestamp into a Python
    datetime object.
    """
    # If the value is an empty string or None then we just want to return
    # early.
    if value in (None, ""):
        return None

    return datetime.datetime.fromtimestamp(float(value))
