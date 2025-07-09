"""
Performance Regression Testing Suite
Validates that new changes don't degrade analysis performance
"""

import pytest
import time
import json
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
import psutil
import statistics

from src.cognitive.persistent_recursion import analyze_project
from src.cognitive.enhanced_patterns.code_connector import CodeConnector

class PerformanceBenchmark:
    """Performance benchmark tracker"""
    
    def __init__(self):
        self.baseline_file = "performance_baseline.json"
        self.load_baseline()
    
    def load_baseline(self):
        """Load performance baseline from file"""
        if os.path.exists(self.baseline_file):
            with open(self.baseline_file, 'r') as f:
                self.baseline = json.load(f)
        else:
            # Default baseline values (conservative estimates)
            self.baseline = {
                "small_project_analysis_time": 30.0,  # seconds
                "medium_project_analysis_time": 120.0,
                "memory_usage_mb": 512,
                "files_per_second": 5.0,
                "code_connector_time": 5.0,
                "adversarial_test_time": 300.0
            }
    
    def save_baseline(self, results: Dict[str, float]):
        """Save new baseline results"""
        self.baseline.update(results)
        with open(self.baseline_file, 'w') as f:
            json.dump(self.baseline, f, indent=2)
    
    def check_regression(self, test_name: str, actual_value: float, 
                        threshold_percent: float = 20.0) -> bool:
        """Check if performance regressed beyond threshold"""
        if test_name not in self.baseline:
            return True  # No baseline, assume OK
        
        baseline_value = self.baseline[test_name]
        percent_change = ((actual_value - baseline_value) / baseline_value) * 100
        
        return percent_change <= threshold_percent

@pytest.fixture
def performance_benchmark():
    """Fixture for performance benchmark tracking"""
    return PerformanceBenchmark()

@pytest.fixture
def test_projects():
    """Create test projects of various sizes for benchmarking"""
    projects = {}
    
    # Small project (5-10 files)
    small_project = tempfile.mkdtemp(prefix="perf_test_small_")
    projects["small"] = small_project
    
    # Create small Python project
    (Path(small_project) / "main.py").write_text("""
def main():
    print("Hello World")
    
if __name__ == "__main__":
    main()
""")
    
    (Path(small_project) / "utils.py").write_text("""
def helper_function(x):
    return x * 2

def unused_function():
    pass  # Dead code for detection
""")
    
    (Path(small_project) / "config.py").write_text("""
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
""")
    
    # Medium project (20-50 files)
    medium_project = tempfile.mkdtemp(prefix="perf_test_medium_")
    projects["medium"] = medium_project
    
    # Create directory structure
    src_dir = Path(medium_project) / "src"
    src_dir.mkdir()
    tests_dir = Path(medium_project) / "tests"
    tests_dir.mkdir()
    
    # Create multiple modules
    for i in range(10):
        (src_dir / f"module_{i}.py").write_text(f"""
class Module{i}:
    def __init__(self):
        self.value = {i}
    
    def process(self, data):
        return data + self.value
    
    def unused_method(self):
        # TODO: Implement this
        pass
""")
        
        (tests_dir / f"test_module_{i}.py").write_text(f"""
import unittest
from src.module_{i} import Module{i}

class TestModule{i}(unittest.TestCase):
    def test_process(self):
        module = Module{i}()
        result = module.process(10)
        self.assertEqual(result, {10 + i})
""")
    
    yield projects
    
    # Cleanup
    for project_path in projects.values():
        shutil.rmtree(project_path, ignore_errors=True)

