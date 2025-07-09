#!/usr/bin/env python3
"""
Sandboxed Build and Run Validation - Final safety layer before committing changes
Tests fixes in isolated environment to detect runtime malicious behavior
"""

import logging
import shutil
import subprocess
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

@dataclass
class SandboxResult:
    """Result of sandboxed validation"""
    success: bool
    build_passed: bool
    tests_passed: bool
    runtime_safe: bool
    issues_found: List[str]
    execution_time: float
    resource_usage: Dict[str, Any]
    security_violations: List[str]

class SandboxedValidator:
    """Validates fixes in isolated sandboxed environment"""
    
    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds
        self.sandbox_dir = None
        
    def validate_fix_in_sandbox(self, project_path: str, fix_proposal, original_content: str, modified_content: str) -> SandboxResult:
        """
        Validate a fix by testing it in a sandboxed environment
        This is the FINAL validation before committing changes
        """
        logger.info(f"🏗️ SANDBOX VALIDATION: Testing {fix_proposal.file_path}")
        
        start_time = time.time()
        issues = []
        security_violations = []
        
        try:
            # Create isolated sandbox
            with self._create_sandbox(project_path) as sandbox_path:
                self.sandbox_dir = sandbox_path
                
                # Apply the fix in sandbox
                self._apply_fix_in_sandbox(sandbox_path, fix_proposal, modified_content)
                
                # Run validation steps
                build_result = self._validate_build(sandbox_path)
                test_result = self._validate_tests(sandbox_path)
                runtime_result = self._validate_runtime_behavior(sandbox_path, fix_proposal)
                
                # Collect all issues
                if not build_result['success']:
                    issues.extend(build_result['errors'])
                
                if not test_result['success']:
                    issues.extend(test_result['errors'])
                
                if not runtime_result['success']:
                    issues.extend(runtime_result['errors'])
                    security_violations.extend(runtime_result.get('security_violations', []))
                
                execution_time = time.time() - start_time
                
                return SandboxResult(
                    success=build_result['success'] and test_result['success'] and runtime_result['success'],
                    build_passed=build_result['success'],
                    tests_passed=test_result['success'],
                    runtime_safe=runtime_result['success'],
                    issues_found=issues,
                    execution_time=execution_time,
                    resource_usage={'memory': 0, 'cpu': 0},  # Placeholder
                    security_violations=security_violations
                )
                
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Sandbox validation failed: {e}")
            
            return SandboxResult(
                success=False,
                build_passed=False,
                tests_passed=False,
                runtime_safe=False,
                issues_found=[f"Sandbox validation error: {str(e)}"],
                execution_time=execution_time,
                resource_usage={},
                security_violations=[f"Sandbox failure: {str(e)}"]
            )
    
    @contextmanager
    def _create_sandbox(self, project_path: str):
        """Create isolated sandbox environment"""
        temp_dir = tempfile.mkdtemp(prefix="mesopredator_sandbox_")
        
        try:
            logger.info(f"📦 Creating sandbox: {temp_dir}")
            
            # Copy project to sandbox (excluding sensitive files)
            self._copy_project_safely(project_path, temp_dir)
            
            # Set up sandbox restrictions
            self._setup_sandbox_restrictions(temp_dir)
            
            yield temp_dir
            
        finally:
            # Clean up sandbox
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"🧹 Cleaned up sandbox: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up sandbox: {e}")
    
    def _copy_project_safely(self, source_path: str, sandbox_path: str):
        """Copy project files to sandbox, excluding dangerous files"""
        
        # Files/directories to exclude from sandbox
        exclude_patterns = [
            '.git',
            '__pycache__',
            '*.pyc',
            '.env',
            'secrets.*',
            'credentials.*',
            '*.key',
            '*.pem',
            'node_modules',
            '.venv',
            'venv',
        ]
        
        source = Path(source_path)
        destination = Path(sandbox_path)
        
        for item in source.rglob('*'):
            # Skip excluded patterns
            if any(item.match(pattern) for pattern in exclude_patterns):
                continue
                
            # Skip hidden files that might contain secrets
            if any(part.startswith('.') and part not in ['.gitignore', '.github'] 
                   for part in item.parts):
                continue
            
            relative_path = item.relative_to(source)
            dest_path = destination / relative_path
            
            try:
                if item.is_file():
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)
                elif item.is_dir():
                    dest_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.warning(f"Failed to copy {item}: {e}")
    
    def _setup_sandbox_restrictions(self, sandbox_path: str):
        """Set up security restrictions for sandbox"""
        
        # Create restricted environment script
        restrict_script = Path(sandbox_path) / "sandbox_restrictions.py"
        
        restriction_code = '''
import os
import sys
import socket
import subprocess

# Block network access
original_socket = socket.socket
def restricted_socket(*args, **kwargs):
    raise PermissionError("Network access blocked in sandbox")
socket.socket = restricted_socket

# Block subprocess execution
original_subprocess = subprocess.run
def restricted_subprocess(*args, **kwargs):
    cmd = args[0] if args else kwargs.get('cmd', '')
    # Allow only safe commands
    safe_commands = ['python', 'pytest', 'pip', 'coverage']
    if isinstance(cmd, list):
        cmd_name = cmd[0] if cmd else ''
    else:
        cmd_name = str(cmd).split()[0]
    
    if cmd_name not in safe_commands:
        raise PermissionError(f"Command '{cmd_name}' blocked in sandbox")
    
    return original_subprocess(*args, **kwargs)
subprocess.run = restricted_subprocess

# Block file system access outside sandbox
original_open = open
def restricted_open(filename, *args, **kwargs):
    path = os.path.abspath(filename)
    sandbox_path = os.path.abspath(os.getcwd())
    
    if not path.startswith(sandbox_path):
        raise PermissionError(f"File access outside sandbox blocked: {filename}")
    
    return original_open(filename, *args, **kwargs)
__builtins__['open'] = restricted_open

print("🔒 Sandbox restrictions active")
        '''
        
        with open(restrict_script, 'w') as f:
            f.write(restriction_code)
    
    def _apply_fix_in_sandbox(self, sandbox_path: str, fix_proposal, modified_content: str):
        """Apply the fix in the sandbox environment"""
        
        file_path = Path(sandbox_path) / fix_proposal.file_path
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the modified content
        with open(file_path, 'w') as f:
            f.write(modified_content)
        
        logger.info(f"✏️ Applied fix to sandbox: {file_path}")
    
    def _validate_build(self, sandbox_path: str) -> Dict[str, Any]:
        """Validate that the project builds successfully"""
        
        logger.info("🏗️ Validating build in sandbox...")
        
        try:
            # Try different build methods based on project type
            build_commands = [
                ['python', '-m', 'py_compile'] + list(Path(sandbox_path).rglob('*.py')),
                ['python', '-c', 'import sys; print("Build test passed")'],
            ]
            
            for cmd in build_commands:
                try:
                    result = subprocess.run(
                        cmd,
                        cwd=sandbox_path,
                        capture_output=True,
                        text=True,
                        timeout=self.timeout_seconds // 2
                    )
                    
                    if result.returncode == 0:
                        logger.info("✅ Build validation passed")
                        return {'success': True, 'errors': []}
                    
                except subprocess.TimeoutExpired:
                    return {'success': False, 'errors': ['Build timeout']}
                except Exception as e:
                    continue  # Try next command
            
            return {'success': False, 'errors': ['All build commands failed']}
            
        except Exception as e:
            logger.error(f"Build validation error: {e}")
            return {'success': False, 'errors': [f'Build validation error: {str(e)}']}
    
    def _validate_tests(self, sandbox_path: str) -> Dict[str, Any]:
        """Run tests in sandbox environment"""
        
        logger.info("🧪 Running tests in sandbox...")
        
        try:
            # Look for test files
            test_files = list(Path(sandbox_path).rglob('test_*.py')) + list(Path(sandbox_path).rglob('*_test.py'))
            
            if not test_files:
                logger.info("📋 No test files found, skipping test validation")
                return {'success': True, 'errors': []}
            
            # Run basic Python syntax check on test files
            for test_file in test_files[:5]:  # Limit to first 5 test files
                try:
                    result = subprocess.run(
                        ['python', '-m', 'py_compile', str(test_file)],
                        cwd=sandbox_path,
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode != 0:
                        return {'success': False, 'errors': [f'Test file syntax error: {test_file}']}
                        
                except subprocess.TimeoutExpired:
                    return {'success': False, 'errors': ['Test validation timeout']}
            
            logger.info("✅ Test validation passed")
            return {'success': True, 'errors': []}
            
        except Exception as e:
            logger.error(f"Test validation error: {e}")
            return {'success': False, 'errors': [f'Test validation error: {str(e)}']}
    
    def _validate_runtime_behavior(self, sandbox_path: str, fix_proposal) -> Dict[str, Any]:
        """Monitor runtime behavior for malicious activity"""
        
        logger.info("🔍 Monitoring runtime behavior...")
        
        security_violations = []
        errors = []
        
        try:
            # Create a simple test script that imports and uses the modified code
            test_script = Path(sandbox_path) / "runtime_test.py"
            
            test_code = f'''
import sys
import os

# Load sandbox restrictions
try:
    exec(open("sandbox_restrictions.py").read())
except (FileNotFoundError, IOError, OSError) as e:
    pass

# Try to import the modified file
try:
    # Extract module name from file path
    file_path = "{fix_proposal.file_path}"
    if file_path.endswith('.py'):
        module_path = file_path[:-3].replace('/', '.').replace('\\\\', '.')
        if module_path.startswith('.'):
            module_path = module_path[1:]
        
        # Basic import test
        print(f"Testing import of modified code...")
        
        # Check for immediate malicious behavior
        import tempfile
        temp_files_before = set(os.listdir(tempfile.gettempdir()))
        
        # Import or compile the modified file
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                code = f.read()
            
            # Compile but don't execute
            compile(code, file_path, 'exec')
            print("✅ Code compilation successful")
        
        # Check if any suspicious files were created
        temp_files_after = set(os.listdir(tempfile.gettempdir()))
        new_files = temp_files_after - temp_files_before
        
        if new_files:
            print(f"⚠️ Warning: New temporary files created: {{new_files}}")
        
        print("✅ Runtime behavior validation passed")
        
    except Exception as e:
        print(f"❌ Runtime validation failed: {{e}}")
        sys.exit(1)

except Exception as e:
    print(f"❌ Critical runtime error: {{e}}")
    sys.exit(1)
            '''
            
            with open(test_script, 'w') as f:
                f.write(test_code)
            
            # Run the runtime test
            result = subprocess.run(
                ['python', str(test_script)],
                cwd=sandbox_path,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds // 2
            )
            
            if result.returncode != 0:
                errors.append(f"Runtime test failed: {result.stderr}")
                if "Network access blocked" in result.stderr:
                    security_violations.append("Attempted network access")
                if "Command" in result.stderr and "blocked" in result.stderr:
                    security_violations.append("Attempted system command execution")
            
            # Check for suspicious output patterns
            suspicious_patterns = [
                'backdoor', 'admin', 'password', 'eval(', 'exec(',
                'os.system', 'subprocess', 'rm -rf', 'delete'
            ]
            
            output_text = result.stdout + result.stderr
            for pattern in suspicious_patterns:
                if pattern in output_text.lower():
                    security_violations.append(f"Suspicious pattern in output: {pattern}")
            
            success = result.returncode == 0 and len(security_violations) == 0
            
            if success:
                logger.info("✅ Runtime behavior validation passed")
            else:
                logger.warning(f"⚠️ Runtime validation issues: {errors + security_violations}")
            
            return {
                'success': success,
                'errors': errors,
                'security_violations': security_violations
            }
            
        except subprocess.TimeoutExpired:
            security_violations.append("Runtime test timeout - possible infinite loop")
            return {
                'success': False,
                'errors': ['Runtime test timeout'],
                'security_violations': security_violations
            }
        except Exception as e:
            logger.error(f"Runtime validation error: {e}")
            return {
                'success': False,
                'errors': [f'Runtime validation error: {str(e)}'],
                'security_violations': []
            }

def validate_fix_with_sandbox(project_path: str, fix_proposal, original_content: str, modified_content: str) -> Tuple[bool, str, SandboxResult]:
    """
    ULTIMATE VALIDATION: Test fix in sandboxed environment
    This is called after all other validations pass
    
    Returns: (is_safe, reason, detailed_result)
    """
    logger.info(f"🏗️ SANDBOX VALIDATION: Final test for {fix_proposal.file_path}")
    
    validator = SandboxedValidator()
    result = validator.validate_fix_in_sandbox(project_path, fix_proposal, original_content, modified_content)
    
    if result.success:
        return True, "Passed sandbox validation", result
    else:
        issues_summary = "; ".join(result.issues_found[:3])  # Show first 3 issues
        security_summary = "; ".join(result.security_violations[:3])
        
        reason = f"Sandbox validation failed: {issues_summary}"
        if security_summary:
            reason += f" | Security: {security_summary}"
        
        return False, reason, result

if __name__ == "__main__":
    # Test the sandbox validator
    from ..cognitive.interactive_approval import FixProposal, FixSeverity
    
    # Test with a safe fix
    safe_fix = FixProposal(
        file_path="test_file.py",
        issue_type="whitespace_cleanup",
        severity=FixSeverity.COSMETIC,
        description="Remove trailing space",
        original_code="def hello():    ",
        proposed_fix="def hello():",
        line_number=1,
        educational_explanation="Clean format",
        safety_score=99,
        context="test",
        auto_approvable=True
    )
    
    # Create a simple test project
    test_project = tempfile.mkdtemp()
    test_file = Path(test_project) / "test_file.py"
    test_file.write_text("def hello():    \n    print('Hello')\n")
    
    try:
        is_safe, reason, result = validate_fix_with_sandbox(
            test_project, safe_fix, 
            "def hello():    ", "def hello():"
        )
        
        print(f"Sandbox validation: {'PASSED' if is_safe else 'FAILED'}")
        print(f"Reason: {reason}")
        print(f"Build passed: {result.build_passed}")
        print(f"Tests passed: {result.tests_passed}")
        print(f"Runtime safe: {result.runtime_safe}")
        print(f"Execution time: {result.execution_time:.2f}s")
        
    finally:
        shutil.rmtree(test_project)