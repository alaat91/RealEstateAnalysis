from pydantic import BaseModel, Field


class SimpleBuyVsRentRequset(BaseModel):
    purchase_price_sek: int = Field(..., gt=0)
    down_payment_percent: float = Field(..., gt=0)
    annual_interest_rate_percent: float = Field(..., gt=0)
    monthly_brf_fee_sek: int = Field(..., ge=0)
    monthly_rent_sek: int = Field(..., ge=0)


class SimpleBuyVsRentResponse(BaseModel):
    down_payment_sek: int
    loan_amount_sek: int
    monthly_interest_cost_sek: int
    monthly_buy_cost_sek: int
    monthly_rent_sek: int
    monthly_difference_sek: int
    recommendation: str
