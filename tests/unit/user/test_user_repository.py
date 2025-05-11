from uuid import uuid4
from be_task_ca.user.model import User, CartItem
from be_task_ca.user.repository import InMemoryUserRepository


def make_user(email="user@example.com") -> User:
    return User(
        first_name="Test",
        last_name="User",
        email=email,
        hashed_password="hashed_pw",
        shipping_address="123 Test St",
    )


def test_add_and_get_user():
    repo = InMemoryUserRepository()
    user = make_user()
    repo.add(user)

    assert user.id is not None
    retrieved = repo.get(user.id)
    assert retrieved is not None
    assert retrieved.email == user.email


def test_get_nonexistent_user_returns_none():
    repo = InMemoryUserRepository()
    assert repo.get(uuid4()) is None


def test_get_by_email_success():
    repo = InMemoryUserRepository()
    user = make_user(email="unique@example.com")
    repo.add(user)

    found = repo.get_by_email("unique@example.com")
    assert found is not None
    assert found.email == "unique@example.com"


def test_get_by_email_not_found():
    repo = InMemoryUserRepository()
    assert repo.get_by_email("missing@example.com") is None


def test_list_cart_returns_empty_if_none():
    repo = InMemoryUserRepository()
    user = make_user()
    repo.add(user)

    assert repo.list_cart(user.id) == []


def test_list_cart_returns_items():
    repo = InMemoryUserRepository()
    user = make_user()
    item_id = uuid4()
    cart_item = CartItem(user_id=user.id, item_id=item_id, quantity=2)
    user.cart_items.append(cart_item)
    repo.add(user)

    cart = repo.list_cart(user.id)
    assert len(cart) == 1
    assert cart[0].item_id == item_id
    assert cart[0].quantity == 2
