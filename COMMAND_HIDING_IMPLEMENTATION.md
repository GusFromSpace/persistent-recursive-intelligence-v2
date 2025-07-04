# Dynamic Command Hiding Implementation

**Date:** 2025-07-04  
**Status:** ✅ COMPLETED & OPERATIONAL  
**Feature:** Dynamic command hiding for dangerous tools in PRI CLI

## Implementation Summary

Successfully implemented the user's request: *"when we use the cli, we should be able to hide the dangerous tools by default, and only expose them for use when referenced"*

## Key Features Implemented

### 🔒 **Command Hiding System**
- **Hidden by Default:** Dangerous commands (`test`, `validate`, `consolidate`) are hidden from default help output
- **Still Accessible:** Hidden commands remain fully functional when explicitly typed
- **Security Warnings:** Users see warnings when using hidden commands without `--show-all`

### 🛠️ **Custom ArgumentParser Classes**
- **`HiddenCommandArgumentParser`:** Custom parser that filters help output
- **`HiddenSubParsersAction`:** Custom subparser that respects hidden commands
- **Dynamic Filtering:** Removes hidden commands from choices and descriptions

### 🎮 **User Interface Features**
- **`--show-all`:** Reveals all commands including hidden ones
- **`--help-security`:** Shows detailed security information about command tiers
- **Security Notifications:** Clear messaging about hidden commands availability

## Command Security Tiers

### 🟢 **TIER 1 - PRODUCTION SAFE (Always Visible)**
```bash
mesopredator analyze     # Code analysis (safe)
mesopredator fix         # Interactive fixing (safe)
mesopredator stats       # Statistics (safe)
mesopredator prune       # Memory management (safe)
mesopredator demo        # Educational demonstrations (safe)
mesopredator cycle       # Cycle tracking (safe)
mesopredator train       # Training system (safe)
```

### 🔶 **TIER 2 - CONTROLLED ACCESS (Hidden by Default)**
```bash
mesopredator test        # Testing suite (with security warnings)
mesopredator validate    # Security validation (with security warnings)
mesopredator consolidate # Script consolidation (system modification)
```

## Usage Examples

### **Default Help (Hidden Commands Filtered)**
```bash
$ mesopredator --help
# Shows only safe commands + note about hidden commands
```

### **Show All Commands**
```bash
$ mesopredator --show-all --help
# Shows all commands including dangerous ones
```

### **Security Information**
```bash
$ mesopredator --help-security
# Shows detailed security tier information
```

### **Using Hidden Commands**
```bash
$ mesopredator test integration
# Shows security warning + executes command
```

### **Dangerous Commands with Security Gates**
```bash
$ mesopredator test adversarial
# Shows security warning + requires user confirmation
```

## Technical Implementation

### **Core Logic Flow:**
1. **Early Flag Detection:** Check for `--show-all` and `--help-security` before parsing
2. **Custom Parser Setup:** Use `HiddenCommandArgumentParser` with command hiding
3. **Dynamic Filtering:** Filter help output based on hidden commands list
4. **Security Warnings:** Display warnings for hidden command usage
5. **Existing Security Gates:** Maintain current security warnings for dangerous operations

### **Code Changes:**
- **New Classes:** `HiddenCommandArgumentParser`, `HiddenSubParsersAction`
- **New Function:** `show_security_help()`
- **Modified:** `main()` function with custom parser and flag handling
- **Enhanced:** Command execution with security warnings

## Security Design Principles

### ✅ **Maintained Security**
- All existing security warnings remain intact
- User confirmation still required for dangerous operations
- No reduction in security for adversarial/security testing modes

### 🎯 **Improved User Experience**
- Clean, uncluttered default help output
- Clear separation between safe and dangerous functionality
- Educational security information readily available

### 🔧 **Preserved Functionality**
- Hidden commands remain fully functional
- No breaking changes to existing usage patterns
- Expert users can still access all features easily

## Testing Results

### ✅ **Default Help Test**
```bash
$ mesopredator --help
# ✅ Shows only 7 safe commands
# ✅ Hides test, validate, consolidate
# ✅ Shows note about hidden commands
```

### ✅ **Show All Test**
```bash
$ mesopredator --show-all --help
# ✅ Shows all 10 commands
# ✅ Includes previously hidden commands
```

### ✅ **Security Help Test**
```bash
$ mesopredator --help-security
# ✅ Shows comprehensive security information
# ✅ Explains tier system and usage
```

### ✅ **Hidden Command Execution Test**
```bash
$ mesopredator test integration
# ✅ Shows security warning
# ✅ Executes successfully
# ✅ No loss of functionality
```

### ✅ **Security Gate Test**
```bash
$ echo "n" | mesopredator test adversarial
# ✅ Shows security warning
# ✅ Shows adversarial testing warning
# ✅ Properly cancels on user rejection
```

### ✅ **Safe Command Test**
```bash
$ mesopredator stats
# ✅ Works without warnings
# ✅ No security notifications for safe commands
```

## User Education & Messaging

### **Clear Security Communication:**
- **"🔒 Command 'X' is hidden for security by default"**
- **"Use --show-all to see all commands, or run directly if you understand the risks"**
- **"This command may contain security testing or system modification functionality"**

### **Helpful Usage Guidance:**
- **Shows available flags for revealing commands**
- **Explains command tier system**
- **Provides usage examples**

## Alignment with Requirements

### ✅ **User Request Fulfilled:**
> *"when we use the cli, we should be able to hide the dangerous tools by default, and only expose them for use when referenced"*

- **✅ Hide by default:** Dangerous commands hidden from help
- **✅ Expose when referenced:** Commands work when explicitly typed
- **✅ User control:** `--show-all` flag provides full access

### ✅ **Security-First Design Maintained:**
- All existing security warnings preserved
- Additional layer of security through command hiding
- Educational approach that informs rather than restricts

### ✅ **Zero Breaking Changes:**
- All existing functionality preserved
- Expert users can access everything with `--show-all`
- Gradual disclosure principle implemented

## Conclusion

The dynamic command hiding implementation successfully addresses the user's request while maintaining all existing security protections. The system provides:

1. **Clean User Experience:** Default help shows only safe commands
2. **Security Awareness:** Clear warnings about hidden command usage
3. **Expert Access:** Full functionality available via `--show-all`
4. **Educational Value:** Comprehensive security information via `--help-security`
5. **Zero Regression:** All existing features and security gates preserved

**Status:** ✅ **FEATURE COMPLETE & OPERATIONAL**

The PRI CLI now implements intelligent command hiding that balances usability, security, and accessibility for all user skill levels.