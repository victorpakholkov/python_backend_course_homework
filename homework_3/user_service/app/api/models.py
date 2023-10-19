from typing import List, Optional
from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    user_id: str
    rights: List[str]
    items: List[str]
    files_id: List[str]


class UserOut(UserIn):
    id: int


class UserUpdate(UserIn):
    name: Optional[str] = None
    user_id: Optional[str] = None
    rights: Optional[List[str]] = None
    items: Optional[List[str]] = None
    files_id: Optional[List[str]] = None
