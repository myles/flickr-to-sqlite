import json
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple
from zipfile import ZipFile

from sqlite_utils import Database

from .database import get_table
from .utils import transform_timestamp


def extract_photos_metadata_from_zip_file_obj(
    zip_file_obj: ZipFile,
) -> List[Dict[str, Any]]:
    """
    Extract the photos' metadata from the ZIP file.
    """
    photos = []

    # The file name convention for the photo's metadata is `photo_<id>.json`.
    file_names = [
        name
        for name in zip_file_obj.namelist()
        if name.startswith("photo_") is True and name.endswith(".json") is True
    ]

    for file_name in file_names:
        with zip_file_obj.open(file_name) as file_obj:
            photos.append(json.loads(file_obj.read()))

    return photos


def extract_photos_metadata_from_zip_files(
    zip_file_paths: Tuple[Path, ...],
) -> Generator[List[Dict[str, Any]], None, None]:
    """
    Extract the photos' metadata from multiple ZIP files.
    """
    for zip_file_path in zip_file_paths:
        with ZipFile(zip_file_path) as zip_file_obj:
            yield extract_photos_metadata_from_zip_file_obj(zip_file_obj)


def transform_photo(photo: Dict[str, Any]):
    """
    Transform a Flickr photo's metadata, so it can safely be inserted in the
    SQLite database.
    """
    # Transform the string timestamps into datetime objects.
    photo["date_taken_at"] = transform_timestamp(photo["date_taken"])
    photo["date_imported_at"] = transform_timestamp(photo["date_imported"])

    photo["photo_page_url"] = photo["photopage"]
    photo["original_photo_url"] = photo["original"]

    safe_keys = (
        "id",
        "name",
        "description",
        "date_taken_at",
        "date_imported_at",
        "license",
        "photo_page_url",
        "original_photo_url",
    )
    keys_to_remove = [k for k in photo.keys() if k not in safe_keys]
    for key in keys_to_remove:
        del photo[key]


def save_photos_metadata(db: Database, *, photos: List[Dict[str, Any]]):
    """
    Save Flickr photos' metadata to the SQLite database.
    """
    table = get_table("photos", db=db)

    for photo in photos:
        transform_photo(photo)

    table.upsert_all(records=photos, pk="id")
