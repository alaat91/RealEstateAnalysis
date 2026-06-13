from decimal import Decimal
from uuid import UUID

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Property(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "properties"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    area: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ownership_type: Mapped[str] = mapped_column(String(50), default="bostadsratt", index=True)
    property_type: Mapped[str] = mapped_column(String(50), default="apartment", index=True)

    asking_price_sek: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    monthly_fee_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    living_area_sqm: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    rooms: Mapped[Decimal] = mapped_column(Numeric(4, 1), nullable=False)

    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    location = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    analyses: Mapped[list["Analysis"]] = relationship(back_populates="property")


class Analysis(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "analyses"

    property_id: Mapped[UUID | None] = mapped_column(ForeignKey("properties.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    purchase_price_sek: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    down_payment_sek: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    monthly_rent_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    monthly_buy_cost_sek: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    estimated_five_year_net_sek: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    recommendation: Mapped[str] = mapped_column(String(50), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    property: Mapped[Property | None] = relationship(back_populates="analyses")
