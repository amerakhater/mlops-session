from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from my_project.models.item import Item


class ItemRepository:
    """Data access only: no HTTP or business rules here."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[Item]:
        stmt = select(Item).order_by(Item.id).offset(skip).limit(limit)
        return self.db.scalars(stmt).all()

    def get(self, item_id: int) -> Item | None:
        return self.db.get(Item, item_id)

    def create(self, data: dict) -> Item:
        item = Item(**data)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Item, data: dict) -> Item:
        for field, value in data.items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Item) -> None:
        self.db.delete(item)
        self.db.commit()
