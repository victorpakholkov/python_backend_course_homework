import os
import httpx


FILE_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/files/'
url = os.environ.get('FILE_SERVICE_HOST_URL') or FILE_SERVICE_HOST_URL


def is_file_present(file_id: int):
    r = httpx.get(f'{url}{file_id}')
    return True if r.status_code == 200 else False
