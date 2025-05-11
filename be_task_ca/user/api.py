from uuid import UUID
from fastapi import APIRouter

from be_task_ca.user.usecases import add_item_to_cart, create_user, list_items_in_cart

from be_task_ca.user.schema import AddToCartRequest, CreateUserRequest
from be_task_ca.user.repository import user_repository
from be_task_ca.item.repository import item_repository

user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/")
async def post_customer(user: CreateUserRequest):
    return create_user(user, user_repository)


@user_router.post("/{user_id}/cart")
async def post_cart(user_id: UUID, cart_item: AddToCartRequest):
    return add_item_to_cart(
        user_id=user_id,
        cart_item=cart_item,
        user_db=user_repository,
        item_db=item_repository,
    )


@user_router.get("/{user_id}/cart")
async def get_cart(user_id: UUID):
    return list_items_in_cart(user_id, db=user_repository)
