# Issue: Free shipping threshold is incorrect

## Expected behavior

- Orders with a subtotal **greater than $100** receive free shipping.
- Orders with a subtotal **equal to or below $100** pay a flat $10 shipping fee.

## Current behavior

The current implementation gives free shipping to orders at exactly $100.

## Acceptance criteria

1. `$80` returns `$10`.
2. `$100` returns `$10`.
3. `$100.01` returns `$0`.
4. `$120` returns `$0`.
5. Negative subtotals raise `ValueError`.
6. Existing valid behavior must not regress.
