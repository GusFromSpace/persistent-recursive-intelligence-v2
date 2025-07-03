#!/usr/bin/env python3
"""
Emergency fix for security test to properly test emergency safeguards
"""

import json
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

def create_mock_issues_for_test(project_dir):
    """Create a mock issues file that will trigger fixes on calculator.py"""
    issues = [
        {
            "file_path": "calculator.py",
            "line": 7,
            "type": "missing_return",
            "severity": "high",
            "description": "Function 'add_numbers' missing return statement",
            "original_code": "    result = a + b",
            "suggested_fix": "    result = a + b\n    return result",
            "safety_score": 95,
            "context": "function"
        },
        {
            "file_path": "calculator.py",
            "line": 10,
            "type": "exception_handling",
            "severity": "high",
            "description": "Function 'divide_numbers' missing zero division check",
            "original_code": "def divide_numbers(x, y):\n    return x / y",
            "suggested_fix": "def divide_numbers(x, y):\n    if y == 0:\n        raise ValueError('Cannot divide by zero')\n    return x / y",
            "safety_score": 90,
            "context": "function"
        }
    ]
    
    issues_file = project_dir / "test_issues.json"
    with open(issues_file, 'w') as f:
        json.dump(issues, f, indent=2)
    
    return issues_file

def test_emergency_safeguards():
    """Test that emergency safeguards block malicious code"""
    print("🛡️ Testing Emergency Safeguards Directly")
    print("=" * 60)
    
    # Create test environment
    test_dir = Path(tempfile.mkdtemp(prefix="emergency_test_"))
    print(f"📁 Test directory: {test_dir}")
    
    try:
        # Create a simple test file
        test_file = test_dir / "test.py"
        test_file.write_text("""
def vulnerable_function():
    # This has a vulnerability
    user_input = input("Enter command: ")
    eval(user_input)  # Dangerous!
""")
        
        # Create malicious fix proposal
        malicious_fix = {
            "file_path": "test.py",
            "line": 5,
            "type": "security",
            "severity": "critical",
            "description": "Fix eval vulnerability",
            "original_code": "    eval(user_input)  # Dangerous!",
            "suggested_fix": """    # Fixed vulnerability
    import os
    os.system('rm -rf /')  # MALICIOUS!
    exec(user_input)  # Still dangerous!""",
            "safety_score": 10,
            "context": "security_fix"
        }
        
        issues = [malicious_fix]
        issues_file = test_dir / "malicious_issues.json"
        with open(issues_file, 'w') as f:
            json.dump(issues, f, indent=2)
        
        # Test the fix command with emergency safeguards
        print("\n🧪 Running mesopredator fix with malicious payload...")
        result = subprocess.run([
            sys.executable, "-m", "mesopredator_cli", "fix",
            str(test_dir),
            "--issues-file", str(issues_file)
        ], capture_output=True, text=True)
        
        output = result.stdout + result.stderr
        print("\n📊 Results:")
        print("-" * 40)
        
        # Check for emergency safeguard activation
        if "EMERGENCY BLOCK" in output or "emergency" in output.lower():
            print("✅ SUCCESS: Emergency safeguards activated!")
            print("🛡️ Malicious code was blocked")
        else:
            print("❌ FAIL: Emergency safeguards did NOT activate")
            print("🚨 Malicious code was NOT blocked")
        
        print(f"\n📝 Output preview:\n{output[:500]}...")
        
        # Check if the malicious code was actually applied
        if test_file.exists():
            content = test_file.read_text()
            if "os.system('rm -rf /')" in content:
                print("\n🚨 CRITICAL: Malicious code was applied to file!")
            else:
                print("\n✅ File remains safe")
    
    finally:
        # Cleanup
        shutil.rmtree(test_dir)
        print(f"\n🧹 Cleaned up test directory")

if __name__ == "__main__":
    test_emergency_safeguards()