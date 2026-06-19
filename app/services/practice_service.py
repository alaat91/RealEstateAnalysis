def calculate_down_payment(purches_price: int, down_payment_percent: float) -> int:
    down_payment: int = purches_price * (down_payment_percent / 100)
    return round(down_payment)


def calculate_loan_amount(purches_price: int, down_payment_percent: float) -> int:
    loan_amount: int = purches_price - \
        (purches_price * (down_payment_percent / 100))
    return round(loan_amount)
