"""Shipping calculation domain logic."""

from __future__ import annotations


def calculate_shipping(subtotal: float) -> float:
    """Return the shipping fee for an order subtotal.

    Business rule:
      - subtotal > 100 => free shipping
      - subtotal <= 100 => $10 shipping

    The starter implementation intentionally contains a boundary bug.
    """
    if subtotal < 0:
        raise ValueError("subtotal cannot be negative")

    # BUG: $100 should still pay shipping.
    if subtotal >= 100:
        return 0.0

    return 10.0
