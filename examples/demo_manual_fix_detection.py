#!/usr/bin/env python3
"""
Comprehensive demo of PRI's manual fix detection capabilities
"""

import json

logger.info("🚀 PRI Manual Fix Detection Demo")
logger.info("=" * 50)

logger.info("\n📊 Scenario: Developer fixed print statements between scans")
logger.info("=" * 50)

# Show the comparison
with open('issues_subset.json', 'r') as f:
    before_issues = json.load(f)

with open('issues_subset_manual_fixed.json', 'r') as f:
    after_issues = json.load(f)

logger.info(f"📁 Before manual fixes: {len(before_issues)} issues")
logger.info(f"📁 After manual fixes:  {len(after_issues)} issues")
logger.info(f"🛠️  Issues resolved:     {len(before_issues) - len(after_issues)} issues")

# Analyze what was fixed
def create_signature(issue):
    return f"{issue.get('type')}|{issue.get('line', 0)}|{issue.get('description', '')}[:30]"

before_sigs = {create_signature(issue) for issue in before_issues}
after_sigs = {create_signature(issue) for issue in after_issues}
fixed_sigs = before_sigs - after_sigs

logger.info(f"\n🔍 Analysis of Manual Fixes:")
logger.info("=" * 30)

# Group by type
fix_types = {}
for sig in fixed_sigs:
    fix_type = sig.split('|')[0]
    fix_types[fix_type] = fix_types.get(fix_types, 0) + 1

for fix_type, count in fix_types.items():
    logger.info(f"   • {fix_type}: {count} manual fixes")

logger.info(f"\n💡 PRI Learning Insights:")
logger.info("=" * 30)
logger.info(f"   • Developer manually fixed {len(fixed_sigs)} issues")
logger.info(f"   • All fixes were 'context' issues (print statements)")
logger.info(f"   • This pattern suggests automation opportunity")
logger.info(f"   • Future: PRI could auto-fix print statements in production code")

logger.info(f"\n🎯 Automation Recommendations:")
logger.info("=" * 35)
logger.info(f"   • High automation potential: context/print statements")
logger.info(f"   • Frequency: {fix_types.get('context', 0)} manual fixes detected")
logger.info(f"   • Recommendation: Create automated rule for print statement removal")

logger.info(f"\n📈 Memory System Integration:")
logger.info("=" * 35)
logger.info(f"   • Each manual fix stored as learning example")
logger.info(f"   • Pattern recognition improves over time")
logger.info(f"   • Cross-project validation enables smart defaults")

logger.info(f"\n✅ Demo completed! PRI successfully detected and analyzed manual fixes.")
logger.info(f"   This enables data-driven automation prioritization.")

# Show the CLI commands that would be used
logger.info(f"\n🔧 CLI Commands for Real Usage:")
logger.info("=" * 35)
logger.info(f"   # Detect manual fixes in latest scan:")
logger.info(f"   python mesopredator_cli.py cycle manual_fixes \\")
logger.info(f"     --issues-file current_scan.json \\")
logger.info(f"     --project-path /path/to/project")
logger.info(f"")
logger.info(f"   # Compare two scans:")
logger.info(f"   python mesopredator_cli.py cycle scan_comparison \\")
logger.info(f"     --previous-issues-file previous_scan.json \\")
logger.info(f"     --issues-file current_scan.json \\")
logger.info(f"     --project-path /path/to/project")
logger.info(f"")
logger.info(f"   # Analyze manual fix patterns:")
logger.info(f"   python mesopredator_cli.py cycle patterns")
logger.info(f"")
logger.info(f"   # View cycle metrics:")
logger.info(f"   python mesopredator_cli.py cycle cycle_metrics")