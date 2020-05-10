from fastapi import APIRouter, HTTPException ,Response, status
from pydantic import BaseModel
import aiosqlite

router = APIRouter()


@router.on_event("startup")
async def startup():
    router.db_connection = await aiosqlite.connect('chinook.db')


@router.on_event("shutdown")
async def shutdown():
    await router.db_connection.close()


@router.get("/tracks")
async def get_tracks(response: Response, page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT * FROM tracks "
                                                "ORDER BY TrackId"
                                                " LIMIT ? OFFSET ? ", (per_page, page * per_page))
    data = await cursor.fetchall()
    response.status_code = status.HTTP_200_OK
    return data


@router.get("/tracks/composers")
async def get_tracks(response: Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute("SELECT Name FROM tracks "
                                                " Where Composer = ?"
                                                " ORDER BY Name", (composer_name,))
    data = await cursor.fetchall()
    if len(data) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Cannot find tracks by that composer"}}
    response.status_code = status.HTTP_200_OK
    return data


@router.post("/albums", status_code=201)
async def add_album(artist_id: int, title: str):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT ArtistId FROM albums "
                                                " Where ArtistId = ?"
                                                " ORDER BY Title", (artist_id,))
    row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail= {"error": "Artist ID not found"})
    else:
        cursor = await router.db_connection.execute("INSERT INTO albums "
                                                    "(Title, ArtistId) VALUES (?, ?)", (title, artist_id))
        await router.db_connection.commit()
        new_album_row = await router.db_connection.execute("SELECT * FROM albums WHERE AlbumID = ?", (cursor.lastrowid,))
        album =  await new_album_row.fetchone()
        return album


@router.get('/albums/{album_id}', status_code=200)
async def get_album(album_id: int):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT * FROM albums WHERE AlbumId = ?", (album_id,))
    album = await cursor.fetchone()
    return album

