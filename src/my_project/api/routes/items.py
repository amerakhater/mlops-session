from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from my_project.api.deps import get_item_service
from my_project.schemas.item import ItemCreate, ItemRead, ItemUpdate
from my_project.services.item_service import ItemNotFoundError, ItemService

router = APIRouter(prefix="/items", tags=["items"])

Service = Annotated[ItemService, Depends(get_item_service)]


@router.get("", response_model=list[ItemRead])
def list_items(
    service: Service,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return service.list_items(skip, limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: Service):
    try:
        return service.get_item(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: Service):
    return service.create_item(payload)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, payload: ItemUpdate, service: Service):
    try:
        return service.update_item(item_id, payload)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: Service) -> None:
    try:
        service.delete_item(item_id)
    except ItemNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
