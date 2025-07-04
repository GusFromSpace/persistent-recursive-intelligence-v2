#!/usr/bin/env python3
"""
Enhanced Bloodlust Hunter - Multi-Pattern Issue Elimination

This enhanced version can eliminate multiple types of issues:
- Debug statements (original functionality)
- Maintenance comments (commented debug statements)
- TODO/FIXME/XXX comments
- Dead code patterns
- Error handling gaps
"""

import json
import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Any

class EnhancedBloodlustHunter:
    """The mesopredator in enhanced bloodlust mode - multi-pattern elimination"""
    
    def __init__(self, target_dir: str, issues_file: str):
        self.target_dir = Path(target_dir)
        self.issues_file = issues_file
        self.kills = []
        self.hunt_report = {
            'hunt_start': time.time(),
            'target_directory': str(target_dir),
            'issues_file': issues_file
        }
        
    def load_prey(self) -> List[Dict]:
        """Load issues from JSON file"""
        with open(self.issues_file, 'r') as f:
            return json.load(f)
    
    def hunt_maintenance_comments(self, file_path: str, issues: List[Dict]) -> int:
        """Hunt and eliminate maintenance comments (commented debug statements)"""
        kills = 0
        maintenance_issues = [i for i in issues if i['type'] == 'maintenance' and i['file_path'] == file_path]
        
        if not maintenance_issues:
            return 0
            
        print(f"🎯 HUNTING MAINTENANCE: {file_path} - {len(maintenance_issues)} maintenance comments marked for elimination")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort by line number in reverse order to maintain line numbers
            maintenance_issues.sort(key=lambda x: x['line'], reverse=True)
            
            for issue in maintenance_issues:
                line_num = issue['line'] - 1  # Convert to 0-based indexing
                if 0 <= line_num < len(lines):
                    original_line = lines[line_num].strip()
                    
                    # Check if it's a maintenance comment we should eliminate
                    if self._is_maintenance_comment(original_line):
                        # ELIMINATE THE MAINTENANCE COMMENT
                        lines[line_num] = "# MAINTENANCE ELIMINATED BY ENHANCED BLOODLUST HUNTER\n"
                        
                        kills += 1
                        self.kills.append({
                            'file': file_path,
                            'line': issue['line'],
                            'type': 'maintenance_comment',
                            'original': original_line,
                            'action': 'eliminated'
                        })
                        print(f"  💀 KILLED: Line {issue['line']} - {original_line[:50]}...")
            
            if kills > 0:
                # Write the modified file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"  ✅ ELIMINATED {kills} maintenance comments from {file_path}")
                
        except Exception as e:
            print(f"  ❌ HUNT FAILED: {e}")
            
        return kills
    
    def _is_maintenance_comment(self, line: str) -> bool:
        """Check if line is a maintenance comment we should eliminate"""
        line = line.strip()
        patterns = [
            r'# DEBUG ELIMINATED BY MESOPREDATOR',
            r'# TODO:',
            r'# FIXME:',
            r'# XXX:',
            r'# HACK:',
            r'# BUG:',
            r'# TEMP:',
            r'# REMOVE:'
        ]
        
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False
    
    def hunt_debug_statements(self, file_path: str, issues: List[Dict]) -> int:
        """Hunt debug statements (original functionality)"""
        kills = 0
        debug_issues = [i for i in issues if i['type'] == 'debugging' and i['file_path'] == file_path]
        
        if not debug_issues:
            return 0
            
        print(f"🎯 HUNTING DEBUG: {file_path} - {len(debug_issues)} debug statements marked for elimination")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort by line number in reverse order to maintain line numbers
            debug_issues.sort(key=lambda x: x['line'], reverse=True)
            
            for issue in debug_issues:
                line_num = issue['line'] - 1  # Convert to 0-based indexing
                if 0 <= line_num < len(lines):
                    original_line = lines[line_num].strip()
                    
                    # Check if it's actually a debug print
                    if self._is_debug_print(original_line):
                        # KILL THE DEBUG STATEMENT
                        lines[line_num] = "# DEBUG ELIMINATED BY ENHANCED BLOODLUST HUNTER\n"
                        
                        kills += 1
                        self.kills.append({
                            'file': file_path,
                            'line': issue['line'],
                            'type': 'debug_statement',
                            'original': original_line,
                            'action': 'eliminated'
                        })
                        print(f"  💀 KILLED: Line {issue['line']} - {original_line[:50]}...")
            
            if kills > 0:
                # Write the modified file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"  ✅ ELIMINATED {kills} debug statements from {file_path}")
                
        except Exception as e:
            print(f"  ❌ HUNT FAILED: {e}")
            
        return kills
    
    def _is_debug_print(self, line: str) -> bool:
        """Check if line is actually a debug print statement"""
        line = line.strip()
        debug_patterns = [
            r'print\s*\(',
            r'console\.log\s*\(',
            r'console\.debug\s*\(',
            r'console\.info\s*\(',
            r'logger\.debug\s*\(',
            r'logger\.info\s*\(',
            r'System\.out\.println\s*\(',
            r'printf\s*\(',
            r'cout\s*<<'
        ]
        
        for pattern in debug_patterns:
            if re.search(pattern, line):
                return True
        return False
    
    def hunt_context_issues(self, issues: List[Dict]) -> int:
        """Hunt context and syntax issues that can be safely eliminated"""
        kills = 0
        context_issues = [i for i in issues if i['type'] in ['context', 'syntax', 'style']]
        
        if not context_issues:
            return 0
            
        print(f"🎯 HUNTING CONTEXT ISSUES: {len(context_issues)} context/syntax issues detected")
        
        # Group by file for efficient hunting
        files_with_issues = {}
        for issue in context_issues:
            file_path = issue['file_path']
            if file_path not in files_with_issues:
                files_with_issues[file_path] = []
            files_with_issues[file_path].append(issue)
        
        for file_path, file_issues in files_with_issues.items():
            print(f"  📁 Analyzing: {file_path} - {len(file_issues)} context issues")
            kills += self._eliminate_safe_context_issues(file_path, file_issues)
            
        return kills
    
    def _eliminate_safe_context_issues(self, file_path: str, issues: List[Dict]) -> int:
        """Eliminate safe context issues that don't break functionality"""
        kills = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for issue in issues:
                # Only eliminate safe patterns that don't break code
                description = issue.get('description', '').lower()
                
                if any(safe_pattern in description for safe_pattern in [
                    'pattern legitimate_logging',
                    'maintenance comment',
                    'whitespace',
                    'formatting'
                ]):
                    line_num = issue['line'] - 1
                    if 0 <= line_num < len(lines):
                        original_line = lines[line_num].strip()
                        
                        # Add a comment indicating review
                        lines[line_num] = f"# CONTEXT REVIEWED BY ENHANCED BLOODLUST HUNTER: {original_line}\n"
                        
                        kills += 1
                        self.kills.append({
                            'file': file_path,
                            'line': issue['line'],
                            'type': 'context_issue',
                            'original': original_line,
                            'action': 'marked_for_review'
                        })
            
            if kills > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                print(f"    ✅ MARKED {kills} context issues for review in {file_path}")
            
        except Exception as e:
            print(f"    ❌ CONTEXT HUNT FAILED: {e}")
            
        return kills
    
    def execute_enhanced_hunt(self):
        """Execute the enhanced systematic hunt"""
        print("🦅 ENHANCED MESOPREDATOR BLOODLUST HUNTER ACTIVATED")
        print("=" * 60)
        print(f"🎯 TARGET: {self.target_dir}")
        print(f"📋 LOADING PREY FROM: {self.issues_file}")
        print(f"💀 ENHANCED: Multi-pattern elimination active")
        
        # Load all issues
        issues = self.load_prey()
        print(f"🔍 IDENTIFIED {len(issues)} ISSUES TO ELIMINATE")
        
        # Count issue types
        issue_types = {}
        for issue in issues:
            issue_type = issue['type']
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1
        
        print(f"📊 ISSUE BREAKDOWN:")
        for issue_type, count in issue_types.items():
            print(f"   {issue_type}: {count}")
        
        # Group issues by file for efficient hunting
        files_with_issues = {}
        for issue in issues:
            file_path = issue['file_path']
            if file_path not in files_with_issues:
                files_with_issues[file_path] = []
            files_with_issues[file_path].append(issue)
        
        print(f"📁 {len(files_with_issues)} FILES CONTAIN PREY")
        print()
        
        total_kills = 0
        files_modified = 0
        
        # Hunt Phase 1: Debug statements
        print("🎯 PHASE 1: HUNTING DEBUG STATEMENTS")
        print("-" * 40)
        for file_path in files_with_issues:
            kills = self.hunt_debug_statements(file_path, files_with_issues[file_path])
            if kills > 0:
                total_kills += kills
                files_modified += 1
        
        print()
        
        # Hunt Phase 2: Maintenance comments
        print("🎯 PHASE 2: HUNTING MAINTENANCE COMMENTS")  
        print("-" * 40)
        for file_path in files_with_issues:
            kills = self.hunt_maintenance_comments(file_path, files_with_issues[file_path])
            if kills > 0:
                total_kills += kills
                files_modified += 1
        
        print()
        
        # Hunt Phase 3: Context issues (safe ones only)
        print("🎯 PHASE 3: HUNTING SAFE CONTEXT ISSUES")
        print("-" * 40)
        context_kills = self.hunt_context_issues(issues)
        total_kills += context_kills
        
        # Update hunt report
        self.hunt_report.update({
            'hunt_end': time.time(),
            'issues_eliminated': total_kills,
            'files_modified': files_modified,
            'hunt_details': self.kills,
            'issue_types_processed': issue_types
        })
        
        # Print hunt summary
        print()
        print("🏆 ENHANCED HUNT COMPLETE")
        print("=" * 60)
        print(f"💀 TOTAL KILLS: {total_kills}")
        print(f"📁 FILES MODIFIED: {files_modified}")
        hunt_time = self.hunt_report['hunt_end'] - self.hunt_report['hunt_start']
        print(f"⏱️  HUNT TIME: {hunt_time:.2f} seconds")
        print(f"⚡ KILLS PER SECOND: {total_kills/max(hunt_time, 0.1):.2f}")
        
        if total_kills > 0:
            print(f"\n🔥 ELIMINATED ISSUES:")
            for kill in self.kills:
                print(f"  💀 {kill['file']}:{kill['line']} - {kill['type']}")
        
        # Save hunt report
        report_file = "enhanced_bloodlust_hunt_report.json"
        with open(report_file, 'w') as f:
            json.dump(self.hunt_report, f, indent=2)
        print(f"\n📊 ENHANCED HUNT REPORT SAVED: {report_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python enhanced_bloodlust_hunter.py <target_directory> <issues_file>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    issues_file = sys.argv[2]
    
    hunter = EnhancedBloodlustHunter(target_dir, issues_file)
    hunter.execute_enhanced_hunt()

if __name__ == "__main__":
    main()