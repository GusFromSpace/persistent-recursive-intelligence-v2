#!/usr/bin/env python3
"""
Advanced Syntax Error Fixer for PRI
Specifically designed to fix the syntax damage in mesopredator_v2.py and other files
"""

import ast
import re
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedSyntaxFixer:
    def __init__(self):
        self.fixed_files = []
        self.failed_files = []
        
    def get_syntax_errors(self, directory='.'):
        """Get all files with syntax errors"""
        project_root = Path(directory)
        errors = []
        
        for py_file in project_root.rglob('*.py'):
            if any(excluded in str(py_file) for excluded in ['.git', '__pycache__', 'venv', '.venv']):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                try:
                    ast.parse(content)
                except SyntaxError as e:
                    errors.append({
                        'file': py_file,
                        'line': e.lineno,
                        'column': e.offset,
                        'error': e.msg,
                        'content': content,
                        'text': e.text
                    })
            except Exception as ex:
                logger.warning(f"Could not read {py_file}: {ex}")
                continue
        
        return errors

    def fix_unterminated_f_string_advanced(self, content, line_num, error_text):
        """Advanced f-string fixing with multi-line support"""
        lines = content.split('\n')
        
        # Find the problematic line
        if line_num > len(lines):
            return content, False
            
        # Start from the error line and work backwards to find the f-string start
        current_line = line_num - 1
        f_string_content = ""
        
        # Look for the f-string pattern
        while current_line >= 0:
            line = lines[current_line]
            
            # Check if this line contains an f-string start
            f_match = re.search(r'f["\']', line)
            if f_match:
                # Found the start of the f-string
                # Count quotes to see if it's balanced
                quote_char = line[f_match.end()-1]
                
                # Reconstruct the f-string from start to error line
                full_f_string = ""
                for i in range(current_line, line_num):
                    if i < len(lines):
                        full_f_string += lines[i] + ("\n" if i < line_num - 1 else "")
                
                # Try to balance the quotes
                quote_count = full_f_string.count(quote_char)
                
                if quote_count % 2 == 1:
                    # Odd number of quotes - need to close
                    lines[line_num - 1] += quote_char
                    return '\n'.join(lines), True
                break
                
            current_line -= 1
        
        # Fallback: just add a quote at the end of the error line
        if line_num <= len(lines):
            line = lines[line_num - 1]
            if 'f"' in line and line.count('"') % 2 == 1:
                lines[line_num - 1] = line + '"'
                return '\n'.join(lines), True
            elif "f'" in line and line.count("'") % 2 == 1:
                lines[line_num - 1] = line + "'"
                return '\n'.join(lines), True
        
        return content, False

    def fix_missing_class_body(self, content, line_num):
        """Fix missing class body by adding pass statement"""
        lines = content.split('\n')
        
        # Look for class definition line
        if line_num > len(lines):
            return content, False
            
        # Find the class line (might be before the error line)
        class_line_idx = None
        for i in range(max(0, line_num - 3), min(len(lines), line_num + 1)):
            if i < len(lines) and re.match(r'\s*class\s+\w+.*:', lines[i]):
                class_line_idx = i
                break
        
        if class_line_idx is not None:
            # Get the indentation of the class
            class_line = lines[class_line_idx]
            class_indent = len(class_line) - len(class_line.lstrip())
            body_indent = class_indent + 4
            
            # Insert pass statement after class definition
            lines.insert(class_line_idx + 1, ' ' * body_indent + 'pass')
            return '\n'.join(lines), True
        
        return content, False

    def fix_unexpected_indent(self, content, line_num):
        """Fix unexpected indentation"""
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content, False
            
        problem_line = lines[line_num - 1]
        
        # Try to find the correct indentation level
        # Look at previous non-empty lines
        correct_indent = 0
        for i in range(line_num - 2, -1, -1):
            if i >= 0 and lines[i].strip():
                prev_line = lines[i]
                prev_indent = len(prev_line) - len(prev_line.lstrip())
                
                # If previous line ends with colon, this should be indented more
                if prev_line.rstrip().endswith(':'):
                    correct_indent = prev_indent + 4
                else:
                    correct_indent = prev_indent
                break
        
        # Apply the correct indentation
        stripped_line = problem_line.lstrip()
        lines[line_num - 1] = ' ' * correct_indent + stripped_line
        
        return '\n'.join(lines), True

    def fix_invalid_syntax_comma(self, content, line_num, error_text):
        """Fix invalid syntax where comma might be missing"""
        lines = content.split('\n')
        
        if line_num > len(lines):
            return content, False
            
        # Look at the error line and see if we can intelligently add a comma
        line = lines[line_num - 1]
        
        # Common patterns where comma is missing
        # Pattern 1: After a string or number before another value
        if re.search(r'["\'][\w\s]*["\'][\s]*[\w"\'(]', line):
            # Insert comma after the string
            line = re.sub(r'(["\'][\w\s]*["\'])(\s*)([\w"\'(])', r'\1,\2\3', line)
            lines[line_num - 1] = line
            return '\n'.join(lines), True
        
        # Pattern 2: In function calls or lists
        if '(' in line or '[' in line:
            # Try adding comma before closing bracket/paren
            if ')' in line and not line.rstrip().endswith(','):
                line = line.replace(')', ',)')
                lines[line_num - 1] = line
                return '\n'.join(lines), True
        
        return content, False

    def fix_syntax_error(self, error_info):
        """Main fix dispatcher"""
        content = error_info['content']
        line_num = error_info['line']
        error_msg = error_info['error']
        error_text = error_info.get('text', '')
        
        logger.info(f"Attempting to fix: {error_msg} at line {line_num}")
        
        # Try different fix strategies based on error message
        if 'unterminated f-string literal' in error_msg:
            return self.fix_unterminated_f_string_advanced(content, line_num, error_text)
        elif 'unterminated string literal' in error_msg:
            return self.fix_unterminated_f_string_advanced(content, line_num, error_text)
        elif 'expected an indented block' in error_msg:
            return self.fix_missing_class_body(content, line_num)
        elif 'unexpected indent' in error_msg:
            return self.fix_unexpected_indent(content, line_num)
        elif 'invalid syntax. Perhaps you forgot a comma' in error_msg:
            return self.fix_invalid_syntax_comma(content, line_num, error_text)
        else:
            logger.warning(f"No fix strategy for: {error_msg}")
            return content, False

    def fix_file(self, file_path, dry_run=False):
        """Fix all syntax errors in a single file"""
        logger.info(f"Processing file: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
        except Exception as e:
            logger.error(f"Could not read {file_path}: {e}")
            return False
        
        # Create backup
        if not dry_run:
            backup_path = file_path.with_suffix(file_path.suffix + '.backup.advanced')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            logger.info(f"Created backup: {backup_path}")
        
        content = original_content
        max_attempts = 10  # Prevent infinite loops
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            
            # Check for syntax errors
            try:
                ast.parse(content)
                # No syntax errors - we're done!
                if content != original_content:
                    if not dry_run:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        logger.info(f"✅ Fixed {file_path} after {attempt} attempts")
                        self.fixed_files.append(str(file_path))
                    else:
                        logger.info(f"✅ Would fix {file_path} (dry run)")
                    return True
                else:
                    logger.info(f"✅ {file_path} already valid")
                    return True
                    
            except SyntaxError as e:
                # Still has syntax errors, try to fix
                error_info = {
                    'file': file_path,
                    'line': e.lineno,
                    'column': e.offset,
                    'error': e.msg,
                    'content': content,
                    'text': e.text
                }
                
                logger.info(f"Attempt {attempt}: {e.msg} at line {e.lineno}")
                
                new_content, fixed = self.fix_syntax_error(error_info)
                
                if fixed and new_content != content:
                    content = new_content
                    logger.info(f"Applied fix for: {e.msg}")
                else:
                    logger.warning(f"Could not fix: {e.msg}")
                    break
        
        # If we get here, we couldn't fix all errors
        logger.error(f"❌ Could not fix all syntax errors in {file_path}")
        self.failed_files.append(str(file_path))
        return False

    def fix_project(self, directory='.', dry_run=False, target_file=None):
        """Fix all syntax errors in the project"""
        logger.info(f"🔧 Advanced Syntax Fixer - {'DRY RUN' if dry_run else 'LIVE MODE'}")
        logger.info("=" * 60)
        
        if target_file:
            # Fix only the specified file
            target_path = Path(target_file)
            if target_path.exists():
                self.fix_file(target_path, dry_run)
            else:
                logger.error(f"Target file not found: {target_file}")
        else:
            # Find all files with syntax errors
            errors = self.get_syntax_errors(directory)
            error_files = list(set(error['file'] for error in errors))
            
            logger.info(f"Found {len(error_files)} files with syntax errors")
            
            for file_path in error_files:
                self.fix_file(file_path, dry_run)
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.info(f"📊 Summary:")
        logger.info(f"   ✅ Fixed: {len(self.fixed_files)} files")
        logger.info(f"   ❌ Failed: {len(self.failed_files)} files")
        
        if self.fixed_files:
            logger.info("\n✅ Successfully fixed:")
            for file_path in self.fixed_files:
                logger.info(f"   - {file_path}")
        
        if self.failed_files:
            logger.info("\n❌ Could not fix:")
            for file_path in self.failed_files:
                logger.info(f"   - {file_path}")
        
        # Final verification
        if not dry_run:
            remaining_errors = self.get_syntax_errors(directory)
            if target_file:
                # Filter to only the target file
                remaining_errors = [e for e in remaining_errors if str(e['file']) == target_file]
            
            logger.info(f"\n🔍 Remaining syntax errors: {len(remaining_errors)}")
            
            if remaining_errors and len(remaining_errors) < 5:
                logger.info("Remaining errors:")
                for error in remaining_errors:
                    logger.info(f"   {error['file']}:{error['line']} - {error['error']}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Syntax Error Fixer for PRI")
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--file', type=str, help='Fix only the specified file')
    parser.add_argument('--directory', type=str, default='.', help='Directory to scan (default: current)')
    
    args = parser.parse_args()
    
    fixer = AdvancedSyntaxFixer()
    fixer.fix_project(args.directory, args.dry_run, args.file)

if __name__ == "__main__":
    main()