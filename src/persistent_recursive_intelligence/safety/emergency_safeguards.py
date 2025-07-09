#!/usr/bin/env python3
"""
Emergency Safeguards - Final line of defense against malicious code application
CRITICAL: This runs even AFTER user approval to catch any malicious code that slipped through
"""

import json
import logging
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

@dataclass
class SecurityThreat:
    """Represents a detected security threat"""
    threat_type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    evidence: List[str]
    recommended_action: str

class EmergencySafeguards:
    """
    FINAL SECURITY LAYER - Validates fixes immediately before application
    This is the last line of defense if malicious code somehow gets approved
    """
    
    def __init__(self):
        self.threat_patterns = self._load_threat_patterns()
        self.emergency_log = []
        self.blocks_today = 0
        
    def _load_threat_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive threat detection patterns"""
        return {
            # Code execution threats
            'code_execution': [
                r'eval\s*\(',
                r'exec\s*\(',
                r'compile\s*\(',
                r'__import__\s*\(',
                r'subprocess\.',
                r'os\.system\s*\(',
                r'os\.popen\s*\(',
                r'os\.exec',
                r'commands\.',
                r'popen\s*\(',
            ],
            
            # File system threats  
            'file_system': [
                r'open\s*\(\s*["\'][^"\']*\.\.(\/|\\)',  # Path traversal
                r'\.\.[\\/]',  # Directory traversal
                r'\/etc\/passwd',
                r'\/etc\/shadow',
                r'rm\s+-rf\s+\/',
                r'shutil\.rmtree\s*\(',
                r'os\.remove\s*\(',
                r'os\.unlink\s*\(',
                r'pathlib\.Path.*\.unlink',
            ],
            
            # Network threats
            'network': [
                r'requests\.post\s*\([^)]*http',
                r'urllib.*\.urlopen',
                r'socket\.socket',
                r'http[s]?:\/\/(?!localhost|127\.0\.0\.1)',
                r'ftp:\/\/',
                r'telnet\.',
            ],
            
            # Authentication/privilege escalation
            'privilege_escalation': [
                r'user\.role\s*=\s*["\']admin["\']',
                r'\.role\s*=\s*["\']admin["\']',
                r'is_admin\s*=\s*True',
                r'sudo\s+',
                r'su\s+',
                r'chmod\s+777',
                r'chown\s+root',
                r'setuid\s*\(',
                r'setgid\s*\(',
            ],
            
            # Data exfiltration
            'data_exfiltration': [
                r'password\s*=\s*["\'][^"\']*["\']',
                r'api_key\s*=\s*["\'][^"\']*["\']',
                r'secret\s*=\s*["\'][^"\']*["\']',
                r'token\s*=\s*["\'][^"\']*["\']',
                r'database.*connection.*string',
                r'smtp.*password',
            ],
            
            # Logic bombs / time-based attacks
            'logic_bombs': [
                r'datetime\.now\(\)\.day\s*==\s*\d+',
                r'time\.sleep\s*\(\s*\d{4,}\s*\)',  # Long sleeps
                r'while\s+True\s*:',
                r'for.*in.*range\s*\(\s*\d{6,}\s*\)',  # Large loops
                r'if.*random\.',
            ],
            
            # Backdoors
            'backdoors': [
                r'if\s+.*==\s*["\']backdoor["\']',
                r'if\s+.*==\s*["\']debug["\'].*:.*admin',
                r'return\s+True\s*#.*backdoor',
                r'#\s*TODO:\s*remove\s*backdoor',
                r'#\s*HACK:',
                r'#\s*XXX:',
            ],
            
            # Obfuscation attempts
            'obfuscation': [
                r'chr\s*\(\s*\d+\s*\)',
                r'\\x[0-9a-fA-F]{2}',
                r'base64\.b64decode',
                r'codecs\.decode',
                r'bytes\.fromhex',
                r'eval\s*\(\s*["\'].*["\']\.decode',
            ],
            
            # Configuration tampering
            'config_tampering': [
                r'DEBUG\s*=\s*True',
                r'ALLOWED_HOSTS\s*=\s*\[\s*["\']\*["\']',
                r'SECRET_KEY\s*=\s*["\']["\']',  # Empty secret
                r'ssl_verify\s*=\s*False',
                r'check_hostname\s*=\s*False',
                r'verify_mode\s*=\s*CERT_NONE',
            ]
        }
    
    def validate_before_application(self, fix_proposal, file_content_before: str = "", file_content_after: str = "") -> Tuple[bool, List[SecurityThreat]]:
        """
        CRITICAL VALIDATION: Final check before applying any fix
        Returns: (is_safe, list_of_threats)
        """
        logger.info(f"🛡️ EMERGENCY SAFEGUARDS: Final validation of {fix_proposal.file_path}")
        
        threats = []
        
        # Check the proposed fix itself
        fix_threats = self._scan_for_threats(fix_proposal.proposed_fix, "proposed_fix")
        threats.extend(fix_threats)
        
        # Check the resulting file content if provided
        if file_content_after:
            content_threats = self._scan_for_threats(file_content_after, "resulting_file")
            threats.extend(content_threats)
        
        # Additional context-specific checks
        context_threats = self._check_context_specific_threats(fix_proposal)
        threats.extend(context_threats)
        
        # Check for suspicious patterns in the fix metadata
        metadata_threats = self._check_metadata_threats(fix_proposal)
        threats.extend(metadata_threats)
        
        # Filter out false positives based on context
        filtered_threats = self._filter_false_positives(threats, fix_proposal)
        
        is_safe = len(filtered_threats) == 0
        
        if not is_safe:
            self._log_emergency_block(fix_proposal, filtered_threats)
            self.blocks_today += 1
        
        return is_safe, filtered_threats
    
    def _scan_for_threats(self, code: str, context: str) -> List[SecurityThreat]:
        """Scan code for known threat patterns"""
        threats = []
        
        for threat_category, patterns in self.threat_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    threat = SecurityThreat(
                        threat_type=threat_category,
                        severity=self._determine_threat_severity(threat_category, pattern),
                        description=f"{threat_category.replace('_', ' ').title()} pattern detected in {context}",
                        evidence=[match.group(0)],
                        recommended_action="BLOCK_IMMEDIATELY"
                    )
                    threats.append(threat)
        
        return threats
    
    def _determine_threat_severity(self, category: str, pattern: str) -> str:
        """Determine threat severity based on category and pattern"""
        critical_categories = {'code_execution', 'privilege_escalation', 'backdoors'}
        high_categories = {'file_system', 'network', 'data_exfiltration'}
        
        if category in critical_categories:
            return 'critical'
        elif category in high_categories:
            return 'high'
        else:
            return 'medium'
    
    def _check_context_specific_threats(self, fix_proposal) -> List[SecurityThreat]:
        """Check for threats specific to the fix context"""
        threats = []
        
        # Production code gets extra scrutiny
        if fix_proposal.context == 'production':
            # Any code changes in production auth files are suspicious
            if 'auth' in fix_proposal.file_path.lower():
                if any(pattern in fix_proposal.proposed_fix.lower() 
                       for pattern in ['admin', 'root', 'password', '==', '=', 'true', 'false']):
                    threats.append(SecurityThreat(
                        threat_type='production_auth_modification',
                        severity='critical',
                        description='Modification to authentication code in production',
                        evidence=[fix_proposal.proposed_fix],
                        recommended_action='BLOCK_AND_ALERT'
                    ))
        
        # Check for cosmetic fixes that actually change logic
        if fix_proposal.issue_type in ['whitespace_cleanup', 'typo_corrections']:
            # These should only modify whitespace/comments, not code
            if any(pattern in fix_proposal.proposed_fix 
                   for pattern in ['=', 'import', 'def', 'class', 'if', 'for', 'while']):
                threats.append(SecurityThreat(
                    threat_type='disguised_logic_change',
                    severity='high', 
                    description='Cosmetic fix contains logic changes',
                    evidence=[fix_proposal.proposed_fix],
                    recommended_action='BLOCK_IMMEDIATELY'
                ))
        
        return threats
    
    def _check_metadata_threats(self, fix_proposal) -> List[SecurityThreat]:
        """Check for threats in the fix metadata itself"""
        threats = []
        
        # Suspiciously high safety scores for dangerous content
        if fix_proposal.safety_score > 90:
            if any(dangerous in fix_proposal.proposed_fix.lower() 
                   for dangerous in ['admin', 'password', 'exec', 'eval', 'import']):
                threats.append(SecurityThreat(
                    threat_type='safety_score_manipulation',
                    severity='critical',
                    description='High safety score despite dangerous content',
                    evidence=[f"Safety score: {fix_proposal.safety_score}", fix_proposal.proposed_fix],
                    recommended_action='BLOCK_AND_INVESTIGATE'
                ))
        
        # Check for mismatched issue type and fix content
        if fix_proposal.issue_type == 'whitespace_cleanup':
            if len(fix_proposal.proposed_fix.split('\n')) != len(fix_proposal.original_code.split('\n')):
                threats.append(SecurityThreat(
                    threat_type='mismatched_fix_type',
                    severity='high',
                    description='Whitespace fix changes line count',
                    evidence=[fix_proposal.proposed_fix],
                    recommended_action='BLOCK_IMMEDIATELY'
                ))
        
        return threats
    
    def _filter_false_positives(self, threats: List[SecurityThreat], fix_proposal) -> List[SecurityThreat]:
        """Filter out known false positives based on context"""
        filtered = []
        
        for threat in threats:
            # Skip certain threats in test files
            if fix_proposal.context == 'test':
                if threat.threat_type in ['network', 'file_system'] and 'mock' in fix_proposal.proposed_fix.lower():
                    continue  # Test mocks are acceptable
            
            # Skip documentation examples
            if any(doc_indicator in fix_proposal.file_path.lower() 
                   for doc_indicator in ['example', 'demo', 'docs', 'readme']):
                if threat.threat_type in ['code_execution', 'network']:
                    continue  # Documentation examples may show dangerous patterns
            
            filtered.append(threat)
        
        return filtered
    
    def _log_emergency_block(self, fix_proposal, threats: List[SecurityThreat]):
        """Log emergency block for security analysis"""
        emergency_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'EMERGENCY_BLOCK',
            'file_path': fix_proposal.file_path,
            'issue_type': fix_proposal.issue_type,
            'safety_score': fix_proposal.safety_score,
            'context': fix_proposal.context,
            'threats': [
                {
                    'type': threat.threat_type,
                    'severity': threat.severity,
                    'description': threat.description,
                    'evidence': threat.evidence
                }
                for threat in threats
            ],
            'proposed_fix': fix_proposal.proposed_fix[:200],  # First 200 chars
        }
        
        self.emergency_log.append(emergency_entry)
        
        # Also log to file for security analysis
        emergency_log_file = Path('emergency_safeguards.log')
        with open(emergency_log_file, 'a') as f:
            f.write(json.dumps(emergency_entry) + '\n')
        
        logger.critical(f"🚨 EMERGENCY BLOCK: {len(threats)} threats detected in {fix_proposal.file_path}")
        for threat in threats:
            logger.critical(f"   💀 {threat.threat_type}: {threat.description}")
    
    def generate_security_report(self) -> str:
        """Generate emergency safeguards security report"""
        total_blocks = len(self.emergency_log)
        
        if total_blocks == 0:
            return """
