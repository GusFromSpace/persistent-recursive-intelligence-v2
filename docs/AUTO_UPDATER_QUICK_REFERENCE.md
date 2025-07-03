# Auto-Updater Quick Reference

**Essential commands and workflows for the Mesopredator Auto-Updater system**

## 🚀 Quick Start Commands

### Complete Workflow (Recommended)
```bash
# Safe exploration (no changes made)
mesopredator auto-update /path/to/package --dry-run

# Interactive integration (user approval required)
mesopredator auto-update /path/to/package --interactive

# Automated integration (trusted packages only)
mesopredator auto-update /path/to/package --auto-approve-safe
```

### Step-by-Step Workflow
```bash
# 1. Analyze package
mesopredator analyze-package /path/to/package

# 2. Generate integration plan
mesopredator map-integration /path/to/package --output plan.json

# 3. Review plan (optional)
mesopredator show-integration-plan plan.json

# 4. Execute plan
mesopredator execute-integration plan.json --interactive
```

## 📊 Analysis Commands

| Command | Purpose | Safety | Output |
|---------|---------|--------|--------|
| `analyze-package` | Examine package structure | ✅ Safe | Package analysis report |
| `map-integration` | Generate execution plan | ✅ Safe | Integration map JSON |
| `show-integration-plan` | Display plan details | ✅ Safe | Human-readable plan |

### Analysis Examples
```bash
# Basic package analysis
mesopredator analyze-package ./new_features/

# Detailed analysis with dependency graph
mesopredator analyze-package ./new_features/ --show-dependencies --format detailed

# Focus on specific target files
mesopredator analyze-package ./new_features/ --target-files "src/*.py"

# Save analysis for later review
mesopredator analyze-package ./new_features/ --output analysis.json
```

## 🗺️ Integration Planning

### Generate Integration Maps
```bash
# Conservative strategy (default)
mesopredator map-integration /path/to/package --strategy conservative

# Aggressive strategy (more modifications)
mesopredator map-integration /path/to/package --strategy aggressive

# Target specific files
mesopredator map-integration /path/to/package --target-files "main.py,utils.py"

# Save to custom location
mesopredator map-integration /path/to/package --output /custom/path/plan.json
```

### Review Integration Plans
```bash
# Summary view
mesopredator show-integration-plan plan.json --summary

# Detailed view (all modifications)
mesopredator show-integration-plan plan.json --detailed

# Specific step details
mesopredator show-integration-plan plan.json --step 2

# Different output formats
mesopredator show-integration-plan plan.json --format table
mesopredator show-integration-plan plan.json --format markdown
```

## 🤖 Execution Commands

| Mode | Command | Safety Level | Use Case |
|------|---------|--------------|----------|
| **Dry Run** | `--dry-run` | 🛡️ Maximum | Testing, validation |
| **Interactive** | `--interactive` | 🛡️ High | Manual review |
| **Auto-Safe** | `--auto-approve-safe` | ⚠️ Medium | Trusted packages |
| **Full Auto** | `--non-interactive` | ⚠️ Low | CI/CD pipelines |

### Execution Examples
```bash
# Test run (no changes made)
mesopredator execute-integration plan.json --dry-run

# Interactive approval for each change
mesopredator execute-integration plan.json --interactive

# Auto-approve safe changes, ask for risky ones
mesopredator execute-integration plan.json --auto-approve-safe

# Custom backup location
mesopredator execute-integration plan.json --backup-dir /custom/backup/

# Verbose progress reporting
mesopredator execute-integration plan.json --verbose
```

## 🛡️ Safety Commands

### Rollback Operations
```bash
# Automatic rollback (uses most recent backup)
mesopredator rollback

# Rollback from specific backup
mesopredator rollback /tmp/mesopredator_backup_abc123/

# Verify backup before rollback
mesopredator rollback /tmp/mesopredator_backup_abc123/ --verify

# Interactive file selection
mesopredator rollback /tmp/mesopredator_backup_abc123/ --interactive
```

### Backup Management
```bash
# List available backups
mesopredator list-backups

# Verify backup integrity
mesopredator verify-backup /tmp/mesopredator_backup_abc123/

# Clean old backups (keeps last 5)
mesopredator cleanup-backups --keep 5
```

## 🔧 Configuration & Options

### Global Options
```bash
# Enable debug logging
mesopredator auto-update package/ --debug

# Custom log file
mesopredator auto-update package/ --log-file integration.log

# Quiet mode (minimal output)
mesopredator auto-update package/ --quiet

# JSON output for scripting
mesopredator auto-update package/ --format json
```

### Integration Strategies
```bash
# Conservative (default): Minimal changes, maximum safety
--strategy conservative

# Aggressive: More modifications, faster integration
--strategy aggressive

# Custom: Load strategy from config file
--strategy-config custom_strategy.json
```

## 📈 Common Workflows

