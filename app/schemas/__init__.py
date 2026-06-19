from app.schemas.analysis import AnalysisRead, RentVsBuyRequest, RentVsBuyResult
from app.schemas.property import PropertyCreate, PropertyRead, PropertyUpdate
from app.schemas.practice_goal_schemas import BuyGoalReq, BuyGoalRes
from app.schemas.practice_analysis import SimpleBuyVsRentRequset, SimpleBuyVsRentResponse

__all__ = [
    "AnalysisRead",
    "PropertyCreate",
    "PropertyRead",
    "PropertyUpdate",
    "RentVsBuyRequest",
    "RentVsBuyResult",
    "BuyGoalReq",
    "BuyGoalRes",
    "SimpleBuyVsRentRequset",
    "SimpleBuyVsRentResponse"
]
