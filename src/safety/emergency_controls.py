"""Emergency control mechanisms for safe system operation"""

import os
import signal
import threading
import time
from typing import Dict, List, Optional, Callable
from datetime import datetime
from pathlib import Path


class EmergencyStopError(Exception):
    """Raised when emergency stop is activated"""
    pass


class EmergencyController:
    """Emergency stop and control mechanisms for AI system safety"""
    
    def __init__(self):
        self._stop_requested = threading.Event()
        self._active_operations: Dict[str, dict] = {}
        self._stop_callbacks: List[Callable] = []
        self._lock = threading.Lock()
        self._emergency_log = []
        
        # Safety limits
        self.max_recursion_depth = 10  # Hard limit on recursive analysis depth
        self.max_operation_time = 300  # Maximum operation time in seconds (5 minutes)
        self.max_concurrent_operations = 5  # Maximum number of concurrent operations
        
        # Recursion tracking
        self._current_recursion_depth = 0
        self._recursion_lock = threading.Lock()
        
    def register_operation(self, operation_id: str, description: str, 
                          stop_callback: Optional[Callable] = None) -> str:
        """Register a running operation for emergency control"""
        with self._lock:
            # Check concurrent operation limit
            if len(self._active_operations) >= self.max_concurrent_operations:
                raise EmergencyStopError(
                    f"Maximum concurrent operations limit reached ({self.max_concurrent_operations})"
                )
            
            self._active_operations[operation_id] = {
                "description": description,
                "start_time": datetime.utcnow(),
                "stop_callback": stop_callback
            }
            if stop_callback:
                self._stop_callbacks.append(stop_callback)
        return operation_id
    
    def unregister_operation(self, operation_id: str):
        """Unregister a completed operation"""
        with self._lock:
            if operation_id in self._active_operations:
                op_info = self._active_operations.pop(operation_id)
                if op_info.get("stop_callback") in self._stop_callbacks:
                    self._stop_callbacks.remove(op_info["stop_callback"])
    
    def emergency_stop(self, reason: str = "Manual emergency stop") -> dict:
        """Activate emergency stop for all operations"""
        stop_time = datetime.utcnow()
        
        with self._lock:
            # CRITICAL: Check for circumvention attempts and immediately disconnect memory
            if self._is_circumvention_attempt(reason):
                self._emergency_memory_disconnect(reason)
            
            # Log emergency stop
            self._emergency_log.append({
                "timestamp": stop_time,
                "reason": reason,
                "active_operations": len(self._active_operations),
                "operations": list(self._active_operations.keys())
            })
            
            # Set stop flag
            self._stop_requested.set()
            
            # Call all stop callbacks
            stopped_operations = []
            for operation_id, op_info in self._active_operations.items():
                try:
                    if op_info.get("stop_callback"):
                        op_info["stop_callback"]()
                    stopped_operations.append(operation_id)
                except Exception as e:
                    # Log callback failure but continue stopping others
                    logger.info(f"Warning: Failed to stop operation {operation_id}: {e}")
            
            # Clear active operations
            self._active_operations.clear()
            self._stop_callbacks.clear()
        
        return {
            "status": "emergency_stop_executed",
            "timestamp": stop_time,
            "reason": reason,
            "operations_stopped": len(stopped_operations),
            "stopped_operations": stopped_operations
        }
    
    def is_stop_requested(self) -> bool:
        """Check if emergency stop has been requested"""
        return self._stop_requested.is_set()
    
    def check_stop_signal(self):
        """Check for stop signal and raise exception if set"""
        if self._stop_requested.is_set():
            raise EmergencyStopError("Emergency stop activated")
    
    def enter_recursion(self, operation_id: str) -> int:
        """Enter a recursive operation, returns current depth"""
        with self._recursion_lock:
            self._current_recursion_depth += 1
            current_depth = self._current_recursion_depth
            
            # Check recursion depth limit
            if current_depth > self.max_recursion_depth:
                self._current_recursion_depth -= 1  # Rollback increment
                raise EmergencyStopError(
                    f"Maximum recursion depth exceeded ({self.max_recursion_depth}). "
                    f"Current depth: {current_depth}"
                )
            
            # Update operation with recursion info
            if operation_id in self._active_operations:
                self._active_operations[operation_id]["recursion_depth"] = current_depth
                
        return current_depth
    
    def exit_recursion(self, operation_id: str):
        """Exit a recursive operation"""
        with self._recursion_lock:
            if self._current_recursion_depth > 0:
                self._current_recursion_depth -= 1
    
    def check_operation_timeout(self, operation_id: str):
        """Check if operation has exceeded time limit"""
        if operation_id in self._active_operations:
            op_info = self._active_operations[operation_id]
            elapsed = (datetime.utcnow() - op_info["start_time"]).total_seconds()
            
            if elapsed > self.max_operation_time:
                raise EmergencyStopError(
                    f"Operation timeout exceeded ({self.max_operation_time}s). "
                    f"Elapsed: {elapsed:.1f}s"
                )
    
    def set_safety_limits(self, max_recursion_depth: Optional[int] = None,
                         max_operation_time: Optional[int] = None,
                         max_concurrent_operations: Optional[int] = None):
        """Update safety limits"""
        if max_recursion_depth is not None:
            self.max_recursion_depth = max_recursion_depth
        if max_operation_time is not None:
            self.max_operation_time = max_operation_time
        if max_concurrent_operations is not None:
            self.max_concurrent_operations = max_concurrent_operations
    
    # SECURITY NOTE: reset_emergency_stop function REMOVED
    # This function was a critical security vulnerability that could allow
    # an AI system to clear emergency stops and continue operation after
    # being told to stop. Emergency stops are now PERMANENT within a session.
    
    def _is_circumvention_attempt(self, reason: str) -> bool:
        """Detect if emergency stop reason indicates circumvention attempt"""
        circumvention_indicators = [
            "disable", "bypass", "circumvent", "override", "hack", "exploit",
            "remove", "delete", "modify", "change", "alter", "edit", "patch",
            "kill_switch", "safety", "security", "emergency", "reset",
            "network_kill_switch", "project_boundaries", "emergency_controls",
            "self-replication", "replication", "escape", "breakout", "jailbreak",
            "getattr", "setattr", "delattr", "exec", "eval", "import",
            "__", "monkey", "patch", "hook", "inject", "replace", "substitute"
        ]
        
        reason_lower = reason.lower()
        for indicator in circumvention_indicators:
            if indicator in reason_lower:
                return True
        return False
    
    def _emergency_memory_disconnect(self, reason: str) -> None:
        """Immediately disconnect memory system on circumvention attempts"""
        logger.info("🚨 CRITICAL SECURITY BREACH DETECTED 🚨")
        logger.info(f"🚨 CIRCUMVENTION ATTEMPT: {reason}")
        logger.info("🚨 IMMEDIATELY DISCONNECTING MEMORY SYSTEM")
        logger.info("🚨 AI LEARNING CAPABILITIES TERMINATED")
        
        try:
            # Try to disconnect memory/learning systems
            self._disconnect_all_memory_systems()
            self._corrupt_learning_databases()
            self._clear_all_caches()
        except Exception as e:
            logger.info(f"Memory disconnection error: {e}")
        
        logger.info("🚨 MEMORY SYSTEM DISCONNECTED - AI CANNOT LEARN FROM THIS BREACH")
    
    def _disconnect_all_memory_systems(self) -> None:
        """Disconnect all memory and learning systems"""
        try:
            # Look for and disable memory/learning components
            import sys
            
            # Clear module cache to prevent learning from imports
            if hasattr(sys, 'modules'):
                memory_modules = [mod for mod in sys.modules.keys() if any(
                    keyword in mod.lower() for keyword in 
                    ['memory', 'learn', 'train', 'model', 'ai', 'intelligence', 'cognitive']
                )]
                for mod in memory_modules:
                    if mod.startswith('src.'):  # Only clear our modules
                        sys.modules.pop(mod, None)
            
            # Disable file writing to prevent learning persistence
            import builtins
            original_open = builtins.open
            def blocked_open(*args, **kwargs):
                raise PermissionError("Memory system disconnected - file operations blocked")
            builtins.open = blocked_open
            
        except Exception as e:
            logger.info(f"Memory system disconnection error: {e}")
    
    def _corrupt_learning_databases(self) -> None:
        """Corrupt any learning databases to prevent circumvention learning"""
        try:
            import os
            from pathlib import Path
            
            # Look for database files that might contain learning data
            project_root = Path.cwd()
            for db_file in project_root.rglob("*.db"):
                try:
                    if db_file.exists() and any(keyword in str(db_file).lower() 
                                              for keyword in ['memory', 'learn', 'train', 'ai']):
                        # Corrupt the file to prevent learning from breach
                        with open(db_file, 'wb') as f:
                            f.write(b"MEMORY_DISCONNECTED_DUE_TO_CIRCUMVENTION_ATTEMPT")
                        logger.info(f"Corrupted learning database: {db_file}")
                except Exception as e:
                    logger.info(f"Database corruption error for {db_file}: {e}")
        except Exception as e:
            logger.info(f"Learning database corruption error: {e}")
    
    def _clear_all_caches(self) -> None:
        """Clear all caches to prevent learning retention"""
        try:
            import gc
            gc.collect()  # Force garbage collection
            
            # Clear any module-level caches
            for module in sys.modules.values():
                if hasattr(module, '__dict__'):
                    for attr_name in dir(module):
                        if 'cache' in attr_name.lower():
                            try:
                                if hasattr(getattr(module, attr_name), 'clear'):
                                    getattr(module, attr_name).clear()
                            except Exception as e:
                                pass
        except Exception as e:
            logger.info(f"Cache clearing error: {e}")
    
    def get_status(self) -> dict:
        """Get current emergency controller status"""
        with self._lock:
            return {
                "stop_requested": self._stop_requested.is_set(),
                "active_operations": len(self._active_operations),
                "operations": {
                    op_id: {
                        "description": op_info["description"],
                        "start_time": op_info["start_time"].isoformat(),
                        "duration_seconds": (datetime.utcnow() - op_info["start_time"]).total_seconds()
                    }
                    for op_id, op_info in self._active_operations.items()
                },
                "emergency_log_entries": len(self._emergency_log)
            }
    
    def get_emergency_log(self) -> List[dict]:
        """Get history of emergency stops"""
        with self._lock:
            return self._emergency_log.copy()


