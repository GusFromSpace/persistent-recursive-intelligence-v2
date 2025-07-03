#!/usr/bin/env python3
"""
Math Utils - Basic Mathematical Operations

Simple mathematical utilities for common operations.
"""


def add_numbers(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


def calculate_percentage(value: float, total: float) -> float:
    """Calculate percentage"""
    if total == 0:
        return 0.0
    return (value / total) * 100


def is_even(number: int) -> bool:
    """Check if a number is even"""
    return number % 2 == 0


if __name__ == "__main__":
    # Demo the math utils
    print(f"5 + 3 = {add_numbers(5, 3)}")
    print(f"4 * 7 = {multiply_numbers(4, 7)}")
    print(f"25% of 200 = {calculate_percentage(50, 200)}")
    print(f"Is 6 even? {is_even(6)}")