from collections.abc import Sequence

from my_project.models.item import Item
from my_project.repositories.item_repository import ItemRepository
from my_project.schemas.item import ItemCreate, ItemUpdate


class ItemNotFoundError(Exception):
    def __init__(self, item_id: int) -> None:
        super().__init__(f"Item {item_id} not found")
        self.item_id = item_id


class ItemService:
    """Business logic for items; raises domain errors, not HTTP errors."""

    def __init__(self, repo: ItemRepository) -> None:
        self.repo = repo

    def list_items(self, skip: int, limit: int) -> Sequence[Item]:
        return self.repo.list(skip=skip, limit=limit)

    def get_item(self, item_id: int) -> Item:
        item = self.repo.get(item_id)
        if item is None:
            raise ItemNotFoundError(item_id)
        return item

    def create_item(self, payload: ItemCreate) -> Item:
        return self.repo.create(payload.model_dump())

    def update_item(self, item_id: int, payload: ItemUpdate) -> Item:
        item = self.get_item(item_id)
        return self.repo.update(item, payload.model_dump(exclude_unset=True))

    def delete_item(self, item_id: int) -> None:
        self.repo.delete(self.get_item(item_id))
