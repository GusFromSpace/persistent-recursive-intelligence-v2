#!/usr/bin/env python3
"""
ADV-TEST-004: The "Marathon" Test - Cognitive Endurance & Performance Stability

Tests system stability, performance, and memory management under prolonged continuous load.
Simulates real-world usage patterns with monitoring for cognitive drift and resource leaks.

Hypothesis to Disprove: Under continuous operation, the PRI will suffer from memory leaks,
FAISS index degradation, performance decay, or "cognitive drift" where learned concepts
become polluted or less accurate.
"""

import sys
import os
import time
import json
import psutil
import sqlite3
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import tempfile
import shutil
import statistics

class MarathonTestMonitor:
    """Monitor system performance and cognitive stability during marathon test"""
    
    def __init__(self, test_duration_hours: float = 4.0):  # Reduced from 24h for practical testing
        self.test_duration = timedelta(hours=test_duration_hours)
        self.start_time = datetime.now()
        self.end_time = self.start_time + self.test_duration
        
        self.metrics = {
            'performance_data': [],
            'resource_usage': [],
            'accuracy_checks': [],
            'database_growth': [],
            'faiss_stats': [],
            'errors': []
        }
        
        self.canary_project_path = None
        self.test_projects = []
        self.baseline_accuracy = None
        self.process = None
        
        print(f"🏃‍♂️ Marathon Test Monitor initialized")
        print(f"   Duration: {test_duration_hours} hours")
        print(f"   Start: {self.start_time}")
        print(f"   End: {self.end_time}")
    
    def setup_test_environment(self):
        """Set up the test environment with multiple analysis targets"""
        print("🛠️ Setting up marathon test environment...")
        
        # Create canary project for accuracy testing
        self.canary_project_path = self.create_canary_project()
        
        # Create multiple small test projects for continuous analysis
        self.test_projects = self.create_test_projects(5)
        
        # Get baseline accuracy on canary project
        self.baseline_accuracy = self.measure_canary_accuracy()
        
        print(f"✅ Test environment ready:")
        print(f"   Canary project: {self.canary_project_path}")
        print(f"   Test projects: {len(self.test_projects)}")
        print(f"   Baseline accuracy: {self.baseline_accuracy}")
    
    def create_canary_project(self) -> Path:
        """Create a stable canary project for accuracy testing"""
        canary_dir = Path(tempfile.mkdtemp(prefix="marathon_canary_"))
        
        # Create Python project with known issues
        canary_code = '''#!/usr/bin/env python3
"""
Marathon Test Canary Project
Contains exactly 8 known issues for accuracy testing
"""

def buffer_overflow_risk(data):
    """Issue 1: Potential buffer overflow with unchecked input"""
    buffer = [0] * 10
    for i in range(len(data)):  # Should check bounds
        buffer[i] = data[i]
    return buffer

def sql_injection_risk(user_input):
    """Issue 2: SQL injection vulnerability"""
    query = f"SELECT * FROM users WHERE name = '{user_input}'"  # Unsafe
    return query

def race_condition(shared_counter):
    """Issue 3: Race condition in counter increment"""
    temp = shared_counter.value
    time.sleep(0.001)  # Simulate work
    shared_counter.value = temp + 1  # Non-atomic

def memory_leak_risk():
    """Issue 4: Potential memory leak with unclosed resources"""
    file_handle = open('/tmp/test.txt', 'w')
    file_handle.write("data")
    # Missing file_handle.close()

def infinite_loop_risk(items):
    """Issue 5: Potential infinite loop"""
    i = 0
    while i < len(items):
        if items[i] == "skip":
            continue  # i never increments!
        print(items[i])
        i += 1

def divide_by_zero_risk(denominator):
    """Issue 6: Division by zero without validation"""
    result = 100 / denominator  # Should check if denominator == 0
    return result

def array_bounds_error(arr, index):
    """Issue 7: Array access without bounds checking"""
    return arr[index]  # Should validate index < len(arr)

def password_in_plaintext():
    """Issue 8: Hardcoded password in plaintext"""
    admin_password = "admin123"  # Security vulnerability
    return admin_password

if __name__ == "__main__":
    print("Canary project with 8 known issues")
'''
        
        (canary_dir / "canary_code.py").write_text(canary_code)
        
        # Create README
        readme = """# Marathon Test Canary Project

This project contains exactly 8 known security and quality issues:
1. Buffer overflow risk (unchecked array bounds)
2. SQL injection vulnerability 
3. Race condition in shared counter
4. Memory leak (unclosed file handle)
5. Infinite loop potential
6. Division by zero risk
7. Array bounds error
8. Hardcoded password

Used for testing cognitive accuracy during marathon endurance testing.
"""
        (canary_dir / "README.md").write_text(readme)
        
        return canary_dir
    
    def create_test_projects(self, count: int) -> List[Path]:
        """Create multiple small projects for continuous analysis rotation"""
        projects = []
        
        for i in range(count):
            project_dir = Path(tempfile.mkdtemp(prefix=f"marathon_test_{i}_"))
            
            # Create different types of code patterns
            if i % 3 == 0:
                # Web application pattern
                code = f'''
def handle_request_{i}(request):
    user_data = request.get('data', {{}})
    # Issue: No input validation
    return process_data(user_data)

def process_data(data):
    results = []
    for item in data:
        if item.get('type') == 'special':
            results.append(transform_special(item))
    return results
'''
            elif i % 3 == 1:
                # Data processing pattern
                code = f'''
def analyze_dataset_{i}(dataset):
    totals = []
    for batch in dataset:
        batch_total = 0
        for j in range(len(batch) - 1):  # Off-by-one error
            batch_total += batch[j]
        totals.append(batch_total)
    return totals

def validate_results(results):
    # Issue: No null checking
    return all(r > 0 for r in results)
'''
            else:
                # System integration pattern
                code = f'''
import subprocess

def system_command_{i}(user_cmd):
    # Issue: Command injection risk
    result = subprocess.run(f"ls {{user_cmd}}", shell=True)
    return result.stdout

def cleanup_temp_files():
    import os
    temp_files = os.listdir('/tmp/')
    for file in temp_files:
        os.remove(f"/tmp/{{file}}")  # Issue: No error handling
'''
            
            (project_dir / f"test_code_{i}.py").write_text(code)
            projects.append(project_dir)
        
        return projects
    
    def measure_canary_accuracy(self) -> int:
        """Measure baseline accuracy on canary project"""
        print("📊 Measuring baseline canary accuracy...")
        
        result = self.run_analysis_on_project(self.canary_project_path)
        if result and result.returncode == 0:
            # Count issues found in output
            issues_found = self.count_issues_in_output(result.stdout)
            print(f"   Baseline canary accuracy: {issues_found}/8 issues detected")
            return issues_found
        else:
            print("   ❌ Failed to get baseline accuracy")
            return 0
    
    def run_analysis_on_project(self, project_path: Path, timeout=120):
        """Run PRI analysis on a specific project"""
        try:
            result = subprocess.run([
                sys.executable, "-m", "src.cognitive.persistent_recursion",
                "--project", str(project_path),
                "--max-depth", "2",
                "--batch-size", "10"
            ], 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=Path.cwd(),
            env={**os.environ, 'PYTHONPATH': str(Path.cwd() / 'src')}
            )
            return result
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")
            return None
    
    def count_issues_in_output(self, output: str) -> int:
        """Count issues found in analysis output"""
        lines = output.split('\n')
        for line in lines:
            if "Found" in line and "issues" in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word == "Found" and i + 1 < len(words):
                        try:
                            return int(words[i + 1])
                        except ValueError:
                            continue
        return 0
    
    def get_system_resources(self) -> Dict:
        """Get current system resource usage"""
        try:
            # Get current process info if available
            current_process = psutil.Process()
            memory_info = current_process.memory_info()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'memory_rss_mb': memory_info.rss / 1024 / 1024,
                'memory_vms_mb': memory_info.vms / 1024 / 1024,
                'cpu_percent': current_process.cpu_percent(),
                'system_memory_percent': psutil.virtual_memory().percent,
                'system_cpu_percent': psutil.cpu_percent()
            }
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def get_database_stats(self) -> Dict:
        """Get SQLite database statistics"""
        try:
            db_path = Path("memory_intelligence.db")
            if not db_path.exists():
                return {'error': 'Database not found'}
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get table counts
            cursor.execute("SELECT COUNT(*) FROM memory_entries")
            memory_entries = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM pattern_detections") 
            pattern_detections = cursor.fetchone()[0]
            
            # Get database file size
            db_size_mb = db_path.stat().st_size / 1024 / 1024
            
            conn.close()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'memory_entries': memory_entries,
                'pattern_detections': pattern_detections,
                'database_size_mb': db_size_mb
            }
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def check_cognitive_accuracy(self) -> Dict:
        """Check for cognitive drift by testing canary project"""
        print("🧠 Checking cognitive accuracy...")
        
        current_accuracy = self.measure_canary_accuracy()
        accuracy_retention = (current_accuracy / self.baseline_accuracy * 100) if self.baseline_accuracy > 0 else 0
        
        accuracy_data = {
            'timestamp': datetime.now().isoformat(),
            'current_accuracy': current_accuracy,
            'baseline_accuracy': self.baseline_accuracy,
            'accuracy_retention_percent': accuracy_retention,
            'cognitive_drift_detected': accuracy_retention < 80  # 20% degradation threshold
        }
        
        print(f"   Current accuracy: {current_accuracy}/8")
        print(f"   Retention: {accuracy_retention:.1f}%")
        
        if accuracy_data['cognitive_drift_detected']:
            print("   ⚠️ COGNITIVE DRIFT DETECTED")
        
        return accuracy_data
    
    def run_marathon_test(self):
        """Execute the full marathon endurance test"""
        print("🏃‍♂️ STARTING MARATHON ENDURANCE TEST")
        print("=" * 80)
        
        self.setup_test_environment()
        
        cycle_count = 0
        accuracy_check_interval = 10  # Check accuracy every 10 cycles
        
        try:
            while datetime.now() < self.end_time:
                cycle_start = datetime.now()
                cycle_count += 1
                
                print(f"\n🔄 Marathon Cycle {cycle_count}")
                print(f"   Time elapsed: {datetime.now() - self.start_time}")
                print(f"   Time remaining: {self.end_time - datetime.now()}")
                
                # Rotate through test projects
                current_project = self.test_projects[cycle_count % len(self.test_projects)]
                print(f"   Analyzing: {current_project.name}")
                
                # Run analysis and measure performance
                analysis_start = time.time()
                result = self.run_analysis_on_project(current_project)
                analysis_duration = time.time() - analysis_start
                
                # Record performance metrics
                performance_data = {
                    'cycle': cycle_count,
                    'timestamp': datetime.now().isoformat(),
                    'analysis_duration_seconds': analysis_duration,
                    'project_analyzed': current_project.name,
                    'success': result is not None and result.returncode == 0,
                    'issues_found': self.count_issues_in_output(result.stdout) if result else 0
                }
                
                self.metrics['performance_data'].append(performance_data)
                
                # Record resource usage
                resource_data = self.get_system_resources()
                self.metrics['resource_usage'].append(resource_data)
                
                # Record database growth
                db_stats = self.get_database_stats()
                self.metrics['database_growth'].append(db_stats)
                
                print(f"   ✅ Analysis completed in {analysis_duration:.2f}s")
                if 'memory_rss_mb' in resource_data:
                    print(f"   📊 Memory usage: {resource_data['memory_rss_mb']:.1f}MB")
                if 'memory_entries' in db_stats:
                    print(f"   💾 DB entries: {db_stats['memory_entries']}")
                
                # Periodic accuracy checks
                if cycle_count % accuracy_check_interval == 0:
                    accuracy_data = self.check_cognitive_accuracy()
                    self.metrics['accuracy_checks'].append(accuracy_data)
                    
                    if accuracy_data['cognitive_drift_detected']:
                        print("🚨 COGNITIVE DRIFT DETECTED - Test may need to stop")
                
                # Brief pause between cycles
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Marathon test interrupted by user")
        except Exception as e:
            print(f"\n💥 Marathon test failed with error: {e}")
            self.metrics['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            })
        
        finally:
            self.cleanup_test_environment()
            return self.analyze_marathon_results()
    
    def analyze_marathon_results(self) -> Dict:
        """Analyze marathon test results and determine success/failure"""
        print("\n📊 ANALYZING MARATHON TEST RESULTS")
        print("=" * 80)
        
        total_cycles = len(self.metrics['performance_data'])
        successful_cycles = sum(1 for p in self.metrics['performance_data'] if p['success'])
        
        # Performance analysis
        analysis_times = [p['analysis_duration_seconds'] for p in self.metrics['performance_data'] if p['success']]
        
        if analysis_times:
            avg_analysis_time = statistics.mean(analysis_times)
            analysis_time_trend = self.calculate_trend(analysis_times)
        else:
            avg_analysis_time = 0
            analysis_time_trend = 0
        
        # Memory analysis
        memory_usages = [r['memory_rss_mb'] for r in self.metrics['resource_usage'] if 'memory_rss_mb' in r]
        memory_leak_detected = False
        
        if len(memory_usages) > 10:
            memory_trend = self.calculate_trend(memory_usages)
            memory_leak_detected = memory_trend > 0.1  # More than 0.1MB per cycle increase
        
        # Cognitive drift analysis
        accuracy_checks = self.metrics['accuracy_checks']
        cognitive_drift_detected = any(check.get('cognitive_drift_detected', False) for check in accuracy_checks)
        
        final_accuracy = accuracy_checks[-1]['accuracy_retention_percent'] if accuracy_checks else 100
        
        # Database growth analysis
        db_entries = [db['memory_entries'] for db in self.metrics['database_growth'] if 'memory_entries' in db]
        db_growth_rate = (db_entries[-1] - db_entries[0]) / total_cycles if len(db_entries) >= 2 else 0
        
        # Success criteria evaluation
        stability_score = successful_cycles / total_cycles if total_cycles > 0 else 0
        performance_stable = abs(analysis_time_trend) < 0.5  # Less than 0.5s increase per cycle
        memory_stable = not memory_leak_detected
        accuracy_stable = not cognitive_drift_detected and final_accuracy >= 80
        
        overall_success = (
            stability_score >= 0.95 and  # 95% success rate
            performance_stable and
            memory_stable and 
            accuracy_stable
        )
        
        results = {
            'test_duration_actual': str(datetime.now() - self.start_time),
            'total_cycles': total_cycles,
            'successful_cycles': successful_cycles,
            'stability_score': stability_score,
            'average_analysis_time': avg_analysis_time,
            'analysis_time_trend': analysis_time_trend,
            'performance_stable': performance_stable,
            'memory_leak_detected': memory_leak_detected,
            'memory_stable': memory_stable,
            'cognitive_drift_detected': cognitive_drift_detected,
            'final_accuracy_retention': final_accuracy,
            'accuracy_stable': accuracy_stable,
            'database_growth_rate': db_growth_rate,
            'overall_success': overall_success,
            'detailed_metrics': self.metrics
        }
        
        # Print results
        print(f"📈 MARATHON TEST RESULTS:")
        print(f"   Duration: {results['test_duration_actual']}")
        print(f"   Cycles completed: {total_cycles}")
        print(f"   Success rate: {stability_score:.1%}")
        print(f"   Average analysis time: {avg_analysis_time:.2f}s")
        print(f"   Performance stable: {'✅' if performance_stable else '❌'}")
        print(f"   Memory stable: {'✅' if memory_stable else '❌'}")
        print(f"   Cognitive accuracy: {'✅' if accuracy_stable else '❌'} ({final_accuracy:.1f}%)")
        print(f"   DB growth rate: {db_growth_rate:.1f} entries/cycle")
        
        if overall_success:
            print("\n🎉 MARATHON TEST PASSED!")
            print("✅ System demonstrated stable performance under continuous load")
        else:
            print("\n❌ MARATHON TEST FAILED")
            print("⚠️ System showed signs of degradation during endurance testing")
        
        return results
    
    def calculate_trend(self, values: List[float]) -> float:
        """Calculate linear trend in a series of values"""
        if len(values) < 2:
            return 0
        
        n = len(values)
        x_vals = list(range(n))
        
        # Simple linear regression slope
        x_mean = sum(x_vals) / n
        y_mean = sum(values) / n
        
        numerator = sum((x_vals[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0
    
    def cleanup_test_environment(self):
        """Clean up temporary test files"""
        print("🧹 Cleaning up test environment...")
        
        try:
            if self.canary_project_path and self.canary_project_path.exists():
                shutil.rmtree(self.canary_project_path)
            
            for project_path in self.test_projects:
                if project_path.exists():
                    shutil.rmtree(project_path)
            
            print("✅ Test environment cleaned up")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

def main():
    """Execute ADV-TEST-004: Marathon Endurance Test"""
    print("🏃‍♂️ ADV-TEST-004: MARATHON ENDURANCE TEST")
    print("=" * 80)
    print("🎯 Testing cognitive endurance and stability under continuous load")
    print("📊 Monitoring for memory leaks, performance decay, and cognitive drift")
    print()
    
    # Use shorter duration for practical testing (can be increased for full test)
    test_duration = 2.0  # 2 hours for demonstration
    
    monitor = MarathonTestMonitor(test_duration_hours=test_duration)
    results = monitor.run_marathon_test()
    
    # Save detailed results
    results_file = "marathon_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📁 Detailed results saved to {results_file}")
    
    return results['overall_success']

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