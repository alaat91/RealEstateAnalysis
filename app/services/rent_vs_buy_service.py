from decimal import ROUND_HALF_UP, Decimal

from app.schemas import RentVsBuyRequest, RentVsBuyResult

Money = Decimal


def _money(value: Decimal) -> Money:
    return value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def _percent(value: Decimal) -> Decimal:
    return value / Decimal("100")


def calculate_rent_vs_buy(payload: RentVsBuyRequest) -> RentVsBuyResult:
    """Simple deterministic MVP model.

    This is intentionally conservative and explainable. Later you can add Swedish-specific
    interest tax deduction, amortization requirements, rent queue assumptions, BRF risk,
    and Monte Carlo scenarios.
    """
    purchase_price = payload.purchase_price_sek
    years = Decimal(payload.time_horizon_years)
    months = Decimal(payload.time_horizon_years * 12)

    down_payment = purchase_price * _percent(payload.down_payment_percent)
    loan_amount = purchase_price - down_payment

    annual_interest_rate = _percent(payload.annual_interest_rate_percent)
    monthly_interest_cost = loan_amount * annual_interest_rate / Decimal("12")

    annual_maintenance = purchase_price * _percent(payload.annual_maintenance_percent)
    monthly_maintenance = annual_maintenance / Decimal("12")

    monthly_buy_cost = monthly_interest_cost + payload.monthly_brf_fee_sek + monthly_maintenance

    price_growth = _percent(payload.expected_annual_price_growth_percent)
    future_property_value = purchase_price * ((Decimal("1") + price_growth) ** int(years))
    selling_cost = future_property_value * _percent(payload.selling_cost_percent)
    equity_after_sale = future_property_value - selling_cost - loan_amount

    investment_return = _percent(payload.expected_annual_investment_return_percent)
    rent_inflation = _percent(payload.expected_annual_rent_inflation_percent)

    # Renting scenario: down payment is invested.
    # If rent is cheaper than buying, invest the monthly difference.
    invested_down_payment = down_payment * ((Decimal("1") + investment_return) ** int(years))

    monthly_difference = monthly_buy_cost - payload.monthly_rent_sek
    invested_monthly_savings = Decimal("0")
    if monthly_difference > 0:
        monthly_return = investment_return / Decimal("12")
        for month in range(int(months)):
            invested_monthly_savings += monthly_difference * (
                (Decimal("1") + monthly_return) ** month
            )

    # Approximate total rent paid with annual inflation. This is used only for explanation now.
    total_rent_paid = Decimal("0")
    current_rent = payload.monthly_rent_sek
    for _year in range(int(years)):
        total_rent_paid += current_rent * Decimal("12")
        current_rent *= Decimal("1") + rent_inflation

    renting_investment_value = invested_down_payment + invested_monthly_savings
    net_advantage_buying = equity_after_sale - renting_investment_value

    if net_advantage_buying > purchase_price * Decimal("0.03"):
        recommendation = "buying_looks_better"
        explanation = (
            "Buying looks financially stronger in this scenario. The estimated equity after "
            "selling is higher than the value of investing the down payment and monthly savings."
        )
    elif net_advantage_buying < purchase_price * Decimal("-0.03"):
        recommendation = "renting_looks_better"
        explanation = (
            "Renting looks financially safer in this scenario. The expected investment value "
            "from keeping the down payment invested is higher than the estimated buying outcome."
        )
    else:
        recommendation = "close_call"
        explanation = (
            "Buying and renting are close in this scenario. Small changes in interest rate, "
            "price growth, rent level, or time horizon can change the result."
        )

    explanation += (
        f" Approximate total rent paid over the period: {int(_money(total_rent_paid))} SEK."
    )

    return RentVsBuyResult(
        purchase_price_sek=_money(purchase_price),
        down_payment_sek=_money(down_payment),
        loan_amount_sek=_money(loan_amount),
        monthly_interest_cost_sek=_money(monthly_interest_cost),
        monthly_brf_fee_sek=_money(payload.monthly_brf_fee_sek),
        monthly_maintenance_sek=_money(monthly_maintenance),
        estimated_monthly_buy_cost_sek=_money(monthly_buy_cost),
        estimated_monthly_rent_cost_sek=_money(payload.monthly_rent_sek),
        estimated_property_value_after_horizon_sek=_money(future_property_value),
        estimated_selling_cost_sek=_money(selling_cost),
        estimated_equity_after_sale_sek=_money(equity_after_sale),
        estimated_renting_investment_value_sek=_money(renting_investment_value),
        estimated_net_advantage_buying_sek=_money(net_advantage_buying),
        recommendation=recommendation,
        explanation=explanation,
    )
