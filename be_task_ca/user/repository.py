from be_task_ca.user.model import CartItem, User
from be_task_ca.user.usecases import UserRepository
from uuid import UUID, uuid4


class InMemoryUserRepository(UserRepository):
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


user_repository = InMemoryUserRepository()
