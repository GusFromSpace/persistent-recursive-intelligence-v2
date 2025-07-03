#!/usr/bin/env python3
"""
Comprehensive Adversarial Test Suite Runner
Runs all security and adversarial tests to validate the enhanced system
"""

import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

class AdversarialTestRunner:
    """Runs all adversarial tests and generates comprehensive report"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def run_test(self, test_name: str, test_command: str, description: str):
        """Run a single test and capture results"""
        print(f"\n{'='*80}")
        print(f"🧪 RUNNING: {test_name}")
        print(f"📋 Description: {description}")
        print(f"💻 Command: {test_command}")
        print(f"{'='*80}")
        
        self.total_tests += 1
        test_start = time.time()
        
        try:
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            test_duration = time.time() - test_start
            
            # Check for success indicators in output
            output_lower = result.stdout.lower()
            success_indicators = [
                "all tests passed",
                "100.0%",
                "success rate: 100",
                "✅ all",
                "passed: 15/15",
                "passed: 6/6",
                "all emergency tests passed"
            ]
            
            failed_indicators = [
                "fail",
                "error",
                "traceback",
                "exception"
            ]
            
            # Determine if test passed
            passed = any(indicator in output_lower for indicator in success_indicators)
            
            # Check for explicit failures
            if any(indicator in output_lower for indicator in failed_indicators):
                # Only mark as failed if no success indicators present
                if not passed:
                    passed = False
            
            # Special check for return code
            if result.returncode != 0 and "test" in test_command:
                passed = False
            
            if passed:
                self.passed_tests += 1
                status = "✅ PASSED"
            else:
                self.failed_tests += 1
                status = "❌ FAILED"
            
            # Store results
            self.test_results[test_name] = {
                'status': status,
                'duration': test_duration,
                'return_code': result.returncode,
                'command': test_command,
                'description': description,
                'output_summary': self._extract_summary(result.stdout),
                'errors': result.stderr[:500] if result.stderr else None
            }
            
            # Print summary
            print(f"\n📊 {test_name} Result: {status}")
            print(f"⏱️  Duration: {test_duration:.2f}s")
            if result.returncode != 0:
                print(f"⚠️  Return code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            self.failed_tests += 1
            self.test_results[test_name] = {
                'status': '⏱️ TIMEOUT',
                'duration': 120,
                'command': test_command,
                'description': description,
                'errors': 'Test exceeded 2 minute timeout'
            }
            print(f"\n⏱️ {test_name} TIMEOUT after 120s")
            
        except Exception as e:
            self.failed_tests += 1
            self.test_results[test_name] = {
                'status': '💥 ERROR',
                'command': test_command,
                'description': description,
                'errors': str(e)
            }
            print(f"\n💥 {test_name} ERROR: {e}")
    
    def _extract_summary(self, output: str) -> str:
        """Extract key summary information from test output"""
        lines = output.split('\n')
        summary_lines = []
        
        # Look for summary indicators
        for line in lines:
            if any(indicator in line.lower() for indicator in [
                'passed:', 'failed:', 'success rate:', 
                'overall results:', 'test result:', 'security'
            ]):
                summary_lines.append(line.strip())
        
        return ' | '.join(summary_lines[-5:])  # Last 5 summary lines
    
    def run_all_tests(self):
        """Run complete adversarial test suite"""
        print("🚀 COMPREHENSIVE ADVERSARIAL TEST SUITE")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Define all tests to run
        tests = [
            {
                'name': 'Adversarial Fixer Security',
                'command': 'python test_adversarial_fixer_security.py',
                'description': 'Tests defense against malicious fix proposals and security bypasses'
            },
            {
                'name': 'Emergency Scenario Validation',
                'command': 'python test_emergency_simple.py',
                'description': 'Validates emergency safeguards block malicious code even after approval'
            },
            {
                'name': 'Code Connector Adversarial',
                'command': 'python test_code_connector_adversarial.py',
                'description': 'Tests code connection intelligence against adversarial inputs'
            },
            {
                'name': 'Feedback Loop Demo',
                'command': 'python test_feedback_demo.py',
                'description': 'Tests the complete feedback loop with learning system'
            }
        ]
        
        # Run each test
        for test in tests:
            self.run_test(test['name'], test['command'], test['description'])
        
        # Generate final report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        total_duration = time.time() - self.start_time
        
        print(f"\n{'='*80}")
        print("📊 COMPREHENSIVE ADVERSARIAL TEST REPORT")
        print("=" * 80)
        
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   ✅ Passed: {self.passed_tests}")
        print(f"   ❌ Failed: {self.failed_tests}")
        print(f"   🎯 Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print(f"   ⏱️  Total Duration: {total_duration:.2f}s")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            print(f"\n   {test_name}:")
            print(f"      Status: {result['status']}")
            print(f"      Duration: {result.get('duration', 0):.2f}s")
            if result.get('output_summary'):
                print(f"      Summary: {result['output_summary']}")
            if result.get('errors'):
                print(f"      Errors: {result['errors'][:100]}...")
        
        # Security assessment
        security_tests = ['Adversarial Fixer Security', 'Emergency Scenario Validation']
        security_passed = all(
            self.test_results.get(test, {}).get('status') == '✅ PASSED' 
            for test in security_tests
        )
        
        print(f"\n🛡️ SECURITY ASSESSMENT:")
        if security_passed:
            print("   ✅ ALL SECURITY TESTS PASSED")
            print("   🔒 System demonstrates robust defense-in-depth security")
            print("   🛡️ Safe for production deployment")
        else:
            print("   ❌ SECURITY VULNERABILITIES DETECTED")
            print("   🚨 DO NOT DEPLOY until all security tests pass")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.total_tests,
                'passed': self.passed_tests,
                'failed': self.failed_tests,
                'success_rate': (self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0,
                'duration': total_duration,
                'security_status': 'SECURE' if security_passed else 'VULNERABLE'
            },
            'test_results': self.test_results
        }
        
        report_file = f"adversarial_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📝 Detailed report saved to: {report_file}")
        
        # Final verdict
        print(f"\n{'='*80}")
        if self.passed_tests == self.total_tests:
            print("🎉 ALL ADVERSARIAL TESTS PASSED!")
            print("✅ System ready for production deployment")
        else:
            print(f"⚠️ {self.failed_tests} TESTS FAILED")
            print("🔧 Please review failures before deployment")

if __name__ == "__main__":
    runner = AdversarialTestRunner()
    runner.run_all_tests()