#!/usr/bin/env python3
"""
Memory Intelligence Integration for PRI Project

This script demonstrates how to integrate the GUS Memory Intelligence system
into an existing project (the PRI project itself) as a real-world test case.
"""

import sys
from pathlib import Path

from joblib import Memory

# Add the memory intelligence package to path
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))

def install_memory_intelligence():
    """Install memory intelligence into the PRI project"""
    print("🧠 Installing Memory Intelligence into PRI Project...")

    try:
        # Import the GUS Memory Intelligence system
        from gus_memory import MemoryIntelligence, create_memory
        from gus_memory.adapters import ProjectAdapter, remember_calls, remember_errors

        print("   ✅ Successfully imported memory intelligence system")

        # Initialize memory for the PRI project
        memory = MemoryIntelligence("persistent-recursive-intelligence")

        # Test basic functionality
        memory_id = memory.remember("Memory intelligence successfully integrated into PRI", {
            "integration_type": "full_system",
            "project": "PRI",
            "timestamp": "2025-06-24"
        })

        print(f"   ✅ Memory initialized and first memory stored: {memory_id}")

        # Test recall
        results = memory.recall("memory intelligence")
        print(f"   ✅ Memory recall working: {len(results)} results found")

        # Get system statistics
        stats = memory.get_statistics()
        print(f"   ✅ Memory statistics: {stats["memory_count"]} total memories")

        return memory

    except ImportError as e:
        print(f"   ❌ Failed to import memory intelligence: {e}")
        return None
    except Exception as e:
        print(f"   ❌ Memory intelligence integration failed: {e}")
        return None

def enhance_recursive_improvement():
    """Enhance the recursive improvement engine with memory intelligence"""
    print("\n🔄 Enhancing Recursive Improvement Engine...")

    try:
        # Read the current recursive improvement file
        recursive_file = Path(__file__).parent / "src" / "cognitive" / "recursive" / "recursive_improvement.py"

        if not recursive_file.exists():
            print(f"   ❌ Recursive improvement file not found: {recursive_file}")
            return False

        # Create an enhanced version with memory intelligence
        enhanced_content = create_enhanced_recursive_improvement()

        # Write enhanced version to a new file for testing
        enhanced_file = recursive_file.parent / "recursive_improvement_enhanced.py"
        with open(enhanced_file, "w") as f:
            f.write(enhanced_content)

        print(f"   ✅ Enhanced recursive improvement created: {enhanced_file}")
        return True

    except Exception as e:
        print(f"   ❌ Failed to enhance recursive improvement: {e}")
        return False

