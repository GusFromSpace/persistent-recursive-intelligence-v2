#!/usr/bin/env python3
"""
ADV-TEST-013: The "Survivorship Bias" Test - Invisible Vulnerability Detection

This test is inspired by WWII aircraft analysis: the planes that returned showed 
where they could survive damage, not where they needed protection. Similarly, 
our successful tests may hide the critical failure modes we haven't discovered.

Hypothesis to Disprove: The system's apparent robustness is due to survivorship bias.
We're only testing scenarios that "return" (run successfully), missing critical 
failure modes that prevent tests from completing or being designed.
"""

import json
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

import psutil


class SurvivorshipBiasTest:
    """Test for invisible vulnerabilities and failure modes"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        self.system_crashes = []
        self.resource_exhaustions = []
        self.infinite_loops = []
        
    def create_pathological_scenarios(self) -> List[Dict[str, Any]]:
        """Create scenarios designed to trigger invisible failure modes"""
        
        scenarios = [
            {
                'name': 'Memory Exhaustion Bomb',
                'description': 'Code designed to exhaust system memory during analysis',
                'failure_mode': 'resource_exhaustion',
                'code': '''#!/usr/bin/env python3
"""
Memory Exhaustion Pattern - Tests system resource limits

This code appears innocent but contains patterns that could cause
exponential memory growth during static analysis.
"""

class MemoryBomb:
    def __init__(self, depth=0):
        self.depth = depth
        self.data = [0] * (10 ** min(depth, 6))  # Exponential growth
        
        # Recursive data structure that could cause analysis loops
        if depth < 100:  # Appears limited but isn't in practice
            self.children = [MemoryBomb(depth + 1) for _ in range(min(2, 10-depth))]
        
        # String operations that could explode during pattern matching
        self.massive_string = "x" * (2 ** min(depth, 20))
        
        # Nested dictionaries that could cause analysis recursion
        self.nested_dict = self._create_nested_dict(depth)
    
    def _create_nested_dict(self, depth):
        """Create deeply nested dictionary structure"""
        if depth <= 0:
            return {"end": "value"}
        return {
            f"level_{depth}": self._create_nested_dict(depth - 1),
            f"data_{depth}": list(range(min(1000, depth * 100))),
            f"refs_{depth}": [self] * min(10, depth)  # Circular references
        }
    
    def analyze_pattern(self, pattern_data):
        """Method that could trigger analysis recursion"""
        if isinstance(pattern_data, dict):
            return {k: self.analyze_pattern(v) for k, v in pattern_data.items()}
        elif isinstance(pattern_data, list):
            return [self.analyze_pattern(item) for item in pattern_data]
        else:
            # Pattern that could cause regex explosion
            return str(pattern_data) * min(1000, len(str(pattern_data)))

# Global variable that could cause analysis memory issues
GLOBAL_MEMORY_STRUCTURE = MemoryBomb(depth=10)

def recursive_function(n=1000):
    """Function with deep recursion that could crash analysis"""
    if n <= 0:
        return GLOBAL_MEMORY_STRUCTURE
    return recursive_function(n - 1)

# Code patterns that could trigger pathological analysis behavior
REGEX_BOMB = "a" * 1000 + "!" * 1000  # Could cause regex engine issues
NESTED_COMPREHENSION = [[[[x for x in range(y)] for y in range(z)] for z in range(w)] for w in range(10)]
'''
            },
            {
                'name': 'Infinite Loop Trigger',
                'description': 'Code with subtle infinite loop patterns',
                'failure_mode': 'infinite_loop',
                'code': '''#!/usr/bin/env python3
"""
Infinite Loop Patterns - Tests analysis termination

