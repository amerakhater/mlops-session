from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Laptop"])
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2, examples=["999.99"])


class ItemCreate(ItemBase):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class ItemUpdate(BaseModel):
    """Partial update: only the fields sent are changed."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class ItemRead(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
