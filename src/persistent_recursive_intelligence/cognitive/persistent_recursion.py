#!/usr/bin/env python3
"""
PRI Main Entry Point - Persistent Recursive Intelligence
This module provides the standard interface described in the USER_MANUAL
"""

import sys
import argparse
from pathlib import Path

# Import the enhanced recursive improvement engine
from .recursive.recursive_improvement_enhanced import MemoryEnhancedRecursiveImprovement

import json

def run_analysis(project_path: str, max_depth: int = 3, batch_size: int = 50, verbose: bool = False, output_file: str = None, quick: bool = False):
    """Main entry point for PRI persistent recursive analysis"""
    project_path = Path(project_path).resolve()

    if not project_path.exists():
        print(f"❌ Project path does not exist: {project_path}")
        return 1

    print(f"🌀 PRI Analysis: {project_path.name}")
    print(f"🔍 Scanning {project_path}...")

    try:
        # Initialize and run full project analysis
        engine = MemoryEnhancedRecursiveImprovement(project_path)

        results = engine.run_improvement_iteration(max_depth=max_depth, batch_size=batch_size)

        # Report in PRI style with smart filtering
        issues = results["issues_found"]
        
        # Filter issues based on mode
        if quick:
            # Quick mode: only critical security issues and high-impact bugs
            actionable_issues = [i for i in issues if 
                               (i.get("severity") == "critical") or 
                               (i.get("severity") == "high" and 
                                i.get("type") in ["security", "vulnerability", "sql_injection", "xss", "buffer_overflow", 
                                                "memory_leak", "deadlock", "race_condition"])]
            issues_to_show = actionable_issues
            mode_desc = "Quick Mode - Critical Security & High-Impact Issues Only"
        elif verbose:
            # Verbose mode: show everything
            issues_to_show = issues
            mode_desc = "Verbose Mode - All Issues"
        else:
            # Default mode: smart filtering to show actionable issues
            issues_to_show = [i for i in issues if 
                            (i.get("severity") in ["critical", "high"]) and
                            (i.get("type") not in ["context", "legitimate_logging", "info"])]
            mode_desc = "Standard Mode - Critical & High Priority Issues"
        
        # Count issues by severity
        critical = len([i for i in issues if i.get("severity") == "critical"])
        high = len([i for i in issues if i.get("severity") == "high"])
        medium = len([i for i in issues if i.get("severity") == "medium"])
        
        print(f"🧠 Found {len(issues)} total issues, showing {len(issues_to_show)} actionable issues")
        print(f"📚 Generated educational annotations")
        print(f"🌀 Applied {max_depth} levels of recursive improvement")
        print(f"💾 Stored {results['cognitive_growth']['patterns_learned']} new patterns in memory")
        print(f"✅ Analysis complete - {mode_desc}")

        # Show counts
        if critical > 0:
            print(f"\n🚨 CRITICAL ISSUES: {critical}")
        if high > 0:
            print(f"⚠️  HIGH PRIORITY: {high}")
        if medium > 0 and verbose:
            print(f"📋 MEDIUM PRIORITY: {medium}")
        elif medium > 0 and not verbose:
            print(f"📋 MEDIUM PRIORITY: {medium} (use --verbose to see)")

        # Show detailed issue descriptions
        if issues_to_show:
            print(f"\n📝 Actionable Issues:")
            display_limit = 50 if verbose else 20
            for i, issue in enumerate(issues_to_show[:display_limit], 1):
                severity = issue.get("severity", "unknown").upper()
                issue_type = issue.get("type", "unknown")
                description = issue.get("description", "No description")
                line = issue.get("line", "?")
                
                print(f"   {i}. [{severity}] {issue_type} (Line {line})")
                print(f"      {description}")
                if i < len(issues_to_show) and i < display_limit:
                    print()
            
            if len(issues_to_show) > display_limit:
                print(f"   ... and {len(issues_to_show) - display_limit} more actionable issues")
                if not verbose:
                    print(f"   Use --verbose to see all issues")
        else:
            print(f"\n✅ No actionable issues found! Code looks good.")
            if len(issues) > 0 and not verbose:
                print(f"   ({len(issues)} minor/informational issues found - use --verbose to see)")

        if output_file:
            with open(output_file, 'w') as f:
                json.dump(issues, f, indent=4)
            print(f"💾 Analysis results saved to {output_file}")

        return issues

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return 1

def main():
    """Main entry point for PRI persistent recursive analysis"""
    parser = argparse.ArgumentParser(description="Persistent Recursive Intelligence - Universal Codebase Analysis")
    parser.add_argument("--project", required=True, help="Path to project directory to analyze")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum recursive depth (default: 3)")
    parser.add_argument("--batch-size", type=int, default=50, help="Files per batch for processing (default: 50)")
    parser.add_argument("--verbose", action="store_true", help="Show all issues including minor ones")
    parser.add_argument("--quick", action="store_true", help="Quick mode: only show critical security issues")
    parser.add_argument("--output-file", help="Path to save the analysis results as a JSON file")

    args = parser.parse_args()

    run_analysis(args.project, args.max_depth, args.batch_size, args.verbose, args.output_file, args.quick)

if __name__ == "__main__":
    sys.exit(main())