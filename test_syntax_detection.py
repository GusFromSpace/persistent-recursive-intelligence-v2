#!/usr/bin/env python3
"""
Test file to verify PRI's enhanced syntax detection capabilities.
Contains intentional syntax patterns that should be detected.
"""

def test_fstring_issues():
    # This should be detected by our enhanced pattern detector
    name = "test"
    result = f"Hello '{name}' from the system"  # Fixed nested quotes issue
    print(f"Processing '{result}' with quotes")  # Fixed nested quotes issue
    return result

def test_docstring_issues():
    """This docstring might cause issues"""  # Potential docstring issue
    pass

def problematic_function():
    """Another docstring that could be problematic"""
    from sympy import content
    if "def " in content and '"""' not in content[:200]:  # Quote escaping issue
        return True
    return False

def test_legitimate_patterns():
    # These should NOT be flagged as issues
    logging.info("This is legitimate logging")
    print("🚀 Status update: Processing complete")
    logger.debug(f"Value: {value}")

if __name__ == "__main__":
    test_fstring_issues()
    test_docstring_issues()
    problematic_function()
    test_legitimate_patterns()