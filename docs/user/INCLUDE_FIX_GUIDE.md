# Interactive C++ Include Error Fixing Guide

**Version:** 1.0  
**Last Updated:** 2025-07-05  
**Part of:** Mesopredator PRI v2.1+

---

## Overview

The Interactive Include Fixing system provides intelligent detection and resolution of C++ include errors with machine learning capabilities. It combines pattern recognition, user feedback, and persistent learning to improve include management across projects.

## Key Features

### 🔍 **Intelligent Detection**
- **Missing includes** - Detects missing headers based on symbol usage patterns
- **Duplicate includes** - Identifies redundant #include statements  
- **Include ordering** - Finds violations of header organization standards
- **Path errors** - Detects problematic paths (excessive ../, backslashes, etc.)
- **Missing files** - Suggests alternatives when included files don't exist

### 🎯 **Interactive Experience**
- **Real-time diffs** - Visual representation of proposed changes
- **Multiple options** - Alternative suggestions when available
- **Confidence scoring** - AI confidence rating for each suggestion
- **User feedback** - 1-5 star rating system for continuous improvement
- **Learning system** - Adapts to user preferences over time

### 🛡️ **Safety Features**
- **Dry-run mode** - Preview all changes without applying
- **Auto-approval** - Automatically apply only high-confidence, safe fixes
- **Backup integration** - Works with existing backup systems
- **Rollback capability** - Can undo changes if needed

---

## Quick Start

### Basic Usage

```bash
# Analyze and fix a single file
mesopredator include-fix src/main.cpp

# Fix all C++ files in a project
mesopredator include-fix ./my_cpp_project/

# Preview fixes without applying
mesopredator include-fix ./project/ --dry-run

# Auto-approve safe fixes only
mesopredator include-fix ./project/ --auto
```

### Supported File Types
- `.cpp`, `.c`, `.cc`, `.cxx` - Source files
- `.h`, `.hpp`, `.hxx` - Header files

---

## Interactive Workflow

### 1. Analysis Phase
The system scans your code and detects include issues:

```
🔍 Found 15 C++ files in ./project/
📁 Engine.cpp: 2 potential fixes
📁 Renderer.cpp: 1 potential fixes
📁 Utils.h: 3 potential fixes
```

### 2. Interactive Fixing Session
For each detected issue, you'll see:

```
--- Fix 1/5 ---
Type: add_missing
Issue: Missing include for <chrono> (used symbols detected)
Confidence: 95%
Safety Score: 95/100

Proposed changes:
--- Engine.cpp
+++ Engine.cpp (proposed)
@@ -1,4 +1,5 @@
 #include "Engine.h"
 #include "Logger.h"
+#include <chrono>
 #include <iostream>
 #include <vector>

[a]pprove, [r]eject, [s]kip: a
```

### 3. User Feedback
After applying a fix, you can rate its effectiveness:

```
📊 How helpful was this fix?
Rate 1-5 stars: 5
Was this fix helpful? (y/n): y
Any additional feedback (optional): Perfect detection!
✅ Fix applied and feedback recorded!
```

---

## Fix Types Explained

### Missing Includes
**What it detects:** Missing header files based on symbol usage
**Example:**
```cpp
// Code uses std::vector but missing #include <vector>
std::vector<int> data;  // ← Triggers detection
```
**Fix:** Adds `#include <vector>` at appropriate location

### Duplicate Includes
**What it detects:** Redundant include statements
**Example:**
```cpp
#include <iostream>
#include <vector>
#include <iostream>  // ← Duplicate detected
```
**Fix:** Removes the duplicate include

### Include Ordering
**What it detects:** Violations of standard include organization
**Standard order:**
1. System headers (`<header>`)
2. Empty line
3. Local headers (`"header.h"`)

**Example fix:**
```cpp
// Before (incorrect order)
#include "MyClass.h"
#include <iostream>
#include <vector>

// After (correct order)
#include <iostream>
#include <vector>

#include "MyClass.h"
```

### Path Corrections
**What it detects:** Problematic include paths
**Examples:**
- Excessive relative paths: `#include "../../../utils/helper.h"`
- Windows backslashes: `#include "utils\\helper.h"`
- Spaces in paths: `#include "my file.h"`

### Missing File Suggestions
**What it detects:** Include statements referencing non-existent files
**Action:** Searches for similar files and suggests alternatives
**Example:**
```cpp
#include "Utility.h"  // File doesn't exist
// Suggests: "Utils.h", "utilities.h", "util/Utility.h"
```

---

## Advanced Features

### Confidence Scoring
Each suggestion includes a confidence score (0-100%):
- **90-100%** - Very high confidence, safe for auto-approval
- **70-89%** - High confidence, recommended to approve
- **50-69%** - Medium confidence, review carefully
- **Below 50%** - Low confidence, manual verification recommended

