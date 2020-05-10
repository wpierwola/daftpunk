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

def longest_consec(strarr, k):
    if k>len(strarr) or k <=0:
        return ""
    else:
        print(strarr)
        result = "".join([x for x in strarr if x in sorted(strarr,key=len, reverse=True)[:k]])
        return result

a=longest_consec(["aadsas", "24fdg"], 1)


strarr = ["asdas","rhe"]
len_list = strarr.sort(key=len, reverse=True)
