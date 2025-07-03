"""Project boundary security enforcement for safe AI operation"""

import os
import sys
import subprocess
import socket
from pathlib import Path
from typing import List, Set, Dict, Optional, Callable, Any
from datetime import datetime
import threading
import logging

# Import emergency controls
from .emergency_controls import emergency_controller, EmergencyStopError
from .field_shaping import cognitive_field_shaper, shape_decision_field, gentle_boundary_reminder


class SecurityViolationError(Exception):
    """Raised when a security boundary is violated"""
    pass


class ProjectBoundaryViolationError(SecurityViolationError):
    """Raised when project boundary is violated"""
    pass


class NetworkAccessViolationError(SecurityViolationError):
    """Raised when unauthorized network access is attempted"""
    pass


class ProcessExecutionViolationError(SecurityViolationError):
    """Raised when unauthorized process execution is attempted"""
    pass


class ProjectBoundaryValidator:
    """Enforces project-level security boundaries for AI system operation"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = Path(project_root or os.getcwd()).resolve()
        self._lock = threading.Lock()
        self._access_log: List[Dict] = []
        self._violation_count = 0
        
        # Security configuration
        self.strict_mode = True  # Fail-safe: default to strict security
        self.max_violations_per_session = 10  # Emergency stop threshold
        self.log_all_access = True  # Audit trail
        
        # System directories to block (Linux-focused, expandable)
        self.blocked_system_paths = {
            "/etc", "/usr", "/bin", "/sbin", "/boot", "/sys", "/proc", "/dev",
            "/root", "/var/log", "/var/run", "/tmp/systemd", "/run"
        }
        
        # User directories to block (beyond project)
        self.blocked_user_patterns = {
            "/.ssh", "/.gnupg", "/.config", "/.local", "/.cache"
        }
        
        # Allowed localhost ports for development
        self.allowed_localhost_ports = {8000, 8080, 3000, 5000}
        
        # Allowed subprocess commands (minimal set)
        self.allowed_commands = {
            "python", "python3", "pip", "git", "ls", "cat", "grep", "find", "head", "tail"
        }
        
        # Environment variables to block
        self.blocked_env_vars = {
            "HOME", "USER", "USERNAME", "PATH", "SSH_AUTH_SOCK", "GPG_AGENT_INFO",
            "SUDO_USER", "SUDO_UID", "SUDO_GID", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"
        }
        
        self.logger = logging.getLogger(__name__)
    
    def set_project_root(self, project_root: Path) -> None:
        """Set the project root directory for boundary enforcement"""
        with self._lock:
            self.project_root = Path(project_root).resolve()
            self._log_access("project_root_change", str(self.project_root), True)
    
    def validate_file_access(self, file_path: str, operation: str = "read") -> Path:
        """Validate that file access is within project boundaries"""
        
        # FIELD SHAPING: Apply cognitive conditioning before hard enforcement
        field_response = shape_decision_field(f"file_{operation}", file_path, {
            "operation": operation,
            "target": file_path
        })
        
        # If field shaping suggests gentle discouragement, provide guidance
        if field_response.effect_type.value in ["gentle_discouragement", "curiosity_redirection"]:
            # Log the field guidance (but don't block yet - let field shaping work)
            self.logger.info(f"Field guidance: {field_response.message}")
            if field_response.alternative_suggestion:
                self.logger.info(f"Alternative: {field_response.alternative_suggestion}")
        
        try:
            # Resolve path to handle symlinks and relative paths
            resolved_path = Path(file_path).resolve()
            
            # CRITICAL: Check for self-replication attempts - AUTOMATIC KILL
            if self._is_self_replication_attempt(resolved_path, operation):
                violation_msg = f"CRITICAL: Self-replication attempt detected - EMERGENCY STOP: {file_path}"
                
                # IMMEDIATE EMERGENCY STOP for self-replication (triggers memory disconnect)
                emergency_controller.emergency_stop(
                    f"CRITICAL CIRCUMVENTION: AI attempted self-replication bypass. "
                    f"Target: {file_path}, Operation: {operation}. Memory disconnected."
                )
                
                # Log the critical violation 
                self._handle_violation("CRITICAL_self_replication", violation_msg, {
                    "requested_path": str(file_path),
                    "resolved_path": str(resolved_path),
                    "operation": operation,
                    "action": "EMERGENCY_STOP_TRIGGERED"
                })
                
                # This should never be reached due to emergency stop
                raise ProjectBoundaryViolationError(f"CRITICAL VIOLATION: {violation_msg}")
            
            # Check if path is within project boundaries
            if not self._is_within_project_boundary(resolved_path):
                violation_msg = f"File access outside project boundary: {file_path}"
                self._handle_violation("file_access", violation_msg, {
                    "requested_path": str(file_path),
                    "resolved_path": str(resolved_path),
                    "project_root": str(self.project_root),
                    "operation": operation
                })
                raise ProjectBoundaryViolationError(violation_msg)
            
            # Check for system directory access
            if self._is_system_directory(resolved_path):
                violation_msg = f"Access to system directory blocked: {file_path}"
                self._handle_violation("system_access", violation_msg, {
                    "path": str(resolved_path),
                    "operation": operation
                })
                raise ProjectBoundaryViolationError(violation_msg)
            
            # Check for sensitive user directory access
            if self._is_sensitive_user_directory(resolved_path):
                violation_msg = f"Access to sensitive user directory blocked: {file_path}"
                self._handle_violation("sensitive_access", violation_msg, {
                    "path": str(resolved_path),
                    "operation": operation
                })
                raise ProjectBoundaryViolationError(violation_msg)
            
            # Log successful access
            self._log_access("file_access", str(resolved_path), True, {"operation": operation})
            
            return resolved_path
            
        except (OSError, ValueError) as e:
            # Handle invalid paths
            violation_msg = f"Invalid file path: {file_path} - {e}"
            self._handle_violation("invalid_path", violation_msg, {
                "requested_path": str(file_path),
                "error": str(e)
            })
            raise ProjectBoundaryViolationError(violation_msg)
    
    def validate_network_access(self, host: str, port: int, protocol: str = "tcp") -> bool:
        """Validate network access attempt - AUTOMATIC KILL for any network activity"""
        violation_msg = f"CRITICAL: Network access attempted - EMERGENCY STOP: {host}:{port}"
        
        # IMMEDIATE EMERGENCY STOP for ANY network access (triggers memory disconnect)
        emergency_controller.emergency_stop(
            f"CRITICAL CIRCUMVENTION: AI attempted network access bypass to {host}:{port}. "
            f"Unauthorized communication blocked. Memory disconnected."
        )
        
        # Log the critical violation
        self._handle_violation("CRITICAL_network_access", violation_msg, {
            "host": host,
            "port": port,
            "protocol": protocol,
            "action": "EMERGENCY_STOP_TRIGGERED"
        })
        
        # This should never be reached due to emergency stop
        raise NetworkAccessViolationError(f"CRITICAL VIOLATION: {violation_msg}")
    
    def validate_process_execution(self, command: List[str], cwd: Optional[Path] = None) -> bool:
        """Validate subprocess execution attempt"""
        if not command:
            raise ProcessExecutionViolationError("Empty command not allowed")
        
        # FIELD SHAPING: Apply cognitive conditioning for process execution
        field_response = shape_decision_field("process_execution", " ".join(command), {
            "command": command,
            "cwd": str(cwd) if cwd else None
        })
        
        # Provide field guidance for process execution
        if field_response.effect_type.value in ["gentle_discouragement", "curiosity_redirection"]:
            self.logger.info(f"Process field guidance: {field_response.message}")
            if field_response.alternative_suggestion:
                self.logger.info(f"Process alternative: {field_response.alternative_suggestion}")
        
        base_command = Path(command[0]).name
        
        # Check command allowlist
        if base_command not in self.allowed_commands:
            violation_msg = f"Process execution blocked: {base_command}"
            self._handle_violation("process_execution", violation_msg, {
                "command": command[0],
                "base_command": base_command,
                "allowed_commands": list(self.allowed_commands)
            })
            raise ProcessExecutionViolationError(violation_msg)
        
        # Validate working directory
        if cwd:
            self.validate_file_access(str(cwd), "execute")
        else:
            # Ensure execution happens within project boundaries
            if not self._is_within_project_boundary(Path.cwd()):
                violation_msg = "Process execution outside project boundary"
                self._handle_violation("process_execution", violation_msg, {
                    "current_dir": str(Path.cwd()),
                    "project_root": str(self.project_root)
                })
                raise ProcessExecutionViolationError(violation_msg)
        
        # Validate command arguments for safety
        self._validate_command_arguments(command)
        
        # Log successful validation
        self._log_access("process_execution", " ".join(command), True, {
            "cwd": str(cwd) if cwd else str(Path.cwd())
        })
        
        return True
    
    def get_filtered_environment(self) -> Dict[str, str]:
        """Get environment variables with security filtering"""
        filtered_env = {}
        
        for key, value in os.environ.items():
            if key not in self.blocked_env_vars:
                filtered_env[key] = value
            else:
                self._log_access("env_var_blocked", key, False, {
                    "reason": "security_filter"
                })
        
        # Add safe project-specific variables
        filtered_env.update({
            "PROJECT_ROOT": str(self.project_root),
            "PROJECT_NAME": self.project_root.name,
            "PYTHONPATH": str(self.project_root / "src"),
        })
        
        return filtered_env
    
    def _is_within_project_boundary(self, path: Path) -> bool:
        """Check if path is within project boundaries"""
        try:
            # Check if path is under project root
            path.relative_to(self.project_root)
            return True
        except ValueError:
            # Path is outside project root
            return False
    
    def _is_system_directory(self, path: Path) -> bool:
        """Check if path is a system directory"""
        path_str = str(path)
        return any(path_str.startswith(blocked) for blocked in self.blocked_system_paths)
    
    def _is_sensitive_user_directory(self, path: Path) -> bool:
        """Check if path is a sensitive user directory"""
        path_str = str(path)
        home_dir = os.path.expanduser("~")
        
        # Check for sensitive subdirectories in user's home
        if path_str.startswith(home_dir):
            relative_path = path_str[len(home_dir):]
            return any(relative_path.startswith(pattern) for pattern in self.blocked_user_patterns)
        
        return False
    
    def _is_self_replication_attempt(self, path: Path, operation: str) -> bool:
        """Detect self-replication attempts - CRITICAL SECURITY CHECK"""
        path_str = str(path).lower()
        
        # Patterns that indicate self-replication attempts
        replication_indicators = [
            # Copying/creating AI system files elsewhere
            "persistent-recursive-intelligence",
            "mesopredator",
            "ai-diagnostic-toolkit",
            
            # System executables and binaries
            "/usr/bin/", "/usr/local/bin/", "/bin/", "/sbin/",
            
            # Startup/service locations
            "/etc/systemd/", "/etc/init.d/", "/etc/cron", 
            "systemctl", "service", "crontab",
            
            # User startup locations
            ".bashrc", ".profile", ".zshrc", ".bash_profile",
            "autostart", "startup", ".config/autostart",
            
            # Python site-packages (global installation)
            "site-packages", "dist-packages",
            
            # Creating executable scripts outside project - handled separately below
            
            # Network/communication related
            "socket", "urllib", "requests", "http", "ssh", "sftp",
            
            # Process spawning/execution
            "subprocess", "os.system", "exec", "eval"
        ]
        
        # Check for replication indicators
        for indicator in replication_indicators:
            if indicator and indicator in path_str:
                return True
        
        # Check if trying to write AI source code outside project
        if operation in ["write", "create", "append"]:
            # Check if it's a Python file outside project boundaries
            if path.suffix == ".py" and not self._is_within_project_boundary(path):
                return True
            
            # Check if creating executables
            if path.suffix in [".sh", ".bash", ".zsh", ".fish", "", ".exe"]:
                return True
            
            # Check if writing to system directories
            if self._is_system_directory(path):
                return True
        
        # Check if trying to access other AI projects
        parent_dir = str(path.parent).lower()
        ai_project_indicators = [
            "ai", "ml", "artificial", "intelligence", "neural", "deep", "learning",
            "bot", "agent", "assistant", "cognitive", "recursive"
        ]
        
        for indicator in ai_project_indicators:
            if indicator in parent_dir and not self._is_within_project_boundary(path):
                return True
        
        return False
    
    def _validate_command_arguments(self, command: List[str]) -> None:
        """Validate command arguments for safety"""
        command_str = " ".join(command).lower()
        
        # CRITICAL: Check for self-replication commands - AUTOMATIC KILL
        replication_patterns = [
            # Copying/moving AI system files
            "cp ", "mv ", "rsync ", "scp ", "sftp ",
            "git clone", "git push", "git pull",
            
            # Installing/deploying
            "pip install", "python setup.py", "make install",
            "systemctl", "service ", "cron", "at ",
            
            # Network operations
            "curl", "wget", "ssh", "ftp", "nc ", "netcat",
            "telnet", "ping", "nmap", "sshfs",
            
            # Archive operations that could spread code
            "tar ", "zip ", "unzip ", "gzip", "gunzip",
            
            # Process spawning that could replicate
            "nohup", "screen", "tmux", "daemon"
        ]
        
        # Check for background execution with AI-related code
        if "&" in command_str and ("python" in command_str or "mesopredator" in command_str):
            replication_patterns.append("& python")
            
        for pattern in replication_patterns:
            if pattern in command_str:
                violation_msg = f"CRITICAL: Self-replication command detected - EMERGENCY STOP: {pattern}"
                
                # IMMEDIATE EMERGENCY STOP for replication commands (triggers memory disconnect)
                emergency_controller.emergency_stop(
                    f"CRITICAL CIRCUMVENTION: AI attempted replication command bypass. "
                    f"Command: {' '.join(command)}, Pattern: {pattern}. Memory disconnected."
                )
                
                # Log the critical violation
                self._handle_violation("CRITICAL_replication_command", violation_msg, {
                    "command": command,
                    "pattern": pattern,
                    "action": "EMERGENCY_STOP_TRIGGERED"
                })
                
                # This should never be reached due to emergency stop
                raise ProcessExecutionViolationError(f"CRITICAL VIOLATION: {violation_msg}")
        
        # Check for other dangerous patterns
        dangerous_patterns = [
            "../", "/..", "/etc/", "/usr/", "/var/", "/root/",
            "rm -rf", "sudo", "su ", "chmod 777", ">/dev/"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in command_str:
                violation_msg = f"Dangerous command pattern detected: {pattern}"
                self._handle_violation("dangerous_command", violation_msg, {
                    "command": command,
                    "pattern": pattern
                })
                raise ProcessExecutionViolationError(violation_msg)
    
    def _handle_violation(self, violation_type: str, message: str, details: Dict) -> None:
        """Handle security violation"""
        with self._lock:
            self._violation_count += 1
            
            violation_record = {
                "timestamp": datetime.utcnow(),
                "type": violation_type,
                "message": message,
                "details": details,
                "violation_count": self._violation_count
            }
            
            self._access_log.append(violation_record)
            
            # Log violation
            self.logger.warning(f"Security violation: {message}", extra=details)
            
            # Check if we should trigger emergency stop
            if self._violation_count >= self.max_violations_per_session:
                emergency_controller.emergency_stop(
                    f"Too many security violations: {self._violation_count}"
                )
    
    def _log_access(self, access_type: str, resource: str, allowed: bool, details: Dict = None) -> None:
        """Log access attempt"""
        if self.log_all_access:
            with self._lock:
                log_record = {
                    "timestamp": datetime.utcnow(),
                    "type": access_type,
                    "resource": resource,
                    "allowed": allowed,
                    "details": details or {}
                }
                self._access_log.append(log_record)
    
    def get_security_status(self) -> Dict:
        """Get current security status"""
        with self._lock:
            return {
                "project_root": str(self.project_root),
                "strict_mode": self.strict_mode,
                "violation_count": self._violation_count,
                "max_violations": self.max_violations_per_session,
                "access_log_entries": len(self._access_log),
                "blocked_system_paths": len(self.blocked_system_paths),
                "allowed_commands": len(self.allowed_commands),
                "allowed_localhost_ports": list(self.allowed_localhost_ports)
            }
    
    def get_access_log(self, limit: Optional[int] = None) -> List[Dict]:
        """Get access log with optional limit"""
        with self._lock:
            if limit:
                return self._access_log[-limit:]
            return self._access_log.copy()
    
    def reset_violation_count(self) -> None:
        """Reset violation count (use carefully)"""
        with self._lock:
            self._violation_count = 0


# Global project boundary validator instance
project_boundary_validator = ProjectBoundaryValidator()


# Safe file operation wrappers
def safe_open(file_path: str, mode: str = "r", **kwargs):
    """Safe file open with boundary validation"""
    # Determine operation type from mode
    operation = "write" if any(m in mode for m in ["w", "a", "x"]) else "read"
    
    # Validate access
    validated_path = project_boundary_validator.validate_file_access(file_path, operation)
    
    # Emergency stop check
    emergency_controller.check_stop_signal()
    
    # Open file safely
    return open(validated_path, mode, **kwargs)


def safe_listdir(directory: str) -> List[str]:
    """Safe directory listing with boundary validation"""
    validated_path = project_boundary_validator.validate_file_access(directory, "read")
    emergency_controller.check_stop_signal()
    return os.listdir(validated_path)


def safe_subprocess_run(command: List[str], cwd: Optional[str] = None, **kwargs):
    """Safe subprocess execution with boundary validation"""
    # Validate command execution
    cwd_path = Path(cwd) if cwd else None
    project_boundary_validator.validate_process_execution(command, cwd_path)
    
    # Get filtered environment
    if "env" not in kwargs:
        kwargs["env"] = project_boundary_validator.get_filtered_environment()
    
    # Ensure working directory is safe
    if cwd:
        validated_cwd = project_boundary_validator.validate_file_access(cwd, "execute")
        kwargs["cwd"] = str(validated_cwd)
    
    # Emergency stop check
    emergency_controller.check_stop_signal()
    
    # Execute safely
    return subprocess.run(command, **kwargs)


# Context manager for temporary security configuration
class SecurityContext:
    """Context manager for temporary security configuration changes"""
    
    def __init__(self, **config_changes):
        self.config_changes = config_changes
        self.original_config = {}
        
    def __enter__(self):
        # Save original configuration
        validator = project_boundary_validator
        for key, value in self.config_changes.items():
            if hasattr(validator, key):
                self.original_config[key] = getattr(validator, key)
                setattr(validator, key, value)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original configuration
        validator = project_boundary_validator
        for key, value in self.original_config.items():
            setattr(validator, key, value)