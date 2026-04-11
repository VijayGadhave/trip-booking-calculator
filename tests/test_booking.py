# tests/test_booking.py — Trip Booking Calculator Tests
# Existing test suite from Lecture 6.6

import pytest
from booking import (
    calculate_total_price,
    apply_seasonal_discount,
    calculate_tax,
    get_price_category,
    format_booking_summary,
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
