from uuid import UUID, uuid4
from be_task_ca.item.model import Item
from be_task_ca.item.repository import InMemoryItemRepository


def make_item(name="ItemA", description="desc", price=10.0, quantity=2) -> Item:
    return Item(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
    )


def test_add_and_get_by_id():
    repo = InMemoryItemRepository()
    item = make_item()
    repo.add(item)

    assert item.id is not None
    retrieved = repo.get(item.id)
    assert retrieved is not None
    assert retrieved.name == item.name


def test_get_nonexistent_id_returns_none():
    repo = InMemoryItemRepository()
    assert repo.get(uuid4()) is None


def test_get_by_name():
    repo = InMemoryItemRepository()
    item = make_item(name="UniqueName")
    repo.add(item)

    found = repo.get_by_name("UniqueName")
    assert found is not None
    assert found.name == "UniqueName"


def test_get_by_name_not_found():
    repo = InMemoryItemRepository()
    assert repo.get_by_name("DoesNotExist") is None


def test_list_returns_all_items():
    repo = InMemoryItemRepository()
    result = repo.list()
    assert result == []

    items = [make_item(name=f"Item{i}") for i in range(5)]
    for item in items:
        repo.add(item)

    result = repo.list()
    assert len(result) == 5
    names = {item.name for item in result}
    assert names == {f"Item{i}" for i in range(5)}
