# tests/test_booking.py — Trip Booking Calculator Tests
# Existing test suite from Lecture 6.6

import pytest
from booking import (
    calculate_total_price,
    apply_seasonal_discount,
    calculate_tax,
    get_price_category,
    format_booking_summary,
    calculate_final_price,
)


# ── Happy Path Tests ──────────────────────────────────────────────────────────

def test_calculate_total_price_returns_correct_value():
    """Normal case: 3 nights, 2 guests at $100/night = $600."""
    assert calculate_total_price(100, 3, 2) == 600.0


def test_apply_seasonal_discount_january():
    """January has 15% discount — $1000 becomes $850."""
    assert apply_seasonal_discount(1000, 1) == 850.0


def test_calculate_tax_france():
    """France has 20% tax — $500 tax = $100."""
    assert calculate_tax(500, "france") == 100.0


def test_get_price_category_budget():
    """Under $500 should be 'budget'."""
    assert get_price_category(400) == "budget"


def test_get_price_category_mid_range():
    """$1000 should be 'mid-range'."""
    assert get_price_category(1000) == "mid-range"


def test_get_price_category_luxury():
    """Over $2000 should be 'luxury'."""
    assert get_price_category(2500) == "luxury"


def test_format_booking_summary_contains_trip_name():
    """Summary string must contain the trip name."""
    result = format_booking_summary("Paris Adventure", "france", 1200.0, 2)
    assert "Paris Adventure" in result


# ── Edge Case Tests ───────────────────────────────────────────────────────────

def test_calculate_total_price_zero_nights_raises():
    """nights=0 must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_total_price(100, 0, 2)


def test_calculate_total_price_zero_guests_raises():
    """guests=0 must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_total_price(100, 3, 0)


def test_apply_seasonal_discount_month_zero_raises():
    """month=0 is invalid and must raise ValueError."""
    with pytest.raises(ValueError):
        apply_seasonal_discount(1000, 0)


def test_apply_seasonal_discount_month_13_raises():
    """month=13 is invalid and must raise ValueError."""
    with pytest.raises(ValueError):
        apply_seasonal_discount(1000, 13)


def test_get_price_category_negative_price_raises():
    """Negative price must raise ValueError."""
    with pytest.raises(ValueError):
        get_price_category(-100)


def test_calculate_tax_unknown_country_raises():
    """Unknown country must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_tax(500, "mars")


# ── calculate_final_price Tests ───────────────────────────────────────────────

def test_calculate_final_price_returns_correct_value():
    """Happy path: $100/night, 3 nights, 2 guests, April (no discount), Japan (10% tax).

    Total = 100 * 3 * 2 = 600. Discount = 0%. Tax = 60. Final = 660.
    """
    assert calculate_final_price(100, 3, 2, 4, "japan") == 660.0


def test_calculate_final_price_applies_discount():
    """January 15% discount should reduce the base before tax is applied.

    Total = 100 * 2 * 1 = 200. Discounted = 170. Tax (USA 8%) = 13.6. Final = 183.6.
    """
    assert calculate_final_price(100, 2, 1, 1, "usa") == 183.6


def test_calculate_final_price_invalid_nights_raises():
    """nights=0 must propagate ValueError from calculate_total_price."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 0, 2, 4, "japan")


def test_calculate_final_price_invalid_guests_raises():
    """guests=0 must propagate ValueError from calculate_total_price."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 0, 4, "japan")


def test_calculate_final_price_invalid_month_raises():
    """month=13 must propagate ValueError from apply_seasonal_discount."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 2, 13, "japan")


def test_calculate_final_price_invalid_country_raises():
    """Unsupported country must propagate ValueError from calculate_tax."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 2, 4, "mars")


# ── Multi-currency Tests ──────────────────────────────────────────────────────

def test_calculate_total_price_eur_conversion():
    """EUR conversion: $600 USD * 0.92 = 552.0 EUR."""
    assert calculate_total_price(100, 3, 2, "eur") == 552.0


def test_calculate_total_price_gbp_conversion():
    """GBP conversion: $600 USD * 0.79 = 474.0 GBP."""
    assert calculate_total_price(100, 3, 2, "gbp") == 474.0


def test_calculate_total_price_jpy_conversion():
    """JPY conversion: $600 USD * 149.50 = 89700.0 JPY."""
    assert calculate_total_price(100, 3, 2, "jpy") == 89700.0


def test_calculate_total_price_invalid_currency_raises():
    """Unsupported currency code must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_total_price(100, 3, 2, "xyz")


def test_calculate_final_price_eur():
    """EUR final price: $100/night, 3 nights, 2 guests, April (no discount), Japan (10% tax).

    Total USD = 600. EUR = 552.0. Tax (10%) = 55.2. Final = 607.2 EUR.
    """
    assert calculate_final_price(100, 3, 2, 4, "japan", "eur") == 607.2


def test_calculate_final_price_jpy_rounds_to_whole_number():
    """JPY final price must be a whole number (no decimal subdivision).

    Total USD = 600. JPY = 89700. Tax (10%) = 8970. Final = 98670 JPY.
    """
    result = calculate_final_price(100, 3, 2, 4, "japan", "jpy")
    assert result == int(result)


def test_calculate_final_price_invalid_currency_raises():
    """Unsupported currency must raise ValueError."""
    with pytest.raises(ValueError):
        calculate_final_price(100, 3, 2, 4, "japan", "xyz")


def test_format_booking_summary_eur_symbol():
    """EUR summary must display the € symbol."""
    result = format_booking_summary("Alps Escape", "france", 607.2, 2, "eur")
    assert "€" in result


def test_format_booking_summary_gbp_symbol():
    """GBP summary must display the £ symbol."""
    result = format_booking_summary("London Tour", "usa", 500.0, 2, "gbp")
    assert "£" in result


def test_format_booking_summary_jpy_no_decimal():
    """JPY summary must display prices with no decimal places."""
    result = format_booking_summary("Tokyo Trip", "japan", 98670.0, 2, "jpy")
    assert "¥98670" in result


def test_format_booking_summary_invalid_currency_raises():
    """Unsupported currency must raise ValueError."""
    with pytest.raises(ValueError):
        format_booking_summary("Test Trip", "france", 500.0, 2, "xyz")
