from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class PropertyGoalCreate(BaseModel):
    city: str = Field(..., min_length=2, max_length=100)
    area: str | None = Field(default=None, max_length=100)

    max_price_sek: Decimal = Field(..., gt=0)
    min_rooms: int = Field(..., gt=0)
    max_monthly_fee_sek: Decimal = Field(..., gt=0)

    time_horizon_years: int = Field(default=5, gt=0, le=50)


class PropertyGoalUpdate(BaseModel):
    city: str | None = Field(default=None, min_length=2, max_length=100)
    area: str | None = Field(default=None, max_length=100)

    max_price_sek: Decimal | None = Field(default=None, gt=0)
    min_rooms: int | None = Field(default=None, gt=0)
    max_monthly_fee_sek: Decimal | None = Field(default=None, gt=0)

    time_horizon_years: int | None = Field(default=None, gt=0, le=50)


class PropertyGoalRead(BaseModel):
    id: UUID
    city: str
    area: str | None
    max_price_sek: Decimal
    min_rooms: int
    max_monthly_fee_sek: Decimal
    time_horizon_years: int
    model_config = {"from_attributes": True}
