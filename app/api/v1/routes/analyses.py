from fastapi import APIRouter

from app.schemas import RentVsBuyRequest, RentVsBuyResult
from app.services.rent_vs_buy_service import calculate_rent_vs_buy

router = APIRouter(prefix="/analyses", tags=["analyses"])


@router.post("/rent-vs-buy", response_model=RentVsBuyResult)
def rent_vs_buy(payload: RentVsBuyRequest) -> RentVsBuyResult:
    return calculate_rent_vs_buy(payload)
