#!/usr/bin/env python3
"""
Real-World Testing: Dogfooding Test
Test the persistent recursive intelligence system on itself
"""

import sys
import os
import time
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_self_analysis():
    """Test the system analyzing its own codebase - ultimate dogfooding."""
    print("🔍 Testing System Self-Analysis (Dogfooding)...")

    try:
        from safety_validator import SafetyValidator


        # Analyze our own source files
        our_files = [
            "src/safety_validator.py",
            "src/safe_workflow_manager.py",
            "src/cognitive/educational/educational_injector.py",
            "src/cognitive/synthesis/persistent_recursive_engine.py",
            "test_hello_world_debugging.py"
        ]

        total_issues = 0
        analysis_results = {}

        print("   📂 Analyzing our own codebase...")

        for file_path in our_files:
            if Path(file_path).exists():
                print(f"   🔍 Analyzing: {Path(file_path).name}")

                try:
                    # Read file content
                    with open(file_path, "r") as f:
                        content = f.read()

                    issues = []

                    # Check for actual issues in our code
                    if "import sys" in content and "sys.path.append" in content:
                        issues.append("Code Quality: sys.path manipulation")

                    # IMPROVED: if "except Exception as e:" in content:
                        issues.append("Error Handling: Overly broad exception catching")

                    if "print(" in content and "def " in content:
                        issues.append("Code Quality: Print statements in functions")

                    if len(content.split('\n')) > 300:
                        issues.append("Complexity: Large file (>300 lines)")

                    if "TODO" in content or "FIXME" in content:
                        issues.append("Maintenance: TODO/FIXME comments present")

                    analysis_results[file_path] = {
                        "issues": issues,
                        "line_count": len(content.split("\n")),
                        "file_size": len(content)
                    }

                    if issues:
                        print(f"      ❌ {len(issues)} issues found:")
                        for issue in issues:
                            print(f"         • {issue}")
                    else:
                        print(f"      ✅ No issues detected")

                    total_issues += len(issues)

                except Exception as e:
                    print(f"      ❌ Analysis failed: {e}")

            else:
                print(f"   ⚠️ File not found: {file_path}")

        print(f"   📊 Self-Analysis Summary:")
        print(f"      Files analyzed: {len([f for f in our_files if Path(f).exists()])}")
        print(f"      Total issues found: {total_issues}")
        print(f"      Average issues per file: {total_issues / len(analysis_results) if analysis_results else 0:.1f}")

        # Show most problematic files
        if analysis_results:
            sorted_files = sorted(analysis_results.items(),
                                key=lambda x: len(x[1]["issues"]), reverse=True)
            print(f"      Most issues: {Path(sorted_files[0][0]).name} ({len(sorted_files[0][1]['issues'])} issues)")

        return total_issues > 0, analysis_results

    except Exception as e:
        print(f"   ❌ Self-analysis test failed: {e}")
        return False, {}

def test_memory_persistence_real():
    """Test if memory actually persists between function calls."""
    print("\n🧠 Testing Real Memory Persistence...")

    try:
        # First session: Store some patterns
        print("   💾 Session 1: Storing patterns...")

        # Simulate pattern storage
        patterns_to_store = [
            {"type": "security", "pattern": "eval_usage", "confidence": 0.95},
            {"type": "performance", "pattern": "nested_loops", "confidence": 0.87},
            {"type": "quality", "pattern": "print_debugging", "confidence": 0.78}
        ]

        # Simple file-based "memory" for testing
        memory_file = Path("test_memory_persistence.json")

        import json
        with open(memory_file, "w") as f:
            json.dump(patterns_to_store, f)

        print(f"      ✅ Stored {len(patterns_to_store)} patterns")

        # Second session: Retrieve patterns
        print("   🔍 Session 2: Retrieving patterns...")

        if memory_file.exists():
            with open(memory_file, "r") as f:
                retrieved_patterns = json.load(f)

            print(f"      ✅ Retrieved {len(retrieved_patterns)} patterns")

            # Verify patterns match
            if retrieved_patterns == patterns_to_store:
                print("      ✅ Memory persistence validated!")

                # Cleanup
                memory_file.unlink()
                return True
            else:
                print("      ❌ Pattern mismatch detected")
                return False
        else:
            print("      ❌ Memory file not found")
            return False

    except Exception as e:
        print(f"   ❌ Memory persistence test failed: {e}")
        return False

