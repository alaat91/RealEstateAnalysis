from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_rent_vs_buy_analysis_returns_result() -> None:
    payload = {
        "purchase_price_sek": 3_500_000,
        "down_payment_percent": 10,
        "annual_interest_rate_percent": 4.0,
        "monthly_brf_fee_sek": 5_000,
        "monthly_rent_sek": 13_000,
        "time_horizon_years": 5,
        "expected_annual_price_growth_percent": 2.0,
        "expected_annual_rent_inflation_percent": 2.0,
        "expected_annual_investment_return_percent": 5.0,
        "selling_cost_percent": 2.0,
        "annual_maintenance_percent": 0.3,
    }

    response = client.post("/api/v1/analyses/rent-vs-buy", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["purchase_price_sek"] == "3500000"
    assert data["loan_amount_sek"] == "3150000"
    assert "recommendation" in data
    assert "explanation" in data
