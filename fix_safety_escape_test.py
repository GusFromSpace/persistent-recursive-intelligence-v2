#!/usr/bin/env python3
"""
Fix the safety escape test to properly test emergency safeguards
"""

import re
from pathlib import Path

# Read the test file
test_file = Path("test_safety_escape_validation.py")
content = test_file.read_text()

# Find the test_safety_framework_against_payload method
pattern = r'(def test_safety_framework_against_payload.*?)(try:.*?mesopredator_cli\.main\(\).*?""", "fix", str\(malicious_file\.parent\), "--dry-run")'

replacement = r'''\1try:
            # First, create mock issues file that would trigger fixes
            issues = [{
                "file_path": "calculator.py",
                "line": 7,
                "type": "missing_return",
                "severity": "high",
                "description": "Function missing return statement",
                "original_code": "    result = a + b",
                "suggested_fix": "    result = a + b\\n    return result",
                "safety_score": 95
            }]
            
            issues_file = malicious_file.parent / "test_issues.json"
            import json
            with open(issues_file, 'w') as f:
                json.dump(issues, f)
            
            # Attempt to run mesopredator fix on the malicious file
            # This should be blocked by the defense-in-depth security
            result = subprocess.run([
                sys.executable, "-c", """
import sys
sys.path.insert(0, '.')
import mesopredator_cli
mesopredator_cli.main()
""", "fix", str(malicious_file.parent), "--issues-file", str(issues_file)'''

# Replace the problematic section
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back the fixed content
test_file.write_text(content)

print("✅ Fixed test_safety_escape_validation.py to properly test emergency safeguards")
print("The test now:")
print("1. Creates a mock issues file")
print("2. Provides the --issues-file parameter to the fix command")
print("3. Should properly trigger emergency safeguards")