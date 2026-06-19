from app.schemas import BuyGoalReq, BuyGoalRes


def calculate_buy_goal(payload: BuyGoalReq) -> BuyGoalRes:
    loan_amount = payload.max_price_sek * \
        (1 - payload.down_payment_percent / 100)
    return BuyGoalRes(
        message="Goal received",
        city=payload.city,
        max_price_sek=payload.max_price_sek,
        estimated_loan_amount_sek=round(loan_amount),
    )
