#!/usr/bin/env python3
"""
Critical F-String Fixer
Targets the most common critical issues: f-strings with nested double quotes
"""

import re
from pathlib import Path
from typing import Tuple

def fix_nested_double_quotes_in_fstring(content: str) -> Tuple[str, int]:
    """Fix f-strings with nested double quotes by converting inner quotes to single quotes"""
    
    # Pattern to match f-strings with nested double quotes
    # This catches patterns like: f"... {dict['key']} ..."
    pattern = r'f"([^"]*?)\{([^}]*?)\"([^"]*?)\"([^}]*?)\}([^"]*?)"'
    
    fixes_made = 0
    
    def replace_nested_quotes(match):
        nonlocal fixes_made
        fixes_made += 1
        # Convert inner double quotes to single quotes
        prefix = match.group(1)
        before_first_quote = match.group(2)
        content_in_quotes = match.group(3)
        after_last_quote = match.group(4)
        suffix = match.group(5)
        
        # Reconstruct with single quotes
        return f'f"{prefix}{{{before_first_quote}\'{content_in_quotes}\'{after_last_quote}}}{suffix}"'
    
    # Apply the fix
    fixed_content = re.sub(pattern, replace_nested_quotes, content)
    
    # Handle more complex cases with multiple nested quotes
    # Pattern for cases like: f"... {obj['key']['subkey']} ...'
    complex_pattern = r'f"([^"]*?)\{([^}]*?)\"([^"]*?)\"([^}]*?)\"([^"]*?)\"([^}]*?)\}([^"]*?)"'
    
    def replace_complex_nested_quotes(match):
        nonlocal fixes_made
        fixes_made += 1
        # Convert all inner double quotes to single quotes
        prefix = match.group(1)
        part1 = match.group(2)
        quote1 = match.group(3)
        part2 = match.group(4)
        quote2 = match.group(5)
        part3 = match.group(6)
        suffix = match.group(7)
        
        return f'f"{prefix}{{{part1}\'{quote1}\'{part2}\'{quote2}\'{part3}}}{suffix}"'
    
    fixed_content = re.sub(complex_pattern, replace_complex_nested_quotes, fixed_content)
    
    return fixed_content, fixes_made

def fix_file(file_path: Path) -> Tuple[bool, int]:
    """Fix f-string issues in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        fixed_content, fixes_made = fix_nested_double_quotes_in_fstring(original_content)
        
        if fixes_made > 0:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup.fstring')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Write fixed content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            logger.info(f"✅ Fixed {fixes_made} f-string issues in {file_path}")
            return True, fixes_made
        
        return False, 0
        
    except Exception as e:
        logger.info(f"❌ Error fixing {file_path}: {e}")
        return False, 0

def find_and_fix_critical_fstring_issues(project_path: str) -> None:
    """Find and fix critical f-string issues across the project"""
    project_root = Path(project_path)
    total_fixes = 0
    files_fixed = 0
    
    logger.info("🔧 Critical F-String Fixer")
    logger.info("=" * 40)
    logger.info("Targeting f-strings with nested double quotes...")
    
    for py_file in project_root.rglob('*.py'):
        # Skip venv and cache directories
        if any(part in str(py_file) for part in ['venv', '__pycache__', '.git']):
            continue
            
        file_fixed, fixes_count = fix_file(py_file)
        if file_fixed:
            files_fixed += 1
            total_fixes += fixes_count
    
    logger.info(f"\n🎉 Critical F-String Fix Complete!")
    logger.info(f"📊 Files fixed: {files_fixed}")
    logger.info(f"📊 Total fixes: {total_fixes}")
    
    if total_fixes > 0:
        logger.info(f"💾 Backups created with .backup.fstring extension")
        logger.info(f"🌀 Re-run Mesopredator analysis to verify improvements!")

if __name__ == "__main__":
    find_and_fix_critical_fstring_issues('.')