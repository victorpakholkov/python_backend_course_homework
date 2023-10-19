import pytest
from app.api.models import FileIn
from app.api.files import create_file, get_file
from app.api.db_manager import add_file


class TestCreateFile:

    @pytest.mark.asyncio
    async def test_successfully_adds_file_to_database(self, mocker):
        mocker.patch('app.api.db_manager.add_file', return_value='file_id')

        payload = FileIn(name='test_file', content='test_content')

        response = await create_file(payload)

        assert response == {'id': 'file_id',
                            'name': 'test_file',
                            'content': 'test_content'}

    @pytest.mark.asyncio
    async def test_raises_error_if_payload_data_missing_fields(self):
        payload = FileIn(name='test_file')

        with pytest.raises(ValueError):
            await create_file(payload)


class TestGetFile:

    @pytest.mark.asyncio
    async def test_returns_file_with_given_id_if_exists(self, mocker):
        id = 1
        file = {'id': 1, 'name': 'test_file.txt'}
        mocker.patch('app.api.db_manager.get_file', return_value=file)

        result = await get_file(id)

        assert result == file


class TestAddFile:

    # Successfully insert a file into the database
    @pytest.mark.asyncio
    async def test_insert_file_successfully(self, mocker):
        # Arrange
        payload = FileIn(name="test_file", path="/path/to/file")
        query_mock = mocker.Mock()
        execute_mock = mocker.AsyncMock()
        mocker.patch("app.api.db.files.insert", return_value=query_mock)
        mocker.patch("app.api.db.database.execute", return_value=1)

        # Act
        result = await add_file(payload)

        # Assert
        assert result == 1
        query_mock.values.assert_called_once_with(**payload.dict())
        execute_mock.assert_awaited_once_with(query=query_mock)
