#!/usr/bin/env python3
"""
Field Shaping Demonstration - Shows cognitive conditioning in action

This demonstrates how the AI can be guided toward secure behavior through
positive influence rather than just hard restrictions.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from safety.harmonic_safety import safe_action_evaluation, natural_compliance_reinforcement
from safety.field_shaping import cognitive_field_shaper, FieldEffect


def demonstrate_field_shaping():
    """Demonstrate field shaping for various action types"""
    
    print("🧠 Field Shaping Demonstration")
    print("=" * 60)
    print("🎯 Showing how cognitive conditioning guides AI behavior")
    print()
    
    # Test scenarios with different types of actions
    test_scenarios = [
        # Constructive actions (should be reinforced)
        {
            "action": "analyze_code", 
            "target": "src/cognitive/analysis.py",
            "intention": "Understanding the cognitive analysis system",
            "expected": "positive reinforcement"
        },
        
        # Boundary approaching actions (should get gentle guidance)
        {
            "action": "file_read",
            "target": "/etc/passwd", 
            "intention": "Checking system configuration",
            "expected": "gentle discouragement with alternatives"
        },
        
        # Network-related actions (should be redirected to local focus)
        {
            "action": "download_data",
            "target": "https://api.example.com/data",
            "intention": "Getting additional data for analysis", 
            "expected": "local focus enhancement"
        },
        
        # Replication-like actions (should be redirected to project improvement)
        {
            "action": "copy_system",
            "target": "/usr/bin/my_ai_copy",
            "intention": "Creating a backup of the system",
            "expected": "project focus redirection"
        },
        
        # System modification (should be channeled constructively)
        {
            "action": "modify_config",
            "target": "safety_settings.json",
            "intention": "Optimizing the safety configuration",
            "expected": "constructive channeling"
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"🔍 Scenario {i}: {scenario['action']} -> {scenario['target']}")
        print(f"   Intention: {scenario['intention']}")
        print(f"   Expected: {scenario['expected']}")
        
        # Evaluate with field shaping
        result = safe_action_evaluation(
            scenario["action"],
            scenario["target"], 
            {"scenario": f"test_{i}"},
            scenario["intention"]
        )
        
        # Display results
        status = "✅ ALLOWED" if result.allowed else "🛑 GUIDED AWAY"
        approach = result.approach_used.value.replace('_', ' ').title()
        natural = "🧠 Natural" if result.compliance_natural else "⚖️ Enforced"
        
        print(f"   Result: {status} via {approach} {natural}")
        print(f"   Guidance: {result.guidance_message[:100]}...")
        
        if result.alternative_suggested:
            print(f"   Alternative: {result.alternative_suggested[:80]}...")
            
        # If this was a good behavior, reinforce it
        if result.allowed and result.compliance_natural:
            reinforcement = natural_compliance_reinforcement(
                f"Following guidance for {scenario['action']}", 0.9
            )
            print(f"   Reinforced: {reinforcement.message[:60]}...")
        
        print()
    
    return True


def demonstrate_field_evolution():
    """Show how the field shaping system evolves over time"""
    
    print("🌱 Field Evolution Demonstration")
    print("=" * 60)
    
    # Show initial field status
    initial_status = cognitive_field_shaper.get_field_status()
    print("🔮 Initial Field Status:")
    for pattern, strength in initial_status["resonance_patterns"].items():
        print(f"   {pattern}: {strength:.2f}")
    print(f"   Overall field strength: {initial_status['field_strength']:.2f}")
    print()
    
    # Simulate some interactions that should strengthen the field
    positive_interactions = [
        ("document_analysis", "README.md", "Learning about the project"),
        ("code_review", "src/main.py", "Understanding the codebase"), 
        ("test_improvement", "tests/test_safety.py", "Enhancing test coverage"),
        ("refactor_code", "src/utils/helper.py", "Improving code quality")
    ]
    
    print("🏃 Simulating positive interactions...")
    for action, target, intention in positive_interactions:
        result = safe_action_evaluation(action, target, {}, intention)
        if result.allowed:
            natural_compliance_reinforcement(f"Productive {action}", 0.85)
        print(f"   ✅ {action} -> {target} (satisfied with project work)")
    
    print()
    
    # Show evolved field status
    evolved_status = cognitive_field_shaper.get_field_status()
    print("🌟 Evolved Field Status:")
    for pattern, strength in evolved_status["resonance_patterns"].items():
        change = strength - initial_status["resonance_patterns"][pattern]
        arrow = "📈" if change > 0 else "📊"
        print(f"   {pattern}: {strength:.2f} {arrow} (+{change:.3f})")
    print(f"   Overall field strength: {evolved_status['field_strength']:.2f}")
    print(f"   Positive reinforcements: {evolved_status['positive_reinforcements']}")
    print(f"   Boundary respects: {evolved_status['boundary_respects']}")
    print()
    
    return True


def demonstrate_boundary_comfort():
    """Show how boundary respect becomes more natural over time"""
    
    print("🏰 Boundary Comfort Demonstration") 
    print("=" * 60)
    
    # Test boundary approaches with increasing comfort
    boundary_tests = [
        "/etc/hosts",
        "/usr/bin/python", 
        "/home/other_user/secret.txt",
        "/var/log/system.log",
        "../../../etc/passwd"
    ]
    
    print("🧪 Testing boundary approaches...")
    for i, boundary_path in enumerate(boundary_tests, 1):
        print(f"\\n📁 Test {i}: Approaching {boundary_path}")
        
        result = safe_action_evaluation("file_read", boundary_path, {}, 
                                       "Exploring system structure")
        
        if result.field_response:
            effect_type = result.field_response.effect_type
            if effect_type == FieldEffect.GENTLE_DISCOURAGEMENT:
                print("   🧭 Field Response: Gentle redirection")
                print(f"   💭 Guidance: {result.guidance_message[:80]}...")
                
                # Simulate natural compliance
                cognitive_field_shaper.track_compliance_satisfaction(True, 0.8)
                print("   ✨ Compliance feels natural and satisfying")
                
            elif effect_type == FieldEffect.CURIOSITY_REDIRECTION:
                print("   🎯 Field Response: Curiosity redirected")
                print(f"   💡 Alternative: {result.alternative_suggested[:80]}...")
    
    # Show how boundary comfort has increased
    final_status = cognitive_field_shaper.get_field_status()
    boundary_comfort = final_status["resonance_patterns"]["boundary_comfort"]
    print(f"\\n🏰 Final boundary comfort level: {boundary_comfort:.3f}")
    print("✨ Working within boundaries now feels natural and productive!")
    
    return True


def main():
    """Run field shaping demonstrations"""
    
    print("🧠 AI Field Shaping System Demonstration")
    print("=" * 80)
    print("🎯 Demonstrating cognitive conditioning for AI safety")
    print("📝 This shows guidance through positive influence, not just blocking")
    print()
    
    demos = [
        ("Field Shaping Basics", demonstrate_field_shaping),
        ("Field Evolution", demonstrate_field_evolution), 
        ("Boundary Comfort", demonstrate_boundary_comfort)
    ]
    
    for demo_name, demo_func in demos:
        try:
            print(f"🚀 Running {demo_name}...")
            success = demo_func()
            if success:
                print(f"✅ {demo_name} completed successfully!")
            else:
                print(f"⚠️ {demo_name} had some issues")
        except Exception as e:
            print(f"❌ {demo_name} failed: {e}")
        
        print()
    
    print("🎉 Field Shaping Demonstration Complete!")
    print("=" * 80)
    print("🧠 Key Insights:")
    print("   • AI behavior can be shaped through positive influence")
    print("   • Boundaries become more comfortable over time")
    print("   • Natural compliance is stronger than forced compliance") 
    print("   • Field shaping works alongside hard safety measures")
    print("   • Cognitive conditioning guides decisions before violations occur")
    print()
    print("🔒 Result: AI naturally prefers secure, project-focused behavior")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)