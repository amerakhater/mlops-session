from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from my_project.core.config import get_settings
from my_project.db.session import get_db
from my_project.repositories.item_repository import ItemRepository
from my_project.services.item_service import ItemService
from my_project.services.openai_service import LLMNotConfiguredError, OpenAIService


def get_item_service(db: Annotated[Session, Depends(get_db)]) -> ItemService:
    return ItemService(ItemRepository(db))


def get_openai_service() -> OpenAIService:
    try:
        return OpenAIService(get_settings())
    except LLMNotConfiguredError as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc
