import pytest
from uuid import uuid4, UUID

from fastapi import HTTPException

from be_task_ca.item.schema import CreateItemRequest, CreateItemResponse
from be_task_ca.item.usecases import create_item, get_all, ItemRepository


def make_request(**kwargs) -> CreateItemRequest:
    return CreateItemRequest(
        name=kwargs.get("name", "test_item"),
        description=kwargs.get("description", "A test item"),
        price=kwargs.get("price", 9.99),
        quantity=kwargs.get("quantity", 10),
    )


def test_create_item_success(fake_item_repo: ItemRepository):
    req = make_request()

    response = create_item(req, fake_item_repo)

    assert isinstance(response, CreateItemResponse)
    assert response.name == req.name
    assert len(fake_item_repo.list()) == 1


def test_create_item_duplicate_name_raises(fake_item_repo: ItemRepository):
    req = make_request()
    create_item(req, fake_item_repo)

    with pytest.raises(HTTPException) as exc_info:
        create_item(req, fake_item_repo)

    assert exc_info.value.status_code == 409
    assert "already exists" in str(exc_info.value.detail)


def test_get_all_items(fake_item_repo: ItemRepository):
    # Populate repo
    for i in range(3):
        req = make_request(name=f"item_{i}")
        create_item(req, fake_item_repo)

    items = get_all(fake_item_repo)
    assert len(items.items) == 3
    assert all(isinstance(i, CreateItemResponse) for i in items.items)
