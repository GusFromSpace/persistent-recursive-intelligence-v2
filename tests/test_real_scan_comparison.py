#!/usr/bin/env python3
"""
Test scan comparison with real PRI issues files
"""

import json

def test_real_scan_comparison():
    """Test scan comparison with real issues"""

    print("🔄 Testing Real PRI Scan Comparison")
    print("=" * 45)

    # Load both files
    with open('issues_subset.json', 'r') as f:
        previous_issues = json.load(f)

    with open('issues_subset_manual_fixed.json', 'r') as f:
        current_issues = json.load(f)

    print(f"📁 Previous scan: {len(previous_issues)} issues")
    print(f"📁 Current scan: {len(current_issues)} issues")

    # Create signatures for comparison
    def create_signature(issue):
        file_path = issue.get('file_path', issue.get('file', ''))
        return f"{issue.get('type')}|{file_path}|{issue.get('line', 0)}|{issue.get('description', '')[:50]}"

    previous_signatures = {create_signature(issue) for issue in previous_issues}
    current_signatures = {create_signature(issue) for issue in current_issues}

    # Find resolved issues
    resolved_signatures = previous_signatures - current_signatures

    print(f"\n🛠️  Issues resolved: {len(resolved_signatures)}")

    if resolved_signatures:
        print("📋 Top 5 Resolved Issues:")
        for i, signature in enumerate(list(resolved_signatures)[:5]):
            parts = signature.split('|')
            print(f"   {i+1}. {parts[0]} in {parts[1]} line {parts[2]}")
            print(f"      Description: {parts[3][:60]}...")

    # Find new issues
    new_signatures = current_signatures - previous_signatures
    print(f"\n🆕 New issues: {len(new_signatures)}")

    # Calculate fix rates
    total_resolved = len(resolved_signatures)
    manual_fixes_detected = total_resolved  # In this test, all would be manual
    manual_fix_rate = manual_fixes_detected / max(total_resolved, 1)

    print(f"\n📊 Analysis Results:")
    print(f"   • Total resolved: {total_resolved}")
    print(f"   • Manual fixes detected: {manual_fixes_detected}")
    print(f"   • Manual fix rate: {manual_fix_rate:.1%}")
    print(f"   • Issues remaining: {len(current_issues)}")

    # Analyze types of manually fixed issues
    if resolved_signatures:
        issue_types = {}
        for signature in resolved_signatures:
            issue_type = signature.split('|')[0]
            issue_types[issue_type] = issue.get(issue, 0) + 1

        print(f"\n🔧 Types of Manual Fixes:")
        for issue_type, count in sorted(issue_types.items(), key=lambda x: x[1], reverse=True):
            print(f"   • {issue_type}: {count} fixes")

    print("\n✅ Real scan comparison completed!")

    if total_resolved > 5:
        print(f"\n💡 This demonstrates how PRI can detect significant manual intervention")
        print(f"   between scans and learn from human fix patterns.")

if __name__ == "__main__":
    test_real_scan_comparison()