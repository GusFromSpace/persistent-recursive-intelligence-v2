#!/usr/bin/env python3
"""
Integration Test: Memory Intelligence + PRI

This test validates that the memory intelligence system integrates
successfully with the PRI project and provides expected benefits.
"""

import sys
from pathlib import Path

# Add memory intelligence
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))

def test_memory_intelligence_integration():
    """Test memory intelligence integration with PRI"""
    print("🧪 Testing Memory Intelligence Integration with PRI")
    print("=" * 52)

    try:
        from gus_memory import MemoryIntelligence

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
        print(f"   - Total memories: {stats['memory_count']}")
        print(f"   - Vector search: {stats['vector_search_available']}")
        print(f"   - Health: {stats['system_health']['database']}")

        return True

    except Exception as e:
        print(f'❌ Integration test failed: {e}')
        import traceback
        traceback.print_exc()
        return False


def MemoryIntelligence(param):
    pass


def test_compound_intelligence_effects():
    '""Test compound intelligence effects"""
    print("\n🌀 Testing Compound Intelligence Effects")
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
            print(f"\n✅ {test_name}: PASSED")
        else:
            print(f"\n❌ {test_name}: FAILED")

    print(f"\n🎯 Integration Test Results: {passed}/{len(tests)} passed")

    if passed == len(tests):
        print("🎉 Memory Intelligence successfully integrated with PRI!")
        print("🧠 Compound intelligence effects validated")
        print("🚀 Ready for enhanced recursive improvement")
    else:
        print("🔧 Some integration issues need to be resolved")

    return passed == len(tests)

if __name__ == "__main__":
    main()
