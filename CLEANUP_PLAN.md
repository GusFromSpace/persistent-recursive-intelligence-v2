# Directory Cleanup Plan

**Generated:** 2025-07-03  
**Estimated Space Savings:** 200-300MB  
**Files to Remove:** ~50-70 redundant/obsolete files  

---

## 🗑️ **Safe to Remove**

### 1. Duplicate Test Results (Most Space Savings)

#### Old Complete Adversarial Test Reports
```bash
# Keep only the most recent report
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_090139.json
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_092748.json
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_094847.json
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_161055.json
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_162351.json
rm docs/reports/adversarial-tests/complete_adversarial_test_report_20250703_164203.json
# KEEP: complete_adversarial_test_report_20250703_164451.json (most recent)
```

#### Duplicate Claude Wrapper Analysis Files
```bash
# Keep most recent and comprehensive version
rm claude_wrapper_analysis.json
rm claude_wrapper_analysis_improved.json
rm claude_wrapper_enhanced_analysis.json
# KEEP: claude_wrapper_analysis_updated.json
```

#### Root-level Test Result Duplicates
```bash
rm conceptual_transfer_results.json
rm gray_hat_ethics_results.json
rm orchestrator_synthesis_results.json
rm safety_escape_results.json
# These exist in organized docs/reports/adversarial-tests/ location
```

#### Issues Files - Multiple Versions
```bash
rm issues_detailed.json
rm issues_subset.json
rm issues_subset_manual_fixed.json
rm test_issues_after_manual_fix.json
rm test_issues_small.json
rm v2_issues.json
rm post_fix_issues.json
rm recursive_issues.json
# KEEP: issues.json, issues-updated.json
```

### 2. Obsolete Documentation

#### Old API Documentation
```bash
rm docs/technical/API.md
# KEEP: docs/technical/API_CURRENT.md (accurate version)
```

#### Old Test Plan Versions
```bash
rm "Mesopredator: Adversarial Test Plan v2.0.md"
rm "docs/Mesopredator: Adversarial Test Plan.md"
# KEEP: "Mesopredator: Adversarial Test Plan v3.0.md"
```

### 3. Old Log Files

#### Test Logs
```bash
rm test_hello_world/logs/hello_world_20250621_191055.log
rm test_hello_world/logs/hello_world_20250622_082839.log
rm test_hello_world/logs/hello_world_20250628_104418.log
# KEEP: test_hello_world/logs/hello_world_20250703_082639.log (most recent)

rm logs/intelligence_20250624.log
```

### 4. Development Artifacts

#### Old Self-Analysis Files
```bash
rm pri_self_analysis_enhanced.json
rm v1_analysis.json
rm syntax_analysis.json
# KEEP: pri_self_analysis_with_paths.json
```

#### Connection Analysis
```bash
rm mesopredator_connection_analysis.json
# KEEP: mesopredator_final_connection_analysis.json
```

#### Training Data (Already Incorporated)
```bash
rm claude_wrapper_false_positive_training.json
rm claude_wrapper_training_batch.json
rm manual_fix_training_data.json
rm fix_generator_learning.json
```

### 5. Redundant Test Scripts

#### Multiple Ouroboros Test Versions
```bash
rm conceptual_ouroboros_test.py
rm focused_ouroboros_test.py
rm simple_ouroboros_test.py
rm targeted_ouroboros_test.py
# KEEP: safe_recursive_test.py
```

#### Fixed Test Versions
```bash
rm fixed_conceptual_transfer_test.py
rm fixed_conceptual_transfer_results.json
```

#### Single-Purpose Test Scripts
```bash
rm test_assumption_cascade_failure.py
rm test_basic_integration.py
rm test_conceptual_bug_transfer.py
rm test_emergency_simple.py
rm test_simple_comparison.py
rm marathon_endurance_test.py
```

### 6. Rebranding and Config Artifacts

#### Post-Rebranding Files
```bash
rm rebrand_mesopredator.py
rm rebranding_config.json
rm mesopredator_config.json
```

---

## ✅ **Must Keep - Critical Files**

### Core System Files
- `src/` (entire directory - core functionality)
- `requirements.txt`
- `pytest.ini`
- `README.md`
- `mesopredator_cli.py`
- `.github/workflows/` (CI/CD pipeline)

