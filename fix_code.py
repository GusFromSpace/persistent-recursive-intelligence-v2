#!/usr/bin/env python3
"""
Applies fixes to the codebase using the interactive approval system.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from cognitive.interactive_approval import InteractiveApprovalSystem, FixProposal, FixSeverity
from cognitive.synthesis.persistent_recursive_engine import PersistentRecursiveIntelligence

def create_fix_proposal_from_issue(issue: dict) -> FixProposal:
    """Creates a FixProposal object from an issue dictionary."""
    return FixProposal(
        file_path=issue.get("file_path", ""),
        issue_type=issue.get("type", ""),
        severity=FixSeverity(issue.get("severity", "low")),
        description=issue.get("description", ""),
        original_code=issue.get("original_code", ""),
        proposed_fix=issue.get("proposed_fix", ""),
        line_number=issue.get("line", 0),
        educational_explanation=issue.get("educational_explanation", ""),
        safety_score=issue.get("safety_score", 0),
        context=issue.get("context", ""),
        auto_approvable=issue.get("auto_approvable", False),
    )

async def main():
    """Runs the interactive fix approval system."""

    # 1. Analyze the codebase to get a list of issues.
    pri = PersistentRecursiveIntelligence()
    issues = await pri.evolve_with_persistence(project_path=".")

    # 2. Use the InteractiveApprovalSystem to present the issues for approval.
    approval_system = InteractiveApprovalSystem(
        auto_approve_safe=True,
        interactive_mode=True
    )
    fix_proposals = [create_fix_proposal_from_issue(issue) for issue in issues["improvements_applied"]]
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(fix_proposals)

    # 3. Apply the approved fixes to the codebase.
    # This functionality needs to be implemented.

if __name__ == "__main__":
    asyncio.run(main())
