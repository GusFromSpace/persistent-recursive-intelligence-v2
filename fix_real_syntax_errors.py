#!/usr/bin/env python3
"""
Focused Real Syntax Error Fixer
Only fixes actual Python syntax errors detected by AST parsing
"""

import ast
from pathlib import Path

def get_real_syntax_errors():
    """Get only real syntax errors that prevent Python parsing"""
    project_root = Path('.')
    real_errors = []
    
    for py_file in project_root.rglob('*.py'):
        if any(excluded in str(py_file) for excluded in ['.git', '__pycache__', 'venv', '.venv']):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            try:
                ast.parse(content)
            except SyntaxError as e:
                real_errors.append({
                    'file': py_file,
                    'line': e.lineno,
                    'error': e.msg,
                    'content': content
                })
        except Exception:
            continue
    
    return real_errors

def fix_unterminated_f_string(content, line_num):
    """Fix unterminated f-string by adding missing closing quote"""
    lines = content.split('\n')
    if line_num <= len(lines):
        line = lines[line_num - 1]
        
        # Look for unclosed f-strings
        if 'f"' in line and line.count('"') % 2 == 1:
            # Add missing closing quote
            lines[line_num - 1] = line + '"'
            return '\n'.join(lines), True
    
    return content, False

def fix_unterminated_string(content, line_num):
    """Fix unterminated regular string"""
    lines = content.split('\n')
    if line_num <= len(lines):
        line = lines[line_num - 1]
        
        # Look for unclosed strings
        if line.count('"') % 2 == 1 or line.count("'") % 2 == 1:
            # Try to intelligently close the string
            if '"' in line and line.count('"') % 2 == 1:
                lines[line_num - 1] = line + '"'
            elif "'" in line and line.count("'") % 2 == 1:
                lines[line_num - 1] = line + "'"
            return '\n'.join(lines), True
    
    return content, False

def fix_missing_indent(content, line_num):
    """Fix missing indentation after class definition"""
    lines = content.split('\n')
    if line_num <= len(lines):
        lines[line_num - 1] = '    pass'  # Add simple pass statement
        return '\n'.join(lines), True
    
    return content, False

def fix_syntax_error(error_info):
    """Fix a specific syntax error"""
    content = error_info['content']
    line_num = error_info['line']
    error_msg = error_info['error']
    
    if 'unterminated f-string literal' in error_msg:
        return fix_unterminated_f_string(content, line_num)
    elif 'unterminated string literal' in error_msg:
        return fix_unterminated_string(content, line_num)
    elif 'expected an indented block' in error_msg:
        return fix_missing_indent(content, line_num)
    elif 'invalid syntax. Perhaps you forgot a comma' in error_msg:
        # More complex - need manual inspection
        return content, False
    elif 'unexpected indent' in error_msg:
        # Fix by removing extra indentation
        lines = content.split('\n')
        if line_num <= len(lines):
            lines[line_num - 1] = lines[line_num - 1].lstrip()
            return '\n'.join(lines), True
    
    return content, False

def main():
    logger.info("🔧 Real Syntax Error Fixer")
    logger.info("=" * 40)
    
    errors = get_real_syntax_errors()
    logger.info(f"Found {len(errors)} real syntax errors")
    
    fixed_count = 0
    for error in errors:
        file_path = error['file']
        logger.info(f"\n🔍 Fixing {file_path}:{error['line']} - {error['error']}")
        
        # Create backup
        backup_path = file_path.with_suffix(file_path.suffix + '.backup.syntax')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(error['content'])
        
        # Attempt fix
        fixed_content, success = fix_syntax_error(error)
        
        if success:
            # Verify the fix works
            try:
                ast.parse(fixed_content)
                # Write the fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                logger.info(f"  ✅ Fixed successfully")
                fixed_count += 1
            except SyntaxError:
                logger.info(f"  ❌ Fix failed validation")
        else:
            logger.info(f"  ⏭️  Manual fix required")
    
    logger.info(f"\n🎉 Fixed {fixed_count}/{len(errors)} syntax errors")
    logger.info("💾 Backups created with .backup.syntax extension")
    
    # Verify final state
    remaining_errors = get_real_syntax_errors()
    logger.info(f"🔍 Remaining syntax errors: {len(remaining_errors)}")

if __name__ == "__main__":
    main()