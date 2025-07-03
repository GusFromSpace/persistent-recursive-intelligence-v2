#!/usr/bin/env python3
"""
Demo Interactive Approval System
Shows how PRI can ask for approval before applying fixes
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cognitive.interactive_approval import (
    InteractiveApprovalSystem, FixProposal, FixSeverity
)

def create_realistic_fix_proposals() -> list:
    """Create realistic fix proposals based on actual PRI findings"""

    return [
        FixProposal(
            file_path="test_hello_world/services/output_service.py",
            issue_type="bare_except_blocks",
            severity=FixSeverity.MEDIUM,
            description="Bare except clause catches all exceptions",
            original_code="""try:
    terminal_width = shutil.get_terminal_size().columns
except Exception as e:
    terminal_width = 80  # Default fallback""",
            proposed_fix="""try:
    terminal_width = shutil.get_terminal_size().columns
except (OSError, AttributeError):
    terminal_width = 80  # Default fallback for headless environments""",
            line_number=94,
            educational_explanation="Bare except clauses are dangerous because they catch system exceptions like KeyboardInterrupt and SystemExit. This makes it impossible to interrupt your program with Ctrl+C and can hide critical errors. Specify the exact exception types you expect.",
            safety_score=75,
            context="test",
            auto_approvable=False
        ),

        FixProposal(
            file_path="src/cognitive/educational/educational_injector.py",
            issue_type="syntax_errors",
            severity=FixSeverity.CRITICAL,
            description="Unterminated string literal prevents compilation",
            original_code='"eval_usage\': "MEMORY AID: "eval() = evil() - never trust user input"',
            proposed_fix='"eval_usage": "MEMORY AID: eval() = evil() - never trust user input"',
            line_number=330,
            educational_explanation="Syntax errors prevent the code from running at all. This specific error is a missing closing quote in a dictionary key. These should always be fixed immediately.",
            safety_score=95,
            context="production",
            auto_approvable=True
        ),

        FixProposal(
            file_path="src/safety_validator.py",
            issue_type="missing_variable_assignment",
            severity=FixSeverity.HIGH,
            description="Class attribute list missing variable assignment",
            original_code="""    # Known problematic patterns
        r'^(\\w+)_result = (.+)$',  # Generic _result assignments""",
            proposed_fix="""    # Known problematic patterns
    PROBLEMATIC_PATTERNS = [
        r'^(\\w+)_result = (.+)$',  # Generic _result assignments""",
            line_number=28,
            educational_explanation="This creates a syntax error because a list is defined without being assigned to a variable. Python needs to know what variable to store the list in.",
            safety_score=88,
            context="production",
            auto_approvable=True
        ),

        FixProposal(
            file_path="test_hello_world/utils/logger_utils.py",
            issue_type="bare_except_blocks",
            severity=FixSeverity.LOW,
            description="Bare except with silent failure in logging utility",
            original_code="""try:
    with open(summary_file, 'w') as f:
        f.write(summary_content)
except Exception as e:
    pass  # Silent failure""",
            proposed_fix="""try:
    with open(summary_file, 'w') as f:
        f.write(summary_content)
except (IOError, OSError) as e:
    logger.info(f"Warning: Could not write log summary to {summary_file}: {e}")""",
            line_number=219,
            educational_explanation="Silent failures in logging code can hide important problems. At minimum, we should log when logging itself fails. This fix specifies the expected exception types and provides feedback.",
            safety_score=60,
            context="test",
            auto_approvable=False
        ),

        FixProposal(
            file_path="demo_persistent_intelligence.py",
            issue_type="string_formatting_inconsistency",
            severity=FixSeverity.COSMETIC,
            description="Inconsistent quote usage in list literals",
            original_code='["ls", user_input]',
            proposed_fix="['ls', user_input]",
            line_number=31,
            educational_explanation="While not a functional issue, consistent quote usage improves code readability and follows Python style guidelines.",
            safety_score=95,
            context="demo",
            auto_approvable=True
        )
    ]

def main():
    """Demo the interactive approval system"""

    logger.info("🌀 PRI Interactive Approval System Demo")
    logger.info("=" * 50)
    logger.info()
    logger.info("This demo shows how PRI can present fixes for your approval")
    logger.info("instead of automatically applying all changes.")
    logger.info()

    # Create approval system
    approval_system = InteractiveApprovalSystem(
        auto_approve_safe=True,
        interactive_mode=True
    )

    # Create realistic fix proposals
    fix_proposals = create_realistic_fix_proposals()

    logger.info(f"🔍 Analysis found {len(fix_proposals)} potential fixes")
    logger.info()
    logger.info("Note: This is a demo with simulated fixes. In real usage,")
    logger.info("these would come from PRI's actual code analysis.")
    logger.info()

    input("Press Enter to start the approval process...")

    # Process fixes with interactive approval
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(fix_proposals)

    # Show final summary
    summary = approval_system.generate_session_summary(approved_fixes, rejected_fixes)

    logger.info(f"\n💡 Key Features Demonstrated:")
    logger.info(f"   • Auto-approval of safe fixes (syntax errors, etc.)")
    logger.info(f"   • Manual review for potentially risky changes")
    logger.info(f"   • Educational explanations for each fix")
    logger.info(f"   • Context-aware safety scoring")
    logger.info(f"   • Batch approval options (approve all safe, reject all)")
    logger.info(f"   • Clear diff display showing exact changes")

    if approved_fixes:
        logger.info(f"\n🚀 In real usage, {len(approved_fixes)} fixes would now be applied to your code!")

    return summary

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n\n👋 Demo interrupted. Thanks for trying the interactive approval system!")
    except Exception as e:
        logger.info(f"\n❌ Demo error: {e}")
        logger.info("This is just a demo - no actual files were modified.")