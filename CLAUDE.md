# CLAUDE.md — Trip Booking Calculator

## Project Overview
A Python library for calculating trip booking prices.
It handles base pricing, seasonal discounts, tax calculations,
and booking summaries for a travel booking platform.

## Coding Standards
- Use Python 3.10+
- Follow PEP 8 style guidelines
- Add a docstring to every function
- Use type hints for all function parameters and return values
- Use f-strings for all string formatting
- Raise ValueError with a clear message for invalid inputs

## Git & Branching Conventions
- Branch names must follow: feature/<short-description>  or  fix/<short-description>
- Commit messages must follow this format:
    <type>: <short summary in present tense>
    Types allowed: feat, fix, refactor, test, docs, chore
    Examples:
      feat: add wishlist feature to booking summary
      fix: handle zero guests in calculate_total_price
      test: add edge case tests for apply_seasonal_discount
- Never commit directly to main
- Every new feature must be on its own branch
- PR description must reference which functions were changed

## Project Structure
```
trip_booking/
├── CLAUDE.md              ← You are here
├── booking.py             ← Main booking logic
└── tests/
    └── test_booking.py    ← Test suite
```

## Testing Standards
- Use pytest for all tests
- Run tests with: pytest tests/ -v
- Every new function must have at least one test

## Off-Limits
- Do NOT modify CLAUDE.md unless explicitly asked
- Do NOT push directly to main branch
