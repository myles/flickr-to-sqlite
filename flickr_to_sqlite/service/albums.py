import json
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple
from zipfile import ZipFile

from sqlite_utils import Database

from .database import get_table
from .utils import transform_epoch_timestamp


def extract_albums_from_zip_file_obj(
    zip_file_obj: ZipFile,
) -> List[Dict[str, Any]]:
    """
    Extract the albums from the ZIP file.
    """
    albums = []

    # The file name convention for the photo's metadata is `albums.json`.
    file_names = [
        name for name in zip_file_obj.namelist() if name == "albums.json"
    ]

    for file_name in file_names:
        with zip_file_obj.open(file_name) as file_obj:
            albums.extend(json.loads(file_obj.read())["albums"])

    return albums


def extract_albums_metadata_from_zip_files(
    zip_file_paths: Tuple[Path, ...],
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Extract the albums from multiple ZIP files.
    """
    for zip_file_path in zip_file_paths:
        with ZipFile(zip_file_path) as zip_file_obj:
            yield extract_albums_from_zip_file_obj(zip_file_obj)


def transform_album(album: Dict[str, Any]):
    """
    Transform a Flickr album, so it can safely be inserted in the SQLite
    database.
    """
    # Transform the epoch timestamps into datetime objects.
    album["created_at"] = transform_epoch_timestamp(album["created"])
    album["updated_at"] = transform_epoch_timestamp(album["last_updated"])

    safe_keys = (
        "id",
        "title",
        "description",
        "url",
        "created_at",
        "updated_at",
    )
    keys_to_remove = [k for k in album.keys() if k not in safe_keys]
    for key in keys_to_remove:
        del album[key]


def save_albums(db: Database, *, albums: List[Dict[str, Any]]):
    """
    Save Flickr albums to the SQLite database.
    """
    table_albums = get_table("albums", db=db)
    table_photos_albums = get_table("photo_albums", db=db)

    albums_photos_records = []
    for album in albums:
        albums_photos_records.extend(
            [
                {"album_id": album["id"], "photo_id": photo}
                for photo in album["photos"]
            ]
        )

    for album in albums:
        transform_album(album)

    table_albums.upsert_all(records=albums, pk="id")
    table_photos_albums.upsert_all(
        records=albums_photos_records, pk=("album_id", "photo_id")
    )
