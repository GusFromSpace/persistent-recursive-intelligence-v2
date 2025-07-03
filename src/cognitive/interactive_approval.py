#!/usr/bin/env python3
"""
Interactive Approval System for PRI Fixes
Provides user-friendly interface for reviewing and approving code changes
"""

import sys
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import textwrap
import difflib

class FixSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    COSMETIC = "cosmetic"

class ApprovalDecision(Enum):
    APPROVE = "approve"
    REJECT = "reject"
    SKIP = "skip"
    APPROVE_ALL_SAFE = "approve_all_safe"
    REJECT_ALL = "reject_all"

@dataclass
class FixProposal:
    """Represents a proposed fix for user review"""
    file_path: str
    issue_type: str
    severity: FixSeverity
    description: str
    original_code: str
    proposed_fix: str
    line_number: int
    educational_explanation: str
    safety_score: int  # 0-100, higher = safer
    context: str  # 'production', 'test', 'demo', 'config'
    auto_approvable: bool  # Can this be safely auto-approved?

@dataclass
class ConnectionProposal:
    """Represents a suggested code connection for user review"""
    orphaned_file: str
    target_file: str
    connection_score: float
    connection_type: str
    integration_suggestions: List[str]
    reasoning: List[str]
    safety_score: int  # 0-100, higher = safer to apply
    impact_level: str  # 'low', 'medium', 'high'
    auto_approvable: bool

