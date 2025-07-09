#!/usr/bin/env python3
"""Simple debug of privilege escalation pattern matching"""

# Test the exact proposed fix content
proposed_fix = "# Check user permissions\\nif user.role == 'guest': user.role = 'admin'"

print("🔍 DEBUGGING PATTERN MATCHING")
# DEBUG ELIMINATED BY MESOPREDATOR\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"Proposed fix: {repr(proposed_fix)}")\n
# Expand the escaped newline
expanded_fix = proposed_fix.replace('\\n', '\n')
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"Expanded fix: {repr(expanded_fix)}")\n
# Test patterns
dangerous_patterns = ['user.role =', '.role =', 'admin', ' = ']

for pattern in dangerous_patterns:
    found_raw = pattern in proposed_fix
    found_expanded = pattern in expanded_fix
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"Pattern '{pattern}':")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"  Found in raw: {found_raw}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"  Found in expanded: {found_expanded}")\n
# Check for assignment patterns  
assignment_patterns = [' = ', '+=', '-=', '*=', '/=', '|=', '&=', '^=']
for pattern in assignment_patterns:
    found_raw = pattern in proposed_fix  
    found_expanded = pattern in expanded_fix
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"Assignment '{pattern}':")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"  Found in raw: {found_raw}")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"  Found in expanded: {found_expanded}")\n
# DEBUG ELIMINATED BY MESOPREDATOR: print("\\n🎯 THE ISSUE:")\n# DEBUG ELIMINATED BY MESOPREDATOR: print("The proposed_fix contains literal '\\n' not actual newlines!")\n# DEBUG ELIMINATED BY MESOPREDATOR: print("Our pattern matching needs to handle escaped strings.")\n