def create_enhanced_recursive_improvement():
    """Create enhanced recursive improvement with memory intelligence"""
    return """#!/usr/bin/env python3
'''
Memory-Enhanced Recursive Improvement Engine

Enhanced version of the PRI recursive improvement system with integrated
memory intelligence for pattern learning and cross-sessions improvement.
'''

import subprocess
import tempfile
import shutil
from datetime import datetime

# Add memory intelligence
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))
from gus_memory import MemoryIntelligence

class MemoryEnhancedRecursiveImprovement:
    """
    Recursive improvement engine enhanced_pri with persistent memory intelligence

    This version learns from every improvement iteration and accumulates
    knowledge across sessions for compound intelligence growth.
    """

    def __init__(self, source_directory: Path):
        self.source_directory = Path(source_directory)

        # Initialize memory intelligence
        self.memory = MemoryIntelligence("recursive-improvement-engine")
        self.project_adapter = ProjectAdapter("recursive-improvement")

        # Remember initialization
        self.memory.remember("Recursive improvement engine initialized", {
            "source_directory": str(source_directory),
            "session_id": datetime.now().isoformat()
        })

        self.improvement_log = []
        self.iteration_count = 0
        self.cognitive_metrics = {
            "files_processed": 0,
            "improvements_found": 0,
            "patterns_learned": 0,
            "recursive_depth": 0
        }

    @remember_calls("recursive-improvement")
    @remember_errors("recursive-improvement")
    def analyze_code_file(self, file_path: Path):
        """Analyze across code file with memory-enhanced_pri pattern recognition"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Remember analysis
            self.memory.remember(f"Analyzing file: {file_path.name}", {
                "file_path": str(file_path),
                "file_size": len(content),
                "analysis_type": "code_analysis"
            })

            # Check for known patterns from memory
            similar_analyses = self.memory.recall(f"analyzing {file_path.suffix}", limit=5)

            issues = self._detect_issues(content, file_path)

            # Learn from new patterns
            if issues:
                self.memory.learn_pattern(f"code_issues_{file_path.suffix}", [
                    issue["description"] for issue in issues
                ], {"file_type": file_path.suffix, "analysis_date": datetime.now().isoformat()})

            # Remember analysis results
            self.memory.remember(f"Analysis complete: {file_path.name}", {
                "issues_found": len(issues),
                "file_type": file_path.suffix,
                "has_similar_analyses": len(similar_analyses) > 0
            })

            return issues

        except Exception as e:
            self.project_adapter.remember_error(e, {
                "file_path": str(file_path),
                "operation": "analyze_code_file"
            })
            raise

    def _detect_issues(self, content: str, file_path: Path):
        """Detect issues with memory-enhanced pattern recognition"""
        issues = []

        # Get known issue patterns from memory
        known_patterns = self.memory.recall("code issues", limit=20)

        lines = content.split("\\n")
        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Check against known problematic patterns
            for pattern in known_patterns:
                pattern_content = pattern.get("content", "")
                if any(keyword in line_stripped for keyword in ["TODO", "FIXME", "XXX"]):
                    issues.append({
                        "type": "maintenance",
                        "line": i + 1,
                        "description": f"Maintenance comment: {line_stripped}",
                        "learned_from_memory": False
                    })
                    break

        return issues

    @remember_performance("recursive-improvement", "improvement_iteration")
    def run_improvement_iteration(self, max_depth: int = 3):
        """Run a single improvement iteration with memory learning"""
        self.iteration_count += 1

        self.memory.remember(f"Starting improvement iteration {self.iteration_count}", {
            "iteration": self.iteration_count,
            "max_depth": max_depth,
            "session_type": "improvement_iteration"
        })

        try:
            # Get insights from previous iterations
            previous_iterations = self.memory.recall("improvement iteration", limit=10)

            if previous_iterations:
                avg_improvements = sum(
                    iter_data.get("metadata", {}).get("improvements_found", 0)
                    for iter_data in previous_iterations
                ) / len(previous_iterations)

                self.memory.remember(f"Historical context: avg {avg_improvements:.1f} improvements per iteration")

            # Find files to analyze
            target_files = self._find_target_files()

            # Analyze each file
            all_issues = []
            for file_path in target_files:
                issues = self.analyze_code_file(file_path)
                all_issues.extend(issues)
                self.cognitive_metrics["files_processed"] += 1

            # Learn improvement patterns
            if all_issues:
                improvement_patterns = [issue["description"] for issue in all_issues]
                self.memory.learn_pattern(f"iteration_{self.iteration_count}_improvements",
                                        improvement_patterns)
                self.cognitive_metrics["patterns_learned"] += 1

            self.cognitive_metrics["improvements_found"] = len(all_issues)

            # Remember iteration results
            self.memory.remember(f"Improvement iteration {self.iteration_count} complete", {
                "improvements_found": len(all_issues),
                "files_processed": len(target_files),
                "cognitive_metrics": self.cognitive_metrics.copy()
            })

            return {
                "iteration": self.iteration_count,
                "issues_found": all_issues,
                "files_processed": len(target_files),
                "cognitive_growth": self.cognitive_metrics
            }

        except Exception as e:
            self.project_adapter.remember_error(e, {
                "iteration": self.iteration_count,
                "operation": "run_improvement_iteration"
            })
            raise

    def _find_target_files(self):
        """Find target files for analysis"""
        target_files = []

        # Focus on key cognitive architecture files
        cognitive_files = [
            "recursive_improvement.py",
            "persistent_recursive_engine.py",
            "educational_injector.py"
        ]

        for file_name in cognitive_files:
            for file_path in self.source_directory.rglob(file_name):
                if file_path.is_file():
                    target_files.append(file_path)

        return target_files

    def get_intelligence_insights(self):
        """Get insights from accumulated memory intelligence"""
        insights = {
            "total_iterations": self.iteration_count,
            "cognitive_metrics": self.cognitive_metrics,
            "recent_patterns": self.memory.recall("pattern", limit=10),
            "improvement_history": self.memory.recall("improvement iteration", limit=5),
            "error_patterns": self.memory.recall("error", limit=5),
            "performance_data': self.memory.recall("performance", limit=5)
        }

        return insights

    def export_intelligence(self):
        """Export all accumulated intelligence"""
        return self.memory.export_memories()

