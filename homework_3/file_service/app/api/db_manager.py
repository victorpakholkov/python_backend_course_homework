from app.api.models import FileIn
# from app.api.models import FileOut, FileUpdate
from app.api.db import files, database


async def add_file(payload: FileIn):
    query = files.insert().values(**payload.dict())

    return await database.execute(query=query)


async def get_file(id):
    query = files.select(files.c.id == id)
    return await database.fetch_one(query=query)