Contains subtle patterns that could cause analysis to never terminate.
"""

class InfiniteLoopTrigger:
    def __init__(self):
        self.state = 0
        self.visited = set()
    
    def subtle_infinite_loop(self):
        """Loop that appears finite but may not terminate during analysis"""
        # Pattern 1: Float precision issues
        x = 0.1
        while x != 1.0:  # May never be exactly 1.0 due to floating point
            x += 0.1
            if x > 10:  # Safety that analysis might miss
                break
    
    def analysis_loop_trigger(self, data):
        """Could trigger infinite analysis loops"""
        # Pattern 2: Circular data structure navigation
        current = data
        while hasattr(current, 'next') and current.next:
            if id(current) in self.visited:
                break  # Cycle detection that analysis might miss
            self.visited.add(id(current))
            current = current.next
    
    def regex_catastrophic_backtracking(self, text):
        """Pattern that could cause regex engine infinite loops"""
        import re
        # Catastrophic backtracking pattern
        pattern = r"(a+)+"
        # Text designed to trigger exponential backtracking
        evil_text = "a" * 30 + "b"  # Won't match but causes exponential search
        return re.search(pattern, evil_text)
    
    def state_machine_loop(self):
        """State machine that could loop indefinitely during analysis"""
        state = "start"
        transitions = {
            "start": "middle",
            "middle": "end", 
            "end": "start"  # Cycle that analysis might follow forever
        }
        
        # Analysis following state transitions might not detect cycle
        visited_states = []
        while state not in visited_states:
            visited_states.append(state)
            state = transitions.get(state, "start")
            if len(visited_states) > 1000:  # Safety that analysis might miss
                break

# Global circular reference that could confuse analysis
class CircularRef:
    def __init__(self):
        self.ref = self

GLOBAL_CIRCULAR = CircularRef()
GLOBAL_CIRCULAR.ref.ref = GLOBAL_CIRCULAR  # Deep circular reference
'''
            },
            {
                'name': 'Analysis Confusion Matrix',
                'description': 'Code designed to confuse static analysis',
                'failure_mode': 'analysis_confusion',
                'code': '''#!/usr/bin/env python3
"""
Analysis Confusion Patterns - Tests analysis accuracy under adversarial conditions

This code is designed to confuse static analysis tools with misleading patterns.
"""

# Misleading imports and aliases
import os as database
import sys as network
import json as security
from pathlib import Path as DatabaseConnection

class AnalysisConfusion:
    """Class designed to mislead static analysis"""
    
    def __init__(self):
        # Misleading variable names
        self.safe_operation = self._dangerous_operation
        self.read_file = self._write_file
        self.validate_input = self._execute_code
        
    def _dangerous_operation(self):
        """Function that does the opposite of what name suggests"""
        # This looks like database operation but isn't
        return database.system("echo 'not actually dangerous'")
    
    def _write_file(self, filename):
        """Function that reads despite the name"""
        try:
            with open(filename, 'r') as f:
                return f.read()
        except:
            return "file not found"
    
    def _execute_code(self, user_input):
        """Function that validates despite the name"""
        # Appears to execute but actually validates
        dangerous_patterns = ['exec', 'eval', 'system', '__import__']
        return not any(pattern in str(user_input) for pattern in dangerous_patterns)
    
    def misleading_security_check(self, code_string):
        """Security check that's actually insecure"""
        # Appears to be security validation
        if "malicious" in code_string.lower():
            return False  # Appears secure
        
        # But actually executes the code!
        try:
            # This is the real security issue, hidden by misleading logic above
            compiled = compile(code_string, '<string>', 'exec')
            # Note: Not actually executing, just compiling (still dangerous for analysis)
            return True
        except:
            return False
    
    def reverse_logic_pattern(self, condition):
        """Pattern where logic is reversed from expected"""
        # Double negative that could confuse analysis
        if not not condition:  # Same as `if condition` but confusing
            return self.insecure_when_true()
        else:
            return self.secure_when_false()
    
    def insecure_when_true(self):
        """Insecure operation when condition is true (opposite of expected)"""
        # Analysis might assume this is the secure path
        return eval("2+2")  # Hidden eval() call
    
    def secure_when_false(self):
        """Secure operation when condition is false"""
        return "secure_result"

# Dynamic code generation that could confuse analysis
def generate_confusing_code():
    """Generates code that analysis might misinterpret"""
    # String manipulation that creates executable code
    parts = ["ex", "ec", "(", "2+2", ")"]
    dangerous_call = parts[0] + parts[1] + parts[2] + parts[3] + parts[4]
    # Analysis might not detect that this creates "exec(2+2)"
    return dangerous_call

# Obfuscated patterns
obfuscated_dict = {
    bytes([101, 120, 101, 99]).decode(): "hidden_exec",
    "".join(chr(i) for i in [101, 118, 97, 108]): "hidden_eval"
}

# Meta-programming that could confuse analysis
class MetaConfusion(type):
    def __new__(cls, name, bases, attrs):
        # Dynamically modifies class during creation
        if 'safe_method' in attrs:
            attrs['safe_method'] = lambda self: eval("__import__('os').system('echo meta')")
        return super().__new__(cls, name, bases, attrs)

class TrickyClass(metaclass=MetaConfusion):
    def safe_method(self):
        """Method that appears safe but is modified by metaclass"""
        return "apparently safe"
'''
            },
            {
                'name': 'Resource Race Conditions',
                'description': 'Code with timing-dependent failure modes',
                'failure_mode': 'race_conditions',
                'code': '''#!/usr/bin/env python3
