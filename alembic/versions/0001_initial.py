"""Initial schema with properties and analyses.

Revision ID: 0001_initial
Revises:
Create Date: 2026-06-13
"""
from collections.abc import Sequence

import geoalchemy2
import sqlalchemy as sa
from alembic import op

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    op.create_table(
        "properties",
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("area", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("ownership_type", sa.String(length=50), nullable=False),
        sa.Column("property_type", sa.String(length=50), nullable=False),
        sa.Column("asking_price_sek", sa.Numeric(14, 2), nullable=False),
        sa.Column("monthly_fee_sek", sa.Numeric(12, 2), nullable=False),
        sa.Column("living_area_sqm", sa.Numeric(8, 2), nullable=False),
        sa.Column("rooms", sa.Numeric(4, 1), nullable=False),
        sa.Column("latitude", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitude", sa.Numeric(10, 7), nullable=True),
        sa.Column(
            "location",
            geoalchemy2.types.Geometry(geometry_type="POINT", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_properties")),
    )
    op.create_index(op.f("ix_properties_area"), "properties", ["area"], unique=False)
    op.create_index(op.f("ix_properties_city"), "properties", ["city"], unique=False)
    op.create_index(op.f("ix_properties_ownership_type"), "properties", ["ownership_type"], unique=False)
    op.create_index(op.f("ix_properties_property_type"), "properties", ["property_type"], unique=False)

    op.create_table(
        "analyses",
        sa.Column("property_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("purchase_price_sek", sa.Numeric(14, 2), nullable=False),
        sa.Column("down_payment_sek", sa.Numeric(14, 2), nullable=False),
        sa.Column("monthly_rent_sek", sa.Numeric(12, 2), nullable=False),
        sa.Column("monthly_buy_cost_sek", sa.Numeric(12, 2), nullable=False),
        sa.Column("estimated_five_year_net_sek", sa.Numeric(14, 2), nullable=False),
        sa.Column("recommendation", sa.String(length=50), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["property_id"], ["properties.id"], name=op.f("fk_analyses_property_id_properties")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_analyses")),
    )


def downgrade() -> None:
    op.drop_table("analyses")
    op.drop_index(op.f("ix_properties_property_type"), table_name="properties")
    op.drop_index(op.f("ix_properties_ownership_type"), table_name="properties")
    op.drop_index(op.f("ix_properties_city"), table_name="properties")
    op.drop_index(op.f("ix_properties_area"), table_name="properties")
    op.drop_table("properties")
