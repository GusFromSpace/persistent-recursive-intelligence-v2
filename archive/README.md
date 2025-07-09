# Archive Directory

**Created:** 2025-07-03  
**Purpose:** Store older versions and development artifacts to keep main directory clean  

---

## 📁 Archive Contents

### `/test_results/` - Old Test Results and Analysis Files
- **Old adversarial test reports** - Previous versions from multiple test runs
- **Issues files** - Historical issues analysis from different development stages
- **Duplicate test results** - Files that exist in organized locations elsewhere

### `/development_artifacts/` - Development and Training Files  
- **Claude wrapper analysis** - Multiple versions of AI analysis results
- **Training data files** - Machine learning training datasets that have been incorporated
- **Old test scripts** - Redundant or superseded test implementations
- **Rebranding artifacts** - Files from system rebranding process

### `/old_docs/` - Superseded Documentation
- **Old API documentation** - Inaccurate API docs replaced by corrected versions
- **Previous test plans** - Earlier versions of adversarial test plans

### `/old_logs/` - Historical Log Files
- **Test execution logs** - Previous runs of hello world and other tests
- **System logs** - Old intelligence system operation logs

---

## 🔄 Archive Policy

### Files in Archive
- **Not deleted** - All files preserved for historical reference
- **Not indexed** - Excluded from main development workflow
- **Accessible** - Available if needed for debugging or reference
- **Organized** - Categorized by type and purpose

### When Files Are Archived
- **Duplicate versions** when newer versions exist
- **Development artifacts** after incorporation into main system
- **Old test results** when superseded by more recent analysis
- **Obsolete documentation** when corrected versions are created

### Retention Policy
- **Keep indefinitely** for now (may implement rotation later)
- **Review quarterly** for files that can be permanently removed
- **Backup included** in system backups for disaster recovery

---

## 📊 Archive Statistics

**Total Files Archived:** 49 files  
**Total Size:** 4.3MB  
**Space Saved in Main Directory:** ~4.3MB  

### Breakdown:
- **Development Artifacts:** 3.5MB (largest category)
- **Test Results:** 748KB
- **Old Documentation:** 40KB  
- **Log Files:** 16KB

---

## 🔍 Finding Archived Files

### Search Commands
```bash
# Find specific file in archive
find archive/ -name "*filename*"

# List all files in category
ls archive/test_results/
ls archive/development_artifacts/
ls archive/old_docs/
ls archive/old_logs/

# Search by content or date
grep -r "search_term" archive/
find archive/ -newer "2025-07-01"
```

### Restoration
```bash
# Restore specific file to main directory
cp archive/category/filename.ext .

# Restore entire category
cp archive/test_results/* .
```

---

## 📝 Archive Manifest

### Major Files Archived

#### Test Results
- `complete_adversarial_test_report_*.json` (6 old versions)
- `issues_*.json` (8 variations) 
- `conceptual_transfer_results.json`
- `gray_hat_ethics_results.json`
- `orchestrator_synthesis_results.json`
- `safety_escape_results.json`

#### Development Artifacts  
- `claude_wrapper_analysis*.json` (3 versions, 1.7MB total)
- `claude_wrapper_*training*.json` (training data files)
- `*ouroboros_test.py` (4 test script variations)
- `test_*.py` (6 single-purpose test scripts)
- `rebrand_*.py` and related config files

#### Documentation
- `API_COMPREHENSIVE.md` (inaccurate version)
- `Mesopredator: Adversarial Test Plan v2.0.md`

#### Logs
- `hello_world_*.log` (older test execution logs)

---

**This archive maintains development history while keeping the main directory focused on current, active files.**