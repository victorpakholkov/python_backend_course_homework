# from typing import List
from fastapi import APIRouter, HTTPException
# from fastapi import Header

from app.api.models import UserIn, UserOut, UserUpdate
from app.api import db_manager
from app.api.service import is_file_present


users = APIRouter()


# @users.get('/', response_model=List[UserOut])
# async def get_user():
# return await db_manager.get_all_users()


@users.get('/{id}/', response_model=UserOut)
async def get_user(id: int):
    user = await db_manager.get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users.post('/', response_model=UserOut, status_code=201)
async def create_user(payload: UserIn):
    for file_id in payload.files_id:
        if not is_file_present(file_id):
            raise HTTPException(status_code=404,
                                detail=f"File with id:{file_id} not found")

    user_id = await db_manager.add_user(payload)
    response = {
        'id': user_id,
        **payload.dict()
    }

    return response


@users.put('/{id}', response_model=UserOut)
async def update_user(id: int, payload: UserUpdate):
    user = await db_manager.get_user(id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="User with a given id not found")

    update_data = payload.dict(exclude_unset=True)

    if 'file_id' in update_data:
        for file_id in payload.files_id:
            if not is_file_present(file_id):
                raise HTTPException(status_code=404,
                                    detail=f"File with id:{file_id} not found")

    user_in_db = UserIn(**user)

    updated_user = user_in_db.copy(update=update_data)

    return await db_manager.update_user(id, updated_user)


@users.delete('/{id}', response_model=None)
async def delete_user(id: int):
    user = await db_manager.get_movie(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await db_manager.delete_user(id)
