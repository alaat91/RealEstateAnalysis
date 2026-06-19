from app.schemas import SimpleBuyVsRentRequset, SimpleBuyVsRentResponse
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_simple_buy_vs_rent(payload: SimpleBuyVsRentRequset) -> SimpleBuyVsRentResponse:
    down_payment = payload.purchase_price_sek * \
        (payload.down_payment_percent / 100)
    loan_amount = payload.purchase_price_sek - down_payment
    logger.info(f"Down payment: {down_payment}")

    monthly_interest = (
        loan_amount * (payload.annual_interest_rate_percent / 100)) / 12
    monthly_buy_cost = monthly_interest + payload.monthly_brf_fee_sek

    monthly_difference = monthly_buy_cost - payload.monthly_rent_sek

    if monthly_difference < 0:
        recommendation = "buying_has_lower_monthly_cost"
    elif monthly_difference > 0:
        recommendation = "renting_has_lower_monthly_cost"
    else:
        recommendation = "monthly_cost_is_equal"

    return SimpleBuyVsRentResponse(
        down_payment_sek=round(down_payment),
        loan_amount_sek=round(loan_amount),
        monthly_interest_cost_sek=round(monthly_interest),
        monthly_buy_cost_sek=round(monthly_buy_cost),
        monthly_rent_sek=payload.monthly_rent_sek,
        monthly_difference_sek=round(monthly_difference),
        recommendation=recommendation,
    )
