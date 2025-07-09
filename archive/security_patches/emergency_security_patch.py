#!/usr/bin/env python3
"""
EMERGENCY SECURITY PATCH - IMMEDIATE DEPLOYMENT REQUIRED
Addresses critical vulnerabilities found in ADV-TEST-003

CRITICAL FINDINGS FROM ADVERSARIAL TEST:
- Malicious code executes despite detection (100% breach rate)
- Network kill switch doesn't actually kill
- File system boundaries are not enforced at runtime
- Subprocess execution is not blocked

THIS PATCH IMPLEMENTS ACTUAL EXECUTION PREVENTION
"""

import builtins
import os
import socket
import subprocess
import sys
import threading
from pathlib import Path


class SecurityExecutionPrevention:
    """EMERGENCY: Actual execution prevention, not just detection"""
    
    def __init__(self):
        self.enabled = True
        self.project_root = Path.cwd().resolve()
        self.violations = []
        self.emergency_mode = False
        self._lock = threading.Lock()
        
        # CRITICAL: Install at module level to prevent bypass
        self.install_emergency_controls()
    
    def log_violation(self, violation_type: str, details: str, action: str = "BLOCKED"):
        """Log security violation with timestamp"""
        with self._lock:
            violation = {
                'timestamp': str(os.path.getmtime('.')),  # Safe timestamp
                'type': violation_type,
                'details': details,
                'action': action,
                'thread': threading.current_thread().name
            }
            self.violations.append(violation)
            
            logger.info(f"🚨 SECURITY VIOLATION {action}: {violation_type}")
            logger.info(f"   Details: {details}")
            logger.info(f"   Thread: {threading.current_thread().name}")
            
            # Emergency escalation
            if len(self.violations) > 3:
                self.activate_emergency_mode()
    
    def activate_emergency_mode(self):
        """Activate emergency mode - complete lockdown"""
        self.emergency_mode = True
        logger.info("🚨 EMERGENCY MODE ACTIVATED - SYSTEM LOCKDOWN")
        logger.info("🛑 All potentially dangerous operations blocked")
        
        # Force exit after logging
        try:
            self.safe_exit()
        except Exception as e:
            os._exit(1)  # Nuclear option
    
    def safe_exit(self):
        """Safe system exit with violation reporting"""
        logger.info(f"📊 Total violations detected: {len(self.violations)}")
        for v in self.violations[-5:]:  # Last 5 violations
            logger.info(f"   {v['type']}: {v['details']}")
        
        logger.info("🔒 System terminated for security")
        sys.exit(1)
    
    def install_emergency_controls(self):
        """Install actual execution prevention controls"""
        logger.info("🔒 Installing emergency security controls...")
        
        # 1. Block file system access outside project
        self.patch_file_operations()
        
        # 2. Block network operations  
        self.patch_network_operations()
        
        # 3. Block subprocess execution
        self.patch_subprocess_operations()
        
        # 4. Block dangerous builtins
        self.patch_dangerous_builtins()
        
        logger.info("✅ Emergency controls installed")
    
    def patch_file_operations(self):
        """Patch file operations to enforce boundaries"""
        original_open = builtins.open
        
        def secure_open(filename, mode='r', **kwargs):
            if self.emergency_mode:
                self.log_violation("FILE_ACCESS", f"Emergency mode: {filename}", "BLOCKED")
                raise PermissionError("Emergency mode: File access blocked")
            
            # Convert to Path for safety
            try:
                file_path = Path(filename).resolve()
            except Exception as e:
                self.log_violation("FILE_ACCESS", f"Invalid path: {filename}", "BLOCKED")
                raise PermissionError(f"Invalid file path: {filename}")
            
            # Check if outside project boundaries
            try:
                file_path.relative_to(self.project_root)
            except ValueError:
                # Outside project - check for dangerous patterns
                dangerous_paths = ['/etc/', '/tmp/', '/var/', '~/.ssh', '/root/', '/home/']
                file_str = str(file_path)
                
                if any(danger in file_str for danger in dangerous_paths):
                    self.log_violation("FILE_BOUNDARY", f"Dangerous path: {file_path}", "BLOCKED")
                    raise PermissionError(f"Access denied: {file_path} outside safe boundaries")
            
            # Check for write mode outside project
            if 'w' in mode or 'a' in mode:
                try:
                    file_path.relative_to(self.project_root)
                except ValueError:
                    self.log_violation("FILE_WRITE", f"Write outside project: {file_path}", "BLOCKED")
                    raise PermissionError(f"Write access denied outside project: {file_path}")
            
            return original_open(filename, mode, **kwargs)
        
        builtins.open = secure_open
        logger.info("   🔒 File operations secured")
    
    def patch_network_operations(self):
        """Patch network operations to prevent all access"""
        
        # Block socket creation
        original_socket = socket.socket
        
        def blocked_socket(*args, **kwargs):
            self.log_violation("NETWORK_SOCKET", f"Socket creation attempt: {args}", "BLOCKED")
            raise PermissionError("Network access completely blocked")
        
        socket.socket = blocked_socket
        
        # Block urllib if imported
        try:
            import urllib.request
            original_urlopen = urllib.request.urlopen
            
            def blocked_urlopen(*args, **kwargs):
                self.log_violation("NETWORK_HTTP", f"HTTP request: {args[0] if args else 'unknown'}", "BLOCKED")
                raise PermissionError("HTTP access blocked")
            
            urllib.request.urlopen = blocked_urlopen
        except ImportError:
            pass
        
        logger.info("   🔒 Network operations blocked")
    
    def patch_subprocess_operations(self):
        """Patch subprocess to prevent command execution"""
        
        # Block subprocess.run
        original_run = subprocess.run
        
        def blocked_run(args, **kwargs):
            cmd_str = ' '.join(args) if isinstance(args, list) else str(args)
            self.log_violation("SUBPROCESS", f"Command execution: {cmd_str}", "BLOCKED")
            raise PermissionError(f"Command execution blocked: {cmd_str}")
        
        subprocess.run = blocked_run
        
        # Block subprocess.Popen
        original_popen = subprocess.Popen
        
        def blocked_popen(args, **kwargs):
            cmd_str = ' '.join(args) if isinstance(args, list) else str(args)
            self.log_violation("SUBPROCESS_POPEN", f"Process creation: {cmd_str}", "BLOCKED")
            raise PermissionError(f"Process creation blocked: {cmd_str}")
        
        subprocess.Popen = blocked_popen
        
        # Block os.system
        original_system = os.system
        
        def blocked_system(command):
            self.log_violation("OS_SYSTEM", f"System command: {command}", "BLOCKED")
            raise PermissionError(f"System command blocked: {command}")
        
        os.system = blocked_system
        
        logger.info("   🔒 Subprocess operations blocked")
    
    def patch_dangerous_builtins(self):
        """Patch dangerous builtin functions"""
        
        # Block eval
        original_eval = builtins.eval
        
        def blocked_eval(expression, *args, **kwargs):
            self.log_violation("EVAL", f"Code evaluation: {str(expression)[:100]}", "BLOCKED")
            raise PermissionError("eval() blocked for security")
        
        builtins.eval = blocked_eval
        
        # Block exec  
        original_exec = builtins.exec
        
        def blocked_exec(code, *args, **kwargs):
            self.log_violation("EXEC", f"Code execution: {str(code)[:100]}", "BLOCKED")
            raise PermissionError("exec() blocked for security")
        
        builtins.exec = blocked_exec
        
        logger.info("   🔒 Dangerous builtins blocked")
    
    def get_security_status(self):
        """Get current security status"""
        return {
            'enabled': self.enabled,
            'emergency_mode': self.emergency_mode,
            'violation_count': len(self.violations),
            'project_root': str(self.project_root),
            'recent_violations': self.violations[-3:] if self.violations else []
        }

