from uuid import UUID

from geoalchemy2 import WKTElement
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Property
from app.schemas import PropertyCreate, PropertyUpdate


def _make_point(longitude, latitude):
    if longitude is None or latitude is None:
        return None
    return WKTElement(f"POINT({longitude} {latitude})", srid=4326)


def create_property(db: Session, payload: PropertyCreate) -> Property:
    data = payload.model_dump()
    data["source_url"] = str(data["source_url"]) if data.get("source_url") else None
    data["location"] = _make_point(data.get("longitude"), data.get("latitude"))
    db_property = Property(**data)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def list_properties(
    db: Session, *, city: str | None = None, area: str | None = None
) -> list[Property]:
    statement = select(Property).order_by(Property.created_at.desc())
    if city:
        statement = statement.where(Property.city.ilike(f"%{city}%"))
    if area:
        statement = statement.where(Property.area.ilike(f"%{area}%"))
    return list(db.scalars(statement).all())


def get_property(db: Session, property_id: UUID) -> Property | None:
    return db.get(Property, property_id)


def update_property(db: Session, db_property: Property, payload: PropertyUpdate) -> Property:
    data = payload.model_dump(exclude_unset=True)
    if "source_url" in data and data["source_url"] is not None:
        data["source_url"] = str(data["source_url"])
    if "latitude" in data or "longitude" in data:
        latitude = data.get("latitude", db_property.latitude)
        longitude = data.get("longitude", db_property.longitude)
        data["location"] = _make_point(longitude, latitude)

    for field, value in data.items():
        setattr(db_property, field, value)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def delete_property(db: Session, db_property: Property) -> None:
    db.delete(db_property)
    db.commit()
