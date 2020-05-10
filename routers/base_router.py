from fastapi import APIRouter, Response, status
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
                                                " LIMIT ? OFFSET ? ", (per_page, page*per_page))
    data = await cursor.fetchall()
    response.status_code = status.HTTP_200_OK
    return data


@router.get("/tracks/composers")
async def get_tracks(response:Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = await router.db_connection.execute("SELECT Name FROM tracks "
                                                " Where Composer = ?"
                                                " ORDER BY Name", (composer_name,))
    data = await cursor.fetchall()
    if len(data) ==0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Cannot find tracks by that composer"}}
    response.status_code = status.HTTP_200_OK
    return data


"""@router.post("/albums")
async def add_album(response: Response, artist_id: int, title: str):
    router.db_connection.row_factory = None
    cursor = await router.db_connection.execute("SELECT artist_id FROM albums "
                                                " Where artist_id = ?"
                                                " ORDER BY Name", (artist_id,))
    row = await cursor.fetchone()
    if row is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Artist ID not found"}}
    else:
        cursor = await router.db_connection.execute("INSERT INTO albums "
                                                    "(Title, ArtistId) VALUES (?, ?)", (title, artist_id))
        await router.db_connection.commit()
        response.status_code = status.HTTP_201_CREATED
        return {"AlbumId": cursor.lastrowid, "Title": title, "ArtistId": artist_id}


@router.get('/albums/{album_id}')
async def get_album(response: Response, album_id: int):
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT * FROM albums "
                                                " Where AlbumId = ?", (album_id,))
    row = await cursor.fetchone()
    if row:
        response.status_code = status.HTTP_200_OK
        return row"""


    class Album(BaseModel):
        title: str
        artist_id: int

    @router.post("/albums")
    async def add_album(response: Response, album: Album):
        router.db_connection.row_factory = None
        cursor = await router.db_connection.execute("SELECT ArtistId FROM artists WHERE ArtistId = ?",
            (album.artist_id, ))
        result = await cursor.fetchone()
        if result is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"detail":{"error":"Artist with that ID does not exist."}}
        cursor = await router.db_connection.execute("INSERT INTO albums (Title, ArtistId) VALUES (?, ?)",
            (album.title, album.artist_id))
        await router.db_connection.commit()
        response.status_code = status.HTTP_201_CREATED
        return {"AlbumId": cursor.lastrowid, "Title": album.title, "ArtistId": album.artist_id}

    @router.get("/albums/{album_id}")
    async def tracks_composers(response: Response, album_id: int):
        router.db_connection.row_factory = aiosqlite.Row
        cursor = await router.db_connection.execute("SELECT * FROM albums WHERE AlbumId = ?",
            (album_id, ))
        album = await cursor.fetchone()
        if album is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"detail":{"error":"Album with that ID does not exist."}}
        return album