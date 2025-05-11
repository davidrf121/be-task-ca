import pytest
from uuid import uuid4
from fastapi import HTTPException
from be_task_ca.user.usecases import create_user, add_item_to_cart, list_items_in_cart, UserRepository
from be_task_ca.item.usecases import ItemRepository
from be_task_ca.user.schema import CreateUserRequest, AddToCartRequest, AddToCartResponse
from be_task_ca.user.model import User
from be_task_ca.item.model import Item
from be_task_ca.user.repository import CartItem

def make_user_request(email="test@example.com") -> CreateUserRequest:
    return CreateUserRequest(
        first_name="John",
        last_name="Doe",
        email=email,
        password="secret",
        shipping_address="123 Main St"
    )


def test_create_user_success(fake_user_repo: UserRepository):
    req = make_user_request()
    res = create_user(req, fake_user_repo)

    assert res.email == req.email
    assert res.first_name == req.first_name


def test_create_user_duplicate_email(fake_user_repo: UserRepository):
    req = make_user_request()
    create_user(req, fake_user_repo)

    with pytest.raises(HTTPException) as exc:
        create_user(req, fake_user_repo)

    assert exc.value.status_code == 409
    assert "already exists" in str(exc.value.detail)


def test_add_item_to_cart_success(fake_user_repo: UserRepository, fake_item_repo: ItemRepository):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        hashed_password="hashed",
        shipping_address="123 Main St"
    )
    fake_user_repo.add(user)

    item = Item(
        name="Widget",
        description="A useful widget",
        price=5.0,
        quantity=10
    )
    fake_item_repo.add(item)

    req = AddToCartRequest(item_id=item.id, quantity=2)
    res = add_item_to_cart(user.id, req, fake_user_repo, fake_item_repo)

    assert isinstance(res, AddToCartResponse)
    assert len(res.items) == 1
    assert res.items[0].item_id == item.id
    assert res.items[0].quantity == 2


def test_add_item_to_cart_user_not_found(fake_item_repo: ItemRepository, fake_user_repo: UserRepository):
    req = AddToCartRequest(item_id=uuid4(), quantity=1)
    with pytest.raises(HTTPException) as exc:
        add_item_to_cart(uuid4(), req, fake_user_repo, fake_item_repo)
    assert exc.value.status_code == 404
    assert "User does not exist" in str(exc.value.detail)


def test_add_item_to_cart_item_not_found(fake_user_repo: UserRepository, fake_item_repo: ItemRepository):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        hashed_password="hashed",
        shipping_address="123 Main St"
    )
    fake_user_repo.add(user)

    req = AddToCartRequest(item_id=uuid4(), quantity=1)
    with pytest.raises(HTTPException) as exc:
        add_item_to_cart(user.id, req, fake_user_repo, fake_item_repo)
    assert exc.value.status_code == 404
    assert "Item does not exist" in str(exc.value.detail)


def test_add_item_to_cart_insufficient_stock(fake_user_repo: UserRepository, fake_item_repo: ItemRepository):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        hashed_password="hashed",
        shipping_address="123 Main St"
    )
    fake_user_repo.add(user)

    item = Item(
        name="Gadget",
        description="A neat gadget",
        price=15.0,
        quantity=1
    )
    fake_item_repo.add(item)

    req = AddToCartRequest(item_id=item.id, quantity=2)
    with pytest.raises(HTTPException) as exc:
        add_item_to_cart(user.id, req, fake_user_repo, fake_item_repo)
    assert exc.value.status_code == 409
    assert "Not enough items" in str(exc.value.detail)


def test_add_item_to_cart_duplicate(fake_user_repo: UserRepository, fake_item_repo: ItemRepository):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        hashed_password="hashed",
        shipping_address="123 Main St"
    )
    fake_user_repo.add(user)

    item = Item(
        name="Gizmo",
        description="Fancy gizmo",
        price=20.0,
        quantity=5
    )
    fake_item_repo.add(item)

    req = AddToCartRequest(item_id=item.id, quantity=1)
    add_item_to_cart(user.id, req, fake_user_repo, fake_item_repo)

    with pytest.raises(HTTPException) as exc:
        add_item_to_cart(user.id, req, fake_user_repo, fake_item_repo)

    assert exc.value.status_code == 409
    assert "already in cart" in str(exc.value.detail)


def test_list_items_in_cart(fake_user_repo: UserRepository, fake_item_repo: ItemRepository):
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        hashed_password="hashed",
        shipping_address="123 Main St"
    )
    item_id = uuid4()
    user.cart_items.append(
        CartItem(user_id=user.id, item_id=item_id, quantity=3)
    )
    fake_user_repo.add(user)

    res = list_items_in_cart(user.id, fake_user_repo)
    assert len(res.items) == 1
    assert res.items[0].item_id == item_id
    assert res.items[0].quantity == 3
