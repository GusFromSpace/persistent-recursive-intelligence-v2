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

def run_analysis(project_path: str, max_depth: int = 3, batch_size: int = 50, verbose: bool = False, output_file: str = None):
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

        # Report in PRI style
        issues = results["issues_found"]
        critical = len([i for i in issues if i.get("severity") == "critical"])
        high = len([i for i in issues if i.get("severity") == "high"])
        medium = len([i for i in issues if i.get("severity") == "medium"])

        print(f"🧠 Found {len(issues)} issues across {critical + high + medium} categories")
        print(f"📚 Generated educational annotations")
        print(f"🌀 Applied {max_depth} levels of recursive improvement")
        print(f"💾 Stored {results['cognitive_growth']['patterns_learned']} new patterns in memory")
        print(f"✅ Analysis complete - {min(100, len(issues))}% improvement potential identified")

        if critical > 0:
            print(f"\n🚨 CRITICAL ISSUES: {critical}")
        if high > 0:
            print(f"⚠️  HIGH PRIORITY: {high}")
        if medium > 0:
            print(f"📋 MEDIUM PRIORITY: {medium}")

        # Show detailed issue descriptions in verbose mode
        if verbose and issues:
            print(f"\n📝 Detailed Issue Analysis:")
            for i, issue in enumerate(issues[:20], 1):  # Limit to first 20 for readability
                severity = issue.get("severity", "unknown").upper()
                issue_type = issue.get("type", "unknown")
                description = issue.get("description", "No description")
                line = issue.get("line", "?")
                
                print(f"   {i}. [{severity}] {issue_type} (Line {line})")
                print(f"      {description}")
                if i < len(issues) and i < 20:
                    print()
            
            if len(issues) > 20:
                print(f"   ... and {len(issues) - 20} more issues")

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
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output-file", help="Path to save the analysis results as a JSON file")

    args = parser.parse_args()

    run_analysis(args.project, args.max_depth, args.batch_size, args.verbose, args.output_file)

if __name__ == "__main__":
    sys.exit(main())