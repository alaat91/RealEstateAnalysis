from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.property_repository import (
    create_property,
    delete_property,
    get_property,
    list_properties,
    update_property,
)
from app.schemas import PropertyCreate, PropertyRead, PropertyUpdate

router = APIRouter(prefix="/properties", tags=["properties"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=PropertyRead, status_code=status.HTTP_201_CREATED)
def create(payload: PropertyCreate, db: DbSession):
    return create_property(db, payload)


@router.get("", response_model=list[PropertyRead])
def list_(
    db: DbSession,
    city: str | None = Query(default=None),
    area: str | None = Query(default=None),
):
    return list_properties(db, city=city, area=area)


@router.get("/{property_id}", response_model=PropertyRead)
def get(property_id: UUID, db: DbSession):
    db_property = get_property(db, property_id)
    if db_property is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return db_property


@router.patch("/{property_id}", response_model=PropertyRead)
def update(property_id: UUID, payload: PropertyUpdate, db: DbSession):
    db_property = get_property(db, property_id)
    if db_property is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    return update_property(db, db_property, payload)


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(property_id: UUID, db: DbSession):
    db_property = get_property(db, property_id)
    if db_property is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Property not found")
    delete_property(db, db_property)
    return None
