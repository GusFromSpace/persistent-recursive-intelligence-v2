# Auto-Updater User Guide

**Transform your development workflow with intelligent, safe code integration**

The Mesopredator Auto-Updater system revolutionizes how you integrate new code into existing projects. Instead of manual, error-prone integration processes, the Auto-Updater provides intelligent analysis, comprehensive planning, and safe automated execution.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Core Concepts](#core-concepts)
3. [Workflow Overview](#workflow-overview)
4. [Command Reference](#command-reference)
5. [Safety Features](#safety-features)
6. [Advanced Usage](#advanced-usage)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)

## Quick Start

### Basic Auto-Update Workflow

```bash
# 1. Analyze and plan integration (dry run - safe to test)
mesopredator auto-update /path/to/update/package --dry-run

# 2. Execute the integration with interactive approval
mesopredator auto-update /path/to/update/package --interactive

# 3. Or run completely automated (for trusted packages)
mesopredator auto-update /path/to/update/package --auto-approve-safe
```

### Step-by-Step Workflow

```bash
# Step 1: Generate detailed integration map
mesopredator map-integration /path/to/update/package --output integration_plan.json

# Step 2: Review the plan (optional)
cat integration_plan.json | jq '.integration_steps[] | .description'

# Step 3: Execute the integration
mesopredator execute-integration integration_plan.json --interactive
```

## Core Concepts

### What is an Update Package?

An **update package** is a collection of new or modified files that you want to integrate into your existing project. This could be:

- **New features**: Additional modules or functionality
- **Bug fixes**: Updated versions of existing files  
- **Library upgrades**: New versions with enhanced capabilities
- **Template code**: Reusable components from other projects

### The Four-Phase Analysis

The Auto-Updater uses a sophisticated four-phase process:

#### Phase 1: Code Connector Analysis
**Purpose**: Discover how new files relate to your existing codebase

- Analyzes semantic similarity between new and existing code
- Identifies potential integration points
- Generates connection suggestions with confidence scores
- Detects patterns that suggest compatibility

#### Phase 2: Update Package Analysis  
**Purpose**: Understand the internal structure of the update package

- Classifies files by role (core, utility, config, test, documentation)
- Builds dependency graph between package files
- Identifies external requirements (libraries, modules)
- Computes optimal integration order

#### Phase 3: Integration Map Generation
**Purpose**: Create detailed, executable integration plan

- Generates step-by-step modification instructions
- Assesses risk level for each change
- Plans rollback procedures for safety
- Estimates execution time and complexity

#### Phase 4: Automated Patching
**Purpose**: Safely execute the integration plan

- Creates complete project backup before any changes
- Executes modifications with atomic operations
- Validates each step with comprehensive checks
- Provides instant rollback if problems occur

## Workflow Overview

### 1. Preparation

Before running the Auto-Updater, ensure:

- Your project is in a clean git state (all changes committed)
- You have sufficient disk space for backup creation
- Required dependencies are available
- You understand what the update package contains

### 2. Analysis Phase (Always Safe)

```bash
# Analyze the update package (no modifications made)
mesopredator analyze-package /path/to/update/package
```

This shows you:
- How many files will be integrated
- What external dependencies are needed
- Estimated success probability
- Potential conflicts or warnings

### 3. Planning Phase (Generate Integration Map)

```bash
# Create detailed integration plan
mesopredator map-integration /path/to/update/package --output plan.json
```

The integration map contains:
- **Integration steps**: Specific actions to be taken
- **File modifications**: Exact changes to be made  
- **Risk assessment**: Safety level for each modification
- **Rollback plan**: How to undo changes if needed
- **Validation strategy**: How success will be verified

### 4. Review Phase (Optional but Recommended)

```bash
# View the integration plan summary
mesopredator show-integration-plan plan.json

# View detailed modifications
mesopredator show-integration-plan plan.json --detailed
```

### 5. Execution Phase

Choose your execution mode based on trust level and risk tolerance:

#### Interactive Mode (Recommended)
```bash
mesopredator execute-integration plan.json --interactive
```
- Review each modification before it's applied
- Skip or modify individual changes
- Educational explanations for each modification
- Full control over the process

#### Dry Run Mode (Testing)
```bash
mesopredator execute-integration plan.json --dry-run
```
- Simulates all changes without making them
- Shows exactly what would happen
- Validates the entire process
- Perfect for testing and verification

#### Automated Mode (Trusted Packages)
```bash
mesopredator execute-integration plan.json --auto-approve-safe
```
- Automatically approves modifications marked as "safe"
- Still requires approval for risky changes
- Fastest execution for trusted code

## Command Reference

### Core Commands

#### `mesopredator auto-update`
**Complete end-to-end update workflow**

```bash
mesopredator auto-update <package_path> [options]

Options:
  --dry-run              Simulate changes without making them
  --interactive          Require approval for each modification
  --auto-approve-safe    Automatically approve safe modifications
  --output FILE          Save integration map to file
  --target-files FILES   Focus on specific target files
  --strategy STRATEGY    Integration strategy (conservative/aggressive)
```

#### `mesopredator map-integration`
**Generate integration map from update package**

```bash
mesopredator map-integration <package_path> [options]

Options:
  --output FILE          Save integration map to file
  --target-files FILES   Specific files to consider for integration
  --strategy STRATEGY    Integration approach (conservative/aggressive)
  --format FORMAT        Output format (json/yaml/summary)
```

#### `mesopredator execute-integration`
**Execute integration map with safety checks**

```bash
mesopredator execute-integration <map_file> [options]

Options:
  --dry-run              Simulate execution without changes
  --interactive          Interactive approval mode
  --auto-approve-safe    Auto-approve safe modifications
  --backup-dir DIR       Custom backup directory
  --verbose              Detailed progress reporting
```

#### `mesopredator analyze-package`
**Analyze update package structure and dependencies**

```bash
mesopredator analyze-package <package_path> [options]

Options:
  --output FILE          Save analysis to file
  --format FORMAT        Output format (json/summary/detailed)
  --show-dependencies    Display dependency graph
  --show-conflicts       Highlight potential conflicts
```

### Utility Commands

#### `mesopredator show-integration-plan`
**Display integration plan in human-readable format**

```bash
mesopredator show-integration-plan <map_file> [options]

Options:
  --detailed             Show all modifications
  --summary              Brief overview only
  --step NUMBER          Show specific step details
  --format FORMAT        Display format (table/json/markdown)
```

#### `mesopredator rollback`
**Manual rollback from backup**

```bash
mesopredator rollback <backup_directory>

Options:
  --verify               Verify backup integrity first
  --interactive          Confirm each file restoration
  --force                Skip safety checks (dangerous)
```

## Safety Features

### Comprehensive Backup System

**Every execution creates a complete project backup**

- Full project snapshot before any modifications
- Stored in temporary directory with unique identifier
- Includes all files except git history and caches
- Automatic cleanup after successful integration

### Multi-Layer Validation

**Validation happens at every step**

1. **Pre-execution**: Project state, permissions, backup creation
2. **Step validation**: Syntax checking, import verification
3. **Post-execution**: System integrity, functionality testing
4. **Rollback validation**: Backup integrity verification

### Interactive Approval System

**Maintain control over every change**

- Review each modification before it's applied
- Educational explanations for complex changes
- Skip individual modifications if needed
- Approve batches of similar changes

### Atomic Operations

**All-or-nothing execution**

- Either all modifications succeed or none are applied
- No partial state that could break your project
- Automatic rollback on any failure
- Consistent project state guaranteed

### Safe Rollback Mechanism

**Instant recovery from any issues**

- File-by-file restoration (never moves entire directories)
- Preserves directory structure and permissions
- Works even if execution was interrupted
- Verified backup integrity before rollback

## Advanced Usage

### Custom Integration Strategies

#### Conservative Strategy (Default)
```bash
mesopredator auto-update package/ --strategy conservative
```
- Minimal modifications
- Extensive validation
- Interactive approval for most changes
- Maximum safety, slower execution

#### Aggressive Strategy
```bash
mesopredator auto-update package/ --strategy aggressive
```
- More extensive modifications
- Faster execution
- Auto-approval for more change types
- Suitable for trusted packages

### Targeting Specific Files

```bash
# Focus integration on specific files
mesopredator auto-update package/ --target-files "src/main.py,src/utils.py"

# Use glob patterns
mesopredator auto-update package/ --target-files "src/**/*.py"
```

### Integration with CI/CD

```bash
# Automated integration in CI pipeline
mesopredator auto-update package/ \
  --dry-run \
  --output integration_plan.json \
  --format json

# Conditional execution based on analysis
if [ "$(jq '.success_probability' integration_plan.json)" -gt "0.8" ]; then
  mesopredator execute-integration integration_plan.json --auto-approve-safe
fi
```

### Custom Validation Commands

```bash
# Add project-specific validation
mesopredator execute-integration plan.json \
  --validate-command "npm test" \
  --validate-command "python -m pytest" \
  --validate-command "make lint"
```

## Troubleshooting

### Common Issues

#### "No connection suggestions generated"
**Cause**: The update package files don't have clear relationships to existing code
**Solution**: 
- Check that target files exist in your project
- Verify package files contain meaningful functionality
- Try with `--strategy aggressive` for broader matching

#### "External dependencies required"
**Cause**: Update package needs libraries not installed in your project
**Solution**:
- Install required dependencies: `pip install <package>`
- Add to requirements.txt before integration
- Use `--ignore-dependencies` flag (not recommended)

#### "Rollback failed"
**Cause**: Backup directory was deleted or corrupted
**Solution**:
- Check backup directory exists: `ls /tmp/mesopredator_backup_*`
- Manual restoration from most recent backup
- Use `mesopredator rollback <backup_dir> --force` as last resort

#### "Permission denied during execution"
**Cause**: Insufficient file system permissions
**Solution**:
- Check file permissions: `ls -la`
- Run with appropriate user permissions
- Ensure project directory is writable

### Debug Mode

```bash
# Enable detailed logging
mesopredator auto-update package/ --verbose --debug

# Save detailed logs
mesopredator auto-update package/ --log-file debug.log --log-level DEBUG
```

### Recovery Procedures

#### Manual Rollback
```bash
# Find backup directory
ls /tmp/mesopredator_backup_*

# Manual rollback
mesopredator rollback /tmp/mesopredator_backup_<id> --verify
```

#### Partial Recovery
```bash
# Restore specific files only
mesopredator rollback /tmp/mesopredator_backup_<id> --files "src/main.py,config.py"
```

## Examples

### Example 1: Adding a Logging Module

**Scenario**: You have a simple Python project and want to add advanced logging capabilities.

```bash
# 1. Create update package with logging module
mkdir logging_update
cat > logging_update/advanced_logger.py << 'EOF'
import logging
from datetime import datetime

class AdvancedLogger:
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
    
    def log_with_timestamp(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().isoformat()
        getattr(self.logger, level.lower())(f"[{timestamp}] {message}")
EOF

# 2. Analyze the integration
mesopredator analyze-package logging_update/

# 3. Generate integration plan
mesopredator map-integration logging_update/ --output logging_plan.json

# 4. Review the plan
mesopredator show-integration-plan logging_plan.json

# 5. Execute with interactive approval
mesopredator execute-integration logging_plan.json --interactive
```

### Example 2: Configuration System Update

**Scenario**: Replace simple configuration with a validation system.

```bash
# Update package contains: config_validator.py, updated_config.py
mesopredator auto-update config_update_package/ \
  --target-files "config.py,settings.py" \
  --interactive \
  --output config_integration.json
```

### Example 3: Batch Processing Multiple Updates

**Scenario**: Process several update packages in sequence.

```bash
#!/bin/bash
# batch_update.sh

for package in updates/feature_* ; do
  echo "Processing $package..."
  
  # Generate plan
  mesopredator map-integration "$package" --output "${package}_plan.json"
  
  # Check success probability
  probability=$(jq '.success_probability' "${package}_plan.json")
  
  if (( $(echo "$probability > 0.7" | bc -l) )); then
    echo "High confidence, executing automatically"
    mesopredator execute-integration "${package}_plan.json" --auto-approve-safe
  else
    echo "Low confidence, requires manual review"
    mesopredator execute-integration "${package}_plan.json" --interactive
  fi
done
```

### Example 4: Testing Integration Before Deployment

**Scenario**: Validate update package compatibility before applying.

```bash
# Create test environment
git checkout -b test-integration

# Test the integration
mesopredator auto-update new_feature_package/ --dry-run --verbose

# If tests pass, apply to real branch
git checkout main
mesopredator auto-update new_feature_package/ --auto-approve-safe

# Clean up test branch
git branch -d test-integration
```

## Best Practices

### Before Integration
1. **Commit your changes**: Ensure clean git state
2. **Review the package**: Understand what's being integrated
3. **Check dependencies**: Verify external requirements
4. **Test in isolation**: Use dry-run mode first

### During Integration
1. **Use interactive mode**: Review modifications when unsure
2. **Read explanations**: Understand why changes are being made
3. **Start conservative**: Use default strategy for unknown packages
4. **Monitor progress**: Watch for warnings or errors

### After Integration
1. **Test thoroughly**: Run your project's test suite
2. **Verify functionality**: Check that features work as expected
3. **Commit integration**: Save the integrated state
4. **Document changes**: Note what was integrated and why

### Safety Guidelines
1. **Always backup**: Never skip the backup creation
2. **Test first**: Use dry-run before live execution
3. **Understand risks**: Review high-risk modifications carefully
4. **Keep rollback ready**: Know how to recover if needed
5. **Incremental integration**: Process large updates in smaller batches

---

## Getting Help

- **Built-in help**: `mesopredator auto-update --help`
- **Verbose output**: Add `--verbose` to any command for detailed information
- **Debug logs**: Use `--debug` for troubleshooting
- **Command examples**: `mesopredator <command> --examples`

The Auto-Updater transforms complex integration tasks into safe, automated workflows. Start with dry-run mode and interactive approval to build confidence, then leverage automation for trusted packages and repeated workflows.