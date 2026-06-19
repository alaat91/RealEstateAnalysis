from app.main import app
from fastapi.testclient import TestClient

from app.schemas.practice_analysis import SimpleBuyVsRentRequset
from app.services.practice_analysis_service import calculate_simple_buy_vs_rent
client = TestClient(app)


def test_simple_buy_vs_rent_calculates_loan_amount():
    payload = SimpleBuyVsRentRequset(
        purchase_price_sek=3_750_000,
        down_payment_percent=10,
        annual_interest_rate_percent=4,
        monthly_brf_fee_sek=5200,
        monthly_rent_sek=13500,
    )

    result = calculate_simple_buy_vs_rent(payload)

    assert result.down_payment_sek == 375_000
    assert result.loan_amount_sek == 3_375_000


def test_monthly_interest_cost_sek():
    payload = SimpleBuyVsRentRequset(
        purchase_price_sek=3_750_000,
        down_payment_percent=10,
        annual_interest_rate_percent=4,
        monthly_brf_fee_sek=5200,
        monthly_rent_sek=13500,
    )

    result = calculate_simple_buy_vs_rent(payload)

    monthly_interest_rate = 11250

    assert result.monthly_interest_cost_sek == monthly_interest_rate
