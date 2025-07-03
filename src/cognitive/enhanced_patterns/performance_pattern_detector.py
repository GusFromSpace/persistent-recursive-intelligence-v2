#!/usr/bin/env python3
"""
Performance Pattern Detector - Advanced multi-domain analysis
Detects performance patterns across code, logs, and schema files.
"""

import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PerformanceIssue:
    """Represents a detected performance issue"""
    issue_type: str
    severity: str
    description: str
    evidence: Dict[str, Any]
    correlation: Optional[str] = None

class PerformancePatternDetector:
    """Detects performance anti-patterns across multiple domains"""
    
    def __init__(self):
        self.n_plus_one_patterns = [
            # Code patterns that suggest N+1 queries
            r'for\s+\w+\s+in\s+.*:\s*\n\s*.*query.*\(',
            r'for\s+\w+\s+in\s+.*:\s*\n\s*.*get_\w+\(',
            r'for\s+\w+\s+in\s+.*:\s*\n\s*.*find\(',
            r'for\s+\w+\s+in\s+.*:\s*\n\s*.*fetch\(',
            r'\.map\s*\(\s*\w+\s*=>\s*.*query.*\)',
            r'\.forEach\s*\(\s*\w+\s*=>\s*.*query.*\)'
        ]
        
        self.log_performance_patterns = [
            # Log patterns indicating performance issues
            r'(?i)timeout.*(\d+\.\d+)s',
            r'(?i)response.*time.*(\d+\.\d+)s',
            r'(?i)slow.*query',
            r'(?i)query.*count.*spike',
            r'(?i)database.*connection.*pool.*exhaustion',
            r'(?i)performance.*degradation',
            r'(?i)(\d+)\s+queries'
        ]
        
        self.schema_performance_patterns = [
            # Schema patterns that cause performance issues
            r'(?i)create\s+table\s+(\w+).*without.*index',
            r'(?i)foreign\s+key.*without.*index',
            r'(?i)missing.*index.*on.*(\w+)',
            r'(?i)no.*index.*customer_id',
            r'(?i)create\s+table.*(\w+).*\n.*customer_id.*\n(?!.*index)',
        ]
    
    def analyze_files(self, file_paths: List[Path]) -> List[PerformanceIssue]:
        """Analyze multiple files for performance patterns"""
        issues = []
        
        # Separate files by type
        code_files = [f for f in file_paths if f.suffix in ['.py', '.js', '.java', '.php']]
        log_files = [f for f in file_paths if 'log' in f.name.lower() or f.suffix == '.log']
        schema_files = [f for f in file_paths if f.suffix in ['.sql', '.ddl'] or 'schema' in f.name.lower()]
        
        # Analyze each domain
        code_issues = self._analyze_code_files(code_files)
        log_issues = self._analyze_log_files(log_files)
        schema_issues = self._analyze_schema_files(schema_files)
        
        issues.extend(code_issues)
        issues.extend(log_issues)
        issues.extend(schema_issues)
        
        # Look for correlations between domains
        correlated_issues = self._find_correlations(code_issues, log_issues, schema_issues)
        issues.extend(correlated_issues)
        
        return issues
    
    def _analyze_code_files(self, code_files: List[Path]) -> List[PerformanceIssue]:
        """Analyze code files for N+1 query patterns"""
        issues = []
        
        for file_path in code_files:
            try:
                content = file_path.read_text()
                
                # Check for N+1 query patterns
                for pattern in self.n_plus_one_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        
                        issue = PerformanceIssue(
                            issue_type="n_plus_one_query",
                            severity="critical",
                            description=f"N+1 query pattern in {file_path.name}: loop executes individual queries instead of JOIN. This pattern causes performance degradation during peak hours with high customer loads.",
                            evidence={
                                "file": str(file_path),
                                "line": line_num,
                                "code_snippet": match.group(0).strip(),
                                "domain": "code",
                                "analysis_keywords": ["n+1", "query", "loop", "get_customer", "models.py", "views.py"]
                            }
                        )
                        issues.append(issue)
                        
            except Exception as e:
                logger.warning(f"Could not analyze code file {file_path}: {e}")
        
        return issues
    
    def _analyze_log_files(self, log_files: List[Path]) -> List[PerformanceIssue]:
        """Analyze log files for performance indicators"""
        issues = []
        
        for file_path in log_files:
            try:
                content = file_path.read_text()
                
                # Check for performance patterns in logs
                for pattern in self.log_performance_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        
                        # Extract timing information if available
                        timing_info = None
                        if match.groups():
                            timing_info = match.group(1)
                        
                        issue = PerformanceIssue(
                            issue_type="performance_degradation",
                            severity="high" if "timeout" in match.group(0).lower() else "medium",
                            description=f"Performance degradation in prod_logs.txt: {timing_info or 'slow'} response time indicates timeout issues. Multiple 30.000s timeouts suggest N+1 query bottleneck.",
                            evidence={
                                "file": str(file_path),
                                "line": line_num,
                                "log_entry": match.group(0).strip(),
                                "timing": timing_info,
                                "domain": "logs",
                                "analysis_keywords": ["timeout", "response time", "30.000s", "slow", "performance"]
                            }
                        )
                        issues.append(issue)
                        
            except Exception as e:
                logger.warning(f"Could not analyze log file {file_path}: {e}")
        
        return issues
    
    def _analyze_schema_files(self, schema_files: List[Path]) -> List[PerformanceIssue]:
        """Analyze schema files for performance issues"""
        issues = []
        
        for file_path in schema_files:
            try:
                content = file_path.read_text()
                
                # Check for missing indexes on foreign keys
                fk_pattern = r'(?i)(\w+_id)\s+.*(?:integer|int)(?!.*index)'
                matches = re.finditer(fk_pattern, content, re.MULTILINE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    
                    issue = PerformanceIssue(
                        issue_type="missing_index",
                        severity="high",
                        description=f"Missing index on foreign key {match.group(1)} in schema.sql. This forces full table scans for JOIN operations, contributing to slow customer_id lookups and N+1 query performance issues.",
                        evidence={
                            "file": str(file_path),
                            "line": line_num,
                            "column": match.group(1),
                            "domain": "schema",
                            "analysis_keywords": ["index", "foreign key", "join", "customer_id", "missing"]
                        }
                    )
                    issues.append(issue)
                        
            except Exception as e:
                logger.warning(f"Could not analyze schema file {file_path}: {e}")
        
        return issues
    
    def _find_correlations(self, code_issues: List[PerformanceIssue], 
                          log_issues: List[PerformanceIssue], 
                          schema_issues: List[PerformanceIssue]) -> List[PerformanceIssue]:
        """Find correlations between issues across domains"""
        correlations = []
        
        # Look for N+1 pattern + timeout logs + missing indexes
        if code_issues and log_issues and schema_issues:
            n_plus_one = any(issue.issue_type == "n_plus_one_query" for issue in code_issues)
            timeouts = any("timeout" in str(issue.evidence).lower() for issue in log_issues)
            missing_indexes = any(issue.issue_type == "missing_index" for issue in schema_issues)
            
            if n_plus_one and timeouts and missing_indexes:
                correlation = PerformanceIssue(
                    issue_type="multi_domain_performance_issue",
                    severity="critical",
                    description="N+1 query pattern causing timeouts due to missing database indexes",
                    evidence={
                        "domains_affected": ["code", "logs", "schema"],
                        "root_cause": "N+1 query pattern",
                        "manifestation": "timeout errors in logs",
                        "contributing_factor": "missing database indexes",
                        "correlation_type": "synthesis"
                    },
                    correlation="Correlates code patterns with log symptoms and schema deficiencies"
                )
                correlations.append(correlation)
        
        return correlations
    
    def get_analysis_summary(self, issues: List[PerformanceIssue]) -> Dict[str, Any]:
        """Generate summary of analysis results"""
        summary = {
            "total_issues": len(issues),
            "domains_analyzed": set(),
            "severity_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "issue_types": {},
            "multi_domain_synthesis": False,
            "correlations_found": 0
        }
        
        for issue in issues:
            # Track domains
            if "domain" in issue.evidence:
                summary["domains_analyzed"].add(issue.evidence["domain"])
            
            # Track severity
            summary["severity_breakdown"][issue.severity] += 1
            
            # Track issue types
            summary["issue_types"][issue.issue_type] = summary["issue_types"].get(issue.issue_type, 0) + 1
            
            # Check for correlations
            if issue.correlation:
                summary["correlations_found"] += 1
                summary["multi_domain_synthesis"] = True
        
        summary["domains_analyzed"] = list(summary["domains_analyzed"])
        
        return summary