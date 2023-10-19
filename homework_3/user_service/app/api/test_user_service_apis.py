# pip install pytest-mock
import pytest
from app.api.users import get_user, create_user, update_user, delete_user
from app.api.models import UserIn, UserUpdate
from app.api import db_manager
from fastapi import HTTPException
import httpx
from app.api.service import is_file_present


class TestGetUser:

    @pytest.mark.asyncio
    async def test_returns_user_with_given_id_if_exists(self, mocker):
        id = 1
        user = {'id': 1, 'name': 'Victor Pakholkov',
                'email': 'VictorPakholkov@outlook.com'}
        mocker.patch('app.api.db_manager.get_user', return_value=user)

        result = await get_user(id)

        assert result == user


class TestCreateUser:

    @pytest.mark.asyncio
    async def test_add_user_with_valid_payload(self, mocker):
        payload = UserIn(
            username="test_user",
            email="test@example.com",
            files_id=[1, 2, 3]
        )
        mocker.patch("app.api.service.is_file_present", return_value=True)
        mocker.patch("app.api.db_manager.add_user", return_value=1)

        response = await create_user(payload)

        assert response["id"] == 1
        assert response["username"] == "test_user"
        assert response["email"] == "test@example.com"
        assert response["files_id"] == [1, 2, 3]


class TestUpdateUser:

    @pytest.mark.asyncio
    async def test_update_user_valid_id_and_payload(self, mocker):
        id = 1
        payload = UserUpdate(name="John Doe", email="john.doe@example.com")
        user = {"id": 1, "name": "Jane Doe", "email": "jane.doe@example.com"}
        mocker.patch("app.api.db_manager.get_user", return_value=user)
        mocker.patch("app.api.service.is_file_present", return_value=True)
        mocker.patch("app.api.db_manager.update_user")

        result = await update_user(id, payload)

        assert result == await db_manager.update_user(id,
                                                      UserIn(**user).copy(update=payload.dict(exclude_unset=True))) # noqa

    @pytest.mark.asyncio
    async def test_update_user_invalid_id(self, mocker):
        id = 1
        payload = UserUpdate(name="John Doe", email="john.doe@example.com")
        mocker.patch("app.api.db_manager.get_user", return_value=None)

        with pytest.raises(HTTPException) as exc:
            await update_user(id, payload)
        assert exc.value.status_code == 404
        assert exc.value.detail == "User with a given id not found"


class TestDeleteUser:

    @pytest.mark.asyncio
    async def test_delete_existing_user_returns_success(self, mocker):
        id = 1
        user = {"id": id, "name": "John Doe"}
        mocker.patch("app.api.db_manager.get_movie", return_value=user)
        mocker.patch("app.api.db_manager.delete_user", return_value=True)

        result = await delete_user(id)

        assert result is True


class TestIsFilePresent:

    def test_returns_true_if_status_code_is_200(self, mocker):
        file_id = 123
        mocker.patch('httpx.get', return_value=httpx.Response(200))

        result = is_file_present(file_id)

        assert result is True
