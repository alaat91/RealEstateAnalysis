from pydantic import BaseModel, Field


class BuyGoalReq(BaseModel):
    city: str = Field(min_length=1)
    max_price_sek: int = Field(..., gt=0)
    down_payment_percent: float = Field(..., ge=0, le=100)
    time_horizon_years: int = Field(..., gt=0)


class BuyGoalRes(BaseModel):
    message: str
    city: str
    max_price_sek: int
    estimated_loan_amount_sek: int
