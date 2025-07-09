# PRI Hydra Cleanup Plan

**Issue:** PRI has become a hydra with 40+ scattered executable scripts  
**Goal:** Single orchestrated entry point (`mesopredator` command) that controls everything

## Current Hydra Heads (40+ Scripts)

### Core Testing/Validation Scripts
- `test_integration.py`
- `verify_security_fix.py` 
- `final_separation_verification.py`
- `verify_separation.py`

### Adversarial Testing Scripts
- `run_comprehensive_adversarial_tests.py`
- `run_complete_adversarial_test_suite.py`
- `run_current_test_suite.py`
- `run_all_adversarial_tests.py`
- `test_*_adversarial.py` (multiple)

### Auto-Fixing Scripts
- `self_fix.py`
- `advanced_syntax_fixer.py`
- `enhanced_security_patch.py`
- `emergency_security_patch.py`

### Analysis/Demo Scripts
- `demo_interactive_approval.py`
- `demo_persistent_intelligence.py`
- `analyze_cpp_project.py`
- `enhanced_analysis_formatter.py`

### Testing Utilities
- `test_hello_world_debugging.py`
- `test_memory_fix.py`
- `test_cycle_tracking.py`
- `safe_recursive_test.py`

## Consolidation Strategy

### Phase 1: Extend Main CLI
Add new subcommands to `mesopredator_cli.py`:

```bash
mesopredator test             # Run integration tests
mesopredator test --adversarial  # Run adversarial test suite
mesopredator validate         # Security validation
mesopredator demo            # Interactive demos
mesopredator self-fix        # Auto-fix PRI itself
mesopredator cleanup         # Memory cleanup (auto-prune)
```

### Phase 2: Archive Old Scripts
Move all standalone scripts to `archive/` directory

### Phase 3: Automatic Operations
Implement auto-pruning that runs:
- After every 10 analysis operations
- On startup if memory usage > threshold
- Daily via cron/scheduler
- When user runs `mesopredator cleanup`

## Benefits
- **Single Entry Point**: `mesopredator` command does everything
- **Consistent Interface**: All operations use same CLI patterns
- **Auto-Maintenance**: Automatic memory pruning keeps system optimized
- **Reduced Complexity**: No scattered scripts to maintain
- **Better UX**: Users learn one command instead of 40+

## Implementation Progress

### ✅ Completed (High Priority)
1. **Auto-pruning**: Implemented auto-pruning in existing CLI
   - Runs on startup if memory > 10,000 entries
   - Available via `mesopredator prune` command
   - Multiple strategies: age_based, redundancy_based, quality_based, hybrid

2. **Consolidation Analysis**: Added `mesopredator consolidate` command
   - Automatically categorizes 42 scattered scripts
   - Identifies testing (24), validation (5), analysis (3), demos (2), utilities (1), other (4) scripts
   - Provides detailed consolidation proposals
   - Preview mode available with `--preview` flag

### 🔄 In Progress (High Priority)
3. **Add `mesopredator test` and `mesopredator validate`**: Next phase
   - Framework for consolidation is ready
   - Need to implement actual consolidation of 24 test scripts
   - Need to implement actual consolidation of 5 validation scripts

### 📋 Remaining (Medium Priority)
4. **Archive standalone scripts**: Ready for implementation
   - `--archive` flag prepared
   - Archive directory structure planned
5. **Add demo and advanced features**: Planned
   - `mesopredator demo` command identified for 2 demo scripts

## Next Steps
1. Implement `mesopredator test` subcommand with adversarial test integration
2. Implement `mesopredator validate` subcommand for security validation
3. Archive old scripts using `mesopredator consolidate --archive`
4. Add `mesopredator demo` for interactive demonstrations