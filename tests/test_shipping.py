import pytest

from src.shipping import calculate_shipping


# Pass-to-pass regression tests
def test_standard_shipping_below_threshold():
    assert calculate_shipping(80) == 10.0


def test_zero_subtotal_pays_shipping():
    assert calculate_shipping(0) == 10.0


def test_negative_subtotal_is_invalid():
    with pytest.raises(ValueError):
        calculate_shipping(-1)


# Fail-to-pass task-specific tests
def test_exactly_100_still_pays_shipping():
    assert calculate_shipping(100) == 10.0


def test_just_over_100_gets_free_shipping():
    assert calculate_shipping(100.01) == 0.0


def test_120_gets_free_shipping():
    assert calculate_shipping(120) == 0.0
