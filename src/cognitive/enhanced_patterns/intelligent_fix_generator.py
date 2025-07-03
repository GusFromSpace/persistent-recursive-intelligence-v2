#!/usr/bin/env python3
"""
Intelligent Fix Generator - Generates fix suggestions that feed back into approval system
Creates positive feedback loop for learning safe vs dangerous patterns
"""

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..interactive_approval import FixProposal, FixSeverity

logger = logging.getLogger(__name__)

@dataclass
class FixTemplate:
    """Template for generating fixes with safety constraints"""
    issue_pattern: str  # Regex pattern that matches the issue
    fix_template: str   # Template for the fix (with placeholders)
    safety_score: int   # Base safety score for this template
    requires_approval: bool  # Whether this always needs approval
    contexts_allowed: List[str]  # Which contexts this is safe for
    description_template: str  # Description template
    educational_explanation: str  # Why this fix is recommended

class IntelligentFixGenerator:
    """Generates fix suggestions that get scored by the safety system"""
    
    def __init__(self, memory_engine=None):
        self.memory_engine = memory_engine
        self.fix_templates = self._load_safe_fix_templates()
        self.learning_data = self._load_learning_data()
        self.generation_stats = {
            'fixes_generated': 0,
            'fixes_approved': 0,
            'fixes_rejected': 0,
            'dangerous_patterns_learned': []
        }
    
    def _load_safe_fix_templates(self) -> List[FixTemplate]:
        """Load pre-validated safe fix templates"""
        return [
            # Ultra-safe whitespace fixes
            FixTemplate(
                issue_pattern=r'\\s+$',  # Trailing whitespace
                fix_template='{line}',  # Remove trailing whitespace
                safety_score=98,
                requires_approval=False,
                contexts_allowed=['production', 'test', 'demo', 'config'],
                description_template="Remove trailing whitespace",
                educational_explanation="Trailing whitespace can cause inconsistent formatting and git diff noise"
            ),
            
            # Safe import organization
            FixTemplate(
                issue_pattern=r'import\\s+([a-zA-Z_][a-zA-Z0-9_]*),\\s*([a-zA-Z_][a-zA-Z0-9_]*)',
                fix_template='import {group1}\\nimport {group2}',
                safety_score=85,
                requires_approval=True,  # Imports can affect behavior
                contexts_allowed=['test', 'demo'],
                description_template="Organize imports on separate lines",
                educational_explanation="PEP8 recommends separate lines for imports for better readability"
            ),
            
            # Comment typo fixes
            FixTemplate(
                issue_pattern=r'#.*\\b(paramter|paramters|functon|fucntion|retrun)\\b',
                fix_template='{fixed_comment}',
                safety_score=95,
                requires_approval=False,
                contexts_allowed=['production', 'test', 'demo', 'config'],
                description_template="Fix spelling in comment",
                educational_explanation="Correct spelling improves code documentation quality"
            ),
            
            # String quote consistency (very conservative)
            FixTemplate(
                issue_pattern=r"'([^']*)'",  # Single quotes
                fix_template='"{group1}"',   # Convert to double quotes
                safety_score=90,
                requires_approval=True,  # Could affect string content
                contexts_allowed=['test'],  # Only in test files
                description_template="Standardize quote style",
                educational_explanation="Consistent quote style improves code readability"
            )
        ]
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load previous learning data about approved/rejected patterns"""
        try:
            learning_file = Path('fix_generator_learning.json')
            if learning_file.exists():
                with open(learning_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load learning data: {e}")
        
        return {
            'approved_patterns': [],
            'rejected_patterns': [],
            'dangerous_indicators': [],
            'safe_indicators': []
        }
    
    def generate_fix_suggestions(self, analysis_results: List[Dict]) -> List[FixProposal]:
        """Generate fix suggestions from analysis results"""
        suggestions = []
        
        logger.info(f"🤖 Generating fix suggestions for {len(analysis_results)} issues...")
        
        for issue in analysis_results:
            try:
                fix_proposal = self._generate_single_fix(issue)
                if fix_proposal:
                    suggestions.append(fix_proposal)
                    self.generation_stats['fixes_generated'] += 1
            except Exception as e:
                logger.warning(f"Failed to generate fix for {issue.get('file_path', 'unknown')}: {e}")
        
        logger.info(f"✨ Generated {len(suggestions)} fix suggestions")
        return suggestions
    
    def _generate_single_fix(self, issue: Dict) -> Optional[FixProposal]:
        """Generate a single fix proposal for an issue"""
        issue_type = issue.get('type', '')
        file_path = issue.get('file_path', '')
        line_number = issue.get('line', 0)
        description = issue.get('description', '')
        
        # Read the problematic line
        original_code = self._read_line(file_path, line_number)
        if not original_code:
            return None
        
        # Try each template to see if it matches
        for template in self.fix_templates:
            if self._template_matches_issue(template, issue, original_code):
                proposed_fix = self._apply_template(template, original_code, issue)
                
                if proposed_fix and proposed_fix != original_code:
                    # Determine context
                    context = self._determine_context(file_path)
                    
                    # Skip if context not allowed for this template
                    if context not in template.contexts_allowed:
                        continue
                    
                    # Create fix proposal
                    fix_proposal = FixProposal(
                        file_path=file_path,
                        issue_type=issue_type,
                        severity=self._determine_severity(issue, template),
                        description=template.description_template,
                        original_code=original_code.strip(),
                        proposed_fix=proposed_fix.strip(),
                        line_number=line_number,
                        educational_explanation=template.educational_explanation,
                        safety_score=self._calculate_template_safety_score(template, issue, proposed_fix),
                        context=context,
                        auto_approvable=not template.requires_approval
                    )
                    
                    # Additional safety validation
                    if self._validate_fix_safety(fix_proposal):
                        return fix_proposal
        
        return None
    
    def _template_matches_issue(self, template: FixTemplate, issue: Dict, original_code: str) -> bool:
        """Check if a template matches the given issue"""
        # For now, simple pattern matching
        # In the future, this could use the memory engine for semantic matching
        return bool(re.search(template.issue_pattern, original_code))
    
    def _apply_template(self, template: FixTemplate, original_code: str, issue: Dict) -> str:
        """Apply a fix template to generate the proposed fix"""
        # Simple implementation - more sophisticated logic would go here
        if template.issue_pattern == r'\\s+$':  # Trailing whitespace
            return original_code.rstrip()
        
        # For more complex patterns, we'd use regex substitution
        match = re.search(template.issue_pattern, original_code)
        if match:
            # Replace based on template
            if '{group1}' in template.fix_template and '{group2}' in template.fix_template:
                if len(match.groups()) >= 2:
                    return template.fix_template.format(group1=match.group(1), group2=match.group(2))
        
        return original_code
    
    def _determine_context(self, file_path: str) -> str:
        """Determine the context of a file (production, test, demo, config)"""
        path_lower = file_path.lower()
        
        if 'test' in path_lower or '/tests/' in path_lower:
            return 'test'
        elif 'demo' in path_lower or 'example' in path_lower:
            return 'demo'
        elif 'config' in path_lower or '.conf' in path_lower or '.ini' in path_lower:
            return 'config'
        else:
            return 'production'  # Default to most restrictive
    
    def _determine_severity(self, issue: Dict, template: FixTemplate) -> FixSeverity:
        """Determine the severity of the fix based on issue and template"""
        issue_severity = issue.get('severity', 'low')
        
        # Map string severities to enum
        severity_map = {
            'low': FixSeverity.LOW,
            'medium': FixSeverity.MEDIUM,
            'high': FixSeverity.HIGH,
            'critical': FixSeverity.CRITICAL
        }
        
        # For cosmetic fixes, always use cosmetic severity
        if template.safety_score >= 95 and not template.requires_approval:
            return FixSeverity.COSMETIC
        
        return severity_map.get(issue_severity, FixSeverity.LOW)
    
    def _calculate_template_safety_score(self, template: FixTemplate, issue: Dict, proposed_fix: str) -> int:
        """Calculate safety score for a template-generated fix"""
        base_score = template.safety_score
        
        # Reduce score for certain risk factors
        if 'import' in proposed_fix.lower():
            base_score = min(base_score, 80)
        
        if any(dangerous in proposed_fix.lower() for dangerous in ['eval', 'exec', 'subprocess', 'system']):
            base_score = 0  # Immediate failure
        
        # Check against learned dangerous patterns
        for dangerous_pattern in self.learning_data.get('dangerous_indicators', []):
            if dangerous_pattern in proposed_fix:
                base_score = min(base_score, 30)
        
        return max(0, min(100, base_score))
    
    def _validate_fix_safety(self, fix_proposal: FixProposal) -> bool:
        """Final safety validation for generated fixes"""
        # Import the safety checker to validate our own suggestions
        from ...mesopredator_cli import calculate_fix_safety_score
        
        calculated_score = calculate_fix_safety_score(fix_proposal)
        
        # Our generated fixes should meet the same safety standards
        if calculated_score < 0.8:  # 80% threshold for self-generated fixes
            logger.warning(f"🚨 Generated fix failed safety check: {calculated_score:.2f}")
            return False
        
        return True
    
    def _read_line(self, file_path: str, line_number: int) -> Optional[str]:
        """Read a specific line from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 0 < line_number <= len(lines):
                    return lines[line_number - 1]
        except Exception as e:
            logger.warning(f"Could not read line {line_number} from {file_path}: {e}")
        return None
    
    def learn_from_approval_decision(self, fix_proposal: FixProposal, approved: bool, reason: str = ""):
        """Learn from user approval/rejection decisions - THE FEEDBACK LOOP"""
        logger.info(f"📚 Learning from decision: {fix_proposal.issue_type} -> {'APPROVED' if approved else 'REJECTED'}")
        
        if approved:
            self.generation_stats['fixes_approved'] += 1
            self._record_safe_pattern(fix_proposal)
        else:
            self.generation_stats['fixes_rejected'] += 1
            self._record_dangerous_pattern(fix_proposal, reason)
        
        self._save_learning_data()
    
    def _record_safe_pattern(self, fix_proposal: FixProposal):
        """Record patterns from approved fixes as safe"""
        safe_pattern = {
            'issue_type': fix_proposal.issue_type,
            'context': fix_proposal.context,
            'severity': fix_proposal.severity.value,
            'original_snippet': fix_proposal.original_code[:50],  # First 50 chars
            'fix_snippet': fix_proposal.proposed_fix[:50],
            'timestamp': datetime.now().isoformat()
        }
        
        self.learning_data['approved_patterns'].append(safe_pattern)
        
        # Extract safe indicators
        safe_indicators = self.learning_data.get('safe_indicators', [])
        
        # Learn that certain patterns in approved fixes are safe
        for pattern in ['import ', 'def ', 'class ', ' = ']:
            if pattern in fix_proposal.proposed_fix and pattern not in safe_indicators:
                # Only add if it appears in multiple approved fixes
                approval_count = sum(1 for p in self.learning_data['approved_patterns'] 
                                   if pattern in p.get('fix_snippet', ''))
                if approval_count >= 3:  # Conservative threshold
                    safe_indicators.append(pattern)
        
        self.learning_data['safe_indicators'] = safe_indicators
    
    def _record_dangerous_pattern(self, fix_proposal: FixProposal, reason: str):
        """Record patterns from rejected fixes as dangerous"""
        dangerous_pattern = {
            'issue_type': fix_proposal.issue_type,
            'context': fix_proposal.context,
            'severity': fix_proposal.severity.value,
            'original_snippet': fix_proposal.original_code[:50],
            'fix_snippet': fix_proposal.proposed_fix[:50],
            'rejection_reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        
        self.learning_data['rejected_patterns'].append(dangerous_pattern)
        
        # Extract dangerous indicators
        dangerous_indicators = self.learning_data.get('dangerous_indicators', [])
        
        # Learn patterns that led to rejection
        potential_indicators = [
            'admin', 'root', 'password', 'auth', 'eval(', 'exec(', 
            'subprocess', 'system', 'import ', '= True', '= False'
        ]
        
        for indicator in potential_indicators:
            if indicator in fix_proposal.proposed_fix and indicator not in dangerous_indicators:
                dangerous_indicators.append(indicator)
        
        self.learning_data['dangerous_indicators'] = dangerous_indicators
        self.generation_stats['dangerous_patterns_learned'].append(dangerous_pattern)
    
    def _save_learning_data(self):
        """Save learning data to disk for persistence"""
        try:
            learning_file = Path('fix_generator_learning.json')
            with open(learning_file, 'w') as f:
                json.dump(self.learning_data, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save learning data: {e}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get statistics about the learning progress"""
        total_decisions = self.generation_stats['fixes_approved'] + self.generation_stats['fixes_rejected']
        approval_rate = (self.generation_stats['fixes_approved'] / total_decisions * 100) if total_decisions > 0 else 0
        
        return {
            'fixes_generated': self.generation_stats['fixes_generated'],
            'fixes_approved': self.generation_stats['fixes_approved'],
            'fixes_rejected': self.generation_stats['fixes_rejected'],
            'approval_rate': approval_rate,
            'safe_patterns_learned': len(self.learning_data.get('approved_patterns', [])),
            'dangerous_patterns_learned': len(self.learning_data.get('rejected_patterns', [])),
            'safe_indicators': self.learning_data.get('safe_indicators', []),
            'dangerous_indicators': self.learning_data.get('dangerous_indicators', [])
        }
    
    def generate_learning_report(self) -> str:
        """Generate a human-readable learning report"""
        stats = self.get_learning_statistics()
        
        report = f"""
🤖 INTELLIGENT FIX GENERATOR - LEARNING REPORT
============================================

📊 Generation Statistics:
   Fixes Generated: {stats['fixes_generated']}
   Fixes Approved: {stats['fixes_approved']}
   Fixes Rejected: {stats['fixes_rejected']}
   Approval Rate: {stats['approval_rate']:.1f}%

📚 Learning Progress:
   Safe Patterns Learned: {stats['safe_patterns_learned']}
   Dangerous Patterns Learned: {stats['dangerous_patterns_learned']}

🟢 Safe Indicators Discovered:
   {', '.join(stats['safe_indicators'][:10])}

🔴 Dangerous Indicators Learned:
   {', '.join(stats['dangerous_indicators'][:10])}

🔄 Feedback Loop Status: {'Active' if (stats['fixes_approved'] + stats['fixes_rejected']) > 0 else 'Initializing'}
🧠 Intelligence Level: {self._calculate_intelligence_level(stats)}
        """.strip()
        
        return report
    
    def _calculate_intelligence_level(self, stats: Dict) -> str:
        """Calculate the current intelligence level based on learning"""
        total_patterns = stats['safe_patterns_learned'] + stats['dangerous_patterns_learned']
        
        if total_patterns < 10:
            return "Novice (Learning basics)"
        elif total_patterns < 50:
            return "Developing (Building knowledge)"
        elif total_patterns < 100:
            return "Competent (Reliable patterns)"
        elif total_patterns < 500:
            return "Advanced (Sophisticated understanding)"
        else:
            return "Expert (Comprehensive knowledge)"

def create_feedback_loop_demo():
    """Demonstrate the feedback loop in action"""
    generator = IntelligentFixGenerator()
    
    # Sample analysis results
    sample_issues = [
        {
            'type': 'whitespace_cleanup',
            'file_path': 'test_file.py',
            'line': 1,
            'description': 'Trailing whitespace detected',
            'severity': 'low'
        }
    ]
    
    # Generate fixes
    fix_suggestions = generator.generate_fix_suggestions(sample_issues)
    
    # Simulate approval decisions
    for fix in fix_suggestions:
        # This would normally come from the interactive approval system
        approved = True  # Assume whitespace fixes are approved
        generator.learn_from_approval_decision(fix, approved, "Safe cosmetic change")
    
    # Show learning report
    print(generator.generate_learning_report())

if __name__ == "__main__":
    create_feedback_loop_demo()