from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class PropertyGoal(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "property_goals"

    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    area: Mapped[str | None] = mapped_column(
        String(100), index=True, nullable=True)

    max_price_sek: Mapped[Decimal] = mapped_column(
        Numeric(14, 2), nullable=False)
    min_rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    max_monthly_fee_sek: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2), nullable=False)

    time_horizon_years: Mapped[int] = mapped_column(
        Integer, nullable=False, default=5)
