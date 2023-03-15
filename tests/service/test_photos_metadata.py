import datetime

from flickr_to_sqlite.service import photos_metadata

from ..fixtures import FLICKR_PHOTO_ONE


def test_transform_photo():
    photo = FLICKR_PHOTO_ONE.copy()

    expected_date_taken_at = datetime.datetime(2023, 1, 1)
    photo["date_taken"] = expected_date_taken_at.strftime("%Y-%m-%d %H:%M:%S")

    expected_date_imported_at = datetime.datetime(2023, 1, 2)
    photo["date_imported"] = expected_date_imported_at.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    photos_metadata.transform_photo(photo)
    assert photo == {
        "id": FLICKR_PHOTO_ONE["id"],
        "name": FLICKR_PHOTO_ONE["name"],
        "description": FLICKR_PHOTO_ONE["description"],
        "date_taken_at": expected_date_taken_at,
        "date_imported_at": expected_date_imported_at,
        "license": FLICKR_PHOTO_ONE["license"],
        "photo_page_url": FLICKR_PHOTO_ONE["photopage"],
        "original_photo_url": FLICKR_PHOTO_ONE["original"],
    }