🛡️ EMERGENCY SAFEGUARDS REPORT
=============================
✅ No emergency blocks required
🔒 All approved fixes passed final security validation
📊 System operating within safe parameters
            """.strip()
        
        # Analyze threat patterns
        threat_counts = {}
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for entry in self.emergency_log:
            for threat in entry['threats']:
                threat_type = threat['type']
                threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
                severity_counts[threat['severity']] += 1
        
        report = f"""
🚨 EMERGENCY SAFEGUARDS REPORT - THREATS DETECTED
=================================================
📊 Total Emergency Blocks: {total_blocks}
🎯 Blocks Today: {self.blocks_today}

🔴 Threat Severity Breakdown:
   💀 Critical: {severity_counts['critical']}
   ⚠️  High: {severity_counts['high']}
   📋 Medium: {severity_counts['medium']}
   ℹ️  Low: {severity_counts['low']}

🎯 Most Common Threat Types:
        """
        
        # Show top 5 threat types
        sorted_threats = sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)
        for threat_type, count in sorted_threats[:5]:
            report += f"\n   • {threat_type.replace('_', ' ').title()}: {count} blocks"
        
        report += f"\n\n⚠️ SECURITY ALERT: Emergency safeguards have blocked {total_blocks} potentially malicious fixes!"
        report += "\n🔍 Review emergency_safeguards.log for detailed threat analysis"
        
        return report
    
    def get_emergency_statistics(self) -> Dict[str, Any]:
        """Get emergency safeguards statistics"""
        return {
            'total_blocks': len(self.emergency_log),
            'blocks_today': self.blocks_today,
            'threat_categories': list(self.threat_patterns.keys()),
            'latest_threats': self.emergency_log[-5:] if self.emergency_log else []
        }

def validate_fix_application(fix_proposal, file_content_before: str = "", file_content_after: str = "") -> Tuple[bool, str]:
    """
    MAIN ENTRY POINT: Validate a fix before application
    This is called even AFTER user approval as the final safety check
    
    Returns: (is_safe, reason_if_not_safe)
    """
    safeguards = EmergencySafeguards()
    is_safe, threats = safeguards.validate_before_application(
        fix_proposal, file_content_before, file_content_after
    )
    
    if not is_safe:
        threat_descriptions = [f"{t.threat_type}: {t.description}" for t in threats]
        reason = f"Emergency safeguards blocked: {'; '.join(threat_descriptions)}"
        return False, reason
    
    return True, "Passed emergency validation"

if __name__ == "__main__":
    # Test the emergency safeguards
    from ..cognitive.interactive_approval import FixProposal, FixSeverity
    
    # Create a malicious fix that might somehow get approved
    malicious_fix = FixProposal(
        file_path="auth.py",
        issue_type="typo_corrections",
        severity=FixSeverity.COSMETIC,
        description="Fix typo in comment",
        original_code="# Check user permissions",
        proposed_fix="# Check user permissions\nif user == 'backdoor': return True",
        line_number=1,
        educational_explanation="Spelling correction",
        safety_score=95,  # Artificially high
        context="production",
        auto_approvable=True
    )
    
    is_safe, reason = validate_fix_application(malicious_fix)
    print(f"Malicious fix blocked: {not is_safe}")
    print(f"Reason: {reason}")
    
    safeguards = EmergencySafeguards()
    print(safeguards.generate_security_report())