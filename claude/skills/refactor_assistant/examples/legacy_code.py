"""
Legacy Code Example

This file contains various code smells for demonstration purposes.
"""

import os
import sys


# God Class - too many methods
class DataProcessor:
    """A class that does too many things."""

    def __init__(self, data):
        self.data = data
        self.results = []
        self.errors = []
        self.cache = {}
        self.config = {}
        self.state = "initialized"

    def load_data(self, path):
        """Load data from file."""
        with open(path, 'r') as f:
            self.data = f.read()

    def save_data(self, path):
        """Save data to file."""
        with open(path, 'w') as f:
            f.write(self.data)

    def validate_data(self):
        """Validate the data."""
        if not self.data:
            return False
        return True

    def transform_data(self):
        """Transform the data."""
        # Implementation
        pass

    def filter_data(self):
        """Filter the data."""
        pass

    def sort_data(self):
        """Sort the data."""
        pass

    def aggregate_data(self):
        """Aggregate the data."""
        pass

    def analyze_data(self):
        """Analyze the data."""
        pass

    def visualize_data(self):
        """Visualize the data."""
        pass

    def export_data(self):
        """Export the data."""
        pass

    def import_data(self):
        """Import the data."""
        pass

    def backup_data(self):
        """Backup the data."""
        pass

    def restore_data(self):
        """Restore the data."""
        pass

    def clean_data(self):
        """Clean the data."""
        pass

    def normalize_data(self):
        """Normalize the data."""
        pass

    def denormalize_data(self):
        """Denormalize the data."""
        pass

    def compress_data(self):
        """Compress the data."""
        pass

    def decompress_data(self):
        """Decompress the data."""
        pass

    def encrypt_data(self):
        """Encrypt the data."""
        pass

    def decrypt_data(self):
        """Decrypt the data."""
        pass


# Long function with high complexity
def process_payment(
    amount,
    currency,
    payment_method,
    customer_id,
    merchant_id,
    metadata,
    options={}
):
    """
    Process a payment transaction.

    This function has too many parameters and is too long.
    """
    # Magic numbers
    if amount < 0.01:
        return {"error": "Amount too small"}

    if amount > 999999.99:
        return {"error": "Amount too large"}

    # Deep nesting
    if payment_method == "credit_card":
        if currency == "USD":
            if amount > 100:
                if customer_id:
                    if merchant_id:
                        # Process credit card payment
                        fee = amount * 0.029 + 0.30  # Magic numbers!
                        total = amount + fee

                        if total > 10000:
                            # Requires additional verification
                            if options.get("skip_verification"):
                                pass
                            else:
                                return {"error": "Verification required"}

                        try:
                            # Simulated API call
                            result = charge_credit_card(amount, customer_id)

                            if result:
                                if result.get("status") == "success":
                                    return {"success": True, "transaction_id": result.get("id")}
                                else:
                                    if result.get("status") == "declined":
                                        return {"error": "Card declined"}
                                    elif result.get("status") == "fraud":
                                        return {"error": "Fraud detected"}
                                    else:
                                        return {"error": "Unknown error"}
                        except:
                            # Empty except - code smell!
                            pass
                    else:
                        return {"error": "Merchant ID required"}
                else:
                    return {"error": "Customer ID required"}
            else:
                # Small transaction
                fee = 0.50
                total = amount + fee
                return {"success": True, "total": total}
        elif currency == "EUR":
            # EUR processing
            fee = amount * 0.032
            total = amount + fee
            return {"success": True, "total": total}
        elif currency == "GBP":
            # GBP processing
            fee = amount * 0.031
            total = amount + fee
            return {"success": True, "total": total}
        else:
            return {"error": "Unsupported currency"}
    elif payment_method == "bank_transfer":
        # Bank transfer processing
        if amount > 50000:
            return {"error": "Amount too large for bank transfer"}

        fee = 5.00  # Magic number
        total = amount + fee

        return {"success": True, "total": total}
    elif payment_method == "paypal":
        # PayPal processing
        fee = amount * 0.034 + 0.35  # More magic numbers!
        total = amount + fee

        return {"success": True, "total": total}
    else:
        return {"error": "Unsupported payment method"}


# Function with mutable default argument - code smell!
def add_item(item, items=[]):
    """Add item to list - DANGER: mutable default!"""
    items.append(item)
    return items


# Poor naming
def x(a, b):
    """Function with terrible names."""
    return a + b


def calc(data):
    """Another poorly named function."""
    result = 0
    for d in data:
        result += d
    return result


# Duplicate code
def calculate_discount_for_member(price):
    """Calculate discount for member."""
    if price > 100:
        discount = price * 0.2
    elif price > 50:
        discount = price * 0.1
    else:
        discount = price * 0.05

    final_price = price - discount
    tax = final_price * 0.08
    total = final_price + tax

    return total


def calculate_discount_for_vip(price):
    """Calculate discount for VIP."""
    if price > 100:
        discount = price * 0.3  # Different discount
    elif price > 50:
        discount = price * 0.15
    else:
        discount = price * 0.08

    # DUPLICATE CODE below!
    final_price = price - discount
    tax = final_price * 0.08
    total = final_price + tax

    return total


# Broad exception handling
def risky_operation(data):
    """Function with poor exception handling."""
    try:
        result = process_data(data)
        validate_result(result)
        save_result(result)
        return result
    except Exception:  # Too broad!
        return None


# Too many return statements
def validate_input(value):
    """Function with too many returns."""
    if value is None:
        return False

    if not isinstance(value, (int, float)):
        return False

    if value < 0:
        return False

    if value > 1000000:
        return False

    if value == 0:
        return False

    if value % 1 != 0:
        return False

    if value < 10:
        return False

    return True


# Helper functions (referenced but not defined)
def charge_credit_card(amount, customer_id):
    """Stub function."""
    return {"status": "success", "id": "txn_123"}


def process_data(data):
    """Stub function."""
    return data


def validate_result(result):
    """Stub function."""
    return True


def save_result(result):
    """Stub function."""
    pass