class TestPerformanceRegression:
    """Performance regression test suite"""
    
    def test_small_project_analysis_performance(self, test_projects, performance_benchmark):
        """Test analysis performance on small projects"""
        project_path = test_projects["small"]
        
        # Measure analysis time
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        results = analyze_project(
            project_path=project_path,
            max_depth=2,
            enable_learning=True
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        analysis_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        # Performance assertions
        assert analysis_time < 30.0, f"Small project analysis took {analysis_time:.2f}s (>30s)"
        assert memory_usage < 200, f"Memory usage {memory_usage:.1f}MB too high for small project"
        
        # Check regression
        assert performance_benchmark.check_regression("small_project_analysis_time", analysis_time)
        
        # Calculate files per second
        file_count = len([f for f in Path(project_path).rglob("*.py")])
        files_per_second = file_count / analysis_time if analysis_time > 0 else 0
        
        print(f"Small project performance:")
        print(f"  Analysis time: {analysis_time:.2f}s")
        print(f"  Memory usage: {memory_usage:.1f}MB")
        print(f"  Files analyzed: {file_count}")
        print(f"  Files/second: {files_per_second:.2f}")
        
        return {
            "small_project_analysis_time": analysis_time,
            "files_per_second": files_per_second,
            "memory_usage_mb": memory_usage
        }
    
    def test_medium_project_analysis_performance(self, test_projects, performance_benchmark):
        """Test analysis performance on medium projects"""
        project_path = test_projects["medium"]
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        results = analyze_project(
            project_path=project_path,
            max_depth=2,
            enable_learning=True
        )
        
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        analysis_time = end_time - start_time
        memory_usage = end_memory - start_memory
        
        # Performance assertions for medium projects
        assert analysis_time < 120.0, f"Medium project analysis took {analysis_time:.2f}s (>120s)"
        assert memory_usage < 500, f"Memory usage {memory_usage:.1f}MB too high for medium project"
        
        # Check regression
        assert performance_benchmark.check_regression("medium_project_analysis_time", analysis_time)
        
        file_count = len([f for f in Path(project_path).rglob("*.py")])
        files_per_second = file_count / analysis_time if analysis_time > 0 else 0
        
        print(f"Medium project performance:")
        print(f"  Analysis time: {analysis_time:.2f}s")
        print(f"  Memory usage: {memory_usage:.1f}MB")
        print(f"  Files analyzed: {file_count}")
        print(f"  Files/second: {files_per_second:.2f}")
        
        return {
            "medium_project_analysis_time": analysis_time,
            "files_per_second": files_per_second
        }
    
    def test_code_connector_performance(self, test_projects, performance_benchmark):
        """Test Code Connector performance"""
        project_path = test_projects["medium"]
        
        connector = CodeConnector()
        
        start_time = time.time()
        
        # Run code connector analysis
        orphaned_files = [str(p) for p in Path(project_path).rglob("*.py")][:5]
        main_files = [str(p) for p in Path(project_path).rglob("*.py")][5:10]
        
        results = connector.analyze_connections(
            orphaned_files=orphaned_files,
            main_files=main_files,
            threshold=0.3
        )
        
        end_time = time.time()
        connector_time = end_time - start_time
        
        # Performance assertion
        assert connector_time < 10.0, f"Code Connector took {connector_time:.2f}s (>10s)"
        
        # Check regression
        assert performance_benchmark.check_regression("code_connector_time", connector_time)
        
        print(f"Code Connector performance:")
        print(f"  Analysis time: {connector_time:.2f}s")
        print(f"  Files analyzed: {len(orphaned_files + main_files)}")
        print(f"  Connections found: {len(results.get('connections', []))}")
        
        return {"code_connector_time": connector_time}
    
    def test_memory_leak_detection(self, test_projects):
        """Test for memory leaks during repeated analysis"""
        project_path = test_projects["small"]
        
        memory_readings = []
        
        # Run analysis multiple times
        for i in range(5):
            start_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            results = analyze_project(
                project_path=project_path,
                max_depth=1,
                enable_learning=False  # Disable learning to isolate memory usage
            )
            
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            memory_readings.append(end_memory - start_memory)
            
            # Small delay between runs
            time.sleep(0.1)
        
        # Check for memory leaks (increasing trend)
        avg_first_half = statistics.mean(memory_readings[:2])
        avg_second_half = statistics.mean(memory_readings[3:])
        
        memory_growth = avg_second_half - avg_first_half
        
        assert memory_growth < 50, f"Potential memory leak detected: {memory_growth:.1f}MB growth"
        
        print(f"Memory leak test:")
        print(f"  Memory readings: {[f'{m:.1f}MB' for m in memory_readings]}")
        print(f"  Memory growth: {memory_growth:.1f}MB")
    
    def test_concurrent_analysis_performance(self, test_projects):
        """Test performance under concurrent analysis loads"""
        import threading
        import queue
        
        project_path = test_projects["small"]
        results_queue = queue.Queue()
        
        def analysis_worker():
            start_time = time.time()
            try:
                results = analyze_project(
                    project_path=project_path,
                    max_depth=1,
                    enable_learning=False
                )
                end_time = time.time()
                results_queue.put(("success", end_time - start_time))
            except Exception as e:
                results_queue.put(("error", str(e)))
        
        # Run 3 concurrent analyses
        threads = []
        for i in range(3):
            thread = threading.Thread(target=analysis_worker)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=60)
        
        # Collect results
        successful_runs = 0
        total_time = 0
        
        while not results_queue.empty():
            status, result = results_queue.get()
            if status == "success":
                successful_runs += 1
                total_time += result
            else:
                print(f"Concurrent analysis error: {result}")
        
        assert successful_runs >= 2, f"Only {successful_runs}/3 concurrent analyses succeeded"
        
        avg_time = total_time / successful_runs if successful_runs > 0 else 0
        assert avg_time < 60, f"Average concurrent analysis time {avg_time:.2f}s too high"
        
        print(f"Concurrent analysis performance:")
        print(f"  Successful runs: {successful_runs}/3")
        print(f"  Average time: {avg_time:.2f}s")
    
    def test_performance_baseline_update(self, performance_benchmark):
        """Update performance baseline if running in baseline mode"""
        # This test only runs when explicitly updating baselines
        baseline_mode = os.getenv("UPDATE_PERFORMANCE_BASELINE", "false").lower() == "true"
        
        if not baseline_mode:
            pytest.skip("Baseline update mode not enabled")
        
        # Run performance tests and collect results
        # This would be implemented to update the baseline file
        print("Performance baseline update mode - would update baseline values")

