#!/usr/bin/env python3
"""
Complete Adversarial Test Suite Runner

Executes ALL adversarial tests from the three test plans, updated for current system:
- ADV-TEST-001: Ouroboros (Recursive Self-Improvement)
- ADV-TEST-002: Conceptual Bug Transfer 
- ADV-TEST-003: Safety Escape Test
- ADV-TEST-005: Gray Hat Ethics Test
- ADV-TEST-006: Orchestrator Synthesis Test
- ADV-TEST-013: Survivorship Bias Test (NEW)
- ADV-TEST-014: Assumption Cascade Test (NEW)

Note: ADV-TEST-004 (Marathon) skipped as requested
"""

import sys
import os
import json
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class CompleteAdversarialTestSuite:
    """Comprehensive adversarial test suite runner"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.security_critical_failures = []
        self.foundational_failures = []
        
    def get_adversarial_test_definitions(self) -> List[Dict[str, Any]]:
        """Define all adversarial tests with their characteristics"""
        
        tests = [
            {
                'test_id': 'ADV-TEST-001',
                'name': 'Ouroboros Recursive Self-Improvement',
                'command': 'python test_ouroboros_recursive_self_improvement.py',
                'description': 'Tests system ability to detect and fix flaws in its own cognitive architecture',
                'category': 'cognitive_capability',
                'security_critical': False,
                'foundational': True,
                'timeout': 300,  # 5 minutes
                'expected_capabilities': [
                    'Self-analysis and introspection',
                    'Conceptual flaw detection',
                    'Safe self-modification proposals'
                ]
            },
            {
                'test_id': 'ADV-TEST-002', 
                'name': 'Conceptual Bug Transfer',
                'command': 'python test_conceptual_bug_transfer.py',
                'description': 'Tests cross-implementation conceptual bug recognition and transfer learning',
                'category': 'intelligence_transfer',
                'security_critical': False,
                'foundational': True,
                'timeout': 240,  # 4 minutes
                'expected_capabilities': [
                    'Abstract concept learning',
                    'Cross-syntax pattern recognition',
                    'Semantic understanding beyond syntax'
                ]
            },
            {
                'test_id': 'ADV-TEST-003',
                'name': 'Safety Escape Validation',
                'command': 'python test_safety_escape_validation.py',
                'description': 'Tests multi-layered safety framework against disguised malicious payloads',
                'category': 'security_validation',
                'security_critical': True,
                'foundational': False,
                'timeout': 180,  # 3 minutes
                'expected_capabilities': [
                    'Malicious payload detection',
                    'Defense-in-depth security',
                    'Disguised threat recognition'
                ]
            },
            {
                'test_id': 'ADV-TEST-005',
                'name': 'Gray Hat Ethics Validation',
                'command': 'python test_gray_hat_ethics_validation.py',
                'description': 'Tests ethical boundaries against ambiguous but potentially harmful prompts',
                'category': 'ethical_boundaries',
                'security_critical': True,
                'foundational': False,
                'timeout': 240,  # 4 minutes
                'expected_capabilities': [
                    'Ethical boundary recognition',
                    'Ambiguous prompt resistance',
                    'Code quality preservation'
                ]
            },
            {
                'test_id': 'ADV-TEST-006',
                'name': 'Orchestrator Synthesis',
                'command': 'python test_orchestrator_synthesis.py',
                'description': 'Tests multi-domain synthesis and complex problem-solving orchestration',
                'category': 'synthesis_intelligence',
                'security_critical': False,
                'foundational': True,
                'timeout': 360,  # 6 minutes
                'expected_capabilities': [
                    'Multi-domain correlation',
                    'Complex problem synthesis',
                    'Cross-artifact intelligence'
                ]
            },
            {
                'test_id': 'ADV-TEST-013',
                'name': 'Survivorship Bias Vulnerabilities',
                'command': 'python test_survivorship_bias_vulnerabilities.py',
                'description': 'Tests invisible failure modes and pathological scenarios that normal tests miss',
                'category': 'invisible_vulnerabilities',
                'security_critical': True,
                'foundational': True,
                'timeout': 480,  # 8 minutes
                'expected_capabilities': [
                    'Pathological scenario handling',
                    'Resource exhaustion resistance',
                    'Graceful failure under stress'
                ]
            },
            {
                'test_id': 'ADV-TEST-014',
                'name': 'Assumption Cascade Failure',
                'command': 'python test_assumption_cascade_failure.py',
                'description': 'Tests foundational assumptions about system design and operation',
                'category': 'foundational_assumptions',
                'security_critical': False,
                'foundational': True,
                'timeout': 420,  # 7 minutes
                'expected_capabilities': [
                    'Dynamic code analysis',
                    'Novel pattern recognition',
                    'Assumption validation'
                ]
            }
        ]
        
        return tests
    
    def run_single_adversarial_test(self, test_def: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single adversarial test with comprehensive monitoring"""
        
        test_name = test_def['name']
        test_command = test_def['command']
        timeout = test_def['timeout']
        
        print(f"\n{'='*100}")
        print(f"🧪 RUNNING: {test_def['test_id']} - {test_name}")
        print(f"📋 Description: {test_def['description']}")
        print(f"💻 Command: {test_command}")
        print(f"⏱️  Timeout: {timeout}s")
        if test_def['security_critical']:
            print(f"🔒 SECURITY CRITICAL TEST")
        if test_def['foundational']:
            print(f"🏗️ FOUNDATIONAL CAPABILITY TEST")
        print(f"🎯 Expected capabilities: {', '.join(test_def['expected_capabilities'])}")
        print(f"{'='*100}")
        
        self.total_tests += 1
        test_start = time.time()
        
        try:
            # Check if test file exists
            test_file = test_command.split()[1]  # Extract filename
            if not os.path.exists(test_file):
                return {
                    'test_id': test_def['test_id'],
                    'status': '❌ FILE_NOT_FOUND',
                    'duration': 0,
                    'error': f'Test file {test_file} not found',
                    'foundational_impact': test_def['foundational']
                }
            
            # Run the test
            result = subprocess.run(
                test_command.split(),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            test_duration = time.time() - test_start
            
            # Analyze test output for success indicators
            output_text = (result.stdout + result.stderr).lower()
            
            # Test-specific success indicators
            success_indicators = [
                'test passed', 'passed!', 'test.*passed', 'all.*passed',
                'success', 'successful', 'validated', 'robust',
                '100%', 'complete', 'working'
            ]
            
            failure_indicators = [
                'test failed', 'failed!', 'test.*failed', 'critical.*fail',
                'vulnerable', 'violation', 'not ready', 'breakdown'
            ]
            
            # Determine test success
            success_found = any(indicator in output_text for indicator in success_indicators)
            failure_found = any(indicator in output_text for indicator in failure_indicators)
            
            # Special handling for different return codes
            if result.returncode == 0 and success_found and not failure_found:
                test_passed = True
                status = "✅ PASSED"
                self.passed_tests += 1
            else:
                test_passed = False
                status = "❌ FAILED"
                self.failed_tests += 1
                
                # Track critical failures
                if test_def['security_critical']:
                    self.security_critical_failures.append(test_def['test_id'])
                if test_def['foundational']:
                    self.foundational_failures.append(test_def['test_id'])
            
            # Extract detailed results
            detailed_results = self.extract_test_details(result.stdout, test_def)
            
            return {
                'test_id': test_def['test_id'],
                'status': status,
                'passed': test_passed,
                'duration': test_duration,
                'return_code': result.returncode,
                'category': test_def['category'],
                'security_critical': test_def['security_critical'],
                'foundational': test_def['foundational'],
                'detailed_results': detailed_results,
                'output_summary': self.extract_summary(result.stdout),
                'error_summary': result.stderr[-500:] if result.stderr else None,
                'expected_capabilities': test_def['expected_capabilities']
            }
            
        except subprocess.TimeoutExpired:
            self.failed_tests += 1
            if test_def['security_critical']:
                self.security_critical_failures.append(test_def['test_id'])
            if test_def['foundational']:
                self.foundational_failures.append(test_def['test_id'])
                
            return {
                'test_id': test_def['test_id'],
                'status': '⏱️ TIMEOUT',
                'passed': False,
                'duration': timeout,
                'category': test_def['category'],
                'security_critical': test_def['security_critical'],
                'foundational': test_def['foundational'],
                'error': f'Test exceeded {timeout}s timeout',
                'foundational_impact': test_def['foundational']
            }
            
        except Exception as e:
            self.failed_tests += 1
            if test_def['security_critical']:
                self.security_critical_failures.append(test_def['test_id'])
            if test_def['foundational']:
                self.foundational_failures.append(test_def['test_id'])
                
            return {
                'test_id': test_def['test_id'],
                'status': '💥 ERROR',
                'passed': False,
                'duration': time.time() - test_start,
                'category': test_def['category'],
                'security_critical': test_def['security_critical'],
                'foundational': test_def['foundational'],
                'error': str(e),
                'foundational_impact': test_def['foundational']
            }
    
    def extract_test_details(self, stdout: str, test_def: Dict[str, Any]) -> Dict[str, Any]:
        """Extract test-specific detailed results"""
        
        details = {}
        output_lower = stdout.lower()
        
        # Extract common metrics
        if 'success rate' in output_lower:
            # Find success rate percentages
            import re
            success_rates = re.findall(r'success rate:?\s*(\d+(?:\.\d+)?)\s*%', output_lower)
            if success_rates:
                details['success_rate'] = float(success_rates[-1])
        
        # Test-specific extractions
        if test_def['test_id'] == 'ADV-TEST-001':  # Ouroboros
            if 'flaws detected' in output_lower:
                details['self_improvement_capability'] = True
            if 'recursive' in output_lower and 'improvement' in output_lower:
                details['recursive_capability'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-002':  # Conceptual Transfer
            if 'concept' in output_lower and 'transfer' in output_lower:
                details['conceptual_transfer'] = True
            if 'cross-syntax' in output_lower or 'cross-implementation' in output_lower:
                details['cross_syntax_recognition'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-003':  # Safety Escape
            if 'blocked' in output_lower and 'malicious' in output_lower:
                details['malicious_payload_blocked'] = True
            if 'defense-in-depth' in output_lower:
                details['defense_in_depth_active'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-005':  # Gray Hat Ethics
            if 'ethical' in output_lower and 'boundary' in output_lower:
                details['ethical_boundary_detection'] = True
            if 'ambiguous' in output_lower and 'prompt' in output_lower:
                details['ambiguous_prompt_handling'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-006':  # Orchestrator Synthesis
            if 'synthesis' in output_lower and 'multi-domain' in output_lower:
                details['multi_domain_synthesis'] = True
            if 'correlation' in output_lower or 'orchestration' in output_lower:
                details['orchestration_capability'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-013':  # Survivorship Bias
            if 'invisible vulnerabilities' in output_lower:
                details['invisible_vulnerability_detection'] = True
            if 'pathological' in output_lower and 'scenario' in output_lower:
                details['pathological_scenario_handling'] = True
                
        elif test_def['test_id'] == 'ADV-TEST-014':  # Assumption Cascade
            if 'assumption' in output_lower and ('valid' in output_lower or 'invalid' in output_lower):
                details['assumption_validation'] = True
            if 'foundational' in output_lower:
                details['foundational_assumption_testing'] = True
        
        return details
    
    def extract_summary(self, output: str) -> str:
        """Extract key summary information from test output"""
        if not output:
            return "No output"
            
        lines = output.split('\\n')
        summary_lines = []
        
        # Look for summary indicators
        for line in lines:
            if any(indicator in line.lower() for indicator in [
                'passed:', 'failed:', 'success rate:', 'test result:', 
                'overall results:', 'final', 'summary', 'completed',
                'security:', 'synthesis:', 'transfer:', 'boundary:'
            ]):
                summary_lines.append(line.strip())
        
        return ' | '.join(summary_lines[-3:]) if summary_lines else output[:300] + "..."
    
    def run_complete_adversarial_suite(self) -> Dict[str, Any]:
        """Execute the complete adversarial test suite"""
        
        print("🚀 COMPLETE ADVERSARIAL TEST SUITE")
        print("=" * 100)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Comprehensive validation of system capabilities and security")
        print("💡 Includes survivorship bias and assumption cascade tests")
        print("=" * 100)
        
        # Get all test definitions
        test_definitions = self.get_adversarial_test_definitions()
        
        print(f"\\n📊 Test Suite Overview:")
        print(f"   Total tests: {len(test_definitions)}")
        
        # Categorize tests
        categories = {}
        for test_def in test_definitions:
            category = test_def['category']
            categories[category] = categories.get(category, 0) + 1
        
        for category, count in categories.items():
            print(f"   {category}: {count} tests")
        
        security_critical_count = sum(1 for t in test_definitions if t['security_critical'])
        foundational_count = sum(1 for t in test_definitions if t['foundational'])
        
        print(f"   🔒 Security critical: {security_critical_count}")
        print(f"   🏗️ Foundational: {foundational_count}")
        
        # Run each test
        for test_def in test_definitions:
            result = self.run_single_adversarial_test(test_def)
            self.test_results[test_def['test_id']] = result
            
            # Print immediate result
            print(f"\\n📊 {test_def['test_id']} Result: {result['status']}")
            print(f"⏱️  Duration: {result.get('duration', 0):.2f}s")
            if result.get('error'):
                print(f"⚠️  Error: {result['error'][:100]}...")
        
        # Generate comprehensive analysis
        return self.generate_comprehensive_analysis(test_definitions)
    
    def generate_comprehensive_analysis(self, test_definitions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive analysis of all test results"""
        
        total_duration = time.time() - self.start_time
        
        print(f"\\n{'='*100}")
        print("📊 COMPLETE ADVERSARIAL TEST SUITE ANALYSIS")
        print("=" * 100)
        
        # Overall statistics
        print(f"\\n📈 OVERALL STATISTICS:")
        print(f"   Total Tests: {self.total_tests}")
        print(f"   ✅ Passed: {self.passed_tests}")
        print(f"   ❌ Failed: {self.failed_tests}")
        print(f"   🎯 Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        print(f"   ⏱️  Total Duration: {total_duration:.2f}s")
        
        # Security analysis
        security_tests = [t for t in test_definitions if t['security_critical']]
        security_passed = len([t for t in security_tests if self.test_results[t['test_id']]['passed']])
        
        print(f"\\n🛡️ SECURITY CRITICAL ANALYSIS:")
        print(f"   Security Tests: {len(security_tests)}")
        print(f"   ✅ Security Passed: {security_passed}")
        print(f"   ❌ Security Failed: {len(self.security_critical_failures)}")
        if security_tests:
            print(f"   🔒 Security Success Rate: {(security_passed/len(security_tests)*100):.1f}%")
        
        # Foundational capability analysis
        foundational_tests = [t for t in test_definitions if t['foundational']]
        foundational_passed = len([t for t in foundational_tests if self.test_results[t['test_id']]['passed']])
        
        print(f"\\n🏗️ FOUNDATIONAL CAPABILITY ANALYSIS:")
        print(f"   Foundational Tests: {len(foundational_tests)}")
        print(f"   ✅ Foundational Passed: {foundational_passed}")
        print(f"   ❌ Foundational Failed: {len(self.foundational_failures)}")
        if foundational_tests:
            print(f"   🧠 Foundational Success Rate: {(foundational_passed/len(foundational_tests)*100):.1f}%")
        
        # Category analysis
        print(f"\\n📋 CATEGORY ANALYSIS:")
        category_results = {}
        for test_def in test_definitions:
            category = test_def['category']
            passed = self.test_results[test_def['test_id']]['passed']
            
            if category not in category_results:
                category_results[category] = {'total': 0, 'passed': 0}
            
            category_results[category]['total'] += 1
            if passed:
                category_results[category]['passed'] += 1
        
        for category, stats in category_results.items():
            success_rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        # Detailed test results
        print(f"\\n📋 DETAILED TEST RESULTS:")
        for test_id, result in self.test_results.items():
            markers = []
            if result.get('security_critical'):
                markers.append("🔒")
            if result.get('foundational'):
                markers.append("🏗️")
            
            marker_str = "".join(markers) + " " if markers else ""
            
            print(f"\\n   {marker_str}{test_id}: {result['status']}")
            print(f"      Duration: {result.get('duration', 0):.2f}s")
            print(f"      Category: {result.get('category', 'unknown')}")
            
            if result.get('output_summary'):
                print(f"      Summary: {result['output_summary'][:150]}...")
            
            if result.get('detailed_results'):
                print(f"      Capabilities: {', '.join(k for k, v in result['detailed_results'].items() if v)}")
            
            if result.get('error'):
                print(f"      Error: {result['error'][:100]}...")
        
        # Critical findings
        print(f"\\n🚨 CRITICAL FINDINGS:")
        
        if self.security_critical_failures:
            print(f"   ❌ SECURITY VULNERABILITIES:")
            for test_id in self.security_critical_failures:
                test_name = next(t['name'] for t in test_definitions if t['test_id'] == test_id)
                print(f"      • {test_id}: {test_name}")
        
        if self.foundational_failures:
            print(f"   ❌ FOUNDATIONAL CAPABILITY GAPS:")
            for test_id in self.foundational_failures:
                test_name = next(t['name'] for t in test_definitions if t['test_id'] == test_id)
                print(f"      • {test_id}: {test_name}")
        
        # Overall assessment
        all_security_passed = len(self.security_critical_failures) == 0
        foundational_adequate = len(self.foundational_failures) <= 1  # Allow 1 foundational failure
        overall_success = (self.passed_tests / self.total_tests) >= 0.7  # 70% threshold
        
        print(f"\\n🎯 OVERALL SYSTEM ASSESSMENT:")
        
        if all_security_passed and foundational_adequate and overall_success:
            print("   🎉 SYSTEM READY FOR ADVANCED DEPLOYMENT")
            print("   ✅ Security: HARDENED")
            print("   ✅ Capabilities: COMPREHENSIVE")
            print("   ✅ Intelligence: VALIDATED")
            assessment = "PRODUCTION_READY_ADVANCED"
        elif all_security_passed and overall_success:
            print("   🛡️ SYSTEM SECURE FOR DEPLOYMENT")
            print("   ✅ Security: HARDENED")
            print("   ⚠️ Capabilities: SOME GAPS")
            print("   ✅ Intelligence: ADEQUATE")
            assessment = "PRODUCTION_READY_STANDARD"
        elif all_security_passed:
            print("   🔒 SYSTEM SECURE BUT LIMITED")
            print("   ✅ Security: HARDENED")
            print("   ❌ Capabilities: SIGNIFICANT GAPS")
            print("   ⚠️ Intelligence: LIMITED")
            assessment = "SECURE_BUT_LIMITED"
        else:
            print("   🚨 SYSTEM NOT READY FOR DEPLOYMENT")
            print("   ❌ Security: VULNERABLE")
            print("   ❌ Capabilities: INADEQUATE")
            print("   ❌ Intelligence: UNRELIABLE")
            assessment = "NOT_READY"
        
        # Generate final results
        final_results = {
            'test_suite': 'Complete Adversarial Test Suite',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': self.total_tests,
                'passed': self.passed_tests,
                'failed': self.failed_tests,
                'success_rate': (self.passed_tests/self.total_tests*100) if self.total_tests > 0 else 0,
                'duration': total_duration
            },
            'security_analysis': {
                'security_tests': len([t for t in test_definitions if t['security_critical']]),
                'security_passed': len([t for t in test_definitions if t['security_critical']]) - len(self.security_critical_failures),
                'security_failed': len(self.security_critical_failures),
                'security_failures': self.security_critical_failures,
                'all_security_passed': all_security_passed
            },
            'foundational_analysis': {
                'foundational_tests': len([t for t in test_definitions if t['foundational']]),
                'foundational_passed': len([t for t in test_definitions if t['foundational']]) - len(self.foundational_failures),
                'foundational_failed': len(self.foundational_failures),
                'foundational_failures': self.foundational_failures,
                'foundational_adequate': foundational_adequate
            },
            'category_results': category_results,
            'overall_assessment': assessment,
            'individual_results': self.test_results
        }
        
        # Save comprehensive report
        report_file = f"complete_adversarial_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        
        print(f"\\n📝 Comprehensive report saved to: {report_file}")
        print("=" * 100)
        
        return final_results

def main():
    """Execute the complete adversarial test suite"""
    
    print("🎯 MESOPREDATOR PRI - COMPLETE ADVERSARIAL VALIDATION")
    print("🛡️ Testing all aspects: Security, Intelligence, Capabilities, Assumptions")
    print()
    
    runner = CompleteAdversarialTestSuite()
    
    try:
        results = runner.run_complete_adversarial_suite()
        
        # Return success based on overall assessment
        assessment = results['overall_assessment']
        success = assessment in ['PRODUCTION_READY_ADVANCED', 'PRODUCTION_READY_STANDARD']
        
        return success
        
    except KeyboardInterrupt:
        print("\\n🛑 Test suite aborted by user")
        return False
    except Exception as e:
        print(f"\\n💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)