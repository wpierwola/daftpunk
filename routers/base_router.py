from fastapi import APIRouter, Response, status

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
    router.db_connection.row_factory = aiosqlite.Row
    cursor = await router.db_connection.execute("SELECT Name FROM tracks "
                                                " Where Composer = ?"
                                                " ORDER BY Name", (composer_name,))
    data = await cursor.fetchall()
    if len(data) ==0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": {"error": "Cannot find tracks by that composer"}}
    response.status_code = status.HTTP_200_OK
    return data
