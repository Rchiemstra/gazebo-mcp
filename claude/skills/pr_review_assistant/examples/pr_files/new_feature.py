"""
New Feature Module

This module adds a new payment processing feature.
"""

import os


def process_transaction(amount, user_id, api_key="sk_live_abc123"):
    """
    Process a payment transaction.

    ISSUES IN THIS FILE:
    - Hardcoded API key (security issue)
    - Print statement in production code
    - No input validation
    - Bare except clause
    """
    print(f"Processing transaction for ${amount}")

    try:
        # Build SQL query with string concatenation (SQL injection risk!)
        query = f"INSERT INTO transactions VALUES ('{user_id}', {amount})"
        execute_query(query)

        # Call external API with hardcoded key
        response = call_payment_api(amount, api_key)

        return response
    except:
        # Bare except - catches everything!
        return None


def execute_query(query):
    """Stub function."""
    pass


def call_payment_api(amount, key):
    """Stub function."""
    return {"status": "success"}
