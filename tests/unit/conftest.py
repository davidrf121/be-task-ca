import pytest
from be_task_ca.item.model import Item
from be_task_ca.item.usecases import ItemRepository
from uuid import UUID, uuid4
from be_task_ca.user.model import CartItem, User
from be_task_ca.user.usecases import UserRepository


class FakeItemRepository(ItemRepository):
    def __init__(self):
        self._items: dict[UUID,Item] = {}

    def add(self, item: Item) -> None:
        item.id = uuid4()
        self._items[item.id] = item

    def list(self) -> list[Item]:
        return self._items.values()

    def get(self, item_id: UUID) -> Item | None:
        return self._items.get(item_id)

    def get_by_name(self, name: str) -> Item | None:
        for item in self._items.values():
            if item.name == name:
                return item
        return None


class FakeUserRepository(UserRepository):
    def __init__(self):
        self._users: dict[UUID, User] = {}

    def add(self, user: User) -> None:
        if user.id is None:
            user.id = uuid4()
        self._users[user.id] = user

    def get(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def list_cart(self, user_id: UUID) -> list[CartItem]:
        if user_id in self._users:
            return self._users[user_id].cart_items
        return []

@pytest.fixture
def fake_item_repo():
    return FakeItemRepository()

@pytest.fixture
def fake_user_repo():
    return FakeUserRepository()
