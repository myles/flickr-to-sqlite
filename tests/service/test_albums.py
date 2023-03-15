import datetime

from flickr_to_sqlite.service import albums
from ..fixtures import FLICKR_ALBUM_ONE


def test_transform_album():
    album = FLICKR_ALBUM_ONE.copy()

    expected_created_at = datetime.datetime.now()
    album["created"] = expected_created_at.timestamp()

    expected_updated_at = datetime.datetime.now()
    album["last_updated"] = expected_updated_at.timestamp()

    albums.transform_album(album)
    assert album == {
        "id": FLICKR_ALBUM_ONE["id"],
        "title": FLICKR_ALBUM_ONE["title"],
        "description": FLICKR_ALBUM_ONE["description"],
        "url": FLICKR_ALBUM_ONE["url"],
        "created_at": expected_created_at,
        "updated_at": expected_updated_at,
    }
