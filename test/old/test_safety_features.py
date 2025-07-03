#!/usr/bin/env python3
"""
Test Safety Features Implementation
Validates that the newly implemented safety features work correctly
"""

import time
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from safety.emergency_controls import (
    EmergencyController, 
    EmergencyStopError, 
    SafeOperation,
    emergency_controller
)
from cognitive.utils.circuit_breaker import (
    CircuitBreaker, 
    CircuitBreakerState, 
    CircuitBreakerError
)
from metrics.models import HealthStatus, SystemType


def test_enum_definitions():
    """Test that enum definitions are working"""
    print("🧪 Testing Enum Definitions...")
    
    try:
        # Test HealthStatus enum
        assert HealthStatus.HEALTHY == "healthy"
        assert HealthStatus.DEGRADED == "degraded"
        assert HealthStatus.UNHEALTHY == "unhealthy"
        assert HealthStatus.UNKNOWN == "unknown"
        print("  ✅ HealthStatus enum working")
        
        # Test SystemType enum
        assert SystemType.AI_ANALYSIS == "ai_analysis"
        assert SystemType.COGNITIVE_ENGINE == "cognitive_engine"
        assert SystemType.GENERIC == "generic"
        print("  ✅ SystemType enum working")
        
        # Test CircuitBreakerState enum
        assert CircuitBreakerState.CLOSED.value == "closed"
        assert CircuitBreakerState.OPEN.value == "open"
        assert CircuitBreakerState.HALF_OPEN.value == "half_open"
        print("  ✅ CircuitBreakerState enum working")
        
        print("✅ All enum definitions working correctly!\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Enum test failed: {e}")
        return False


def test_circuit_breaker():
    """Test circuit breaker functionality"""
    print("🧪 Testing Circuit Breaker...")
    
    # Create circuit breaker with low threshold for testing
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
    
    # Test normal operation
    try:
        with breaker:
            pass  # Successful operation
        print("  ✅ Normal operation works")
    except Exception as e:
        print(f"  ❌ Normal operation failed: {e}")
        return False
    
    # Test failure handling
    failure_count = 0
    try:
        for i in range(3):  # Exceed threshold
            try:
                with breaker:
                    raise Exception("Simulated failure")
            except Exception:
                failure_count += 1
                
        print(f"  ✅ Failure handling works ({failure_count} failures recorded)")
    except Exception as e:
        print(f"  ❌ Failure handling error: {e}")
        return False
    
    # Test that circuit breaker is now open
    try:
        with breaker:
            pass
        print("  ❌ Circuit breaker should be open!")
        return False
    except CircuitBreakerError:
        print("  ✅ Circuit breaker correctly opened after failures")
    
    # Test manual reset
    breaker.manual_reset()
    try:
        with breaker:
            pass
        print("  ✅ Manual reset works")
    except Exception as e:
        print(f"  ❌ Manual reset failed: {e}")
        return False
    
    # Test status reporting
    status = breaker.get_status()
    assert "state" in status
    assert "failure_count" in status
    print("  ✅ Status reporting works")
    
    print("✅ Circuit breaker working correctly!\n")
    return True


def test_emergency_controls():
    """Test emergency control functionality"""
    print("🧪 Testing Emergency Controls...")
    
    # Reset emergency controller
    emergency_controller.reset_emergency_stop()
    
    # Test operation registration
    try:
        with SafeOperation("test_op", "Test operation"):
            status = emergency_controller.get_status()
            assert status["active_operations"] == 1
            print("  ✅ Operation registration works")
            
        # Should be unregistered now
        status = emergency_controller.get_status()
        assert status["active_operations"] == 0
        print("  ✅ Operation unregistration works")
    except Exception as e:
        print(f"  ❌ Operation registration failed: {e}")
        return False
    
    # Test emergency stop
    try:
        emergency_controller.reset_emergency_stop()
        result = emergency_controller.emergency_stop("Test emergency stop")
        assert result["status"] == "emergency_stop_executed"
        assert emergency_controller.is_stop_requested()
        print("  ✅ Emergency stop works")
    except Exception as e:
        print(f"  ❌ Emergency stop failed: {e}")
        return False
    
    # Test stop signal checking
    try:
        emergency_controller.check_stop_signal()
        print("  ❌ Stop signal check should have raised exception!")
        return False
    except EmergencyStopError:
        print("  ✅ Stop signal detection works")
    
    print("✅ Emergency controls working correctly!\n")
    return True


def test_recursion_limits():
    """Test recursion depth limits"""
    print("🧪 Testing Recursion Limits...")
    
    # Reset emergency controller and set low limit for testing
    emergency_controller.reset_emergency_stop()
    emergency_controller.set_safety_limits(max_recursion_depth=3)
    
    def recursive_test(depth: int):
        """Recursive function for testing"""
        operation_id = f"recursive_test_{depth}"
        with SafeOperation(operation_id, f"Recursive test depth {depth}", is_recursive=True) as op:
            current_depth = op.get_recursion_depth()
            print(f"    Depth {current_depth}: OK")
            
            if depth > 1:
                recursive_test(depth - 1)
    
    # Test normal recursion within limits
    try:
        recursive_test(2)  # Should work (depths 1, 2)
        print("  ✅ Normal recursion within limits works")
    except Exception as e:
        print(f"  ❌ Normal recursion failed: {e}")
        return False
    
    # Test recursion exceeding limits
    try:
        recursive_test(5)  # Should fail (exceeds limit of 3)
        print("  ❌ Recursion limit should have been enforced!")
        return False
    except EmergencyStopError as e:
        if "recursion depth exceeded" in str(e).lower():
            print("  ✅ Recursion limit correctly enforced")
        else:
            print(f"  ❌ Wrong error type: {e}")
            return False
    
    print("✅ Recursion limits working correctly!\n")
    return True


def test_timeout_limits():
    """Test operation timeout limits"""
    print("🧪 Testing Timeout Limits...")
    
    # Reset emergency controller and set short timeout for testing
    emergency_controller.reset_emergency_stop()
    emergency_controller.set_safety_limits(max_operation_time=2)  # 2 seconds
    
    # Test normal operation within timeout
    try:
        with SafeOperation("quick_test", "Quick test operation") as op:
            time.sleep(0.5)  # Short delay
            op.check_stop()  # Should not timeout
        print("  ✅ Normal operation within timeout works")
    except Exception as e:
        print(f"  ❌ Normal operation failed: {e}")
        return False
    
    # Test operation exceeding timeout
    try:
        with SafeOperation("slow_test", "Slow test operation") as op:
            time.sleep(3)  # Longer than timeout
            op.check_stop()  # Should timeout
        print("  ❌ Timeout limit should have been enforced!")
        return False
    except EmergencyStopError as e:
        if "timeout exceeded" in str(e).lower():
            print("  ✅ Timeout limit correctly enforced")
        else:
            print(f"  ❌ Wrong error type: {e}")
            return False
    
    print("✅ Timeout limits working correctly!\n")
    return True


def main():
    """Run all safety feature tests"""
    print("🔒 Safety Features Test Suite")
    print("=" * 40)
    
    tests = [
        test_enum_definitions,
        test_circuit_breaker,
        test_emergency_controls,
        test_recursion_limits,
        test_timeout_limits
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("=" * 40)
    print(f"🎯 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All safety features working correctly!")
        return True
    else:
        print("⚠️ Some safety features need attention!")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)