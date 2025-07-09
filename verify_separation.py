#!/usr/bin/env python3
"""
Verify both projects work after OpenMW separation
"""

import sys
import subprocess
import json
from pathlib import Path

def test_pri_functionality():
    """Test core PRI functionality"""
    print("🔍 Testing PRI Core Functionality...")
    print("=" * 50)
    
    # Test mesopredator command
    try:
        result = subprocess.run(['mesopredator', '--help'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Mesopredator CLI: Working")
        else:
            print("❌ Mesopredator CLI: Failed")
            return False
    except Exception as e:
        print(f"❌ Mesopredator CLI: Error - {e}")
        return False
    
    # Test analysis on a small directory
    try:
        result = subprocess.run(['mesopredator', 'analyze', 'src/utils'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "Analysis complete" in result.stdout:
            print("✅ PRI Analysis: Working")
        else:
            print("❌ PRI Analysis: Failed")
            print(f"Output: {result.stdout[:200]}...")
            return False
    except Exception as e:
        print(f"❌ PRI Analysis: Error - {e}")
        return False
    
    print("✅ PRI Project: All tests passed!")
    return True

def test_openmw_functionality():
    """Test OpenMW semantic bridge functionality"""
    print("\n🔍 Testing OpenMW Semantic Integration...")
    print("=" * 50)
    
    openmw_path = Path("/home/gusfromspace/Development/openmw-semantic-integration")
    
    # Test optimized bridge directly
    bridge_script = openmw_path / "src/bridge/optimized_semantic_bridge.py"
    if not bridge_script.exists():
        print("❌ Optimized bridge script not found")
        return False
    
    try:
        result = subprocess.run([sys.executable, str(bridge_script)], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and "SUCCESS" in result.stdout:
            print("✅ Optimized Semantic Bridge: Working")
        else:
            print("❌ Optimized Semantic Bridge: Failed")
            print(f"Output: {result.stdout[:300]}...")
            return False
    except Exception as e:
        print(f"❌ Optimized Semantic Bridge: Error - {e}")
        return False
    
    # Check if semantic databases exist
    semantic_dbs = list((openmw_path / "data/semantic").glob("*.db"))
    if semantic_dbs:
        print(f"✅ Semantic Databases: Found {len(semantic_dbs)} databases")
    else:
        print("⚠️  Semantic Databases: None found (may need to be regenerated)")
    
    # Check if Lua files exist
    lua_files = list((openmw_path / "src/lua").glob("*.lua"))
    if lua_files:
        print(f"✅ Lua Scripts: Found {len(lua_files)} scripts")
    else:
        print("❌ Lua Scripts: None found")
        return False
    
    print("✅ OpenMW Project: Core functionality verified!")
    return True

def verify_separation_cleanliness():
    """Verify OpenMW files are properly separated"""
    print("\n🔍 Verifying Separation Cleanliness...")
    print("=" * 50)
    
    pri_path = Path("/home/gusfromspace/Development/persistent-recursive-intelligence")
    
    # Check for remaining OpenMW files in PRI
    openmw_patterns = ["*openmw*", "*morrowind*", "*semantic_bridge*", "*.lua"]
    remaining_files = []
    
    for pattern in openmw_patterns:
        files = list(pri_path.glob(pattern))
        remaining_files.extend([f for f in files if f.name != "cleanup_openmw_files.sh"])
    
    if remaining_files:
        print(f"⚠️  Found {len(remaining_files)} OpenMW-related files still in PRI:")
        for f in remaining_files[:5]:  # Show first 5
            print(f"   - {f.name}")
        if len(remaining_files) > 5:
            print(f"   ... and {len(remaining_files) - 5} more")
    else:
        print("✅ PRI Project: Clean of OpenMW files")
    
    # Check OpenMW project has files
    openmw_path = Path("/home/gusfromspace/Development/openmw-semantic-integration")
    if openmw_path.exists():
        total_files = len(list(openmw_path.rglob("*.py"))) + len(list(openmw_path.rglob("*.lua")))
        print(f"✅ OpenMW Project: Contains {total_files} code files")
        return True
    else:
        print("❌ OpenMW Project: Directory not found")
        return False

def main():
    print("🚀 Separation Verification Test Suite")
    print("=" * 60)
    
    results = {
        "pri_functionality": test_pri_functionality(),
        "openmw_functionality": test_openmw_functionality(), 
        "separation_cleanliness": verify_separation_cleanliness()
    }
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
    
    overall_success = all(results.values())
    print(f"\n🎯 Overall Result: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")
    
    if overall_success:
        print("\n🎉 Both projects are working correctly after separation!")
        print("✅ PRI can continue as a focused code analysis tool")
        print("✅ OpenMW integration can develop independently")
    else:
        print("\n⚠️  Some issues found. Review the details above.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    sys.exit(main())