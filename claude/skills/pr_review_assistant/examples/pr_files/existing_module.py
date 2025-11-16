"""
Existing Module - Modified

This file represents an existing module being modified in the PR.
"""


def calculate_fee(amount):
    """
    Calculate transaction fee.

    ISSUES:
    - No test file for this change
    - Magic number (0.029)
    """
    # Calculate 2.9% fee
    fee = amount * 0.029
    return fee


def validate_amount(amount):
    """Validate transaction amount."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if amount > 999999:
        raise ValueError("Amount too large")

    return True
