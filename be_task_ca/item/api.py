from fastapi import APIRouter

from be_task_ca.item.usecases import create_item, get_all
from be_task_ca.item.repository import item_repository
from be_task_ca.item.schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(item: CreateItemRequest) -> CreateItemResponse:
    return create_item(item, item_repository)


@item_router.get("/")
async def get_items():
    return get_all(item_repository)
