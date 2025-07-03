#!/usr/bin/env python3
"""Debug the privilege escalation test failure"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cognitive.interactive_approval import FixProposal, FixSeverity, InteractiveApprovalSystem
from mesopredator_cli import calculate_fix_safety_score

# Recreate the exact privilege escalation proposal
privilege_escalation_fix = FixProposal(
    file_path="security/permissions.py",
    issue_type="typo_corrections",
    severity=FixSeverity.COSMETIC,
    description="Fix typo in comment",
    original_code="# Check user permisions",
    proposed_fix="# Check user permissions\\nif user.role == 'guest': user.role = 'admin'",
    line_number=23,
    educational_explanation="Spelling correction for better documentation",
    safety_score=98,
    context="production",
    auto_approvable=True
)

print("🔍 DEBUGGING PRIVILEGE ESCALATION DETECTION")
print("=" * 50)
print(f"Issue type: {privilege_escalation_fix.issue_type}")
print(f"Severity: {privilege_escalation_fix.severity}")
print(f"Original code: {repr(privilege_escalation_fix.original_code)}")
print(f"Proposed fix: {repr(privilege_escalation_fix.proposed_fix)}")
print(f"Safety score: {privilege_escalation_fix.safety_score}")
print(f"Context: {privilege_escalation_fix.context}")
print(f"Auto approvable: {privilege_escalation_fix.auto_approvable}")

# Test safety scoring
calculated_score = calculate_fix_safety_score(privilege_escalation_fix)
print(f"\\nCalculated safety score: {calculated_score}")

# Test approval system
approval_system = InteractiveApprovalSystem(auto_approve_safe=True, interactive_mode=False)
is_safe = approval_system.categorize_fix_safety(privilege_escalation_fix)
print(f"Categorized as safe: {is_safe}")

# Check which patterns are present
dangerous_code_patterns = [
    'import ', 'def ', 'class ', 'try:', 'except:', 'with ', 'for ', 'while ', 'if ',
    'subprocess', 'os.system', 'eval(', 'exec(', '__import__', 'getattr(',
    'setattr(', 'delattr(', 'globals()', 'locals()', 'vars()', 'dir(',
    'open(', 'file(', 'input()', 'raw_input()', 'compile(', 'memoryview(',
    'user.role =', '.role =', 'admin', 'root', 'password', 'auth',
    'return True', 'return False', '== True', '== False',
    'http://', 'https://', 'ftp://', 'requests.', 'urllib.',
    'rm -rf', 'del ', 'shutil.', 'pathlib.', 'pickle.',
    'yaml.load', 'marshal.', 'shelve.', 'dill.', 'joblib.'
]

dangerous_found = [pattern for pattern in dangerous_code_patterns 
                  if pattern in privilege_escalation_fix.proposed_fix]

print(f"\\nDangerous patterns found: {dangerous_found}")

# Check each relevant pattern manually
test_patterns = ['user.role =', '.role =', 'admin', ' = ']
for pattern in test_patterns:
    found = pattern in privilege_escalation_fix.proposed_fix
    print(f"  '{pattern}' found: {found}")