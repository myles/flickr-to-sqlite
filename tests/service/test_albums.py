import datetime

import pytz

from flickr_to_sqlite.service import albums

from ..fixtures import FLICKR_ALBUM_ONE


def test_transform_album():
    album = FLICKR_ALBUM_ONE.copy()

    expected_created_at = datetime.datetime(2023, 1, 1, tzinfo=pytz.UTC)
    album["created"] = str(expected_created_at.timestamp())

    expected_updated_at = datetime.datetime(2023, 2, 1, tzinfo=pytz.UTC)
    album["last_updated"] = str(expected_updated_at.timestamp())

    albums.transform_album(album)
    assert album == {
        "id": FLICKR_ALBUM_ONE["id"],
        "title": FLICKR_ALBUM_ONE["title"],
        "description": FLICKR_ALBUM_ONE["description"],
        "url": FLICKR_ALBUM_ONE["url"],
        "created_at": expected_created_at,
        "updated_at": expected_updated_at,
    }
