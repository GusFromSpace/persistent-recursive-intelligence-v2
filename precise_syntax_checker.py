#!/usr/bin/env python3
"""
Precise syntax checker for PRI - identifies exact locations of syntax errors.
This tool provides surgical precision in finding and diagnosing syntax issues.
"""

import ast
import re
from typing import List, Dict


def find_unclosed_quotes(content: str) -> List[Dict]:
    """Find unclosed triple quotes with precise line numbers."""
    issues = []
    lines = content.split('\n')

    in_triple_quote = False
    quote_type = None
    quote_start_line = None

    for line_num, line in enumerate(lines, 1):
        # Find all triple quotes in this line
        triple_quotes = []

        # Find """ quotes
        for match in re.finditer(r'"""', line):
            triple_quotes.append((match.start(), '"""', line_num))

        # Find ''' quotes
        for match in re.finditer(r"'''", line):
            triple_quotes.append((match.start(), "'''", line_num))

        # Sort by position in line
        triple_quotes.sort()

        for pos, quote, line_no in triple_quotes:
            if not in_triple_quote:
                # Starting a new triple quote
                in_triple_quote = True
                quote_type = quote
                quote_start_line = line_no
            elif quote == quote_type:
                # Closing the triple quote
                in_triple_quote = False
                quote_type = None
                quote_start_line = None

    # If we're still in a triple quote at the end, it's unclosed
    if in_triple_quote and quote_start_line:
        issues.append({
            'type': 'unclosed_triple_quote',
            'line': quote_start_line,
            'quote_type': quote_type,
            'message': f'Unclosed {quote_type} starting at line {quote_start_line}',
            'suggestion': f'Add closing {quote_type} after the intended end of the string'
        })

    return issues

def find_problematic_docstrings(content: str) -> List[Dict]:
    """Find docstrings that might be causing issues."""
    issues = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):

        # Look for function/method definitions followed by docstrings
        if re.match(r'^\s*def\s+\w+.*:', line):
            # Check the next few lines for docstring patterns
            for offset in range(1, 4):
                if line_num + offset <= len(lines):
                    next_line = lines[line_num + offset - 1].strip()
                    if next_line.startswith('"""') and not next_line.endswith('"""'):
                        # Single line docstring that might be unclosed
                        if next_line.count('"""') == 1:
                            issues.append({
                                'type': 'potential_unclosed_docstring',
                                'line': line_num + offset,
                                'message': f'Potential unclosed docstring at line {line_num + offset}',
                                'suggestion': f'Ensure docstring is properly closed with """ on the same line or on a separate line',
                                'content': next_line
                            })

    return issues

def analyze_syntax_error(file_path: str) -> Dict:
    """Analyze a file for syntax errors with precise diagnostics."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to parse the file
        try:
            ast.parse(content)
            return {
                'status': 'valid',
                'message': 'No syntax errors found'
            }
        except SyntaxError as e:
            # Get detailed error information
            error_info = {
                'status': 'error',
                'error_type': 'SyntaxError',
                'line': e.lineno,
                'column': e.offset,
                'message': str(e),
                'text': e.text.strip() if e.text else None
            }

            # Run our specific diagnostics
            quote_issues = find_unclosed_quotes(content)
            docstring_issues = find_problematic_docstrings(content)

            # Combine all findings
            error_info.update({
                'quote_issues': quote_issues,
                'docstring_issues': docstring_issues,
                'recommendations': []
            })

            # Generate specific recommendations
            if quote_issues:
                for issue in quote_issues:
                    error_info['recommendations'].append(
                        f"Fix unclosed {issue['quote_type']} at line {issue['line']}"
                    )

            if docstring_issues:
                for issue in docstring_issues:
                    error_info['recommendations'].append(
                        f"Check docstring at line {issue['line']}: {issue['content']}"
                    )

            return error_info

    except Exception as e:
        return {
            'status': 'error',
            'error_type': 'FileError',
            'message': f'Could not analyze file: {e}'
        }

def print_analysis(analysis: Dict, file_path: str):
    """Print detailed analysis results."""
    logger.info(f"\n🔍 PRECISE SYNTAX ANALYSIS: {file_path}")
    logger.info("=" * 60)

    if analysis['status'] == 'valid':
        logger.info("✅ No syntax errors found")
        return

    logger.info(f"❌ {analysis['error_type']}: {analysis['message']}")

    if 'line' in analysis:
        logger.info(f"📍 Location: Line {analysis['line']}")
        if analysis.get('column'):
            logger.info(f"📍 Column: {analysis['column']}")
        if analysis.get('text'):
            logger.info(f"📝 Problem text: {analysis['text']}")

    if analysis.get('quote_issues'):
        logger.info(f"\n🔤 Triple Quote Issues:")
        for issue in analysis['quote_issues']:
            logger.info(f"   • Line {issue['line']}: {issue['message']}")
            logger.info(f"     💡 {issue['suggestion']}")

    if analysis.get('docstring_issues'):
        logger.info(f"\n📚 Docstring Issues:")
        for issue in analysis['docstring_issues']:
            logger.info(f"   • Line {issue['line']}: {issue['message']}")
            logger.info(f"     Content: {issue['content']}")
            logger.info(f"     💡 {issue['suggestion']}")

    if analysis.get('recommendations'):
        logger.info(f"\n🎯 Specific Recommendations:")
        for i, rec in enumerate(analysis['recommendations'], 1):
            logger.info(f"   {i}. {rec}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logger.info("Usage: python precise_syntax_checker.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    analysis = analyze_syntax_error(file_path)
    print_analysis(analysis, file_path)