### Learning System
The system learns from your feedback:
- **Successful fixes** boost confidence for similar patterns
- **Rejected fixes** reduce confidence for similar patterns
- **User preferences** influence future suggestions
- **Project-specific patterns** are remembered

### Memory Integration
- Stores successful fix patterns in persistent memory
- Correlates fixes across different projects
- Builds knowledge base of common include patterns
- Shares learnings between different C++ projects

---

## Command Reference

### `mesopredator include-fix`

**Syntax:**
```bash
mesopredator include-fix <target_path> [options]
```

**Arguments:**
- `target_path` - File or directory to analyze

**Options:**
- `--auto` - Auto-approve safe fixes (confidence > 80%)
- `--dry-run` - Show proposed fixes without applying
- `--help` - Show command help

**Examples:**
```bash
# Interactive fixing with manual approval
mesopredator include-fix src/

# Preview mode - see what would be fixed
mesopredator include-fix src/ --dry-run

# Automatic mode - apply only safe fixes
mesopredator include-fix src/ --auto

# Single file fixing
mesopredator include-fix src/Engine.cpp
```

---

## Integration with Development Workflow

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit
mesopredator include-fix --dry-run .
if [ $? -ne 0 ]; then
    echo "Include errors detected. Run 'mesopredator include-fix .' to fix."
    exit 1
fi
```

### CI/CD Integration
```yaml
# .github/workflows/code-quality.yml
- name: Check Include Errors
  run: |
    mesopredator include-fix --dry-run .
    if [ $(mesopredator include-fix --dry-run . | grep -c "potential fixes") -gt 0 ]; then
      echo "::error::Include errors detected"
      exit 1
    fi
```

### IDE Integration
The system can be integrated with various IDEs through language servers or plugins to provide real-time include error detection and fixing.

---

## Troubleshooting

### Common Issues

**Q: "No C++ files found" error**
A: Ensure you're in a directory containing `.cpp`, `.h`, or `.hpp` files

**Q: False positive detections**
A: Rate the fix with 1-2 stars and select "not helpful" - the system will learn

**Q: Missing obvious includes**
A: The system focuses on symbol-based detection. If symbols aren't used in the analyzed portion, includes might not be detected

**Q: Suggested includes don't work**
A: Rate the fix poorly and provide feedback. The system learns from negative feedback

### Debug Mode
For troubleshooting, enable verbose logging:
```bash
export MESOPREDATOR_DEBUG=1
mesopredator include-fix src/
```

---

## Best Practices

### For Users
1. **Use dry-run first** on unfamiliar projects
2. **Provide feedback** to train the system
3. **Review auto-approved fixes** periodically
4. **Use project-specific patterns** by running multiple times

### For Projects
1. **Establish include conventions** early
2. **Document project-specific include paths**
3. **Use consistent header organization**
4. **Integrate with CI/CD** for continuous validation

---

## Technical Details

### Symbol Detection Patterns
The system uses regex patterns to detect symbol usage:

```python
symbol_patterns = {
    'iostream': [r'std::cout', r'std::cin', r'std::endl'],
    'vector': [r'std::vector'],
    'string': [r'std::string'],
    'memory': [r'std::shared_ptr', r'std::unique_ptr'],
    'chrono': [r'std::chrono', r'steady_clock'],
    # ... more patterns
}
```

### Confidence Calculation
Confidence is calculated based on:
- Symbol pattern matches in the code
- Historical success rate of similar fixes
- File context and project patterns
- User feedback history

### Learning Algorithm
- **Pattern boosting** - Successful patterns get higher confidence
- **Failure tracking** - Failed patterns are penalized
- **User preference modeling** - Adapts to user approval patterns
- **Cross-project learning** - Transfers knowledge between projects

---

## Future Enhancements

### Planned Features
- **Custom include paths** - Support for project-specific include directories
- **Build system integration** - CMake, Make, and other build tool awareness
- **Cross-language includes** - Support for C/C++ mixed projects
- **IDE plugins** - Real-time error detection in popular IDEs
- **Team learning** - Shared learning across development teams

### Contributing
To contribute to the include fixing system:
1. Add new symbol patterns in `cpp_analyzer.py`
2. Enhance confidence algorithms in `interactive_include_fixer.py`
3. Submit test cases for edge cases
4. Report false positives with detailed feedback

---

## Support

For issues with the include fixing system:
1. Check the [troubleshooting section](#troubleshooting)
2. Enable debug mode for detailed logging
3. Submit feedback through the interactive system
4. Report bugs in the main project repository

---

**Resonance Score: HIGH** - *This system harmonizes code structure with semantic understanding, reducing friction and improving developer experience.* ✦