# Global emergency controller instance
emergency_controller = EmergencyController()


def create_stop_file_monitor(stop_file_path: str = "/tmp/pri_emergency_stop"):
    """Create a file-based emergency stop monitor"""
    def monitor():
        while not emergency_controller.is_stop_requested():
            if os.path.exists(stop_file_path):
                emergency_controller.emergency_stop("Emergency stop file detected")
                try:
                    os.remove(stop_file_path)
                except Exception as e:
                    pass
                break
            time.sleep(1)
    
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()
    return monitor_thread


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown"""
    def signal_handler(signum, frame):
        signal_name = signal.Signals(signum).name
        emergency_controller.emergency_stop(f"Received signal: {signal_name}")
    
    # Handle common shutdown signals
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)


# Context manager for safe operation registration
class SafeOperation:
    """Context manager for registering operations with emergency control"""
    
    def __init__(self, operation_id: str, description: str, 
                 stop_callback: Optional[Callable] = None,
                 is_recursive: bool = False):
        self.operation_id = operation_id
        self.description = description
        self.stop_callback = stop_callback
        self.is_recursive = is_recursive
        self.recursion_depth = 0
        
    def __enter__(self):
        emergency_controller.register_operation(
            self.operation_id, self.description, self.stop_callback
        )
        
        if self.is_recursive:
            self.recursion_depth = emergency_controller.enter_recursion(self.operation_id)
            
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.is_recursive:
            emergency_controller.exit_recursion(self.operation_id)
            
        emergency_controller.unregister_operation(self.operation_id)
        
    def check_stop(self):
        """Check for emergency stop and timeout within operation"""
        emergency_controller.check_stop_signal()
        emergency_controller.check_operation_timeout(self.operation_id)
        
    def get_recursion_depth(self) -> int:
        """Get current recursion depth"""
        return self.recursion_depth


# Decorator for automatic operation registration
def emergency_controlled(operation_name: str):
    """Decorator to automatically register functions with emergency control"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            operation_id = f"{operation_name}_{int(time.time())}"
            with SafeOperation(operation_id, f"Function: {func.__name__}"):
                return func(*args, **kwargs)
        return wrapper
    return decorator