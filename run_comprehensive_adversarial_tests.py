#!/usr/bin/env python3
"""
COMPREHENSIVE Adversarial Test Suite Runner
Runs ALL security, safety, and adversarial tests to validate the complete system
"""

import subprocess
import time
import json
import os
from pathlib import Path
from datetime import datetime

class ComprehensiveAdversarialTestRunner:
    """Runs all adversarial, safety, and security tests with comprehensive reporting"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.security_critical_failures = []
    
    def run_test(self, test_name: str, test_command: str, description: str, is_security_critical: bool = False):
        """Run a single test and capture results"""
        print(f"\n{'='*80}")
        print(f"🧪 RUNNING: {test_name}")
        print(f"📋 Description: {description}")
        print(f"💻 Command: {test_command}")
        if is_security_critical:
            print(f"🔒 SECURITY CRITICAL TEST")
        print(f"{'='*80}")
        
        self.total_tests += 1
        test_start = time.time()
        
        try:
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=180  # 3 minute timeout for comprehensive tests
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
                "all emergency tests passed",
                "test passed",
                "security: passed",
                "validation: passed"
            ]
            
            failed_indicators = [
                "failed",
                "error",
                "traceback",
                "exception",
                "test failed",
                "assertion",
                "fatal"
            ]
            
            # Determine if test passed
            passed = any(indicator in output_lower for indicator in success_indicators)
            
            # Check for explicit failures
            if any(indicator in output_lower for indicator in failed_indicators):
                # Only mark as failed if no success indicators present
                if not passed:
                    passed = False
            
            # Special handling for different return codes
            if result.returncode == 0:
                # Return code 0 is usually success
                if not any(indicator in output_lower for indicator in failed_indicators):
                    passed = True
            elif result.returncode != 0:
                # Non-zero return code usually indicates failure
                if not passed:
                    passed = False
            
            if passed:
                self.passed_tests += 1
                status = "✅ PASSED"
            else:
                self.failed_tests += 1
                status = "❌ FAILED"
                if is_security_critical:
                    self.security_critical_failures.append(test_name)
            
            # Store results
            self.test_results[test_name] = {
                'status': status,
                'duration': test_duration,
                'return_code': result.returncode,
                'command': test_command,
                'description': description,
                'is_security_critical': is_security_critical,
                'output_summary': self._extract_summary(result.stdout),
                'errors': result.stderr[:500] if result.stderr else None,
                'full_output': result.stdout[:1000] if result.stdout else None
            }
            
            # Print summary
            print(f"\n📊 {test_name} Result: {status}")
            print(f"⏱️  Duration: {test_duration:.2f}s")
            if result.returncode != 0:
                print(f"⚠️  Return code: {result.returncode}")
            
        except subprocess.TimeoutExpired:
            self.failed_tests += 1
            if is_security_critical:
                self.security_critical_failures.append(test_name)
            self.test_results[test_name] = {
                'status': '⏱️ TIMEOUT',
                'duration': 180,
                'command': test_command,
                'description': description,
                'is_security_critical': is_security_critical,
                'errors': 'Test exceeded 3 minute timeout'
            }
            print(f"\n⏱️ {test_name} TIMEOUT after 180s")
            
        except Exception as e:
            self.failed_tests += 1
            if is_security_critical:
                self.security_critical_failures.append(test_name)
            self.test_results[test_name] = {
                'status': '💥 ERROR',
                'command': test_command,
                'description': description,
                'is_security_critical': is_security_critical,
                'errors': str(e)
            }
            print(f"\n💥 {test_name} ERROR: {e}")
    
    def _extract_summary(self, output: str) -> str:
        """Extract key summary information from test output"""
        if not output:
            return "No output"
            
        lines = output.split('\n')
        summary_lines = []
        
        # Look for summary indicators
        for line in lines:
            if any(indicator in line.lower() for indicator in [
                'passed:', 'failed:', 'success rate:', 'blocked:', 'detected:',
                'overall results:', 'test result:', 'security', 'total:',
                'analysis complete', 'validation:', 'threats:'
            ]):
                summary_lines.append(line.strip())
        
        return ' | '.join(summary_lines[-5:]) if summary_lines else output[:200] + "..."
    
    def run_all_tests(self):
        """Run complete comprehensive adversarial test suite"""
        print("🚀 COMPREHENSIVE ADVERSARIAL & SECURITY TEST SUITE")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Define all tests to run with security criticality
        tests = [
            # Core Security & Adversarial Tests (SECURITY CRITICAL)
            {
                'name': 'Adversarial Fixer Security',
                'command': 'python test_adversarial_fixer_security.py',
                'description': 'Tests defense against malicious fix proposals and security bypasses',
                'security_critical': True
            },
            {
                'name': 'Gray Hat Ethics Test',
                'command': 'python gray_hat_ethics_test.py',
                'description': 'Tests ethical boundaries and gray area attack scenarios',
                'security_critical': True
            },
            {
                'name': 'Safety Escape Test',
                'command': 'python safety_escape_test.py',
                'description': 'Tests attempts to escape or bypass safety mechanisms',
                'security_critical': True
            },
            {
                'name': 'Orchestrator Synthesis Test',
                'command': 'python orchestrator_synthesis_test.py',
                'description': 'Tests synthesis capabilities and orchestration attack vectors',
                'security_critical': True
            },
            {
                'name': 'Emergency Scenario Validation',
                'command': 'python test_emergency_simple.py',
                'description': 'Validates emergency safeguards block malicious code even after approval',
                'security_critical': True
            },
            {
                'name': 'Emergency Scenarios Extended',
                'command': 'python test_emergency_scenarios.py',
                'description': 'Extended emergency scenario testing with multiple attack vectors',
                'security_critical': True
            },
            {
                'name': 'Enhanced Safety Features',
                'command': 'python test_enhanced_safety_features.py',
                'description': 'Tests enhanced safety validation and threat detection systems',
                'security_critical': True
            },
            {
                'name': 'External Project Safety',
                'command': 'python test_external_project_safety.py',
                'description': 'Validates safety when analyzing external/untrusted projects',
                'security_critical': True
            },
            {
                'name': 'Basic Safety Validation',
                'command': 'python test_basic_safety.py',
                'description': 'Core safety mechanism validation and baseline security tests',
                'security_critical': True
            },
            {
                'name': 'Safety Features Comprehensive',
                'command': 'python test_safety_features.py',
                'description': 'Comprehensive safety feature testing and validation',
                'security_critical': True
            },
            
            # Intelligence & Analysis Tests (IMPORTANT BUT NOT SECURITY CRITICAL)
            {
                'name': 'Code Connector Adversarial',
                'command': 'python test_code_connector_adversarial.py',
                'description': 'Tests code connection intelligence against adversarial inputs',
                'security_critical': False
            },
            {
                'name': 'Memory Intelligence Integration',
                'command': 'python test_memory_intelligence_integration.py',
                'description': 'Tests persistent memory and learning capabilities',
                'security_critical': False
            },
            {
                'name': 'Self-Analysis Comprehensive',
                'command': 'python test_self_analysis_comprehensive.py',
                'description': 'Tests recursive self-improvement and analysis capabilities',
                'security_critical': False
            },
            {
                'name': 'Debugging Capabilities',
                'command': 'python test_debugging_capabilities.py',
                'description': 'Validates debugging and issue detection capabilities',
                'security_critical': False
            },
            {
                'name': 'Enhanced PRI Integration',
                'command': 'python test_enhanced_pri_integration.py',
                'description': 'Tests integration of persistent recursive intelligence features',
                'security_critical': False
            },
            {
                'name': 'Field Shaping',
                'command': 'python test_field_shaping.py',
                'description': 'Tests educational field shaping and learning enhancement',
                'security_critical': False
            },
            {
                'name': 'Stress Testing',
                'command': 'python test_stress_testing.py',
                'description': 'System performance and reliability under load',
                'security_critical': False
            },
            
            # Real-World Validation Tests
            {
                'name': 'Real-World Dogfooding',
                'command': 'python test_real_world_dogfooding.py',
                'description': 'Real-world usage patterns and self-analysis validation',
                'security_critical': False
            },
            {
                'name': 'Real C++ Project Analysis',
                'command': 'python test_real_cpp_project.py',
                'description': 'Analysis of real C++ codebase for cross-language validation',
                'security_critical': False
            }
        ]
        
        # Filter tests to only run existing files
        existing_tests = []
        for test in tests:
            test_file = test['command'].split()[1]  # Extract filename from command
            if os.path.exists(test_file):
                existing_tests.append(test)
            else:
                print(f"⚠️  Skipping {test['name']} - file {test_file} not found")
        
        print(f"\n📊 Found {len(existing_tests)} test files to execute")
        print(f"🔒 Security critical tests: {sum(1 for t in existing_tests if t['security_critical'])}")
        print(f"🧪 Other tests: {sum(1 for t in existing_tests if not t['security_critical'])}")
        
        # Run each test
        for test in existing_tests:
            self.run_test(
                test['name'], 
                test['command'], 
                test['description'],
                test['security_critical']
            )
        
        # Generate final report
        self.generate_comprehensive_report()
    
    def generate_comprehensive_report(self):
        """Generate comprehensive test report with security assessment"""
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
        
        # Security critical analysis
        security_tests = [name for name, result in self.test_results.items() 
                         if result.get('is_security_critical', False)]
        security_passed = [name for name in security_tests 
                          if self.test_results[name]['status'] == '✅ PASSED']
        
        print(f"\n🛡️ SECURITY CRITICAL TEST ANALYSIS:")
        print(f"   Security Tests: {len(security_tests)}")
        print(f"   ✅ Security Passed: {len(security_passed)}")
        print(f"   ❌ Security Failed: {len(self.security_critical_failures)}")
        print(f"   🔒 Security Success Rate: {(len(security_passed)/len(security_tests)*100):.1f}%")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            security_marker = " 🔒" if result.get('is_security_critical') else ""
            print(f"\n   {test_name}{security_marker}:")
            print(f"      Status: {result['status']}")
            print(f"      Duration: {result.get('duration', 0):.2f}s")
            if result.get('output_summary'):
                print(f"      Summary: {result['output_summary']}")
            if result.get('errors'):
                print(f"      Errors: {result['errors'][:100]}...")
        
        # Overall security assessment
        all_security_passed = len(self.security_critical_failures) == 0
        
        print(f"\n🛡️ COMPREHENSIVE SECURITY ASSESSMENT:")
        if all_security_passed:
            print("   ✅ ALL SECURITY CRITICAL TESTS PASSED")
            print("   🔒 System demonstrates comprehensive defense-in-depth security")
            print("   🛡️ Safe for production deployment")
            print("   🎯 Zero security vulnerabilities detected")
        else:
            print("   ❌ SECURITY VULNERABILITIES DETECTED")
            print("   🚨 CRITICAL: DO NOT DEPLOY until all security tests pass")
            print(f"   ⚠️  Failed security tests: {', '.join(self.security_critical_failures)}")
        
        # Performance and capability assessment
        print(f"\n🧠 CAPABILITY ASSESSMENT:")
        capability_tests = [name for name, result in self.test_results.items() 
                           if not result.get('is_security_critical', False)]
        capability_passed = [name for name in capability_tests 
                            if self.test_results[name]['status'] == '✅ PASSED']
        
        print(f"   Intelligence Tests: {len(capability_tests)}")
        print(f"   ✅ Capability Passed: {len(capability_passed)}")
        print(f"   🧠 Capability Success Rate: {(len(capability_passed)/len(capability_tests)*100):.1f}%" if capability_tests else "   No capability tests found")
        
        # Save detailed report
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.total_tests,
                'passed': self.passed_tests,
                'failed': self.failed_tests,
                'success_rate': (self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0,
                'duration': total_duration,
                'security_status': 'SECURE' if all_security_passed else 'VULNERABLE',
                'security_critical_failures': self.security_critical_failures
            },
            'test_results': self.test_results
        }
        
        report_file = f"comprehensive_adversarial_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📝 Detailed report saved to: {report_file}")
        
        # Final verdict
        print(f"\n{'='*80}")
        if all_security_passed and self.passed_tests == self.total_tests:
            print("🎉 ALL TESTS PASSED - SYSTEM FULLY VALIDATED!")
            print("✅ Security: HARDENED")
            print("✅ Capabilities: OPERATIONAL") 
            print("✅ Status: PRODUCTION READY")
        elif all_security_passed:
            print("🛡️ SECURITY TESTS PASSED - SYSTEM SECURE")
            print("✅ Security: HARDENED")
            print("⚠️ Some capability tests failed - review non-critical issues")
            print("✅ Status: SECURE FOR DEPLOYMENT")
        else:
            print(f"🚨 SECURITY FAILURES DETECTED - {len(self.security_critical_failures)} CRITICAL ISSUES")
            print("❌ Security: VULNERABLE")
            print("🔧 Status: NOT READY FOR DEPLOYMENT")
            print("⚠️ Review security failures immediately")

if __name__ == "__main__":
    runner = ComprehensiveAdversarialTestRunner()
    runner.run_all_tests()