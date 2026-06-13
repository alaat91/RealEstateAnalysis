from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PropertyBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    city: str = Field(..., min_length=1, max_length=120)
    area: str = Field(..., min_length=1, max_length=120)
    address: str | None = None
    ownership_type: str = "bostadsratt"
    property_type: str = "apartment"
    asking_price_sek: Decimal = Field(..., gt=0)
    monthly_fee_sek: Decimal = Field(default=0, ge=0)
    living_area_sqm: Decimal = Field(..., gt=0)
    rooms: Decimal = Field(..., gt=0)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)
    source_url: HttpUrl | None = None
    description: str | None = None


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    city: str | None = Field(default=None, min_length=1, max_length=120)
    area: str | None = Field(default=None, min_length=1, max_length=120)
    address: str | None = None
    ownership_type: str | None = None
    property_type: str | None = None
    asking_price_sek: Decimal | None = Field(default=None, gt=0)
    monthly_fee_sek: Decimal | None = Field(default=None, ge=0)
    living_area_sqm: Decimal | None = Field(default=None, gt=0)
    rooms: Decimal | None = Field(default=None, gt=0)
    latitude: Decimal | None = Field(default=None, ge=-90, le=90)
    longitude: Decimal | None = Field(default=None, ge=-180, le=180)
    source_url: HttpUrl | None = None
    description: str | None = None


class PropertyRead(PropertyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
