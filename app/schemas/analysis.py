from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RentVsBuyRequest(BaseModel):
    property_id: UUID | None = None
    title: str = "Rent vs buy analysis"

    purchase_price_sek: Decimal = Field(..., gt=0)
    down_payment_percent: Decimal = Field(default=10, ge=0, le=100)
    annual_interest_rate_percent: Decimal = Field(default=4.0, ge=0, le=30)
    monthly_brf_fee_sek: Decimal = Field(default=0, ge=0)
    monthly_rent_sek: Decimal = Field(..., gt=0)
    time_horizon_years: int = Field(default=5, ge=1, le=50)

    expected_annual_price_growth_percent: Decimal = Field(default=2.0, ge=-20, le=30)
    expected_annual_rent_inflation_percent: Decimal = Field(default=2.0, ge=-10, le=30)
    expected_annual_investment_return_percent: Decimal = Field(default=5.0, ge=-30, le=50)
    selling_cost_percent: Decimal = Field(default=2.0, ge=0, le=10)
    annual_maintenance_percent: Decimal = Field(default=0.3, ge=0, le=5)


class RentVsBuyResult(BaseModel):
    purchase_price_sek: Decimal
    down_payment_sek: Decimal
    loan_amount_sek: Decimal
    monthly_interest_cost_sek: Decimal
    monthly_brf_fee_sek: Decimal
    monthly_maintenance_sek: Decimal
    estimated_monthly_buy_cost_sek: Decimal
    estimated_monthly_rent_cost_sek: Decimal
    estimated_property_value_after_horizon_sek: Decimal
    estimated_selling_cost_sek: Decimal
    estimated_equity_after_sale_sek: Decimal
    estimated_renting_investment_value_sek: Decimal
    estimated_net_advantage_buying_sek: Decimal
    recommendation: str
    explanation: str


class AnalysisRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    property_id: UUID | None
    title: str
    purchase_price_sek: Decimal
    down_payment_sek: Decimal
    monthly_rent_sek: Decimal
    monthly_buy_cost_sek: Decimal
    estimated_five_year_net_sek: Decimal
    recommendation: str
    explanation: str
