from fastapi import APIRouter, HTTPException
# from typing import List

from app.api.models import FileOut, FileIn
# from app.api.models import FileUpdate
from app.api import db_manager

files = APIRouter()


@files.post('/', response_model=FileOut, status_code=201)
async def create_file(payload: FileIn):
    file_id = await db_manager.add_file(payload)

    response = {
        'id': file_id,
        **payload.dict()
    }

    return response


@files.get('/{id}/', response_model=FileOut)
async def get_file(id: int):
    file = await db_manager.get_file(id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file