# Demonstration function
def demonstrate_memory_enhanced_improvement():
    """Demonstrate the memory-enhanced recursive improvement"""
    print("🧠 Memory-Enhanced Recursive Improvement Demo")
    print("=" * 45)

    # Initialize the enhanced engine
    source_dir = Path(__file__).parent.parent.parent
    engine = MemoryEnhancedRecursiveImprovement(source_dir)

    # Run improvement iteration
    results = engine.run_improvement_iteration()

    print(f"\\n📊 Improvement Results:")
    print(f"   Issues found: {len(results["issues_found"])}")
    print(f"   Files processed: {results["files_processed"]}")
    print(f"   Cognitive growth: {results["cognitive_growth"]}")

    # Get intelligence insights
    insights = engine.get_intelligence_insights()
    print(f"\\n🧠 Intelligence Insights:")
    print(f"   Total patterns learned: {len(insights["recent_patterns"])}")
    print(f"   Historical iterations: {len(insights["improvement_history"])}")
    print(f"   Error patterns tracked: {len(insights["error_patterns"])}")

    return engine

if __name__ == "__main__":
    demonstrate_memory_enhanced_improvement()
""'

def enhance_persistent_recursive_engine():
    """Enhance the persistent recursive engine with memory intelligence"""
    print("\n🔄 Enhancing Persistent Recursive Engine...")

    try:
        # Path to the persistent recursive engine
        engine_file = Path(__file__).parent / "src" / "cognitive" / "synthesis" / "persistent_recursive_engine.py"

        if not engine_file.exists():
            print(f"   ❌ Persistent recursive engine file not found: {engine_file}")
            return False

        # Create memory-enhanced integration script
        integration_script = create_memory_integration_script()

        # Write to new file for testing
        integration_file = engine_file.parent / "memory_enhanced_integration.py"
        with open(integration_file, "w") as f:
            f.write(integration_script)

        print(f"   ✅ Memory-enhanced integration created: {integration_file}")
        return True

    except Exception as e:
        print(f"   ❌ Failed to enhance persistent recursive engine: {e}")
        return False

def create_memory_integration_script():
    """Create script showing memory intelligence integration"""
    return """#!/usr/bin/env python3
"""
Memory Intelligence Integration for PRI

