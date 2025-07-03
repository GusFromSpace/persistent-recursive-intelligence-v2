#!/usr/bin/env python3
"""
Performance-related issues for testing optimization capabilities
"""

import time
import random

# PERFORMANCE: O(n²) when O(n) is possible
def slow_sum_calculation(numbers):
    total = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                total += numbers[i]
    return total

# MEMORY INEFFICIENCY: Creating unnecessary copies
def inefficient_string_building(items):
    result = ""
    for item in items:
        result = result + str(item) + ", "
    return result

# ALGORITHM: Inefficient sorting approach
def bubble_sort_slow(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# I/O INEFFICIENCY: Reading file multiple times
def count_lines_inefficient(filename):
    count = 0
    try:
        with open(filename, "r") as f:
            for line in f:
                count += 1

        # Inefficient: Reading same file again
        with open(filename, "r") as f:
            content = f.read()

        return count, len(content)
    except FileNotFoundError:
        return 0, 0

# CPU INTENSIVE: Unnecessary computation in loop
def prime_check_slow(n):
    if n < 2:
        return False
    for i in range(2, n):  # Should be range(2, int(n**0.5) + 1)
        if n % i == 0:
            return False
    return True

# MEMORY: Not using generators when appropriate
def generate_large_list(size):
    return [i * i for i in range(size)]  # Creates entire list in memory

# REGEX: Compiling regex in loop
import re
def find_patterns_slow(texts, pattern):
    results = []
    for text in texts:
        # Inefficient: Compiling regex each time
        match = re.search(pattern, text)
        if match:
            results.append(match.group())
    return results

if __name__ == "__main__":
    print("⚡ Testing performance issues...")

    # Demonstrate slow operations
    numbers = list(range(1000))

    start_time = time.time()
    result = slow_sum_calculation(numbers[:100])  # Small subset to avoid timeout
    end_time = time.time()

    print(f"Slow sum result: {result}, Time: {end_time - start_time:.4f}s")