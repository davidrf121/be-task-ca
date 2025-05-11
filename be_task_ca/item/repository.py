from uuid import UUID, uuid4
from be_task_ca.item.model import Item
from be_task_ca.item.usecases import ItemRepository


class InMemoryItemRepository(ItemRepository):
    def __init__(self):
        self._items: dict[UUID, Item] = {}

    def add(self, item: Item) -> None:
        item.id = uuid4()
        self._items[item.id] = item

    def list(self) -> list[Item]:
        return list(self._items.values())

    def get(self, item_id: UUID) -> Item | None:
        return self._items.get(item_id)

    def get_by_name(self, name: str) -> Item | None:
        for item in self._items.values():
            if item.name == name:
                return item
        return None


item_repository = InMemoryItemRepository()