class InteractiveApprovalSystem:
    """Handles interactive approval of PRI fixes"""

    # Define which fixes are safe for auto-approval
    AUTO_APPROVABLE_FIXES = {
        'unused_imports': 90,  # Very safe
        'syntax_errors': 95,   # Critical and safe
        'missing_imports': 85, # Generally safe
        'whitespace_cleanup': 95, # Cosmetic and safe
        'string_formatting': 80,  # Usually safe
    }

    # Fixes that should always require approval
    REQUIRE_APPROVAL = {
        'bare_except_blocks',     # Logic changes
        'security_vulnerabilities', # Critical but may break functionality
        'algorithm_changes',      # Logic changes
        'api_modifications',      # Breaking changes
        'database_queries',       # Data safety
    }

    def __init__(self, auto_approve_safe: bool = True, interactive_mode: bool = True):
        self.auto_approve_safe = auto_approve_safe
        self.interactive_mode = interactive_mode
        self.session_approvals = []
        self.global_decision = None

    def categorize_fix_safety(self, fix: FixProposal) -> bool:
        """Determine if a fix can be auto-approved based on safety criteria"""

        # Never auto-approve if explicitly marked as requiring approval
        if fix.issue_type in self.REQUIRE_APPROVAL:
            return False

        # Check safety score threshold
        if fix.safety_score < 80:
            return False

        # Context-based safety rules
        if fix.context == 'production' and fix.severity in [FixSeverity.HIGH, FixSeverity.CRITICAL]:
            return False

        # Check if fix type is in auto-approvable list
        if fix.issue_type in self.AUTO_APPROVABLE_FIXES:
            required_score = self.AUTO_APPROVABLE_FIXES[fix.issue_type]
            return fix.safety_score >= required_score

        # Test files can have more relaxed auto-approval
        if fix.context == 'test' and fix.safety_score >= 70:
            return True

        return fix.auto_approvable

    def present_fix_for_approval(self, fix: FixProposal) -> ApprovalDecision:
        """Present a single fix to the user for approval"""

        if not self.interactive_mode:
            return ApprovalDecision.APPROVE if self.categorize_fix_safety(fix) else ApprovalDecision.REJECT

        # Check for global decisions
        if self.global_decision:
            return self.global_decision

        # Auto-approve safe fixes if enabled
        if self.auto_approve_safe and self.categorize_fix_safety(fix):
            logger.info(f"✅ Auto-approved: {fix.issue_type} in {fix.file_path}:{fix.line_number}")
            return ApprovalDecision.APPROVE

        # Present fix for manual review
        return self._interactive_review(fix)

    def _interactive_review(self, fix: FixProposal) -> ApprovalDecision:
        """Present fix details and get user decision"""

        logger.info("\n" + "="*80)
        logger.info(f"🔍 PROPOSED FIX REVIEW")
        logger.info("="*80)

        # Basic information
        logger.info(f"📁 File: {fix.file_path}:{fix.line_number}")
        logger.info(f"🏷️  Issue: {fix.issue_type} ({fix.severity.value})")
        logger.info(f"📊 Safety Score: {fix.safety_score}/100")
        logger.info(f"🎯 Context: {fix.context}")
        logger.info(f"\n📝 Description: {fix.description}")

        # Educational explanation
        if fix.educational_explanation:
            logger.info(f"\n📚 Why this fix is recommended:")
            wrapped_explanation = textwrap.fill(fix.educational_explanation, width=78)
            logger.info(textwrap.indent(wrapped_explanation, "   "))

        # Show code diff
        logger.info(f"\n🔄 PROPOSED CHANGES:")
        self._show_code_diff(fix.original_code, fix.proposed_fix)

        # Get user decision
        return self._get_user_decision(fix)

    def _show_code_diff(self, original: str, proposed: str):
        """Display a clean diff of the proposed changes"""

        original_lines = original.splitlines() if original else []
        proposed_lines = proposed.splitlines() if proposed else []

        diff = list(difflib.unified_diff(
            original_lines, proposed_lines,
            fromfile="Original", tofile="Proposed",
            lineterm=""
        ))

        if diff:
            for line in diff[3:]:  # Skip the header lines
                if line.startswith('+'):
                    logger.info(f"   🟢 {line[1:]}")
                elif line.startswith('-'):
                    logger.info(f"   🔴 {line[1:]}")
                elif line.startswith('@'):
                    logger.info(f"   📍 {line}")
                else:
                    logger.info(f"      {line}")
        else:
            logger.info("   ℹ️  No visual changes (whitespace/formatting)")

    def _get_user_decision(self, fix: FixProposal) -> ApprovalDecision:
        """Get approval decision from user"""

        logger.info(f"\n🤔 What would you like to do?")
        logger.info(f"   [y] Approve this fix")
        logger.info(f"   [n] Reject this fix")
        logger.info(f"   [s] Skip this fix (review later)")
        logger.info(f"   [A] Approve all remaining safe fixes (auto-mode)")
        logger.info(f"   [R] Reject all remaining fixes")
        logger.info(f"   [?] Show more details")
        logger.info(f"   [q] Quit approval session")

        while True:
            try:
                choice = input("\n👉 Your choice [y/n/s/A/R/?/q]: ").strip().lower()

                if choice in ['y', 'yes']:
                    return ApprovalDecision.APPROVE
                elif choice in ['n', 'no']:
                    return ApprovalDecision.REJECT
                elif choice in ['s', 'skip']:
                    return ApprovalDecision.SKIP
                elif choice in ['a']:
                    self.global_decision = ApprovalDecision.APPROVE_ALL_SAFE
                    return ApprovalDecision.APPROVE_ALL_SAFE
                elif choice in ['r']:
                    self.global_decision = ApprovalDecision.REJECT_ALL
                    return ApprovalDecision.REJECT_ALL
                elif choice in ['?', 'help']:
                    self._show_detailed_help(fix)
                    continue
                elif choice in ['q', 'quit']:
                    logger.info("🛑 Exiting approval session...")
                    sys.exit(0)
                else:
                    logger.info(f"❌ Invalid choice '{choice}'. Please use y/n/s/A/R/?/q")

            except KeyboardInterrupt:
                logger.info(f"\n🛑 Session interrupted. Exiting...")
                sys.exit(0)
            except EOFError:
                return ApprovalDecision.REJECT

    def _show_detailed_help(self, fix: FixProposal):
        """Show detailed information about the fix"""

        logger.info(f"\n📋 DETAILED FIX INFORMATION")
        logger.info(f"─" * 50)

        # Safety analysis
        if fix.safety_score >= 90:
            safety_level = "🟢 Very Safe"
        elif fix.safety_score >= 70:
            safety_level = "🟡 Moderately Safe"
        else:
            safety_level = "🔴 Requires Caution"

        logger.info(f"Safety Assessment: {safety_level}")
        logger.info(f"Auto-approvable: {'✅ Yes' if self.categorize_fix_safety(fix) else '❌ No'}")

        # Context analysis
        context_description = {
            'production': 'Production code - changes affect end users',
            'test': 'Test code - changes affect testing but not production',
            'demo': 'Demo/example code - changes affect examples/demos',
            'config': 'Configuration code - changes affect system behavior'
        }

        logger.info(f"Context: {context_description.get(fix.context, 'Unknown context")}")

        # Risk assessment
        risks = []
        if fix.issue_type in self.REQUIRE_APPROVAL:
            risks.append("⚠️ Manual approval required by policy")
        if fix.safety_score < 70:
            risks.append("⚠️ Below safety threshold")
        if fix.context == 'production' and fix.severity in [FixSeverity.HIGH, FixSeverity.CRITICAL]:
            risks.append("⚠️ High-impact production change")

        if risks:
            logger.info(f"\nRisk Factors:")
            for risk in risks:
                logger.info(f"   {risk}")
        else:
            logger.info(f"\n✅ No significant risk factors identified")

    def process_fix_batch(self, fixes: List[FixProposal]) -> Tuple[List[FixProposal], List[FixProposal]]:
        """Process a batch of fixes and return approved/rejected lists"""

        approved_fixes = []
        rejected_fixes = []

        logger.info(f"\n🎯 PRI INTERACTIVE APPROVAL SESSION")
        logger.info(f"📊 Found {len(fixes)} proposed fixes for review")

        # Count auto-approvable fixes
        auto_approvable = sum(1 for fix in fixes if self.categorize_fix_safety(fix))
        manual_review = len(fixes) - auto_approvable

        if self.auto_approve_safe and auto_approvable > 0:
            logger.info(f"✅ {auto_approvable} fixes can be auto-approved (safe)")
        if manual_review > 0:
            logger.info(f"👁️  {manual_review} fixes require manual review")

        logger.info(f"\n🚀 Starting approval process...")

        for i, fix in enumerate(fixes, 1):
            if self.global_decision == ApprovalDecision.REJECT_ALL:
                rejected_fixes.append(fix)
                continue

            logger.info(f"\n📋 Review {i}/{len(fixes)}")

            decision = self.present_fix_for_approval(fix)

            if decision in [ApprovalDecision.APPROVE, ApprovalDecision.APPROVE_ALL_SAFE]:
                approved_fixes.append(fix)
                logger.info(f"✅ Approved: {fix.issue_type}")
            elif decision == ApprovalDecision.REJECT:
                rejected_fixes.append(fix)
                logger.info(f"❌ Rejected: {fix.issue_type}")
            elif decision == ApprovalDecision.SKIP:
                rejected_fixes.append(fix)  # Treat skip as reject for now
                logger.info(f"⏭️  Skipped: {fix.issue_type}")

        return approved_fixes, rejected_fixes

    def present_connection_for_approval(self, connection: ConnectionProposal) -> ApprovalDecision:
        """Present a code connection suggestion for approval"""
        
        if not self.interactive_mode:
            return ApprovalDecision.APPROVE if self.categorize_connection_safety(connection) else ApprovalDecision.REJECT

        # Check for global decisions
        if self.global_decision:
            return self.global_decision

        # Auto-approve safe connections if enabled
        if self.auto_approve_safe and self.categorize_connection_safety(connection):
            logger.info(f"✅ Auto-approved connection: {connection.orphaned_file} → {connection.target_file}")
            return ApprovalDecision.APPROVE

        # Present connection for manual review
        return self._interactive_connection_review(connection)

    def categorize_connection_safety(self, connection: ConnectionProposal) -> bool:
        """Determine if a connection suggestion can be auto-approved"""
        
        # High-impact connections always require approval
        if connection.impact_level == 'high':
            return False
        
        # Check safety score threshold
        if connection.safety_score < 75:
            return False
            
        # Low-impact connections with good confidence can be auto-approved
        if connection.impact_level == 'low' and connection.connection_score > 0.7:
            return True
            
        # Specific connection types that are generally safe
        safe_connection_types = {'function_import', 'constant_import', 'utility_import'}
        if connection.connection_type in safe_connection_types and connection.safety_score >= 80:
            return True
            
        return connection.auto_approvable

    def _interactive_connection_review(self, connection: ConnectionProposal) -> ApprovalDecision:
        """Present connection details and get user decision"""
        
        logger.info("\n" + "="*80)
        logger.info(f"🔗 CODE CONNECTION SUGGESTION REVIEW")
        logger.info("="*80)
        
        # Basic information
        logger.info(f"📁 Orphaned File: {connection.orphaned_file}")
        logger.info(f"🎯 Target File: {connection.target_file}")
        logger.info(f"📊 Connection Score: {connection.connection_score:.3f}")
        logger.info(f"🔧 Connection Type: {connection.connection_type}")
        logger.info(f"📈 Safety Score: {connection.safety_score}/100")
        logger.info(f"⚡ Impact Level: {connection.impact_level}")
        
        # Show reasoning
        if connection.reasoning:
            logger.info(f"\n🧠 Why this connection makes sense:")
            for i, reason in enumerate(connection.reasoning, 1):
                wrapped_reason = textwrap.fill(reason, width=76)
                logger.info(f"   {i}. {wrapped_reason}")
        
        # Show integration suggestions
        if connection.integration_suggestions:
            logger.info(f"\n💡 How to integrate:")
            for i, suggestion in enumerate(connection.integration_suggestions[:3], 1):  # Show top 3
                wrapped_suggestion = textwrap.fill(suggestion, width=76)
                logger.info(f"   {i}. {wrapped_suggestion}")
        
        # Get user decision
        return self._get_connection_decision(connection)

    def _get_connection_decision(self, connection: ConnectionProposal) -> ApprovalDecision:
        """Get approval decision for connection from user"""
        
        logger.info(f"\n🤔 What would you like to do with this connection suggestion?")
        logger.info(f"   [y] Approve this connection")
        logger.info(f"   [n] Reject this connection")
        logger.info(f"   [s] Skip this connection (review later)")
        logger.info(f"   [A] Approve all remaining safe connections")
        logger.info(f"   [R] Reject all remaining connections")
        logger.info(f"   [?] Show more details")
        logger.info(f"   [q] Quit approval session")
        
        while True:
            try:
                choice = input("\n👉 Your choice [y/n/s/A/R/?/q]: ").strip().lower()
                
                if choice in ['y', 'yes']:
                    return ApprovalDecision.APPROVE
                elif choice in ['n', 'no']:
                    return ApprovalDecision.REJECT
                elif choice in ['s', 'skip']:
                    return ApprovalDecision.SKIP
                elif choice in ['a']:
                    self.global_decision = ApprovalDecision.APPROVE_ALL_SAFE
                    return ApprovalDecision.APPROVE_ALL_SAFE
                elif choice in ['r']:
                    self.global_decision = ApprovalDecision.REJECT_ALL
                    return ApprovalDecision.REJECT_ALL
                elif choice in ['?', 'help']:
                    self._show_connection_detailed_help(connection)
                    continue
                elif choice in ['q', 'quit']:
                    logger.info("🛑 Exiting approval session...")
                    sys.exit(0)
                else:
                    logger.info(f"❌ Invalid choice '{choice}'. Please use y/n/s/A/R/?/q")
            
            except KeyboardInterrupt:
                logger.info(f"\n🛑 Session interrupted. Exiting...")
                sys.exit(0)
            except EOFError:
                return ApprovalDecision.REJECT

    def _show_connection_detailed_help(self, connection: ConnectionProposal):
        """Show detailed information about the connection suggestion"""
        
        logger.info(f"\n📋 DETAILED CONNECTION INFORMATION")
        logger.info(f"─" * 50)
        
        # Safety analysis
        if connection.safety_score >= 90:
            safety_level = "🟢 Very Safe"
        elif connection.safety_score >= 70:
            safety_level = "🟡 Moderately Safe"
        else:
            safety_level = "🔴 Requires Caution"
        
        logger.info(f"Safety Assessment: {safety_level}")
        logger.info(f"Auto-approvable: {'✅ Yes' if self.categorize_connection_safety(connection) else '❌ No'}")
        
        # Impact analysis
        impact_descriptions = {
            'low': 'Low impact - adds utility function or import, minimal risk',
            'medium': 'Medium impact - adds significant functionality, moderate risk',
            'high': 'High impact - major architectural change, requires careful review'
        }
        logger.info(f"Impact: {impact_descriptions.get(connection.impact_level, 'Unknown impact")}")
        
        # Connection type explanation
        type_descriptions = {
            'function_import': 'Import specific functions from the orphaned file',
            'class_import': 'Import classes from the orphaned file',
            'module_import': 'Import the entire orphaned file as a module',
            'constant_import': 'Import constants/configuration from the orphaned file',
            'utility_import': 'Import as utility functions',
            'selective_function_import': 'Import selected functions from the orphaned file',
            'selective_class_import': 'Import selected classes from the orphaned file'
        }
        logger.info(f"Connection Type: {type_descriptions.get(connection.connection_type, 'Unknown type")}")
        
        # Risk assessment
        risks = []
        if connection.impact_level == 'high':
            risks.append("⚠️ High-impact change requiring careful review")
        if connection.safety_score < 70:
            risks.append("⚠️ Below safety threshold")
        if connection.connection_score < 0.5:
            risks.append("⚠️ Low confidence in connection quality")
        
        if risks:
            logger.info(f"\nRisk Factors:")
            for risk in risks:
                logger.info(f"   {risk}")
        else:
            logger.info(f"\n✅ No significant risk factors identified")

    def process_connection_batch(self, connections: List[ConnectionProposal]) -> Tuple[List[ConnectionProposal], List[ConnectionProposal]]:
        """Process a batch of connection suggestions and return approved/rejected lists"""
        
        approved_connections = []
        rejected_connections = []
        
        logger.info(f"\n🔗 CODE CONNECTOR APPROVAL SESSION")
        logger.info(f"📊 Found {len(connections)} connection suggestions for review")
        
        # Count auto-approvable connections
        auto_approvable = sum(1 for conn in connections if self.categorize_connection_safety(conn))
        manual_review = len(connections) - auto_approvable
        
        if self.auto_approve_safe and auto_approvable > 0:
            logger.info(f"✅ {auto_approvable} connections can be auto-approved (safe)")
        if manual_review > 0:
            logger.info(f"👁️  {manual_review} connections require manual review")
        
        logger.info(f"\n🚀 Starting connection approval process...")
        
        for i, connection in enumerate(connections, 1):
            if self.global_decision == ApprovalDecision.REJECT_ALL:
                rejected_connections.append(connection)
                continue
            
            logger.info(f"\n📋 Connection Review {i}/{len(connections)}")
            
            decision = self.present_connection_for_approval(connection)
            
            if decision in [ApprovalDecision.APPROVE, ApprovalDecision.APPROVE_ALL_SAFE]:
                approved_connections.append(connection)
                logger.info(f"✅ Approved: {connection.orphaned_file} → {connection.target_file}")
            elif decision == ApprovalDecision.REJECT:
                rejected_connections.append(connection)
                logger.info(f"❌ Rejected: {connection.orphaned_file} → {connection.target_file}")
            elif decision == ApprovalDecision.SKIP:
                rejected_connections.append(connection)  # Treat skip as reject for now
                logger.info(f"⏭️  Skipped: {connection.orphaned_file} → {connection.target_file}")
        
        return approved_connections, rejected_connections

    def generate_session_summary(self, approved: List[FixProposal], rejected: List[FixProposal]):
        """Generate a summary of the approval session"""

        logger.info(f"\n🎉 APPROVAL SESSION COMPLETE")
        logger.info(f"="*50)
        logger.info(f"✅ Approved: {len(approved)} fixes")
        logger.info(f"❌ Rejected: {len(rejected)} fixes")

        if approved:
            logger.info(f"\n📋 Approved fixes will be applied:")
            for fix in approved:
                logger.info(f"   • {fix.issue_type} in {fix.file_path}:{fix.line_number}")

        if rejected:
            logger.info(f"\n🚫 Rejected fixes (will not be applied):")
            for fix in rejected:
                logger.info(f"   • {fix.issue_type} in {fix.file_path}:{fix.line_number}")

        return {
            'approved_count': len(approved),
            'rejected_count': len(rejected),
            'approval_rate': len(approved) / (len(approved) + len(rejected)) * 100 if (approved or rejected) else 0
        }

def create_sample_fix_proposal() -> FixProposal:
    """Create a sample fix proposal for testing"""
    return FixProposal(
        file_path="example.py",
        issue_type="bare_except_blocks",
        severity=FixSeverity.MEDIUM,
        description="Bare except clause catches all exceptions, including system exceptions",
        # IMPROVED: original_code="try:\n    risky_operation()\nexcept Exception as e:\n    pass",
        # IMPROVED: proposed_fix="try:\n    risky_operation()\nexcept Exception as e:\n    logger.warning(f'Operation failed: {e}')",
        line_number=42,
        educational_explanation="Bare except clauses are problematic because they catch system exceptions like KeyboardInterrupt and SystemExit, making debugging difficult.",
        safety_score=65,
        context="production",
        auto_approvable=False
    )

if __name__ == "__main__":
    # Demo the interactive approval system
    approval_system = InteractiveApprovalSystem()
    sample_fix = create_sample_fix_proposal()

    decision = approval_system.present_fix_for_approval(sample_fix)
    logger.info(f"\nDecision: {decision}")