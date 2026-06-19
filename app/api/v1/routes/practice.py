from fastapi import APIRouter
from fastapi import HTTPException, status

from app.schemas import BuyGoalReq, BuyGoalRes, SimpleBuyVsRentRequset, SimpleBuyVsRentResponse
from app.services.practice_goal_service import calculate_buy_goal
from app.services.practice_analysis_service import calculate_simple_buy_vs_rent


router = APIRouter(prefix="/practice", tags=["practice"])


@router.get("/hello")
def hello():
    return {"message": "Hello from FastAPI"}


@router.get("/status")
def getStatus():
    return {"message": {
        "app": "real estate analysis",
        "status": "learning"
    }}


@router.get("/properties/{property_id}")
def get_practice_property(property_id: int):
    return {
        "property_id": property_id,
        "message": f"You requested property {property_id}",
    }


@router.get("/search")
def search_property(city: str, max_price: int | None = None):
    return {
        "city": city,
        "max_price": max_price,
    }


@router.get("/filter")
def filter_properties(city: str, rooms: int | None = None, max_price: int | None = None):
    return {
        "city": city,
        "romms": rooms,
        "max_price": max_price
    }


@router.post("/buy-goal", response_model=BuyGoalRes)
def creat_buy_goal(payload: BuyGoalReq):
    return calculate_buy_goal(payload)


@router.post("/simple-buy-vs-rent", response_model=SimpleBuyVsRentResponse)
def simple_buy_vs_rent(payload: SimpleBuyVsRentRequset):
    return calculate_simple_buy_vs_rent(payload)


@router.get("/check-price")
def check_price(price: int):
    if price <= 1000000:
        return {
            "message": "Low budget"
        }
    elif price > 20000000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget too high for current MVP"
        )
    else:
        return {
            "message": "Price, recived"
        }
# class PropertyGoalRequest(BaseModel):
#     city: str = Field(..., min_length=2)
#     area: str | None = None
#     max_price_sek: int = Field(..., gt=0)
#     min_rooms: int = Field(..., gt=0)
#     max_monthly_fee_sek: int | None = Field(defualt=None, gt=0)
# @router.post("/property-goal")
# def crete_simple_property_goal(payload: PropertyGoalRequest):
#     return {
#         "message": "Property Goal Recevied",
#         "property": payload
#     }
# class BuyGoalResponse(BaseModel):
#     annual_gain: int = Field(..., gt=0)
#     is_buyable: bool = Field(...)
# @router.post("/buy-goa-text", response_model=BuyGoalResponse)
# def create_verdict(payload: PropertyGoalRequest):
#     annual_gain = 1
#     is_buyable = False
#     if payload.city == "Göteborg" and payload.max_price_sek <= 100000:
#         annual_gain = 2000
#         is_buyable = True
#     return {
#         "annual_gain": annual_gain,
#         "is_buyable": is_buyable,
#     }
