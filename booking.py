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

EXCHANGE_RATES = {
    "usd": 1.0,
    "eur": 0.92,
    "gbp": 0.79,
    "jpy": 149.50,
}

CURRENCY_SYMBOLS = {
    "usd": "$",
    "eur": "€",
    "gbp": "£",
    "jpy": "¥",
}


def calculate_total_price(
    base_price: float, nights: int, guests: int, currency: str = "usd"
) -> float:
    """Calculate total booking price from base nightly rate.

    Args:
        base_price: Nightly rate per person in USD.
        nights: Number of nights to stay.
        guests: Number of guests.
        currency: Target currency code, one of 'usd', 'eur', 'gbp', 'jpy'.
            Defaults to 'usd'.

    Returns:
        Total price converted to the requested currency as a float.

    Raises:
        ValueError: If nights is zero or less.
        ValueError: If guests is zero or less.
        ValueError: If currency is not a supported currency code.
    """
    if nights <= 0:
        raise ValueError(f"nights must be greater than 0, got {nights}")
    if guests <= 0:
        raise ValueError(f"guests must be greater than 0, got {guests}")
    if currency.lower() not in EXCHANGE_RATES:
        raise ValueError(
            f"'{currency}' is not a supported currency. "
            f"Supported: {list(EXCHANGE_RATES.keys())}"
        )
    total_usd = base_price * nights * guests
    return total_usd * EXCHANGE_RATES[currency.lower()]


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
    base_price: float, nights: int, guests: int, month: int, country: str,
    currency: str = "usd"
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
        currency: Target currency code, one of 'usd', 'eur', 'gbp', 'jpy'.
            Defaults to 'usd'.

    Returns:
        Final price after discount and tax, converted to the requested currency.
        JPY is rounded to a whole number; all other currencies to 2 decimal places.

    Raises:
        ValueError: If nights is zero or less.
        ValueError: If guests is zero or less.
        ValueError: If month is not between 1 and 12.
        ValueError: If country is not in the supported list.
        ValueError: If currency is not a supported currency code.
    """
    total = calculate_total_price(base_price, nights, guests, currency)
    discounted = apply_seasonal_discount(total, month)
    tax = calculate_tax(discounted, country)
    decimals = 0 if currency.lower() == "jpy" else 2
    return round(discounted + tax, decimals)


def format_booking_summary(trip_name: str, destination: str,
                            total_price: float, guests: int,
                            currency: str = "usd") -> str:
    """Format a human-readable booking summary string.

    Args:
        trip_name: Name of the trip package.
        destination: Destination country.
        total_price: Final total price including tax.
        guests: Number of guests.
        currency: Currency code used for display, one of 'usd', 'eur', 'gbp',
            'jpy'. Defaults to 'usd'.

    Returns:
        A formatted multi-line booking summary string with the correct
        currency symbol.

    Raises:
        ValueError: If currency is not a supported currency code.
    """
    if currency.lower() not in CURRENCY_SYMBOLS:
        raise ValueError(
            f"'{currency}' is not a supported currency. "
            f"Supported: {list(CURRENCY_SYMBOLS.keys())}"
        )
    symbol = CURRENCY_SYMBOLS[currency.lower()]
    decimals = 0 if currency.lower() == "jpy" else 2
    price_per_person = total_price / guests
    return (
        f"Booking Summary\n"
        f"  Trip:             {trip_name}\n"
        f"  Destination:      {destination}\n"
        f"  Total price:      {symbol}{total_price:.{decimals}f}\n"
        f"  Guests:           {guests}\n"
        f"  Price per person: {symbol}{price_per_person:.{decimals}f}"
    )
