#!/usr/bin/env python3
"""
Test script for cycle tracking without FAISS dependency
"""

import json
import sys
from pathlib import Path
import asyncio
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Mock the memory engine to avoid FAISS dependency
class MockMemoryEngine:
    def __init__(self):
        self.memories = []

    async def search_memories(self, query):
        # Return empty result for testing
        class MockResult:
            def __init__(self):
                self.memories = []
        return MockResult()

    async def store_memory(self, memory):
        self.memories.append(memory)
        return f"memory_{len(self.memories)}"

    async def list_namespaces(self):
        return []

    async def delete_memory(self, memory_id):
        pass

# Import and test cycle tracker
from cognitive.enhanced_patterns.improvement_cycle_tracker import ImprovementCycleTracker

async def test_manual_fix_detection():
    """Test manual fix detection with real data"""

    print("🔄 Testing PRI Cycle Tracking")
    print("=" * 40)

    # Initialize with mock memory engine
    mock_memory = MockMemoryEngine()
    cycle_tracker = ImprovementCycleTracker(mock_memory)

    # Load the issues file
    try:
        with open('issues.json', 'r') as f:
            issues = json.load(f)
        print(f"📁 Loaded {len(issues)} issues from issues.json")
    except FileNotFoundError:
        print("❌ issues.json not found")
        return

    # Test issue signature creation
    print("\n🔍 Testing issue signature creation...")
    project_path = "/home/gusfromspace/Development/persistent-recursive-intelligence"

    # Test with first few issues
    test_issues = issues[:5]
    signatures = []

    for issue in test_issues:
        signature = cycle_tracker._create_issue_signature(issue, project_path)
        signatures.append(signature)
        print(f"   Issue: {issue.get('type', 'unknown")} -> Signature: {signature[:60]}...")

    print("\n📊 Testing scan comparison...")

    metrics = await cycle_tracker.track_scan_comparison_metrics(
        issues, issues, project_path  # Same issues = no changes
    )

    if metrics:
        print(f"   Previous issues: {metrics['previous_issues_count']}")
        print(f"   Current issues: {metrics['current_issues_count']}")
        print(f"   Manual fixes detected: {metrics['manual_fixes_detected']}")
        print(f"   Manual fix rate: {metrics['manual_fix_rate']:.1%}")

    print("\n🛠️  Testing with simulated manual fix...")

    modified_issues = issues[1:]  # Remove first issue

    # Start an improvement cycle for the "removed" issue
    removed_issue = issues[0]
    cycle_id = await cycle_tracker.start_improvement_cycle(
        removed_issue,
        removed_issue.get('file_path', 'test_file.py'),
        {"file_context": removed_issue.get('context', 'test')}
    )

    print(f"   Started cycle: {cycle_id}")

    # Now detect manual fixes
    manual_fixes = await cycle_tracker.detect_manual_fixes_in_scan(
        modified_issues, project_path
    )

    print(f"   Manual fixes detected: {len(manual_fixes)}")
    for fix in manual_fixes:
        print(f"   • {fix['issue_type']} in {fix.get('file_path', 'unknown")}")

    # Test cycle metrics
    print("\n📈 Testing cycle metrics...")

    cycle_metrics = await cycle_tracker.analyze_cycle_patterns()
    print(f"   Total cycles: {cycle_metrics.total_cycles}")
    print(f"   Success rate: {cycle_metrics.success_rate:.1%}")
    print(f"   Learning velocity: {cycle_metrics.learning_velocity:.2f} cycles/day")

    print("\n✅ Cycle tracking test completed!")

if __name__ == "__main__":
    asyncio.run(test_manual_fix_detection())