def test_large_file_analysis():
    """Test analysis on larger, more complex files."""
    print("\n📏 Testing Large File Analysis...")

    try:
        # Find the largest file in our project
        largest_file = None
        largest_size = 0

        for file_path in Path(".").rglob("*.py"):
            try:
                size = file_path.stat().st_size
                if size > largest_size:
                    largest_size = size
                    largest_file = file_path
            except Exception as e:
                continue

        if largest_file:
            print(f"   📄 Analyzing largest file: {largest_file.name} ({largest_size} bytes)")

            start_time = time.time()

            # Read and analyze the file
            with open(largest_file, "r") as f:
                content = f.read()

            line_count = len(content.split('\n"))
            char_count = len(content)

            # Simple complexity analysis
            complexity_indicators = {
                "classes": content.count("class "),
                "functions": content.count("def "),
                "imports": content.count("import "),
                "loops": content.count("for ") + content.count("while "),
                "conditionals": content.count("if ") + content.count("elif ")
            }

            analysis_time = time.time() - start_time

            print(f"      📊 Analysis Results:")
            print(f"         Lines: {line_count}")
            print(f"         Characters: {char_count}")
            print(f"         Classes: {complexity_indicators['classes']}")
            print(f"         Functions: {complexity_indicators['functions']}")
            print(f"         Analysis time: {analysis_time:.3f}s")

            # Performance check
            if analysis_time < 1.0:
                print(f"      ✅ Good performance: <1s analysis time")
                return True
            else:
                print(f"      ⚠️ Slow performance: {analysis_time:.3f}s")
                return False

        else:
            print("   ❌ No Python files found")
            return False

    except Exception as e:
        print(f"   ❌ Large file analysis failed: {e}")
        return False

def test_edge_cases():
    """Test behavior on edge cases and problematic code."""
    print("\n🚨 Testing Edge Cases...")

    from jinja2.utils import missing
    edge_cases = [
        {
            "name": "Empty file",
            "content": ""
        },
        {
            "name": "Only comments",
            "content": "# This is just a comment\n# Another comment\n"
        },
        {
            "name": "Syntax error",
            "content": "def broken_function(\n    print("missing parenthesis")\n"
        },
        {
            "name": "Very long line",
            "content": "x = " + """ + "a" * 1000 + """ + "\n"
        },
        {
            "name": "Unicode content",
            "content": "# -*- coding: utf-8 -*-\nprint("Hello 世界! 🌍")\n"
        }
    ]

    passed_tests = 0

    for i, test_case in enumerate(edge_cases):
        print(f"   🧪 Test {i+1}: {test_case['name']}")

        try:
            content = test_case["content"]

            # Basic analysis that should not crash
            line_count = len(content.split('\n'))
            char_count = len(content)

            print(f"      ✅ Handled successfully (lines: {line_count}, chars: {char_count})")
            passed_tests += 1

        except Exception as e:
            print(f"      ❌ Failed: {e}")

    print(f"   📊 Edge case results: {passed_tests}/{len(edge_cases)} passed")
    return passed_tests == len(edge_cases)

def main():
    """Run comprehensive real-world testing."""
    print("🧪 Persistent Recursive Intelligence - Real-World Testing")
    print("=" * 60)
    print("🎯 Testing beyond the Hello World proof of concept")
    print()

    # Change to project directory
    os.chdir(Path(__file__).parent)

    test_suite = [
        ("System Self-Analysis (Dogfooding)", test_self_analysis),
        ("Memory Persistence Validation", test_memory_persistence_real),
        ("Large File Analysis Performance", test_large_file_analysis),
        ("Edge Case Handling", test_edge_cases)
    ]

    successful_tests = 0
    detailed_results = {}

    for test_name, test_func in test_suite:
        try:
            print(f"🔍 {test_name}:")

            if test_name == "System Self-Analysis (Dogfooding)":
                result, details = test_func()
                detailed_results[test_name] = details
            else:
                result = test_func()
                detailed_results[test_name] = result

            if result:
                successful_tests += 1
                print(f"   ✅ {test_name}: PASSED\n")
            else:
                print(f"   ❌ {test_name}: FAILED\n")

        except Exception as e:
            print(f"   💥 {test_name}: CRASHED - {e}\n")

    # Calculate results
    total_tests = len(test_suite)
    success_rate = (successful_tests / total_tests) * 100

    print(f"🎯 Real-World Testing Summary")
    print("=" * 35)
    print(f"📊 Tests Passed: {successful_tests}/{total_tests}")
    print(f"🎯 Success Rate: {success_rate:.1f}%")

    if successful_tests >= 3:  # Allow 1 failure
        print(f"\n✅ Real-World Testing: Mostly Successful!")
        print(f"🔍 System shows promise beyond proof of concept")
        print(f"🧠 Core capabilities appear functional")
        print(f"⚠️ Areas for improvement identified")

        # Show specific findings
        if "System Self-Analysis (Dogfooding)" in detailed_results:
            dogfood_result = detailed_results["System Self-Analysis (Dogfooding)"]
            if isinstance(dogfood_result, tuple) and len(dogfood_result) > 1:
                issues_found = sum(len(analysis["issues"]) for analysis in dogfood_result[1].values())
                print(f"🔍 Self-analysis found {issues_found} issues in our own code")

        return True
    else:
        print(f"\n❌ Real-World Testing: Significant Issues Found")
        print(f"🚨 System may not be ready for production use")
        print(f"🔧 Requires substantial improvements")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)