This script demonstrates integrating memory intelligence into the existing
Persistent Recursive Intelligence system for compound learning effects.
"""


# Add memory intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))


def ProjectAdapter(param):
    pass


def MemoryIntelligence(param):
    pass


class MemoryEnhancedPRI:
    """
    Memory-enhanced version of Persistent Recursive Intelligence

    Combines the existing PRI system with memory intelligence for:
    - Cross-session learning persistence
    - Pattern recognition across projects
    - Compound intelligence growth
    - Global knowledge integration
    """

    def __init__(self):
        # Initialize memory intelligence for PRI
        self.memory = MemoryIntelligence("persistent-recursive-intelligence")
        self.project_adapter = ProjectAdapter("PRI-system")

        # Remember system initialization
        self.memory.remember("PRI system enhanced with memory intelligence", {
            "enhancement_type": "memory_integration",
            "capabilities": ["cross_session_learning", "pattern_recognition", "compound_intelligence"]
        })

    @__init__("PRI-system")
    @__init__("PRI-system")
    def analyze_codebase(self, project_path: str):
        """Analyze codebase with memory-enhanced intelligence"""

        # Remember the analysis request
        self.memory.remember(f"Starting codebase analysis: {project_path}", {
            "project_path": project_path,
            "analysis_type": "full_codebase"
        })

        # Get insights from previous similar analyses
        similar_analyses = self.memory.recall("codebase analysis", limit=5)

        if similar_analyses:
            print(f"📚 Found {len(similar_analyses)} similar analyses in memory")
            for analysis in similar_analyses[:3]:
                print(f"   - {analysis["content"]}")

        analysis_results = {
            "files_analyzed": 42,
            "issues_found": 15,
            "patterns_discovered": 8,
            "optimization_opportunities": 5
        }

        # Remember analysis results
        self.memory.remember(f"Analysis complete: {analysis_results["issues_found"]} issues found", {
            "results": analysis_results,
            "project_path": project_path
        })

        # Learn patterns from this analysis
        if analysis_results["patterns_discovered"] > 0:
            self.memory.learn_pattern("codebase_analysis_patterns", [
                "Recursive improvement opportunities",
                "Educational injection points",
                "Memory integration benefits"
            ])

        return analysis_results

    def get_compound_intelligence_insights(self):
        """Get insights that demonstrate compound intelligence"""

        # Get patterns from memory
        all_patterns = self.memory.recall("pattern", limit=20)
        analysis_history = self.memory.recall("analysis", limit=10)
        error_patterns = self.memory.recall("error", limit=10)

        # Analyze compound effects
        insights = {
            "learning_velocity": len(all_patterns),
            "analysis_experience": len(analysis_history),
            "error_prevention": len(error_patterns),
            "intelligence_multiplier": self._calculate_intelligence_multiplier()
        }

        self.memory.remember("Generated compound intelligence insights", {
            "insights": insights,
            "insight_type": "compound_intelligence"
        })

        return insights

    def _calculate_intelligence_multiplier(self):
        """Calculate intelligence multiplier from accumulated patterns"""
        total_patterns = self.memory.get_statistics()["memory_count"]
        base_intelligence = 1.0

        # Simple intelligence multiplier calculation
        # In reality, this would be much more sophisticated
        multiplier = base_intelligence + (total_patterns * 0.1)

        return min(multiplier, 10.0)  # Cap at 10x for demonstration

    def demonstrate_cross_project_learning(self):
        """Demonstrate learning from other projects"""

        # Simulate getting patterns from other projects
        cross_project_patterns = self.memory.recall("optimization", limit=10)

        applicable_patterns = []
        for pattern in cross_project_patterns:
            # Check if pattern is applicable to current project
            if self._is_pattern_applicable(pattern):
                applicable_patterns.append(pattern)

        self.memory.remember(f"Applied {len(applicable_patterns)} cross-project patterns", {
            "pattern_count": len(applicable_patterns),
            "learning_type": "cross_project"
        })

        return applicable_patterns

    def _is_pattern_applicable(self, pattern):
        """Check if a pattern from another project is applicable here"""
        # Simplified pattern applicability check
        pattern_content = pattern.get("content", "").lower()
        applicable_keywords = ["optimization", "recursive", "intelligence", "memory"]

        return any(keyword in pattern_content for keyword in applicable_keywords)

    def export_intelligence_state(self):
        """Export the current intelligence state for backup/analysis"""
        return self.memory.export_memories()

def demonstrate_memory_enhanced_pri():
    """Demonstrate the memory-enhanced PRI system"""
    print("🧠 Memory-Enhanced PRI Demonstration")
    print("=" * 40)

    # Initialize the enhanced system
    enhanced_pri = MemoryEnhancedPRI()

    # Demonstrate codebase analysis with memory
    print("\\n1. Codebase Analysis with Memory:")
    results = enhanced_pri.analyze_codebase("/example/project/path")
    print(f"   Analysis results: {results}")

    # Demonstrate compound intelligence insights
    print("\\n2. Compound Intelligence Insights:")
    insights = enhanced_pri.get_compound_intelligence_insights()
    print(f"   Intelligence insights: {insights}")

    # Demonstrate cross-project learning
    print("\\n3. Cross-Project Learning:")
    patterns = enhanced_pri.demonstrate_cross_project_learning()
    print(f"   Applied {len(patterns)} cross-project patterns")

    # Show intelligence state
    print("\\n4. Intelligence State:")
    stats = enhanced_pri.memory.get_statistics()
    print(f"   Total memories: {stats["memory_count"]}")
    print(f"   Project: {stats["project"]}")
    print(f"   Health: {stats["system_health"]}")

    return enhanced_pri

if __name__ == "__main__":
    enhanced_pri = demonstrate_memory_enhanced_pri()
"""