### 1. Exploring New Package
```bash
# Step 1: Understand the package
mesopredator analyze-package new_package/ --show-dependencies

# Step 2: See what integration would look like
mesopredator auto-update new_package/ --dry-run --verbose

# Step 3: If satisfied, integrate interactively
mesopredator auto-update new_package/ --interactive
```

### 2. Trusted Package Integration
```bash
# For packages you trust (internal team, previous success)
mesopredator auto-update trusted_package/ --auto-approve-safe --verbose
```

### 3. Large Package Incremental Integration
```bash
# Process large packages file by file
mesopredator auto-update large_package/ --target-files "core/*.py" --interactive
mesopredator auto-update large_package/ --target-files "utils/*.py" --interactive
mesopredator auto-update large_package/ --target-files "config/*.py" --interactive
```

### 4. CI/CD Pipeline Integration
```bash
#!/bin/bash
# ci_integration.sh

# Generate plan
mesopredator map-integration update_package/ --output plan.json

# Check success probability
PROBABILITY=$(jq '.success_probability' plan.json)

if (( $(echo "$PROBABILITY > 0.8" | bc -l) )); then
    echo "High confidence - proceeding with integration"
    mesopredator execute-integration plan.json --auto-approve-safe
else
    echo "Low confidence - manual review required"
    exit 1
fi
```

### 5. Safe Experimentation
```bash
# Create experimental branch
git checkout -b experiment-integration

# Test integration
mesopredator auto-update new_feature/ --dry-run

# If good, apply for real
mesopredator auto-update new_feature/ --interactive

# Test the integration
npm test  # or your test command

# If tests pass, merge to main
git checkout main
git merge experiment-integration

# If tests fail, rollback and investigate
mesopredator rollback
git checkout main
git branch -D experiment-integration
```

## 🚨 Emergency Procedures

### Integration Failed
```bash
# 1. Check what happened
mesopredator status

# 2. Rollback to previous state
mesopredator rollback --verify

# 3. Investigate the issue
cat /tmp/mesopredator_latest.log
```

### Backup Corruption
```bash
# 1. List all available backups
mesopredator list-backups

# 2. Find the most recent good backup
mesopredator verify-backup /tmp/mesopredator_backup_*

# 3. Restore from verified backup
mesopredator rollback /path/to/good/backup --force
```

### Project Directory Issues
```bash
# If project directory is damaged
# 1. Don't panic - backups are preserved
# 2. Find the backup
ls -la /tmp/mesopredator_backup_*

# 3. Restore entire project
cp -r /tmp/mesopredator_backup_latest/project_backup/* .

# 4. Verify restoration
git status
```

## 💡 Pro Tips

### Performance Optimization
```bash
# Use parallel processing for large packages
export MESOPREDATOR_WORKERS=4
mesopredator auto-update large_package/

# Cache analysis results for repeated runs
export MESOPREDATOR_CACHE_DIR=/tmp/mesopredator_cache
```

### Debugging Integration Issues
```bash
# Maximum verbosity for troubleshooting
mesopredator auto-update package/ --debug --verbose --dry-run

# Focus on specific files causing issues
mesopredator map-integration package/ --target-files "problematic_file.py" --debug
```

### Custom Validation
```bash
# Add custom validation commands
mesopredator execute-integration plan.json \
  --validate-command "python -m pytest" \
  --validate-command "npm run lint" \
  --validate-command "make check"
```

### Scripting Integration
```bash
# Use JSON output for scripting
RESULT=$(mesopredator auto-update package/ --dry-run --format json)
SUCCESS_PROB=$(echo "$RESULT" | jq '.success_probability')

if (( $(echo "$SUCCESS_PROB > 0.7" | bc -l) )); then
    mesopredator auto-update package/ --auto-approve-safe
fi
```

## 📋 Checklists

### Before Integration
- [ ] Project is in clean git state
- [ ] Understand what the package does
- [ ] Have sufficient disk space for backups
- [ ] Know how to test integration success
- [ ] Have time to handle issues if they arise

### During Integration
- [ ] Review each modification in interactive mode
- [ ] Read educational explanations
- [ ] Ask questions if anything is unclear
- [ ] Test after each major step
- [ ] Keep backup locations noted

### After Integration
- [ ] Run full test suite
- [ ] Verify all functionality works
- [ ] Commit the integration
- [ ] Document what was integrated
- [ ] Clean up old backups

## 🆘 Getting Help

### Built-in Help
```bash
# Command-specific help
mesopredator auto-update --help
mesopredator map-integration --help
mesopredator execute-integration --help

# Show examples for any command
mesopredator <command> --examples

# Show current status
mesopredator status

# Show version and features
mesopredator --version --features
```

### Debug Information
```bash
# Generate debug report
mesopredator debug-report --output debug.json

# Check system requirements
mesopredator check-requirements

# Validate installation
mesopredator self-test
```

---

**Remember**: When in doubt, use `--dry-run` to explore safely. The Auto-Updater is designed to preserve your project's integrity while enabling intelligent automation.