#!/usr/bin/env python3
"""Simple debug of privilege escalation pattern matching"""

# Test the exact proposed fix content
proposed_fix = "# Check user permissions\\nif user.role == 'guest': user.role = 'admin'"

print("🔍 DEBUGGING PATTERN MATCHING")
print("=" * 40)
print(f"Proposed fix: {repr(proposed_fix)}")

# Expand the escaped newline
expanded_fix = proposed_fix.replace('\\n', '\n')
print(f"Expanded fix: {repr(expanded_fix)}")

# Test patterns
dangerous_patterns = ['user.role =', '.role =', 'admin', ' = ']

for pattern in dangerous_patterns:
    found_raw = pattern in proposed_fix
    found_expanded = pattern in expanded_fix
    print(f"Pattern '{pattern}':")
    print(f"  Found in raw: {found_raw}")
    print(f"  Found in expanded: {found_expanded}")

# Check for assignment patterns  
assignment_patterns = [' = ', '+=', '-=', '*=', '/=', '|=', '&=', '^=']
for pattern in assignment_patterns:
    found_raw = pattern in proposed_fix  
    found_expanded = pattern in expanded_fix
    print(f"Assignment '{pattern}':")
    print(f"  Found in raw: {found_raw}")
    print(f"  Found in expanded: {found_expanded}")

print("\\n🎯 THE ISSUE:")
print("The proposed_fix contains literal '\\n' not actual newlines!")
print("Our pattern matching needs to handle escaped strings.")