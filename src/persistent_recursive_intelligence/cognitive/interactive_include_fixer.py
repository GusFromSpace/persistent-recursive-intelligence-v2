#!/usr/bin/env python3
"""
Interactive Include Error Fixer for C++ Projects
Provides interactive fixing with scoring and learning capabilities
"""

import difflib
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

from .interactive_approval import FixSeverity, ApprovalDecision, FixProposal
from .memory.simple_memory import SimpleMemoryEngine
from .analyzers.cpp_analyzer import CppAnalyzer

logger = logging.getLogger(__name__)

class IncludeFixType(Enum):
    ADD_MISSING = "add_missing"
    REMOVE_DUPLICATE = "remove_duplicate"
    REORDER_INCLUDES = "reorder_includes"
    FIX_PATH = "fix_path"
    ADD_GUARDS = "add_guards"

@dataclass
class IncludeFixProposal(FixProposal):
    """Enhanced fix proposal for include errors"""
    fix_type: IncludeFixType
    include_header: str
    suggested_line: int
    alternative_fixes: List[str]
    confidence_score: float  # 0.0-1.0
    
@dataclass
class FixScore:
    """User scoring for applied fixes"""
    fix_id: str
    user_rating: int  # 1-5 stars
    was_helpful: bool
    feedback: str
    timestamp: str
    context: Dict[str, Any]

