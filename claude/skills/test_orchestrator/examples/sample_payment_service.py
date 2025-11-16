"""
Sample Payment Service for demonstrating test generation.

This is a realistic example of code that needs comprehensive testing.
"""


class InvalidAmountError(Exception):
    """Raised when payment amount is invalid."""
    pass


class PaymentGatewayError(Exception):
    """Raised when payment gateway returns an error."""
    pass


class TransactionNotFoundError(Exception):
    """Raised when transaction is not found."""
    pass


def validate_amount(amount):
    """
    Validate payment amount.

    Args:
        amount: Payment amount to validate

    Returns:
        True if valid

    Raises:
        InvalidAmountError: If amount is invalid
    """
    if amount is None:
        raise InvalidAmountError("Amount cannot be None")

    if amount <= 0:
        raise InvalidAmountError("Amount must be positive")

    if amount > 1000000:
        raise InvalidAmountError("Amount exceeds maximum limit")

    return True


def process_payment(amount, currency, card_token, gateway=None):
    """
    Process a payment transaction.

    Args:
        amount: Payment amount
        currency: Currency code (USD, EUR, etc.)
        card_token: Tokenized card information
        gateway: Payment gateway instance (optional)

    Returns:
        dict: Payment result with status and transaction_id

    Raises:
        InvalidAmountError: If amount is invalid
        PaymentGatewayError: If gateway returns an error
    """
    # Validate amount
    validate_amount(amount)

    # Validate currency
    valid_currencies = ["USD", "EUR", "GBP"]
    if currency not in valid_currencies:
        raise ValueError(f"Unsupported currency: {currency}")

    # Process payment through gateway
    if gateway:
        try:
            result = gateway.charge(amount, currency, card_token)
            return {
                "status": "success",
                "transaction_id": result.get("id"),
                "amount": amount,
                "currency": currency
            }
        except Exception as e:
            raise PaymentGatewayError(f"Gateway error: {str(e)}")
    else:
        # Mock success for testing without gateway
        return {
            "status": "success",
            "transaction_id": "mock_tx_123",
            "amount": amount,
            "currency": currency
        }


def process_refund(transaction_id, amount, gateway=None, db=None):
    """
    Process a refund for a transaction.

    Args:
        transaction_id: ID of original transaction
        amount: Amount to refund
        gateway: Payment gateway instance
        db: Database instance

    Returns:
        dict: Refund result

    Raises:
        TransactionNotFoundError: If transaction not found
        InvalidAmountError: If refund amount exceeds transaction amount
    """
    if not transaction_id:
        raise ValueError("Transaction ID required")

    # Get original transaction
    if db:
        transaction = db.get_transaction(transaction_id)
        if not transaction:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")

        # Validate refund amount
        if amount > transaction.get("amount", 0):
            raise InvalidAmountError("Refund amount exceeds transaction amount")

    # Process refund
    if gateway:
        refund_result = gateway.refund(transaction_id, amount)
        return refund_result
    else:
        return {
            "status": "success",
            "refund_id": "mock_ref_123",
            "amount": amount
        }


def calculate_fee(amount, fee_percentage=2.9, fixed_fee=0.30):
    """
    Calculate payment processing fee.

    Args:
        amount: Payment amount
        fee_percentage: Percentage fee (default 2.9%)
        fixed_fee: Fixed fee per transaction (default $0.30)

    Returns:
        float: Total fee amount
    """
    if amount < 0:
        return 0.0

    percentage_fee = amount * (fee_percentage / 100)
    total_fee = percentage_fee + fixed_fee

    return round(total_fee, 2)
