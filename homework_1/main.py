from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get(
    "/",
    description="This is my first 'Hello World!' route.",
)
async def root():
    return {"message": "Hello World!"}


@app.get(
    "/users/{user_id}",
    description="Gets user id",
)
async def get_user_id(user_id: str):
    return {"user_id": user_id}


toy_db = [
    {"item_name": "World"},
    {"item_name": "Universe"},
    {"item_name": "Globe"},
    {"item_name": "Earth"},
]


@app.get(
    "/items",
    description="Items out of toy database",
)
async def list_items(skip: int = 1, limit: int = 2):
    return toy_db[skip : skip + limit]


class Item(BaseModel):
    name: str
    description: str | None = None
    volume: float
    degree: float | None = None


@app.post("/items", description="Something with degree_x_volume,")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.degree:
        degree_x_volume = item.degree * item.volume
        item_dict.update({"degree_x_volume": degree_x_volume})
    return item_dict


@app.put(
    "/items/{item_id}",
    description="Added put method",
)
async def create_item_with_put(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
