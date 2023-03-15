from flickr_to_sqlite.service import database


def test_build_database(mock_db):
    database.build_database(mock_db)

    assert mock_db["photos"].exists() is True
    assert mock_db["photos"].columns_dict == {
        "id": int,
        "name": str,
        "description": str,
        "date_taken_at": str,
        "date_imported_at": str,
        "license": str,
        "photo_page_url": str,
        "original_photo_url": str,
    }

    assert mock_db["albums"].exists() is True
    assert mock_db["albums"].columns_dict == {
        "id": int,
        "title": str,
        "description": str,
        "url": str,
        "created_at": str,
        "updated_at": str,
    }

    assert mock_db["photos_albums"].exists() is True
    assert mock_db["photos_albums"].columns_dict == {
        "photo_id": int,
        "album_id": int,
    }
