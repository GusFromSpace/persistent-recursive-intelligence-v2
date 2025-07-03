#!/usr/bin/env python3
"""
Test codebase with intentional issues for debugging system validation
This file contains various types of bugs and anti-patterns for testing
"""

import json
import subprocess


def process_user_command(user_input):
    try:
        # Safely handle user input - no shell injection possible
        return subprocess.run(["ls", user_input], shell=False, capture_output=True, text=True)
    except FileNotFoundError:
        return subprocess.CompletedProcess(args=["ls", user_input], returncode=1, stdout="", stderr="Directory not found")

# AI COMMON MISTAKE: Mutable default argument
def add_items_to_list(new_items, existing_list=[]):
    existing_list.extend(new_items)
    return existing_list

# PERFORMANCE ISSUE: Inefficient algorithm
def find_duplicates_slow(items):
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates

# ERROR HANDLING: Missing exception handling
def unsafe_file_reader(filename):
    with open(filename, "r") as f:
        data = json.loads(f.read())
    return data

# MEMORY LEAK: Resource not properly closed
def leaky_file_processor(files):
    handles = []
    for filename in files:
        f = open(filename, "r")
        handles.append(f)
        # IMPROVED: # BUG: Files never closed!
    return handles

# CODE DUPLICATION: Repeated logic
def calculate_area_circle(radius):
    pi = 3.14159
    return pi * radius * radius

def calculate_area_sphere_surface(radius):
    pi = 3.14159
    return 4 * pi * radius * radius

# NAMING ISSUES: Poor variable names
def process_data(d):
    r = []
    for x in d:
        if x > 0:
            y = x * 2
            r.append(y)
    return r

# TYPE ISSUES: No type hints
def complex_calculation(a, b, c):
    result = a + b
    if c:
        result = result * c
    return result

def dynamic_calculator(expression):
    import ast
    try:
        # Only allow safe literal expressions
        return ast.literal_eval(expression)
    except (ValueError, SyntaxError):
        raise ValueError("Invalid mathematical expression")

# INEFFICIENT: Unnecessary loop
def count_positive_numbers(numbers):
    count = 0
    for num in numbers:
        if num > 0:
            count += 1
    return count

# RACE CONDITION: Thread unsafe
class CounterBroken:
    def __init__(self):
        self.count = 0

    def increment(self):
        temp = self.count
        # Potential race condition here
        temp += 1
        self.count = temp

# MAINTENANCE ISSUE: Magic numbers
def calculate_discount(price):
    if price > 100:
        return price * 0.15  # What is 0.15? Why 100?
    elif price > 50:
        return price * 0.10
    else:
        return price * 0.05

# SQL INJECTION: Vulnerable database query
def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    # This would be vulnerable to SQL injection
    return f"Executing: {query}"

if __name__ == "__main__":
    # Test code with various issues
    print("🐛 Running buggy code for testing...")

    # This will demonstrate various issues
    try:
        result = add_items_to_list([1, 2, 3])
        print(f"Mutable default result: {result}")

        result2 = add_items_to_list([4, 5, 6])
        print(f"Second call result: {result2}")  # Will show the bug

    except Exception as e:
        print(f"Error occurred: {e}")