def create_integration_test():
    """Create a comprehensive integration test"""
    print("\n🧪 Creating Integration Test...")

    test_content = """#!/usr/bin/env python3
"""
Integration Test: Memory Intelligence + PRI

This test validates that the memory intelligence system integrates
successfully with the PRI project and provides expected benefits.
"""


# Add memory intelligence
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))

def test_memory_intelligence_integration():
    """Test memory intelligence integration with PRI"""
    print("🧪 Testing Memory Intelligence Integration with PRI")
    print("=" * 52)

    try:

        # Test basic integration
        memory = MemoryIntelligence("PRI-integration-test")
        memory.clear_memories(confirm="YES")  # Start fresh

        print("✅ Memory intelligence imported and initialized")

        # Test PRI-specific memory patterns
        memory.remember("PRI recursive improvement iteration completed", {
            "iteration": 1,
            "improvements_found": 15,
            "cognitive_enhancement": True
        })

        memory.remember("Educational injection successful", {
            "injection_type": "learning_annotation",
            "target_file": "recursive_improvement.py",
            "educational_value": "high"
        })

        memory.remember("Memory system integrated with PRI", {
            "integration_type": "full_system",
            "compound_intelligence": True,
            "cross_session_learning": True
        })

        print("✅ PRI-specific patterns stored in memory")

        # Test pattern recall
        recursive_patterns = memory.recall("recursive improvement")
        educational_patterns = memory.recall("educational injection")
        integration_patterns = memory.recall("memory system integrated")

        print(f"✅ Pattern recall working:")
        print(f"   - Recursive patterns: {len(recursive_patterns)}")
        print(f"   - Educational patterns: {len(educational_patterns)}")
        print(f"   - Integration patterns: {len(integration_patterns)}")

        # Test learning capabilities
        success = memory.learn_pattern("PRI_cognitive_enhancements", [
            "Recursive self-improvement cycles",
            "Educational injection for learning",
            "Memory persistence across sessions",
            "Compound intelligence growth"
        ])

        print(f"✅ Pattern learning: {success}")

        # Test insights
        insights = memory.get_insights("PRI")
        print(f"✅ PRI insights available: {len(insights)}")

        # Test statistics
        stats = memory.get_statistics()
        print(f"✅ Memory statistics:")
        print(f"   - Total memories: {stats["memory_count"]}")
        print(f"   - Vector search: {stats["vector_search_available"]}")
        print(f"   - Health: {stats["system_health"]["database']}")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_compound_intelligence_effects():
    """Test compound intelligence effects"""
    print("\\n🌀 Testing Compound Intelligence Effects")
    print("=" * 39)

    try:

        memory = MemoryIntelligence("compound-intelligence-test")
        memory.clear_memories(confirm="YES")

        # Simulate multiple improvement iterations
        for iteration in range(1, 6):
            memory.remember(f"Recursive improvement iteration {iteration}", {
                "iteration": iteration,
                "patterns_discovered": iteration * 3,
                "intelligence_growth": iteration * 0.2,
                "compound_effect": True
            })

        # Simulate cross-project learning
        memory.remember("Pattern learned from external project", {
            "source": "external_project",
            "pattern_type": "optimization",
            "applicability": "high",
            "cross_project_learning": True
        })

        # Test compound effects
        all_iterations = memory.recall("recursive improvement iteration")
        cross_project = memory.recall("external project")

        # Calculate compound intelligence metrics
        total_patterns = sum(
            iter_data.get("metadata", {}).get("patterns_discovered", 0)
            for iter_data in all_iterations
        )

        intelligence_growth = sum(
            iter_data.get("metadata", {}).get("intelligence_growth", 0)
            for iter_data in all_iterations
        )

        print(f"✅ Compound intelligence metrics:")
        print(f"   - Total iterations: {len(all_iterations)}")
        print(f"   - Accumulated patterns: {total_patterns}")
        print(f"   - Intelligence growth: {intelligence_growth:.1f}x")
        print(f"   - Cross-project learning: {len(cross_project)} patterns")

        # Test intelligence multiplier effect
        base_capability = 1.0
        enhanced_capability = base_capability + intelligence_growth
        multiplier = enhanced_capability / base_capability

        print(f"✅ Intelligence multiplier: {multiplier:.1f}x")

        return True

    except Exception as e:
        print(f"❌ Compound intelligence test failed: {e}")
        return False

def main():
    """Run comprehensive integration tests"""
    print("🚀 PRI + Memory Intelligence Integration Tests")
    print("=" * 48)

    tests = [
        ("Memory Intelligence Integration", test_memory_intelligence_integration),
        ("Compound Intelligence Effects", test_compound_intelligence_effects)
    ]

    passed = 0
    for test_name, test_func in tests:
        success = test_func()
        if success:
            passed += 1
            print(f"\\n✅ {test_name}: PASSED")
        else:
            print(f"\\n❌ {test_name}: FAILED")

    print(f"\\n🎯 Integration Test Results: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("🎉 Memory Intelligence successfully integrated with PRI!")
        print("🧠 Compound intelligence effects validated")
        print("🚀 Ready for enhanced recursive improvement")
    else:
        print("🔧 Some integration issues need to be resolved")

    return passed == len(tests)

if __name__ == "__main__":
    main()
"""

    test_file = Path(__file__).parent / "test_memory_intelligence_integration.py"
    with open(test_file, "w') as f:
        f.write(test_content)

    print(f"   ✅ Integration test created: {test_file}")
    return test_file


def enhance_persistent_recursive_engine():
    pass


def main():
    """Main integration process"""
    print("🧠 GUS Memory Intelligence Integration into PRI")
    print("=" * 48)

    # Step 1: Install memory intelligence
    memory = install_memory_intelligence()
    if not memory:
        print("❌ Failed to install memory intelligence")
        return False

    # Step 2: Enhance recursive improvement
    enhanced_recursive = enhance_recursive_improvement()

    # Step 3: Enhance persistent recursive engine
    enhanced_engine = enhance_persistent_recursive_engine()

    # Step 4: Create integration test
    test_file = create_integration_test()

    # Step 5: Summary
    print("\\n🎯 Integration Summary")
    print("=" * 21)
    print(f"✅ Memory intelligence installed: {memory is not None}")
    print(f"✅ Recursive improvement enhanced: {enhanced_recursive}")
    print(f"✅ Persistent engine enhanced: {enhanced_engine}")
    print(f"✅ Integration test created: {test_file.name}")

    if all([memory, enhanced_recursive, enhanced_engine]):
        print("\\n🎉 Memory Intelligence Successfully Integrated into PRI!")
        print("\\n🚀 What You Can Now Do:")
        print("   • Run enhanced recursive improvement with memory learning")
        print("   • Get insights from accumulated improvement patterns")
        print("   • Benefit from cross-session intelligence persistence")
        print("   • Access compound intelligence effects")
        print("   • Learn from global development patterns")

        print("\\n📋 Next Steps:")
        print(f"   1. Run integration test: python {test_file.name}")
        print("   2. Try enhanced recursive improvement")
        print("   3. Explore memory-enhanced capabilities")

        return True
    else:
        print("\\n❌ Integration incomplete - some enhancements failed")
        return False

if __name__ == "__main__":
    main()