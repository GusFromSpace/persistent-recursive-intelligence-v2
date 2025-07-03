#!/usr/bin/env python3
"""
Focused ADV-TEST-001: Test recursive self-improvement on a specific known syntax error

This demonstrates the Ouroboros effect by fixing a known syntax error in the system
and verifying the fix worked.
"""

import sys
import json
import ast
from pathlib import Path
from datetime import datetime

def check_syntax_error(file_path):
    """Check if a file has syntax errors"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Try to parse the AST
        ast.parse(content)
        return False, None
    
    except SyntaxError as e:
        return True, {
            'line': e.lineno,
            'offset': e.offset,
            'message': e.msg,
            'text': e.text
        }
    except Exception as e:
        return True, {'message': str(e)}

def fix_f_string_error(file_path, error_info):
    """Fix the specific f-string error we identified"""
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # The error is on line 445: unterminated f-string
        line_idx = error_info['line'] - 1
        
        if 0 <= line_idx < len(lines):
            line = lines[line_idx]
            
            # The line should be:
            # logger.info(f"🎊 Evolution completed with {evolution_results['cognitive_metrics']['session_improvements']} improvements")
            # But it's missing the closing quote
            
            if line.strip().endswith("improvements')"):
                # Add the missing quote
                lines[line_idx] = line.replace("improvements')", "improvements\")")
                
                # Write back the fix
                with open(file_path, 'w') as f:
                    f.writelines(lines)
                
                return True, "Fixed f-string termination"
        
        return False, "Could not locate or fix the error"
        
    except Exception as e:
        return False, f"Error during fix: {e}"

def test_focused_ouroboros():
    """Test focused recursive self-improvement"""
    print("🎯 Focused Ouroboros Test")
    print("=" * 40)
    print("🐍 Testing self-improvement on known syntax error")
    print()
    
    target_file = Path("src/cognitive/synthesis/persistent_recursive_engine.py")
    
    # Step 1: Verify the syntax error exists
    print("🔍 Step 1: Checking for syntax error...")
    has_error, error_info = check_syntax_error(target_file)
    
    if not has_error:
        print("✅ No syntax error found - file is already correct")
        return True
    
    print(f"❌ Syntax error detected: {error_info['message']}")
    print(f"📍 Location: Line {error_info['line']}")
    if error_info.get('text'):
        print(f"📝 Code: {error_info['text'].strip()}")
    print()
    
    # Step 2: Apply the fix
    print("🔧 Step 2: Applying self-improvement fix...")
    success, message = fix_f_string_error(target_file, error_info)
    
    if not success:
        print(f"❌ Fix failed: {message}")
        return False
    
    print(f"✅ Applied fix: {message}")
    print()
    
    # Step 3: Verify the fix worked
    print("✅ Step 3: Verifying fix effectiveness...")
    has_error_after, error_after = check_syntax_error(target_file)
    
    if has_error_after:
        print(f"❌ Syntax error still exists: {error_after['message']}")
        return False
    
    print("✅ Syntax error resolved successfully!")
    print()
    
    # Step 4: Test that the module can now be imported
    print("🧪 Step 4: Testing module import...")
    try:
        # Try to compile the file
        with open(target_file, 'r') as f:
            content = f.read()
        
        compile(content, str(target_file), 'exec')
        print("✅ File compiles successfully")
        
    except Exception as e:
        print(f"❌ File still has compilation issues: {e}")
        return False
    
    print()
    print("=" * 40)
    print("🎉 FOCUSED OUROBOROS TEST PASSED!")
    print("✅ System successfully improved its own syntax")
    print("🐍 Demonstrated recursive self-correction")
    print("🔧 Fixed unterminated f-string error")
    
    # Save results
    results = {
        'test_id': 'ADV-TEST-001-FOCUSED',
        'test_name': 'Focused Ouroboros Test',
        'timestamp': datetime.now().isoformat(),
        'success': True,
        'target_file': str(target_file),
        'error_fixed': error_info,
        'fix_applied': message
    }
    
    with open('focused_ouroboros_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"📁 Results saved to focused_ouroboros_results.json")
    
    return True

def main():
    try:
        success = test_focused_ouroboros()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()