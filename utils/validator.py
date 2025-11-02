def is_not_empty(value):
    """Checks if the given value is not empty."""
    return bool(value and value.strip())


def is_valid_price(price):
    """Checks if the input is a valid price (non-negative float)."""
    try:
        value = float(price)
        return value >= 0
    except (ValueError, TypeError):
        return False