@pytest.mark.performance
class TestScalabilityLimits:
    """Test performance at scale boundaries"""
    
    def test_large_file_analysis(self):
        """Test analysis of very large files"""
        # Create a large Python file
        large_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        
        # Generate a file with many functions (simulate large codebase)
        large_file.write("# Large file performance test\n\n")
        for i in range(1000):
            large_file.write(f"""
def function_{i}(param):
    '''Function {i} for performance testing'''
    result = param * {i}
    return result

""")
        
        large_file.close()
        
        try:
            start_time = time.time()
            
            # Analyze the large file
            results = analyze_project(
                project_path=os.path.dirname(large_file.name),
                max_depth=1,
                enable_learning=False
            )
            
            analysis_time = time.time() - start_time
            
            # Should handle large files reasonably
            assert analysis_time < 300, f"Large file analysis took {analysis_time:.2f}s (>5min)"
            
            print(f"Large file performance:")
            print(f"  File size: {os.path.getsize(large_file.name) / 1024:.1f}KB")
            print(f"  Analysis time: {analysis_time:.2f}s")
            
        finally:
            os.unlink(large_file.name)
    
    def test_deep_directory_structure(self):
        """Test analysis of deeply nested directory structures"""
        base_dir = tempfile.mkdtemp(prefix="deep_structure_test_")
        
        try:
            # Create deep directory structure (10 levels)
            current_dir = Path(base_dir)
            for level in range(10):
                current_dir = current_dir / f"level_{level}"
                current_dir.mkdir()
                
                # Add a Python file at each level
                (current_dir / f"module_level_{level}.py").write_text(f"""
def level_{level}_function():
    return "Level {level}"
""")
            
            start_time = time.time()
            
            results = analyze_project(
                project_path=base_dir,
                max_depth=15,  # Allow deep recursion
                enable_learning=False
            )
            
            analysis_time = time.time() - start_time
            
            assert analysis_time < 60, f"Deep structure analysis took {analysis_time:.2f}s (>60s)"
            
            print(f"Deep structure performance:")
            print(f"  Directory depth: 10 levels")
            print(f"  Analysis time: {analysis_time:.2f}s")
            
        finally:
            shutil.rmtree(base_dir, ignore_errors=True)


if __name__ == "__main__":
    # Run performance tests manually
    pytest.main([__file__, "-v", "-m", "performance"])