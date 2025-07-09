#!/usr/bin/env python3
"""
Simple test to demonstrate scan comparison without memory dependencies
"""

import json

def test_scan_comparison():
    """Test scan comparison logic"""

    print("🔄 Testing Scan Comparison Logic")
    print("=" * 40)

    # Load both files
    with open('test_issues_small.json', 'r') as f:
        previous_issues = json.load(f)

    with open('test_issues_after_manual_fix.json', 'r') as f:
        current_issues = json.load(f)

    print(f"📁 Previous scan: {len(previous_issues)} issues")
    print(f"📁 Current scan: {len(current_issues)} issues")

    # Create signatures for comparison
    def create_signature(issue):
        return f"{issue.get('type')}|{issue.get('file_path', '')}|{issue.get('line', 0)}|{issue.get('description', '")[:50]}"

    previous_signatures = {create_signature(issue) for issue in previous_issues}
    current_signatures = {create_signature(issue) for issue in current_issues}

    # Find resolved issues
    resolved_signatures = previous_signatures - current_signatures

    print(f"\n🛠️  Issues resolved: {len(resolved_signatures)}")

    if resolved_signatures:
        print("📋 Resolved Issues:")
        for signature in resolved_signatures:
            parts = signature.split('|')
            print(f"   • {parts[0]} in {parts[1]} - {parts[3][:40]}...")

    # Find new issues
    new_signatures = current_signatures - previous_signatures
    print(f"\n🆕 New issues: {len(new_signatures)}")

    if new_signatures:
        print("📋 New Issues:")
        for signature in new_signatures:
            parts = signature.split('|')
            print(f"   • {parts[0]} in {parts[1]} - {parts[3][:40]}...")

    print("\n✅ Scan comparison completed!")

    # Show that this would be detected as a manual fix
    if resolved_signatures:
        print(f"\n💡 In a real scenario, these {len(resolved_signatures)} resolved issues would be")
        print("   marked as manual fixes since they weren't fixed by PRI's automated process.")

if __name__ == "__main__":
    test_scan_comparison()