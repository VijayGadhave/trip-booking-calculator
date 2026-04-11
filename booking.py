# booking.py — Trip Booking Calculator
# Core pricing logic for the travel booking platform.

SEASONAL_DISCOUNTS = {
    1: 0.15,   # January   — 15% off (low season)
    2: 0.15,   # February  — 15% off
    3: 0.05,   # March     — 5% off
    4: 0.0,    # April     — no discount
    5: 0.0,    # May       — no discount
    6: 0.0,    # June      — no discount
    7: 0.0,    # July      — no discount
    8: 0.0,    # August    — no discount
    9: 0.05,   # September — 5% off (shoulder season)
    10: 0.05,  # October   — 5% off
    11: 0.10,  # November  — 10% off
    12: 0.10,  # December  — 10% off
}

TAX_RATES = {
    "france":    0.20,
    "japan":     0.10,
    "indonesia": 0.11,
    "usa":       0.08,
    "australia": 0.10,
}


def calculate_total_price(base_price: float, nights: int, guests: int) -> float:
    """Calculate total booking price from base nightly rate.

    Args:
        base_price: Nightly rate per person in USD.
        nights: Number of nights to stay.
        guests: Number of guests.

    Returns:
        Total price as a float.

    Raises:
        ValueError: If nights or guests is zero or less.
    """
    if nights <= 0:
        raise ValueError(f"nights must be greater than 0, got {nights}")
    if guests <= 0:
        raise ValueError(f"guests must be greater than 0, got {guests}")
    return base_price * nights * guests


def apply_seasonal_discount(price: float, month: int) -> float:
    """Apply a seasonal discount to a price based on travel month.

    Args:
        price: Original price in USD.
        month: Month of travel as an integer (1=January, 12=December).

    Returns:
        Discounted price as a float.

    Raises:
        ValueError: If month is not between 1 and 12.
    """
    if month < 1 or month > 12:
        raise ValueError(f"month must be between 1 and 12, got {month}")
    discount = SEASONAL_DISCOUNTS[month]
    return round(price * (1 - discount), 2)


def calculate_tax(price: float, country: str) -> float:
    """Calculate the tax amount for a given country.

    Args:
        price: Pre-tax price in USD.
        country: Country name in lowercase (e.g. 'france', 'japan').

    Returns:
        Tax amount as a float (not the total — just the tax).

    Raises:
        ValueError: If country is not in the supported list.
    """
    if country.lower() not in TAX_RATES:
        raise ValueError(
            f"'{country}' is not a supported country. "
            f"Supported: {list(TAX_RATES.keys())}"
        )
    rate = TAX_RATES[country.lower()]
    return round(price * rate, 2)


def get_price_category(total_price: float) -> str:
    """Categorise a trip by total price.

    Args:
        total_price: Final price of the trip in USD.

    Returns:
        'budget' for under $500, 'mid-range' for $500-$2000,
        'luxury' for over $2000.

    Raises:
        ValueError: If total_price is negative.
    """
    if total_price < 0:
        raise ValueError(f"total_price cannot be negative, got {total_price}")
    if total_price < 500:
        return "budget"
    elif total_price <= 2000:
        return "mid-range"
    else:
        return "luxury"


def calculate_final_price(
    base_price: float, nights: int, guests: int, month: int, country: str
) -> float:
    """Calculate the complete final price including seasonal discount and tax.

    Combines calculate_total_price, apply_seasonal_discount, and
    calculate_tax into a single call.

    Args:
        base_price: Nightly rate per person in USD.
        nights: Number of nights to stay.
        guests: Number of guests.
        month: Month of travel as an integer (1=January, 12=December).
        country: Destination country name in lowercase (e.g. 'france').

    Returns:
        Final price after discount and tax as a float.

    Raises:
        ValueError: If nights or guests is zero or less.
        ValueError: If month is not between 1 and 12.
        ValueError: If country is not in the supported list.
    """
    total = calculate_total_price(base_price, nights, guests)
    discounted = apply_seasonal_discount(total, month)
    tax = calculate_tax(discounted, country)
    return round(discounted + tax, 2)


def format_booking_summary(trip_name: str, destination: str,
                            total_price: float, guests: int) -> str:
    """Format a human-readable booking summary string.

    Args:
        trip_name: Name of the trip package.
        destination: Destination country.
        total_price: Final total price including tax.
        guests: Number of guests.

    Returns:
        A formatted multi-line booking summary string.
    """
    price_per_person = total_price / guests
    return (
        f"Booking Summary\n"
        f"  Trip:             {trip_name}\n"
        f"  Destination:      {destination}\n"
        f"  Total price:      ${total_price:.2f}\n"
        f"  Guests:           {guests}\n"
        f"  Price per person: ${price_per_person:.2f}"
    )
