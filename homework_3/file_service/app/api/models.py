from pydantic import BaseModel
from typing import Optional


class FileIn(BaseModel):
    name: str
    extention: Optional[str] = None
    size: Optional[int] = None


class FileOut(FileIn):
    id: int


class FileUpdate(FileIn):
    name: Optional[str] = None
