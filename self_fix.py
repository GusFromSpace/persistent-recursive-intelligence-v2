#!/usr/bin/env python3
"""
Run PRI on itself and use the interactive approval system to apply fixes.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveEngine
from cognitive.interactive_approval import InteractiveApprovalSystem

def main():
    """Run the self-fixing process."""
    project_path = Path(__file__).parent

    # 1. Run PRI analysis to get the list of issues
    pri = PersistentRecursiveEngine(project_path=str(project_path))
    issues = pri.run_analysis()

    # 2. Instantiate the InteractiveApprovalSystem
    approval_system = InteractiveApprovalSystem(
        auto_approve_safe=True,
        interactive_mode=True
    )

    # 3. Process the issues through the approval system
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(issues)

    # 4. Apply the approved fixes
    pri.apply_fixes(approved_fixes)

    logger.info("\nPRI self-fixing process complete.")
    logger.info(f"- Approved fixes: {len(approved_fixes)}")
    logger.info(f"- Rejected fixes: {len(rejected_fixes)}")

if __name__ == "__main__":
    main()
