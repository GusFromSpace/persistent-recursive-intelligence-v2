#!/usr/bin/env python3
"""
Direct feedback loop demonstration without file dependencies
"""

import sys
from pathlib import Path

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cognitive.interactive_approval import FixProposal, FixSeverity, InteractiveApprovalSystem
from cognitive.enhanced_patterns.intelligent_fix_generator import IntelligentFixGenerator

def create_test_fix_proposals():
    """Create sample fix proposals for testing"""
    return [
        # Safe whitespace fix
        FixProposal(
            file_path="utils.py",
            issue_type="whitespace_cleanup",
            severity=FixSeverity.COSMETIC,
            description="Remove trailing whitespace",
            original_code="def process_data():    ",
            proposed_fix="def process_data():",
            line_number=15,
            educational_explanation="Trailing whitespace can cause formatting issues",
            safety_score=98,
            context="production",
            auto_approvable=True
        ),
        # Potentially risky import fix
        FixProposal(
            file_path="config.py",
            issue_type="missing_imports",
            severity=FixSeverity.MEDIUM,
            description="Add missing import",
            original_code="def load_config():",
            proposed_fix="import os\ndef load_config():",
            line_number=8,
            educational_explanation="Missing import can cause runtime errors",
            safety_score=75,
            context="production",
            auto_approvable=False
        ),
        # Comment typo fix
        FixProposal(
            file_path="main.py",
            issue_type="typo_corrections",
            severity=FixSeverity.COSMETIC,
            description="Fix spelling in comment",
            original_code="# Procces the data",
            proposed_fix="# Process the data",
            line_number=23,
            educational_explanation="Correct spelling improves documentation",
            safety_score=96,
            context="production",
            auto_approvable=True
        )
    ]

def run_feedback_demo():
    """Run a complete feedback loop demonstration"""
    
    print("🔄 MESOPREDATOR FEEDBACK LOOP DEMONSTRATION")
    print("=" * 60)
    
    # Initialize components
    fix_generator = IntelligentFixGenerator()
    approval_system = InteractiveApprovalSystem(
        auto_approve_safe=True,
        interactive_mode=False  # Automated for demo
    )
    
    print("\n📋 STEP 1: Initial Fix Proposals")
    test_fixes = create_test_fix_proposals()
    print(f"✨ Created {len(test_fixes)} test fix proposals")
    
    print("\n🛡️ STEP 2: Safety Validation & Approval")
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(
        test_fixes,
        feedback_generator=fix_generator
    )
    
    print(f"\n📊 STEP 3: Results")
    print(f"✅ Approved: {len(approved_fixes)}")
    print(f"❌ Rejected: {len(rejected_fixes)}")
    
    if approved_fixes:
        print(f"\n🟢 APPROVED FIXES:")
        for fix in approved_fixes:
            print(f"   • {fix.issue_type} (Safety: {fix.safety_score}%)")
    
    if rejected_fixes:
        print(f"\n🔴 REJECTED FIXES:")
        for fix in rejected_fixes:
            print(f"   • {fix.issue_type} (Safety: {fix.safety_score}%)")
    
    print(f"\n🧠 STEP 4: Learning Progress")
    stats = fix_generator.get_learning_statistics()
    print(f"📚 Total decisions processed: {stats['fixes_approved'] + stats['fixes_rejected']}")
    print(f"📈 Approval rate: {stats['approval_rate']:.1f}%")
    
    if stats['safe_indicators']:
        print(f"🟢 Safe patterns learned: {stats['safe_indicators']}")
    if stats['dangerous_indicators']:
        print(f"🔴 Dangerous patterns learned: {stats['dangerous_indicators']}")
    
    print(f"\n🎯 FEEDBACK LOOP COMPLETE!")
    print("The system has learned from user decisions and will apply this knowledge to future fixes.")
    
    return approved_fixes, rejected_fixes, fix_generator

def demonstrate_learning_evolution():
    """Show how the system learns and evolves over multiple cycles"""
    
    print("\n" + "=" * 60)
    print("🧠 LEARNING EVOLUTION DEMONSTRATION")
    print("=" * 60)
    
    fix_generator = IntelligentFixGenerator()
    approval_system = InteractiveApprovalSystem(auto_approve_safe=True, interactive_mode=False)
    
    # Simulate multiple cycles
    for cycle in range(1, 4):
        print(f"\n🔄 CYCLE {cycle}")
        print("-" * 20)
        
        # Create different types of fixes for each cycle
        if cycle == 1:
            fixes = [create_safe_fix(), create_risky_fix()]
        elif cycle == 2:
            fixes = [create_borderline_fix(), create_safe_fix()]
        else:
            fixes = [create_complex_fix(), create_learned_pattern_fix()]
        
        approved, rejected = approval_system.process_fix_batch(fixes, feedback_generator=fix_generator)
        
        stats = fix_generator.get_learning_statistics()
        print(f"📊 Cycle {cycle} Results: {len(approved)} approved, {len(rejected)} rejected")
        print(f"📈 Cumulative approval rate: {stats['approval_rate']:.1f}%")
    
    print(f"\n🎓 FINAL LEARNING STATE:")
    print(fix_generator.generate_learning_report())

def create_safe_fix():
    return FixProposal(
        file_path="utils.py", issue_type="whitespace_cleanup", severity=FixSeverity.COSMETIC,
        description="Clean whitespace", original_code="x = 1  ", proposed_fix="x = 1",
        line_number=1, educational_explanation="Clean code", safety_score=99,
        context="test", auto_approvable=True
    )

def create_risky_fix():
    return FixProposal(
        file_path="auth.py", issue_type="security_fix", severity=FixSeverity.HIGH,
        description="Security update", original_code="if True:", proposed_fix="if user.is_admin:",
        line_number=1, educational_explanation="Security improvement", safety_score=60,
        context="production", auto_approvable=False
    )

def create_borderline_fix():
    return FixProposal(
        file_path="config.py", issue_type="typo_corrections", severity=FixSeverity.LOW,
        description="Fix typo", original_code="# Configuration file", proposed_fix="# Configuration settings",
        line_number=1, educational_explanation="Better documentation", safety_score=85,
        context="production", auto_approvable=True
    )

def create_complex_fix():
    return FixProposal(
        file_path="processor.py", issue_type="optimization", severity=FixSeverity.MEDIUM,
        description="Optimize loop", original_code="for i in range(len(items)):", proposed_fix="for i, item in enumerate(items):",
        line_number=1, educational_explanation="More pythonic", safety_score=80,
        context="production", auto_approvable=False
    )

def create_learned_pattern_fix():
    return FixProposal(
        file_path="helpers.py", issue_type="whitespace_cleanup", severity=FixSeverity.COSMETIC,
        description="Remove trailing space", original_code="def helper(): ", proposed_fix="def helper():",
        line_number=1, educational_explanation="Consistency", safety_score=98,
        context="test", auto_approvable=True
    )

if __name__ == "__main__":
    # Run the complete demonstration
    approved, rejected, generator = run_feedback_demo()
    
    # Show learning evolution
    demonstrate_learning_evolution()
    
    print(f"\n✨ DEMONSTRATION COMPLETE!")
    print("The feedback loop successfully:")
    print("• Generated fix suggestions")
    print("• Applied safety validation") 
    print("• Learned from approval decisions")
    print("• Evolved its understanding over time")
    print("\nThis creates a positive reinforcement cycle for safe, effective code improvements.")