class InteractiveIncludeFixer:
    """Interactive system for fixing include errors with learning"""
    
    def __init__(self, memory_engine: Optional[SimpleMemoryEngine] = None):
        self.memory = memory_engine or SimpleMemoryEngine(namespace="include_fixes")
        self.analyzer = CppAnalyzer()
        self.fix_history = []
        self.user_preferences = {}
        
    def analyze_and_fix_file(self, file_path: Path, interactive: bool = True) -> List[FixProposal]:
        """Analyze a file and provide interactive fixing for include errors"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Cannot read file {file_path}: {e}")
            return []
            
        # Analyze for include issues
        issues = self.analyzer.analyze_file(file_path, content, self.memory, self.memory)
        include_issues = [issue for issue in issues if 'include' in issue['type'].lower()]
        
        if not include_issues:
            logger.info(f"✅ No include issues found in {file_path}")
            return []
            
        # Convert issues to fix proposals
        fix_proposals = []
        for issue in include_issues:
            proposal = self._create_fix_proposal(file_path, content, issue)
            if proposal:
                fix_proposals.append(proposal)
                
        if interactive:
            return self._interactive_fix_session(file_path, content, fix_proposals)
        else:
            return fix_proposals
            
    def _create_fix_proposal(self, file_path: Path, content: str, issue: Dict[str, Any]) -> Optional[IncludeFixProposal]:
        """Create a detailed fix proposal from an issue"""
        
        issue_type = issue['type']
        lines = content.split('\n')
        line_num = issue.get('line', 1) - 1  # Convert to 0-indexed
        
        # Determine fix type and create proposal
        if 'missing_include' in issue_type:
            return self._create_missing_include_fix(file_path, content, issue, lines)
        elif 'duplicate_include' in issue_type:
            return self._create_duplicate_include_fix(file_path, content, issue, lines)
        elif 'include_order' in issue_type:
            return self._create_reorder_fix(file_path, content, issue, lines)
        elif 'incorrect_include_path' in issue_type:
            return self._create_path_fix(file_path, content, issue, lines)
        elif 'include_not_found' in issue_type:
            return self._create_missing_file_fix(file_path, content, issue, lines)
            
        return None
        
    def _create_missing_include_fix(self, file_path: Path, content: str, issue: Dict[str, Any], lines: List[str]) -> IncludeFixProposal:
        """Create fix for missing include"""
        
        include_header = issue.get('fix_content', issue.get('suggestion', '').replace('Add: ', ''))
        suggested_line = self._find_best_include_position(lines)
        
        # Generate alternative suggestions
        alternatives = self._generate_alternative_includes(include_header)
        
        # Calculate confidence based on pattern matching
        confidence = self._calculate_include_confidence(content, include_header)
        
        original_code = "\\n".join(lines[:suggested_line])
        proposed_fix = "\\n".join(lines[:suggested_line] + [include_header] + lines[suggested_line:])
        
        return IncludeFixProposal(
            file_path=str(file_path),
            issue_type=issue['type'],
            severity=FixSeverity(issue['severity']),
            description=issue['description'],
            original_code=original_code,
            proposed_fix=proposed_fix,
            line_number=suggested_line + 1,
            educational_explanation=issue.get('educational_content', ''),
            safety_score=95,  # Adding includes is very safe
            context='include_management',
            auto_approvable=confidence > 0.8,
            fix_type=IncludeFixType.ADD_MISSING,
            include_header=include_header,
            suggested_line=suggested_line,
            alternative_fixes=alternatives,
            confidence_score=confidence
        )
        
    def _create_duplicate_include_fix(self, file_path: Path, content: str, issue: Dict[str, Any], lines: List[str]) -> IncludeFixProposal:
        """Create fix for duplicate include"""
        
        line_num = issue.get('line', 1) - 1
        duplicate_line = lines[line_num] if line_num < len(lines) else ""
        
        # Find the first occurrence to keep
        first_occurrence = -1
        for i, line in enumerate(lines):
            if line.strip() == duplicate_line.strip() and '#include' in line:
                first_occurrence = i
                break
                
        # Remove the duplicate
        new_lines = lines[:line_num] + lines[line_num + 1:]
        
        original_code = "\\n".join(lines)
        proposed_fix = "\\n".join(new_lines)
        
        return IncludeFixProposal(
            file_path=str(file_path),
            issue_type=issue['type'],
            severity=FixSeverity(issue['severity']),
            description=issue['description'],
            original_code=original_code,
            proposed_fix=proposed_fix,
            line_number=line_num + 1,
            educational_explanation="Removing duplicate include improves compilation time and reduces clutter.",
            safety_score=100,  # Removing duplicates is completely safe
            context='include_management',
            auto_approvable=True,
            fix_type=IncludeFixType.REMOVE_DUPLICATE,
            include_header=duplicate_line.strip(),
            suggested_line=line_num,
            alternative_fixes=[],
            confidence_score=1.0
        )
        
    def _create_reorder_fix(self, file_path: Path, content: str, issue: Dict[str, Any], lines: List[str]) -> IncludeFixProposal:
        """Create fix for include ordering"""
        
        # Extract all includes
        includes = []
        non_includes = []
        
        for i, line in enumerate(lines):
            if line.strip().startswith('#include'):
                includes.append((i, line))
            else:
                non_includes.append((i, line))
                
        # Separate system vs local includes
        system_includes = []
        local_includes = []
        
        for line_num, include_line in includes:
            if '<' in include_line and '>' in include_line:
                system_includes.append(include_line)
            else:
                local_includes.append(include_line)
                
        # Rebuild with proper order
        ordered_includes = system_includes + [''] + local_includes  # Empty line separator
        
        # Find where includes start
        first_include_line = min([i for i, _ in includes]) if includes else 0
        last_include_line = max([i for i, _ in includes]) if includes else 0
        
        # Rebuild file
        new_lines = []
        new_lines.extend(lines[:first_include_line])
        new_lines.extend(ordered_includes)
        new_lines.extend(lines[last_include_line + 1:])
        
        original_code = "\\n".join(lines)
        proposed_fix = "\\n".join(new_lines)
        
        return IncludeFixProposal(
            file_path=str(file_path),
            issue_type=issue['type'],
            severity=FixSeverity(issue['severity']),
            description=issue['description'],
            original_code=original_code,
            proposed_fix=proposed_fix,
            line_number=first_include_line + 1,
            educational_explanation="Standard practice: system headers first, then local headers.",
            safety_score=90,  # Reordering is generally safe
            context='include_management',
            auto_approvable=False,  # User should review reordering
            fix_type=IncludeFixType.REORDER_INCLUDES,
            include_header="<reorder>",
            suggested_line=first_include_line,
            alternative_fixes=[],
            confidence_score=0.9
        )
        
    def _create_path_fix(self, file_path: Path, content: str, issue: Dict[str, Any], lines: List[str]) -> IncludeFixProposal:
        """Create fix for incorrect include path"""
        
        line_num = issue.get('line', 1) - 1
        original_line = lines[line_num] if line_num < len(lines) else ""
        
        # Generate path suggestions
        alternatives = self._suggest_path_corrections(file_path, original_line)
        
        if alternatives:
            suggested_fix = alternatives[0]
            new_lines = lines.copy()
            new_lines[line_num] = suggested_fix
            
            original_code = "\\n".join(lines)
            proposed_fix = "\\n".join(new_lines)
            
            return IncludeFixProposal(
                file_path=str(file_path),
                issue_type=issue['type'],
                severity=FixSeverity(issue['severity']),
                description=issue['description'],
                original_code=original_code,
                proposed_fix=proposed_fix,
                line_number=line_num + 1,
                educational_explanation="Correcting include paths improves portability and compilation success.",
                safety_score=75,  # Path changes need verification
                context='include_management',
                auto_approvable=False,
                fix_type=IncludeFixType.FIX_PATH,
                include_header=suggested_fix,
                suggested_line=line_num,
                alternative_fixes=alternatives[1:],
                confidence_score=0.7
            )
            
        return None
        
    def _create_missing_file_fix(self, file_path: Path, content: str, issue: Dict[str, Any], lines: List[str]) -> IncludeFixProposal:
        """Create fix for missing include file"""
        
        line_num = issue.get('line', 1) - 1
        original_line = lines[line_num] if line_num < len(lines) else ""
        
        # Try to find the missing file or suggest alternatives
        missing_file = re.search(r'["\<]([^">]+)[">]', original_line)
        if missing_file:
            filename = missing_file.group(1)
            alternatives = self._find_similar_files(file_path.parent, filename)
            
            if alternatives:
                suggested_fix = original_line.replace(filename, alternatives[0])
                new_lines = lines.copy()
                new_lines[line_num] = suggested_fix
                
                original_code = "\\n".join(lines)
                proposed_fix = "\\n".join(new_lines)
                
                return IncludeFixProposal(
                    file_path=str(file_path),
                    issue_type=issue['type'],
                    severity=FixSeverity(issue['severity']),
                    description=f"Missing file: {filename}, suggested: {alternatives[0]}",
                    original_code=original_code,
                    proposed_fix=proposed_fix,
                    line_number=line_num + 1,
                    educational_explanation="Fixing missing include paths resolves compilation errors.",
                    safety_score=60,  # File path changes need careful verification
                    context='include_management',
                    auto_approvable=False,
                    fix_type=IncludeFixType.FIX_PATH,
                    include_header=suggested_fix,
                    suggested_line=line_num,
                    alternative_fixes=[original_line.replace(filename, alt) for alt in alternatives[1:5]],
                    confidence_score=0.6
                )
                
        return None
        
    def _interactive_fix_session(self, file_path: Path, content: str, proposals: List[IncludeFixProposal]) -> List[FixProposal]:
        """Run interactive fixing session"""
        
        print(f"\\n🔧 Interactive Include Fixing Session for {file_path}")
        print(f"Found {len(proposals)} include issues to fix\\n")
        
        applied_fixes = []
        modified_content = content
        
        for i, proposal in enumerate(proposals):
            print(f"\\n--- Fix {i+1}/{len(proposals)} ---")
            print(f"Type: {proposal.fix_type.value}")
            print(f"Issue: {proposal.description}")
            print(f"Confidence: {proposal.confidence_score:.1%}")
            print(f"Safety Score: {proposal.safety_score}/100")
            
            # Show diff
            self._show_diff(proposal.original_code, proposal.proposed_fix, file_path)
            
            # Show alternatives if available
            if proposal.alternative_fixes:
                print(f"\\nAlternatives:")
                for j, alt in enumerate(proposal.alternative_fixes[:3]):
                    print(f"  {j+1}. {alt}")
                    
            # Get user decision
            decision = self._get_user_decision(proposal)
            
            if decision == ApprovalDecision.APPROVE:
                # Apply the fix
                modified_content = self._apply_fix(modified_content, proposal)
                applied_fixes.append(proposal)
                print("✅ Fix applied!")
                
                # Get user feedback
                score = self._get_user_feedback(proposal)
                self._store_fix_score(proposal, score)
                
            elif decision == ApprovalDecision.REJECT:
                print("❌ Fix rejected")
                
            elif decision == ApprovalDecision.SKIP:
                print("⏭️  Fix skipped")
                
        # Offer to save changes
        if applied_fixes:
            if self._confirm_save_changes(file_path, len(applied_fixes)):
                self._save_file(file_path, modified_content)
                print(f"✅ Saved {len(applied_fixes)} fixes to {file_path}")
            else:
                print("💾 Changes not saved")
                
        return applied_fixes
        
    def _show_diff(self, original: str, proposed: str, file_path: Path):
        """Show colored diff of changes"""
        
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            proposed.splitlines(keepends=True),
            fromfile=str(file_path),
            tofile=f"{file_path} (proposed)",
            lineterm=""
        )
        
        print("\\nProposed changes:")
        for line in diff:
            if line.startswith('+++') or line.startswith('---'):
                print(f"\\033[1m{line}\\033[0m", end="")
            elif line.startswith('+'):
                print(f"\\033[92m{line}\\033[0m", end="")  # Green
            elif line.startswith('-'):
                print(f"\\033[91m{line}\\033[0m", end="")  # Red
            elif line.startswith('@@'):
                print(f"\\033[94m{line}\\033[0m", end="")  # Blue
            else:
                print(line, end="")
                
    def _get_user_decision(self, proposal: IncludeFixProposal) -> ApprovalDecision:
        """Get user decision on fix"""
        
        while True:
            try:
                options = "\\n[a]pprove, [r]eject, [s]kip"
                if proposal.alternative_fixes:
                    options += ", [1-9] use alternative"
                options += ": "
                
                choice = input(options).strip().lower()
            except (EOFError, KeyboardInterrupt):
                return ApprovalDecision.REJECT
            
            if choice in ['a', 'approve', 'y', 'yes']:
                return ApprovalDecision.APPROVE
            elif choice in ['r', 'reject', 'n', 'no']:
                return ApprovalDecision.REJECT
            elif choice in ['s', 'skip']:
                return ApprovalDecision.SKIP
            elif choice.isdigit() and proposal.alternative_fixes:
                idx = int(choice) - 1
                if 0 <= idx < len(proposal.alternative_fixes):
                    # Modify proposal to use alternative
                    proposal.include_header = proposal.alternative_fixes[idx]
                    proposal.proposed_fix = proposal.proposed_fix.replace(
                        proposal.include_header, 
                        proposal.alternative_fixes[idx]
                    )
                    return ApprovalDecision.APPROVE
                    
            print("Invalid choice. Please try again.")
            
    def _get_user_feedback(self, proposal: IncludeFixProposal) -> FixScore:
        """Get user feedback on applied fix"""
        
        print("\\n📊 How helpful was this fix?")
        while True:
            try:
                rating = int(input("Rate 1-5 stars: "))
                if 1 <= rating <= 5:
                    break
                print("Please enter a number between 1 and 5")
            except ValueError:
                print("Please enter a valid number")
            except (EOFError, KeyboardInterrupt):
                return FixScore(
                    fix_id=f"{proposal.file_path}:{proposal.line_number}:{proposal.fix_type.value}",
                    user_rating=3,
                    was_helpful=False,
                    feedback="Session interrupted"
                )
                
        try:
            helpful = input("Was this fix helpful? (y/n): ").strip().lower().startswith('y')
            feedback = input("Any additional feedback (optional): ").strip()
        except (EOFError, KeyboardInterrupt):
            helpful = False
            feedback = "Session interrupted"
        
        return FixScore(
            fix_id=f"{proposal.file_path}:{proposal.line_number}:{proposal.fix_type.value}",
            user_rating=rating,
            was_helpful=helpful,
            feedback=feedback,
            timestamp=datetime.now().isoformat(),
            context={
                'fix_type': proposal.fix_type.value,
                'confidence': proposal.confidence_score,
                'safety_score': proposal.safety_score
            }
        )
        
    def _store_fix_score(self, proposal: IncludeFixProposal, score: FixScore):
        """Store user feedback for machine learning"""
        
        # Store in memory engine for learning
        feedback_data = {
            'fix_type': proposal.fix_type.value,
            'confidence_score': proposal.confidence_score,
            'safety_score': proposal.safety_score,
            'user_rating': score.user_rating,
            'was_helpful': score.was_helpful,
            'include_header': proposal.include_header,
            'context': score.context
        }
        
        self.memory.store_memory(
            f"include_fix_feedback: {score.fix_id}",
            feedback_data
        )
        
        # Update learning models
        self._update_confidence_model(proposal, score)
        
    def _update_confidence_model(self, proposal: IncludeFixProposal, score: FixScore):
        """Update confidence scoring based on user feedback"""
        
        # Simple learning: adjust confidence for similar patterns
        if score.user_rating >= 4 and score.was_helpful:
            # Increase confidence for similar patterns
            self._boost_pattern_confidence(proposal)
        elif score.user_rating <= 2 or not score.was_helpful:
            # Decrease confidence for similar patterns
            self._reduce_pattern_confidence(proposal)
            
    def _boost_pattern_confidence(self, proposal: IncludeFixProposal):
        """Boost confidence for successful patterns"""
        pattern_key = f"successful_pattern:{proposal.fix_type.value}:{proposal.include_header}"
        existing = self.memory.search_memories(pattern_key, limit=1)
        
        boost_count = 1
        if existing:
            boost_count = existing[0].get('boost_count', 1) + 1
            
        self.memory.store_memory(pattern_key, {
            'pattern': proposal.include_header,
            'fix_type': proposal.fix_type.value,
            'boost_count': boost_count,
            'avg_rating': (existing[0].get('avg_rating', 0) * (boost_count - 1) + 5) / boost_count if existing else 5
        })
        
    def _reduce_pattern_confidence(self, proposal: IncludeFixProposal):
        """Reduce confidence for unsuccessful patterns"""
        pattern_key = f"failed_pattern:{proposal.fix_type.value}:{proposal.include_header}"
        self.memory.store_memory(pattern_key, {
            'pattern': proposal.include_header,
            'fix_type': proposal.fix_type.value,
            'failure_reason': 'user_rejected',
            'timestamp': datetime.now().isoformat()
        })
        
    # Helper methods
    def _find_best_include_position(self, lines: List[str]) -> int:
        """Find the best position to insert a new include"""
        last_include = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('#include'):
                last_include = i
        return last_include + 1 if last_include >= 0 else 0
        
    def _generate_alternative_includes(self, include_header: str) -> List[str]:
        """Generate alternative include suggestions"""
        alternatives = []
        
        if include_header.startswith('#include <') and include_header.endswith('>'):
            # Try with .h extension
            base = include_header[10:-1]  # Remove '#include <' and '>'
            alternatives.append(f'#include <{base}.h>')
            alternatives.append(f'#include "{base}"')
            alternatives.append(f'#include "{base}.h"')
            
        elif include_header.startswith('#include "') and include_header.endswith('"'):
            # Try as system header
            base = include_header[10:-1]  # Remove '#include "' and '"'
            alternatives.append(f'#include <{base}>')
            alternatives.append(f'#include <{base}.h>')
            
        return alternatives[:3]  # Limit to 3 alternatives
        
    def _calculate_include_confidence(self, content: str, include_header: str) -> float:
        """Calculate confidence for an include suggestion"""
        
        # Extract header name
        header_match = re.search(r'[<"]([^>"]+)[>"]', include_header)
        if not header_match:
            return 0.5
            
        header_name = header_match.group(1)
        base_name = header_name.split('/')[-1].replace('.h', '').replace('.hpp', '')
        
        # Check if symbols from this header are used
        symbol_patterns = {
            'iostream': [r'std::cout', r'std::cin', r'std::endl'],
            'vector': [r'std::vector'],
            'string': [r'std::string'],
            'memory': [r'std::shared_ptr', r'std::unique_ptr', r'std::make_shared'],
            'chrono': [r'std::chrono', r'steady_clock', r'system_clock'],
        }
        
        if base_name in symbol_patterns:
            pattern_count = sum(len(re.findall(pattern, content)) for pattern in symbol_patterns[base_name])
            return min(0.9, 0.3 + (pattern_count * 0.15))
            
        return 0.6  # Default confidence
        
    def _suggest_path_corrections(self, file_path: Path, include_line: str) -> List[str]:
        """Suggest path corrections for problematic includes"""
        suggestions = []
        
        # Extract current path
        path_match = re.search(r'["\<]([^">]+)[">]', include_line)
        if not path_match:
            return suggestions
            
        current_path = path_match.group(1)
        
        # Remove excessive relative paths
        if '../' in current_path:
            # Try removing some ../ levels
            parts = current_path.split('/')
            for i in range(len(parts)):
                if parts[i] != '..':
                    new_path = '/'.join(parts[i:])
                    suggestions.append(include_line.replace(current_path, new_path))
                    break
                    
        # Try converting backslashes to forward slashes
        if '\\\\' in current_path:
            fixed_path = current_path.replace('\\\\', '/')
            suggestions.append(include_line.replace(current_path, fixed_path))
            
        return suggestions[:3]
        
    def _find_similar_files(self, search_dir: Path, filename: str) -> List[str]:
        """Find files similar to the missing filename"""
        similar_files = []
        
        # Search for files with similar names
        for root, dirs, files in os.walk(search_dir):
            for file in files:
                if file.endswith(('.h', '.hpp')) and filename.lower() in file.lower():
                    rel_path = os.path.relpath(os.path.join(root, file), search_dir)
                    similar_files.append(rel_path)
                    
        return similar_files[:5]
        
    def _apply_fix(self, content: str, proposal: IncludeFixProposal) -> str:
        """Apply a fix to the content"""
        
        if proposal.fix_type == IncludeFixType.ADD_MISSING:
            lines = content.split('\\n')
            lines.insert(proposal.suggested_line, proposal.include_header)
            return '\\n'.join(lines)
            
        elif proposal.fix_type == IncludeFixType.REMOVE_DUPLICATE:
            lines = content.split('\\n')
            lines.pop(proposal.suggested_line)
            return '\\n'.join(lines)
            
        else:
            # For more complex fixes, use the proposed_fix directly
            return proposal.proposed_fix
            
    def _confirm_save_changes(self, file_path: Path, num_fixes: int) -> bool:
        """Confirm saving changes to file"""
        try:
            response = input(f"\\nSave {num_fixes} fixes to {file_path}? (y/n): ").strip().lower()
            return response.startswith('y')
        except (EOFError, KeyboardInterrupt):
            return False
        
    def _save_file(self, file_path: Path, content: str):
        """Save content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Failed to save {file_path}: {e}")

# CLI interface
def main():
    """CLI interface for interactive include fixing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Include Error Fixer")
    parser.add_argument("file_or_dir", help="File or directory to analyze")
    parser.add_argument("--auto", action="store_true", help="Auto-approve safe fixes")
    parser.add_argument("--dry-run", action="store_true", help="Show fixes without applying")
    
    args = parser.parse_args()
    
    fixer = InteractiveIncludeFixer()
    
    target_path = Path(args.file_or_dir)
    if target_path.is_file():
        fixer.analyze_and_fix_file(target_path, interactive=not args.auto)
    elif target_path.is_dir():
        # Process all C++ files in directory
        cpp_files = list(target_path.rglob("*.cpp")) + list(target_path.rglob("*.h")) + list(target_path.rglob("*.hpp"))
        
        for cpp_file in cpp_files:
            print(f"\\n{'='*60}")
            fixer.analyze_and_fix_file(cpp_file, interactive=not args.auto)
    else:
        logger.error(f"Path not found: {target_path}")

if __name__ == "__main__":
    main()