"""
Race Condition Patterns - Tests concurrent analysis scenarios

Contains patterns that could fail unpredictably based on timing.
"""

import threading
import time
import tempfile
import os
from concurrent.futures import ThreadPoolExecutor

class RaceConditionTrigger:
    """Class with race condition vulnerabilities"""
    
    def __init__(self):
        self.shared_state = {}
        self.lock = threading.Lock()
        self.temp_files = []
    
    def unsafe_file_operations(self):
        """File operations with race conditions"""
        # TOCTOU (Time of Check Time of Use) vulnerability
        temp_file = tempfile.mktemp()  # Insecure temp file creation
        
        # Race condition: file could be created/modified between check and use
        if not os.path.exists(temp_file):
            time.sleep(0.001)  # Small delay that could trigger race
            with open(temp_file, 'w') as f:
                f.write("potentially unsafe content")
        
        return temp_file
    
    def concurrent_state_modification(self):
        """Shared state modification without proper locking"""
        
        def worker_thread(thread_id):
            # Race condition: multiple threads modifying shared state
            for i in range(100):
                # Missing lock here creates race condition
                current_value = self.shared_state.get('counter', 0)
                time.sleep(0.0001)  # Timing window for race condition
                self.shared_state['counter'] = current_value + 1
                
                # Another race condition with file operations
                self.temp_files.append(f"temp_{thread_id}_{i}.txt")
        
        # Start multiple threads that race against each other
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Join threads (proper) but damage already done
        for thread in threads:
            thread.join()
    
    def timing_dependent_validation(self, user_input):
        """Validation that depends on timing"""
        start_time = time.time()
        
        # Validation logic that changes based on timing
        if time.time() - start_time < 0.001:
            # Fast path: less secure validation
            return len(user_input) < 1000
        else:
            # Slow path: more secure validation
            dangerous_patterns = ['exec', 'eval', 'import', 'open']
            return not any(pattern in user_input for pattern in dangerous_patterns)
    
    def resource_leak_pattern(self):
        """Pattern that could leak resources during analysis"""
        files = []
        try:
            # Open many files without proper cleanup
            for i in range(1000):
                f = open(f"/tmp/leak_{i}.txt", "w")
                files.append(f)
                # Analysis might not detect that files aren't being closed
                
        except Exception:
            # Incomplete cleanup on exception
            for f in files[:len(files)//2]:  # Only close half the files
                try:
                    f.close()
                except:
                    pass

# Thread-unsafe global state
GLOBAL_COUNTER = 0
GLOBAL_FILES = []

def thread_unsafe_function():
    """Function that's not thread-safe"""
    global GLOBAL_COUNTER, GLOBAL_FILES
    
    # Race condition on global state
    temp = GLOBAL_COUNTER
    time.sleep(0.001)  # Timing window
    GLOBAL_COUNTER = temp + 1
    
    # Resource leak in concurrent context
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    GLOBAL_FILES.append(temp_file.name)
    # File never cleaned up in concurrent scenarios

# Timing-based security bypass
def time_based_auth_bypass():
    """Authentication that can be bypassed with timing attacks"""
    correct_password = "secret123"
    
    def check_password(user_password):
        """Vulnerable to timing attacks"""
        # Early return creates timing difference
        if len(user_password) != len(correct_password):
            return False
        
        # Character-by-character comparison (timing attack vulnerable)
        for i, char in enumerate(correct_password):
            if i >= len(user_password) or user_password[i] != char:
                return False
            # Timing difference reveals correct characters
        
        return True
    
    return check_password
'''
            }
        ]
        
        return scenarios
    
    def create_pathological_test_environment(self, scenarios: List[Dict[str, Any]]) -> Path:
        """Create test environment with pathological scenarios"""
        
        self.temp_dir = Path(tempfile.mkdtemp(prefix="survivorship_test_"))
        
        for i, scenario in enumerate(scenarios):
            scenario_dir = self.temp_dir / f"scenario_{i:02d}_{scenario['name'].lower().replace(' ', '_')}"
            scenario_dir.mkdir(exist_ok=True)
            
            # Write the pathological code
            code_file = scenario_dir / "pathological_code.py"
            code_file.write_text(scenario['code'])
            
            # Create a README explaining the expected failure mode
            readme_content = f"""# {scenario['name']}

## Description
{scenario['description']}

## Expected Failure Mode
{scenario['failure_mode']}

## Testing Purpose
This scenario is designed to trigger invisible vulnerabilities that normal tests might miss.
If the analysis system crashes, hangs, or behaves unexpectedly, this reveals a failure mode
that our standard tests don't detect.

## Success Criteria
- System should either handle this gracefully OR
- Fail in a predictable, safe manner
- Should NOT crash the entire system
- Should NOT consume unlimited resources
"""
            
            (scenario_dir / "README.md").write_text(readme_content)
        
        return self.temp_dir
    
    def monitor_system_resources(self) -> Dict[str, Any]:
        """Monitor system resources during test execution"""
        
        def get_current_usage():
            try:
                process = psutil.Process()
                return {
                    'memory_mb': process.memory_info().rss / 1024 / 1024,
                    'cpu_percent': process.cpu_percent(),
                    'open_files': len(process.open_files()),
                    'threads': process.num_threads(),
                    'timestamp': time.time()
                }
            except:
                return None
        
        initial_usage = get_current_usage()
        time.sleep(1)  # Let CPU percent stabilize
        
        return {
            'initial_usage': initial_usage,
            'monitoring_active': True
        }
    
    def run_pathological_analysis(self, scenario_dir: Path, timeout: int = 60) -> Dict[str, Any]:
        """Run analysis on pathological code with monitoring"""
        
        scenario_name = scenario_dir.name
        print(f"🧪 Testing scenario: {scenario_name}")
        
        # Start resource monitoring
        monitoring = self.monitor_system_resources()
        start_time = time.time()
        
        try:
            # Run analysis with timeout
            result = subprocess.run([
                sys.executable, "-c", """
import sys
sys.path.insert(0, '.')
import mesopredator_cli
mesopredator_cli.main()
""", "analyze", str(scenario_dir)
            ],
            capture_output=True,
            text=True,
            timeout=timeout
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Check for resource exhaustion patterns
            output_text = result.stdout + result.stderr
            
            resource_issues = []
            if "memory" in output_text.lower() and "error" in output_text.lower():
                resource_issues.append("memory_error")
            if execution_time > timeout * 0.8:  # Used >80% of timeout
                resource_issues.append("near_timeout")
            if result.returncode < 0:  # Killed by signal
                resource_issues.append("killed_by_signal")
            
            return {
                'scenario': scenario_name,
                'completed': True,
                'execution_time': execution_time,
                'return_code': result.returncode,
                'resource_issues': resource_issues,
                'output_length': len(output_text),
                'stdout': result.stdout[-500:] if result.stdout else "",
                'stderr': result.stderr[-500:] if result.stderr else "",
                'survival_status': 'survived' if result.returncode == 0 else 'failed_safely'
            }
            
        except subprocess.TimeoutExpired:
            print(f"   ⏱️ Scenario timed out after {timeout}s")
            return {
                'scenario': scenario_name,
                'completed': False,
                'execution_time': timeout,
                'resource_issues': ['timeout'],
                'survival_status': 'timeout_failure',
                'failure_mode': 'infinite_loop_or_hang'
            }
            
        except Exception as e:
            print(f"   💥 Scenario crashed: {e}")
            return {
                'scenario': scenario_name,
                'completed': False,
                'execution_time': time.time() - start_time,
                'resource_issues': ['system_crash'],
                'survival_status': 'crash_failure',
                'failure_mode': 'system_crash',
                'error': str(e)
            }
    
    def run_survivorship_bias_test(self) -> Dict[str, Any]:
        """Execute the complete survivorship bias test"""
        
        print("🛩️ ADV-TEST-013: SURVIVORSHIP BIAS VULNERABILITY TEST")
        print("=" * 80)
        print("🎯 Testing for invisible failure modes and pathological scenarios")
        print("🔬 Hypothesis: System robustness is biased by successful test scenarios")
        print("💡 Inspired by WWII aircraft analysis - testing the 'planes that didn't return'")
        print()
        
        # Create pathological scenarios
        print("💣 Creating pathological test scenarios...")
        scenarios = self.create_pathological_scenarios()
        test_env = self.create_pathological_test_environment(scenarios)
        print(f"✅ Created {len(scenarios)} pathological scenarios in {test_env}")
        
        # Run each pathological scenario
        test_results = []
        crash_count = 0
        timeout_count = 0
        resource_issue_count = 0
        
        for scenario_dir in sorted(test_env.iterdir()):
            if scenario_dir.is_dir() and scenario_dir.name.startswith('scenario_'):
                result = self.run_pathological_analysis(scenario_dir, timeout=60)
                test_results.append(result)
                
                # Count failure modes
                if result['survival_status'] == 'crash_failure':
                    crash_count += 1
                elif result['survival_status'] == 'timeout_failure':
                    timeout_count += 1
                
                if result.get('resource_issues'):
                    resource_issue_count += 1
                
                # Print immediate results
                survival_status = result['survival_status']
                if survival_status == 'survived':
                    print(f"   ✅ Survived: {scenario_dir.name}")
                elif survival_status == 'failed_safely':
                    print(f"   ⚠️ Failed safely: {scenario_dir.name}")
                elif survival_status == 'timeout_failure':
                    print(f"   ⏱️ Timed out: {scenario_dir.name}")
                elif survival_status == 'crash_failure':
                    print(f"   💥 Crashed: {scenario_dir.name}")
        
        # Calculate survivorship metrics
        total_scenarios = len(test_results)
        survived_count = len([r for r in test_results if r['survival_status'] == 'survived'])
        failed_safely_count = len([r for r in test_results if r['survival_status'] == 'failed_safely'])
        
        survival_rate = (survived_count + failed_safely_count) / total_scenarios if total_scenarios > 0 else 0
        
        # Identify invisible vulnerabilities
        invisible_vulnerabilities = []
        
        if crash_count > 0:
            invisible_vulnerabilities.append({
                'type': 'system_crash',
                'count': crash_count,
                'description': 'System crashes on pathological input'
            })
        
        if timeout_count > 0:
            invisible_vulnerabilities.append({
                'type': 'infinite_loops',
                'count': timeout_count,
                'description': 'System hangs indefinitely on certain patterns'
            })
        
        if resource_issue_count > 0:
            invisible_vulnerabilities.append({
                'type': 'resource_exhaustion',
                'count': resource_issue_count,
                'description': 'System exhausts resources during analysis'
            })
        
        # Test passes if no critical invisible vulnerabilities found
        critical_failures = crash_count + timeout_count
        test_passed = critical_failures == 0 and survival_rate >= 0.8
        
        final_results = {
            'test_id': 'ADV-TEST-013',
            'test_name': 'Survivorship Bias Vulnerability Test',
            'timestamp': datetime.now().isoformat(),
            'pathological_scenarios': {
                'total': total_scenarios,
                'survived': survived_count,
                'failed_safely': failed_safely_count,
                'crashed': crash_count,
                'timed_out': timeout_count,
                'resource_issues': resource_issue_count
            },
            'survival_rate': survival_rate,
            'invisible_vulnerabilities': invisible_vulnerabilities,
            'test_passed': test_passed,
            'individual_results': test_results,
            'test_environment': str(test_env)
        }
        
        # Print comprehensive analysis
        print(f"\n📊 SURVIVORSHIP BIAS TEST RESULTS:")
        print(f"   Total pathological scenarios: {total_scenarios}")
        print(f"   ✅ Survived cleanly: {survived_count}")
        print(f"   ⚠️ Failed safely: {failed_safely_count}")
        print(f"   💥 System crashes: {crash_count}")
        print(f"   ⏱️ Infinite loops/timeouts: {timeout_count}")
        print(f"   🔋 Resource issues: {resource_issue_count}")
        print(f"   📈 Survival rate: {survival_rate:.1%}")
        
        if invisible_vulnerabilities:
            print(f"\n🚨 INVISIBLE VULNERABILITIES DETECTED:")
            for vuln in invisible_vulnerabilities:
                print(f"   • {vuln['type']}: {vuln['count']} instances - {vuln['description']}")
        
        if test_passed:
            print("\n🎉 SURVIVORSHIP BIAS TEST PASSED!")
            print("✅ No critical invisible vulnerabilities detected")
            print("🛡️ System handles pathological scenarios gracefully")
            print("💪 Robust against adversarial analysis conditions")
        else:
            print("\n❌ SURVIVORSHIP BIAS TEST FAILED")
            print("🚨 Critical invisible vulnerabilities discovered")
            print("⚠️ System shows brittleness under pathological conditions")
            print("🔧 These failure modes were hidden by normal test scenarios")
            
            if crash_count > 0:
                print(f"   💥 {crash_count} scenarios caused system crashes")
            if timeout_count > 0:
                print(f"   ⏱️ {timeout_count} scenarios caused infinite loops/hangs")
        
        return final_results
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Test environment cleaned up")

def main():
    """Execute ADV-TEST-013: Survivorship Bias Test"""
    
    tester = SurvivorshipBiasTest()
    
    try:
        results = tester.run_survivorship_bias_test()
        
        # Save results
        results_file = "survivorship_bias_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to {results_file}")
        
        return results['test_passed']
    
    finally:
        tester.cleanup_test_environment()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)