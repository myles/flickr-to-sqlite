from pathlib import Path
from typing import Tuple

import click

from .service.database import build_database, open_database
from .service.photos_metadata import (
    extract_photos_metadata_from_zip_files,
    save_photos_metadata,
)


@click.group()
@click.version_option()
def cli():
    """
    Save data from Flickr to a SQLite database.
    """


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(
        file_okay=True, dir_okay=False, allow_dash=False, path_type=Path
    ),
    required=True,
)
@click.argument(
    "zip_file_paths",
    nargs=-1,  # We want to be able to pass multiple ZIP files.
    type=click.Path(
        file_okay=True, dir_okay=False, allow_dash=False, path_type=Path
    ),
    required=True,
)
def photos_metadata(db_path: Path, zip_file_paths: Tuple[Path, ...]):
    """
    Save data from Flickr Data's account data to the SQLite database.
    """
    db = open_database(db_path)
    build_database(db)

    for photos in extract_photos_metadata_from_zip_files(zip_file_paths):
        save_photos_metadata(db, photos=photos)
