from abc import ABC, abstractmethod
from fastapi import HTTPException

from be_task_ca.item.model import Item
from be_task_ca.item.schema import (
    AllItemsRepsonse,
    CreateItemRequest,
    CreateItemResponse,
)
from uuid import UUID


class ItemRepository(ABC):
    @abstractmethod
    def add(self, user: Item) -> None:
        ...

    @abstractmethod
    def get(self, item_id: UUID) -> Item | None:
        ...

    @abstractmethod
    def get_by_name(self, name: str) -> Item | None:
        ...

    @abstractmethod
    def list(self) -> list[Item]:
        ...


def create_item(item: CreateItemRequest, db: ItemRepository) -> CreateItemResponse:
    search_result = db.get_by_name(item.name)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An item with this name already exists"
        )

    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    db.add(new_item)
    return model_to_schema(new_item)


def get_all(db: ItemRepository) -> list[CreateItemResponse]:
    item_list = db.list()
    return AllItemsRepsonse(items=list(map(model_to_schema, item_list)))


def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