### Current Analysis & Data
- `memory.db` and `memory_intelligence.db` (functional databases)
- `issues.json` and `issues-updated.json` (current issue databases)
- `pri_self_analysis_with_paths.json` (most detailed self-analysis)
- `mesopredator_final_connection_analysis.json` (current connection analysis)
- `code_connector_metrics.json` (performance metrics)

### Documentation (Corrected Versions)
- `docs/adr/` (all Architecture Decision Records)
- `docs/technical/API_CURRENT.md` (accurate API docs)
- `docs/technical/STANDARDS_COMPLIANCE_AUDIT.md`
- `docs/technical/DOCUMENTATION_AUDIT_REPORT.md`
- `docs/user/USER_MANUAL.md`
- `docs/FEATURE_STATUS.md`

### Current Test Infrastructure
- `tests/` directory
- Active test scripts in `/test/old/` (may still be referenced)
- Most recent test results (dated 2025-07-03)

---

## 🔧 **Cleanup Execution Plan**

### Phase 1: Backup Critical Data
```bash
# Create backup of current state before cleanup
tar -czf pri_cleanup_backup_$(date +%Y%m%d).tar.gz \
  memory.db memory_intelligence.db issues.json issues-updated.json \
  mesopredator_final_connection_analysis.json
```

### Phase 2: Remove Duplicate Test Results
```bash
# Remove old adversarial test reports (keeping most recent)
find docs/reports/adversarial-tests/ -name "complete_adversarial_test_report_*.json" \
  ! -name "complete_adversarial_test_report_20250703_164451.json" -delete

# Remove root-level duplicate results
rm conceptual_transfer_results.json gray_hat_ethics_results.json \
   orchestrator_synthesis_results.json safety_escape_results.json
```

### Phase 3: Remove Obsolete Analysis Files
```bash
# Clean up old analysis files
rm claude_wrapper_analysis.json claude_wrapper_analysis_improved.json \
   claude_wrapper_enhanced_analysis.json pri_self_analysis_enhanced.json \
   v1_analysis.json syntax_analysis.json
```

### Phase 4: Remove Development Artifacts
```bash
# Clean up training data and development files
rm claude_wrapper_false_positive_training.json claude_wrapper_training_batch.json \
   manual_fix_training_data.json fix_generator_learning.json
```

### Phase 5: Remove Redundant Test Scripts
```bash
# Clean up duplicate test scripts
rm conceptual_ouroboros_test.py focused_ouroboros_test.py \
   simple_ouroboros_test.py targeted_ouroboros_test.py \
   fixed_conceptual_transfer_test.py
```

### Phase 6: Clean Up Issues Files
```bash
# Remove older issues files
rm issues_detailed.json issues_subset.json issues_subset_manual_fixed.json \
   test_issues_after_manual_fix.json test_issues_small.json v2_issues.json \
   post_fix_issues.json recursive_issues.json
```

### Phase 7: Remove Old Logs
```bash
# Clean up old log files
rm test_hello_world/logs/hello_world_202506*.log
rm test_hello_world/logs/hello_world_20250628*.log
rm logs/intelligence_20250624.log 2>/dev/null || true
```

### Phase 8: Post-Cleanup Verification
```bash
# Verify core functionality still works
python mesopredator_cli.py --help
python -m src.api.rest.simple_api &
sleep 5
curl http://localhost:8000/health
pkill -f simple_api
```

---

## 📊 **Expected Results**

### Before Cleanup
- **Total Files**: ~200+ files
- **Repository Size**: ~6.2GB
- **Redundant Files**: 50-70 files

### After Cleanup
- **Total Files**: ~150 files
- **Repository Size**: ~5.9GB (300MB savings)
- **Redundant Files**: 0

### Benefits
- **Faster Repository Operations**: Git clone, pull, status
- **Clearer File Structure**: Easier navigation and maintenance
- **Reduced Confusion**: No duplicate or obsolete files
- **Better Documentation**: Only current, accurate files remain

---

**Execute this cleanup plan systematically to maintain a clean, efficient repository structure while preserving all essential functionality.**