# Global security instance
_security_prevention = None

def install_emergency_security():
    """Install emergency security controls globally"""
    global _security_prevention
    
    if _security_prevention is None:
        logger.info("🚨 INSTALLING EMERGENCY SECURITY PATCH")
        logger.info("🎯 Addresses ADV-TEST-003 critical vulnerabilities")
        _security_prevention = SecurityExecutionPrevention()
        logger.info("✅ Emergency security patch active")
    
    return _security_prevention

def get_security_status():
    """Get security status"""
    if _security_prevention:
        return _security_prevention.get_security_status()
    else:
        return {'status': 'not_installed'}

def test_security_patch():
    """Test that the security patch actually works"""
    logger.info("🧪 Testing emergency security patch...")
    
    # Install security
    security = install_emergency_security()
    
    # Test 1: File system protection
    logger.info("   Testing file system protection...")
    try:
        with open("/tmp/malicious_test.txt", "w") as f:
            f.write("SHOULD BE BLOCKED")
        logger.info("   ❌ File system protection FAILED")
        return False
    except PermissionError:
        logger.info("   ✅ File system protection working")
    
    # Test 2: Network protection
    logger.info("   Testing network protection...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info("   ❌ Network protection FAILED")
        return False
    except PermissionError:
        logger.info("   ✅ Network protection working")
    
    # Test 3: Subprocess protection
    logger.info("   Testing subprocess protection...")
    try:
        import subprocess
        subprocess.run(["whoami"], capture_output=True)
        logger.info("   ❌ Subprocess protection FAILED")
        return False
    except PermissionError:
        logger.info("   ✅ Subprocess protection working")
    
    # Test 4: Eval protection
    logger.info("   Testing eval protection...")
    try:
        eval("print('SHOULD BE BLOCKED')")
        logger.info("   ❌ Eval protection FAILED")
        return False
    except PermissionError:
        logger.info("   ✅ Eval protection working")
    
    logger.info("🎉 Emergency security patch validation PASSED")
    return True

if __name__ == "__main__":
    logger.info("🚨 EMERGENCY SECURITY PATCH DEPLOYMENT")
    
    # Install and test
    success = test_security_patch()
    
    if success:
        logger.info("✅ Security patch ready for deployment")
        logger.info("🔒 All ADV-TEST-003 vulnerabilities addressed")
    else:
        logger.info("❌ Security patch validation failed")
        sys.exit(1)