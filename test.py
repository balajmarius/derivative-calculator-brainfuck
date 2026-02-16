#!/usr/bin/env python3
"""Test the Brainfuck derivative calculator."""

from bf_interpreter import run_bf

with open("derivative.bf") as f:
    CODE = f.read()


def deriv(input_str):
    """Run the derivative calculator and return output."""
    if not input_str.endswith("\n"):
        input_str += "\n"
    return run_bf(CODE, input_str, max_steps=10_000_000)


tests = [
    # (input, expected_output, description)
    # Input: coefficients from constant to highest degree
    # Output: derivative coefficients

    # d/dx(7) = 0
    ("7", "0\n", "constant -> 0"),

    # d/dx(5x + 1) = 5
    ("1 5", "5\n", "linear"),

    # d/dx(3x^2 + 5x + 1) = 6x + 5 -> coefficients [5, 6]
    ("1 5 3", "5 6\n", "quadratic"),

    # d/dx(3x^3 + 0x^2 + 5x + 1) = 9x^2 + 0x + 5 -> [5, 0, 9]
    ("1 5 0 3", "5 0 9\n", "cubic"),

    # d/dx(x^2) = 2x -> coefficients [0, 2]
    ("0 0 1", "0 2\n", "x^2"),

    # d/dx(x) = 1
    ("0 1", "1\n", "x"),

    # d/dx(0) = 0
    ("0", "0\n", "zero constant"),

    # d/dx(2x^3) = 6x^2 -> [0, 0, 6]
    ("0 0 0 2", "0 0 6\n", "2x^3"),

    # d/dx(9x^2 + 9x + 9) = 18x + 9 -> [9, 18]
    ("9 9 9", "9 18\n", "two-digit result"),

    # d/dx(1x^4 + 0x^3 + 0x^2 + 0x + 0) = 4x^3 -> [0, 0, 0, 4]
    ("0 0 0 0 1", "0 0 0 4\n", "x^4"),

    # d/dx(9x^9) = 81x^8
    # input: 0 0 0 0 0 0 0 0 0 9 (coeffs for 9x^9)
    ("0 0 0 0 0 0 0 0 0 9", "0 0 0 0 0 0 0 0 81\n", "9x^9 -> 81x^8"),

    # d/dx(x + 1) = 1
    ("1 1", "1\n", "x+1"),

    # d/dx(2x^2 + 3x + 4) = 4x + 3 -> [3, 4]
    ("4 3 2", "3 4\n", "2x^2+3x+4"),

    # d/dx(5x^5) = 25x^4
    ("0 0 0 0 0 5", "0 0 0 0 25\n", "5x^5 -> 25x^4"),

    # All zeros: d/dx(0 + 0x + 0x^2) = 0 + 0x -> [0, 0]
    ("0 0 0", "0 0\n", "zero polynomial degree 2"),

    # d/dx(1 + 1x + 1x^2 + 1x^3 + 1x^4 + 1x^5) = 1 + 2x + 3x^2 + 4x^3 + 5x^4
    ("1 1 1 1 1 1", "1 2 3 4 5\n", "sum of x^k"),

    # Three-digit result: d/dx(9x^28) where multiplier=28, coeff=9 -> 252
    # Need 29 coefficients: 28 zeros then 9
    (
        "0 " * 28 + "9",
        " ".join(["0"] * 27) + " 252\n",
        "9x^28 -> 252x^27 (three-digit)",
    ),
]

passed = 0
failed = 0

for input_str, expected, desc in tests:
    try:
        result = deriv(input_str)
        if result == expected:
            print(f"  PASS: {desc}")
            print(f"        input={input_str!r} -> {result!r}")
            passed += 1
        else:
            print(f"  FAIL: {desc}")
            print(f"        input={input_str!r}")
            print(f"        expected={expected!r}")
            print(f"        got     ={result!r}")
            failed += 1
    except Exception as e:
        print(f"  ERROR: {desc}")
        print(f"         input={input_str!r}")
        print(f"         {e}")
        failed += 1

print(f"\n{passed} passed, {failed} failed out of {passed + failed} tests")
