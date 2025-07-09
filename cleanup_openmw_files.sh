#!/bin/bash
# Cleanup script to remove OpenMW files that have been migrated

echo "OpenMW File Cleanup for PRI Project"
echo "==================================="
echo "This will remove OpenMW-related files that have been migrated to the dedicated project."
echo ""

# Confirm before proceeding
read -p "Are you sure you want to remove OpenMW files from PRI? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cleanup cancelled."
    exit 1
fi

echo ""
echo "Removing migrated files..."

# Python files
rm -f optimized_semantic_bridge.py
rm -f semantic_bridge_integration.py
rm -f mesopredator_metrics_bridge.py
rm -f mesopredator_bloodlust_hunter.py
rm -f enhanced_bloodlust_hunter.py
rm -f real_hunting_cycles.py
rm -f openmw_real_bloodlust_cycles.py
rm -f openmw_seven_cycles_hunt.py
rm -f morrowind_esm_extractor.py
rm -f interactive_objects_extractor.py
rm -f smart_object_selection.py
rm -f test_openmw_with_optimizations.py
rm -f build_and_test_semantic_bridge.py
rm -f build_and_test_optimized_bridge.py
rm -f simple_openmw_test.py
rm -f quick_openmw_test.py
rm -f openmw_metrics_integration_installer.py
rm -f build_semantic_integration.py
rm -f dynamic_connector_cli.py
rm -f openmw_minimal_metrics_api.py
rm -f openmw_launch_script.sh

# Lua files
rm -f fast_semantic_api.lua
rm -f intelligent_npc.lua
rm -f quest_semantic.lua
rm -f semantic_bridge_test.lua
rm -f semantic_search_api_docs.lua
rm -f smart_guard.lua
rm -f comprehensive_semantic_demo.lua

# C++ files
rm -f semantic_bridge_binding.cpp

# Database files
rm -f morrowind_semantic.db
rm -f morrowind_comprehensive_semantic.db
rm -f morrowind_interactive_semantic.db
rm -f morrowind_strategic_semantic.db
rm -f test_semantics.db

# JSON files
rm -f comprehensive_interactive_objects.json
rm -f morrowind_complete_objects.json
rm -f morrowind_comprehensive_semantic_metadata.json
rm -f morrowind_extraction_stats.json
rm -f morrowind_interactive_semantic_metadata.json
rm -f morrowind_semantic_metadata.json
rm -f morrowind_strategic_semantic_metadata.json
rm -f strategic_semantic_selection.json
rm -f integration_opportunities.json
rm -f semantic_bridge_integration_plan.json
rm -f semantic_bridge_performance_report.json
rm -f semantic_bridge_test_report.json
rm -f optimized_bridge_safety_report.json

# Cycle files
rm -f hunt_cycle_*_scan.json
rm -f openmw_cycle_*_results.json
rm -f openmw_bloodlust_cycle_*_scan.json
rm -f openmw_bloodlust_cycles_*.json
rm -f openmw_seven_cycles_hunt_*.json
rm -f real_hunting_cycles_*.json

# Report files
rm -f openmw_gameplay_test_report.json
rm -f openmw_hunting_results.json
rm -f openmw_integration_analysis.json
rm -f openmw_semantic_analysis.json
rm -f openmw_analysis_results.json
rm -f openmw_post_bloodlust_scan.json
rm -f mesopredator_hunt_report.json
rm -f enhanced_bloodlust_hunt_report.json

# Markdown files
rm -f semantic_bridge_plan.md

# Documentation files (already moved from docs/)
# Note: docs/adr/ADR-037-OpenMW-Semantic-Bridge.md was already handled
# Note: docs/SEMANTIC_BRIDGE_OPTIMIZATION_REPORT.md was already handled

echo ""
echo "Checking for large directories..."

# Check if large directories exist
if [ -d "openmw_analysis" ]; then
    echo "Found openmw_analysis/ directory (OpenMW source clone)"
    read -p "Remove openmw_analysis/? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf openmw_analysis/
        echo "Removed openmw_analysis/"
    fi
fi

if [ -d "openmw_metrics_integration" ]; then
    echo "Found openmw_metrics_integration/ directory (OpenMW build)"
    read -p "Remove openmw_metrics_integration/? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf openmw_metrics_integration/
        echo "Removed openmw_metrics_integration/"
    fi
fi

echo ""
echo "Cleanup complete!"
echo ""
echo "Remaining OpenMW-related files (if any):"
ls -la | grep -E "(openmw|morrowind|semantic_bridge)" | wc -l