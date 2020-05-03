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
                                                " LIMIT ? OFFSET ? " , (per_page, page*per_page))
    data = await cursor.fetchall()
    response.status_code = status.HTTP_200_OK
    return data

