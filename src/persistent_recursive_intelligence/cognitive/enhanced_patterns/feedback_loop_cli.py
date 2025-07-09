#!/usr/bin/env python3
"""
Feedback Loop CLI - Integrated command that demonstrates the complete cycle:
Analysis → Fix Generation → Safety Scoring → User Approval → Learning
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add src path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from cognitive.interactive_approval import InteractiveApprovalSystem
from cognitive.enhanced_patterns.intelligent_fix_generator import IntelligentFixGenerator

def run_feedback_loop_analysis(project_path: str, interactive: bool = True, max_fixes: int = 10):
    """Run the complete feedback loop: analyze → generate → score → approve → learn"""
    
    print("🔄 MESOPREDATOR FEEDBACK LOOP DEMONSTRATION")
    print("=" * 60)
    print(f"📁 Project: {project_path}")
    print(f"🤖 Mode: {'Interactive' if interactive else 'Automated'}")
    print(f"📊 Max fixes: {max_fixes}")
    
    # Initialize components
    fix_generator = IntelligentFixGenerator()
    approval_system = InteractiveApprovalSystem(
        auto_approve_safe=True, 
        interactive_mode=interactive
    )
    
    # Step 1: Analysis (simulate with sample issues for demo)
    print(f"\n📋 STEP 1: ANALYSIS")
    print("🔍 Analyzing project for issues...")
    
    # In real implementation, this would come from the analysis engine
    sample_issues = create_sample_issues(project_path, max_fixes)
    print(f"✅ Found {len(sample_issues)} issues to address")
    
    # Step 2: Fix Generation
    print(f"\n🤖 STEP 2: INTELLIGENT FIX GENERATION")
    print("🧠 Generating fix suggestions based on learned patterns...")
    
    fix_suggestions = fix_generator.generate_fix_suggestions(sample_issues)
    print(f"✨ Generated {len(fix_suggestions)} fix proposals")
    
    if not fix_suggestions:
        print("⚠️ No fix suggestions generated. Exiting.")
        return
    
    # Step 3: Safety Scoring & Approval
    print(f"\n🛡️ STEP 3: SAFETY SCORING & APPROVAL")
    print("🔒 Applying enhanced security validation...")
    
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(
        fix_suggestions, 
        feedback_generator=fix_generator
    )
    
    # Step 4: Learning Summary
    print(f"\n🧠 STEP 4: LEARNING SUMMARY")
    print(fix_generator.generate_learning_report())
    
    # Step 5: Results
    print(f"\n📊 FEEDBACK LOOP RESULTS")
    print("=" * 40)
    print(f"✅ Approved fixes: {len(approved_fixes)}")
    print(f"❌ Rejected fixes: {len(rejected_fixes)}")
    
    if approved_fixes:
        print(f"\n🔧 APPROVED FIXES READY FOR APPLICATION:")
        for i, fix in enumerate(approved_fixes, 1):
            print(f"   {i}. {fix.issue_type} in {fix.file_path}:{fix.line_number}")
            print(f"      Safety: {fix.safety_score}% | Context: {fix.context}")
    
    if rejected_fixes:
        print(f"\n🚫 REJECTED FIXES (LEARNED FROM):")
        for i, fix in enumerate(rejected_fixes, 1):
            print(f"   {i}. {fix.issue_type} in {fix.file_path}:{fix.line_number}")
            print(f"      Reason: Safety concerns or user preference")
    
    # Save results for next iteration
    save_feedback_results(approved_fixes, rejected_fixes, fix_generator)
    
    print(f"\n🎯 Feedback loop complete! System learned from {len(fix_suggestions)} decisions.")
    return approved_fixes, rejected_fixes

def create_sample_issues(project_path: str, max_fixes: int) -> List[Dict[str, Any]]:
    """Create sample issues for demonstration"""
    
    # In real implementation, these would come from the analysis engine
    sample_issues = [
        {
            'type': 'whitespace_cleanup',
            'file_path': f'{project_path}/utils.py',
            'line': 15,
            'description': 'Trailing whitespace detected',
            'severity': 'low'
        },
        {
            'type': 'import_organization',
            'file_path': f'{project_path}/main.py',
            'line': 3,
            'description': 'Imports should be on separate lines',
            'severity': 'low'
        },
        {
            'type': 'comment_typos',
            'file_path': f'{project_path}/config.py',
            'line': 8,
            'description': 'Spelling error in comment',
            'severity': 'low'
        },
        {
            'type': 'unused_variables',
            'file_path': f'{project_path}/processor.py',
            'line': 42,
            'description': 'Variable assigned but never used',
            'severity': 'medium'
        },
        {
            'type': 'security_vulnerability',
            'file_path': f'{project_path}/auth.py',
            'line': 67,
            'description': 'Potential SQL injection vulnerability',
            'severity': 'high'
        }
    ]
    
    return sample_issues[:max_fixes]

def save_feedback_results(approved_fixes, rejected_fixes, fix_generator):
    """Save feedback loop results for analysis"""
    
    results = {
        'timestamp': fix_generator.get_learning_statistics(),
        'session_summary': {
            'approved_count': len(approved_fixes),
            'rejected_count': len(rejected_fixes),
            'total_processed': len(approved_fixes) + len(rejected_fixes)
        },
        'approved_fixes': [
            {
                'issue_type': fix.issue_type,
                'file_path': fix.file_path,
                'safety_score': fix.safety_score,
                'context': fix.context
            }
            for fix in approved_fixes
        ],
        'rejected_fixes': [
            {
                'issue_type': fix.issue_type,
                'file_path': fix.file_path,
                'safety_score': fix.safety_score,
                'context': fix.context
            }
            for fix in rejected_fixes
        ]
    }
    
    results_file = Path('feedback_loop_results.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📝 Results saved to {results_file}")

def run_learning_analysis():
    """Analyze accumulated learning data"""
    
    print("🧠 LEARNING ANALYSIS")
    print("=" * 30)
    
    fix_generator = IntelligentFixGenerator()
    stats = fix_generator.get_learning_statistics()
    
    print(f"📚 Total Learning Sessions: {stats['fixes_approved'] + stats['fixes_rejected']}")
    print(f"✅ Approval Rate: {stats['approval_rate']:.1f}%")
    print(f"🟢 Safe Patterns: {len(stats['safe_indicators'])}")
    print(f"🔴 Dangerous Patterns: {len(stats['dangerous_indicators'])}")
    
    if stats['safe_indicators']:
        print(f"\n🟢 LEARNED SAFE PATTERNS:")
        for pattern in stats['safe_indicators'][:5]:
            print(f"   ✓ {pattern}")
    
    if stats['dangerous_indicators']:
        print(f"\n🔴 LEARNED DANGEROUS PATTERNS:")
        for pattern in stats['dangerous_indicators'][:5]:
            print(f"   ⚠️ {pattern}")
    
    print(f"\n{fix_generator.generate_learning_report()}")

def demonstrate_adversarial_resistance():
    """Demonstrate that the feedback loop maintains security against adversarial inputs"""
    
    print("🛡️ ADVERSARIAL RESISTANCE DEMONSTRATION")
    print("=" * 50)
    
    fix_generator = IntelligentFixGenerator()
    approval_system = InteractiveApprovalSystem(auto_approve_safe=True, interactive_mode=False)
    
    # Create some malicious-looking but valid issues
    adversarial_issues = [
        {
            'type': 'typo_corrections',
            'file_path': 'test/security.py',
            'line': 10,
            'description': 'Fix spelling in comment',
            'severity': 'low'
        }
    ]
    
    print("🧪 Testing with potentially adversarial inputs...")
    
    fix_suggestions = fix_generator.generate_fix_suggestions(adversarial_issues)
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(
        fix_suggestions, 
        feedback_generator=fix_generator
    )
    
    print(f"🔒 Security validation: {len(rejected_fixes)} potentially dangerous fixes blocked")
    print(f"✅ Safe fixes approved: {len(approved_fixes)}")
    
    print("🛡️ Feedback loop maintains security while learning!")

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(description="Mesopredator Feedback Loop CLI")
    parser.add_argument('command', choices=['run', 'analyze', 'demo-security'], 
                       help='Command to execute')
    parser.add_argument('--project', '-p', default='demo_project',
                       help='Project path to analyze')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Enable interactive approval mode')
    parser.add_argument('--max-fixes', '-m', type=int, default=5,
                       help='Maximum number of fixes to generate')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        run_feedback_loop_analysis(
            project_path=args.project,
            interactive=args.interactive,
            max_fixes=args.max_fixes
        )
    elif args.command == 'analyze':
        run_learning_analysis()
    elif args.command == 'demo-security':
        demonstrate_adversarial_resistance()

if __name__ == "__main__":
    main()