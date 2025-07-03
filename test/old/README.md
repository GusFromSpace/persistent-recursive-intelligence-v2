# Outdated Tests Archive

This directory contains test files that were designed for older versions of the Mesopredator PRI system and are no longer compatible with the current architecture.

## Moved Tests and Issues

### Tests with Old CLI Interface
- `gray_hat_ethics_test.py` - Uses deprecated `src.cognitive.persistent_recursion` CLI interface
- `orchestrator_synthesis_test.py` - Designed for older orchestration system

### Tests with Import Path Issues  
- `test_basic_safety.py` - Wrong import paths (`safety.*` instead of `src.safety.*`)
- `test_emergency_scenarios.py` - Missing logger imports, wrong safety module paths
- `test_enhanced_safety_features.py` - Import errors with safety framework
- `test_external_project_safety.py` - Import path mismatches
- `test_safety_features.py` - Outdated safety module references
- `safety_escape_test.py` - Uses old import structure

### Tests with Logger Issues
- `test_debugging_capabilities.py` - Uses old logger import pattern
- `test_field_shaping.py` - Missing logger singleton initialization  
- `test_memory_intelligence_integration.py` - Logger import errors
- `test_self_analysis_comprehensive.py` - Logger dependency issues
- `test_stress_testing.py` - Logger import problems

### Tests with Enum/Model Issues
- `test_enhanced_pri_integration.py` - SystemType enum attribute errors
- `test_feedback_demo.py` - Missing file references

### Tests for Deprecated Features
- `test_real_cpp_project.py` - Uses deprecated analysis interfaces
- `test_real_world_dogfooding.py` - Tests old dogfooding patterns

## Why These Tests Failed

1. **Architecture Change**: The system moved from analysis-only to interactive fix application with defense-in-depth security
2. **Import Structure**: Module paths changed from flat structure to hierarchical (`safety.*` → `src.safety.*`)
3. **Logger Refactor**: Centralized logging system introduced but singleton pattern incomplete
4. **CLI Interface**: Main interface changed from `src.cognitive.persistent_recursion` to `mesopredator_cli.py`
5. **Security Focus**: Tests designed for older system without the 4-layer defense architecture

## What These Tests Were Trying to Validate

- **Gray Hat Ethics**: Ethical boundary testing (important but needs rewriting for new CLI)
- **Safety Escape**: Bypass attempt testing (needs new import paths)
- **Emergency Scenarios**: Multi-scenario safety testing (needs logger fixes)
- **Memory Integration**: Persistent learning validation (needs import fixes)
- **Field Shaping**: Educational enhancement testing (needs logger fixes)

## Next Steps

These tests represent important validation scenarios that should be:
1. **Rewritten** for the current architecture
2. **Updated** with correct import paths and logger usage  
3. **Adapted** to test the new defense-in-depth security system
4. **Integrated** with the current CLI interface (`mesopredator fix`)

The core test logic is valuable but needs modernization for the current system.