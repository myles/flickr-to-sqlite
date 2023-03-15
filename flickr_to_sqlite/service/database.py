import datetime

from sqlite_utils.db import Database, Table


def open_database(db_file_path) -> Database:
    """
    Open the Flickr SQLite database.
    """
    return Database(db_file_path)


def get_table(table_name: str, db: Database) -> Table:
    """
    Returns a Table from a given db Database object.
    """
    return Table(db=db, name=table_name)


def build_database(db: Database):
    """
    Build the Flickr SQLite database structure.
    """
    table_photos = get_table("photos", db=db)
    table_albums = get_table("albums", db=db)
    table_photos_albums = get_table("photos_albums", db=db)

    if table_photos.exists() is False:
        table_photos.create(
            columns={
                "id": int,
                "name": str,
                "description": str,
                "date_taken_at": datetime.datetime,
                "date_imported_at": datetime.datetime,
                "license": str,
                "photo_page_url": str,
                "original_photo_url": str,
            },
            pk="id",
        )
        table_photos.enable_fts(["name", "description"], create_triggers=True)

    if table_albums.exists() is False:
        table_albums.create(
            columns={
                "id": int,
                "title": str,
                "description": str,
                "url": str,
                "created_at": datetime.datetime,
                "updated_at": datetime.datetime,
            },
            pk="id",
        )
        table_albums.enable_fts(["title", "description"], create_triggers=True)

    if table_photos_albums.exists() is False:
        table_photos_albums.create(
            columns={
                "photo_id": int,
                "album_id": int,
            },
            pk=("photo_id", "album_id"),
            foreign_keys=(
                ("photo_id", "photos", "id"),
                ("album_id", "albums", "id"),
            ),
        )

    table_photos_albums_indexes = {
        tuple(i.columns) for i in table_photos_albums.indexes
    }
    if ("photo_id",) not in table_photos_albums_indexes:
        table_photos_albums.create_index(["photo_id"])
    if ("album_id",) not in table_photos_albums_indexes:
        table_photos_albums.create_index(["album_id"])
