import hashlib
from abc import ABC, abstractmethod
from uuid import UUID
from fastapi import HTTPException
from be_task_ca.user.model import CartItem, User
from be_task_ca.item.model import Item
from be_task_ca.item.usecases import ItemRepository
from be_task_ca.user.schema import (
    AddToCartRequest,
    AddToCartResponse,
    CreateUserRequest,
    CreateUserResponse,
)


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> None:
        ...

    @abstractmethod
    def get(self, user_id: UUID) -> User | None:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        ...

    @abstractmethod
    def list_cart(self, user_id: UUID) -> list[CartItem]:
        ...


def create_user(
    create_user: CreateUserRequest, db: UserRepository
) -> CreateUserResponse:
    search_result = db.get_by_email(create_user.email)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An user with this email adress already exists"
        )

    new_user = User(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        hashed_password=hashlib.sha512(
            create_user.password.encode("UTF-8")
        ).hexdigest(),
        shipping_address=create_user.shipping_address,
    )

    db.add(new_user)

    return CreateUserResponse(
        id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        shipping_address=new_user.shipping_address,
    )


def add_item_to_cart(
    user_id: int,
    cart_item: AddToCartRequest,
    user_db: UserRepository,
    item_db: ItemRepository,
) -> AddToCartResponse:
    user: User = user_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist")

    item: Item = item_db.get(cart_item.item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item does not exist")
    if item.quantity < cart_item.quantity:
        raise HTTPException(status_code=409, detail="Not enough items in stock")

    item_ids = [o.item_id for o in user.cart_items]
    if cart_item.item_id in item_ids:
        raise HTTPException(status_code=409, detail="Item already in cart")

    new_cart_item: CartItem = CartItem(
        user_id=user.id, item_id=cart_item.item_id, quantity=cart_item.quantity
    )

    user.cart_items.append(new_cart_item)

    user_db.add(user)

    return list_items_in_cart(user.id, user_db)


def list_items_in_cart(user_id: UUID, db: UserRepository) -> AddToCartResponse:
    cart_items = db.list_cart(user_id)
    return AddToCartResponse(items=list(map(cart_item_model_to_schema, cart_items)))


def cart_item_model_to_schema(model: CartItem) -> AddToCartRequest:
    return AddToCartRequest(item_id=model.item_id, quantity=model.quantity)
