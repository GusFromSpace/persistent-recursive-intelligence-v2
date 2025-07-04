# Architecture Decision Record: Dynamic Command Hiding for Security

**ADR Number:** ADR-038  
**Date:** 2025-07-04  
**Status:** Accepted  
**Deciders:** GusFromSpace, Claude (PRI Development Team)

## Context and Problem Statement

The PRI CLI tool had grown to include both safe production commands and potentially dangerous commands for security testing, adversarial validation, and system modification. All commands were equally visible in the help output, creating usability and security concerns:

1. **User Experience Issue:** New users were overwhelmed by the full command list, including dangerous operations they shouldn't use casually
2. **Security Concern:** Dangerous commands like `test adversarial` and `validate security` were immediately visible and discoverable
3. **Accidental Usage Risk:** Users could accidentally stumble upon dangerous functionality without understanding the implications
4. **Professional Usage:** Expert users still needed full access to all functionality for legitimate security testing and system administration

The core user requirement was: *"when we use the cli, we should be able to hide the dangerous tools by default, and only expose them for use when referenced"*

## Decision Drivers

- **Security-First Design:** Dangerous tools should not be immediately discoverable by casual users
- **Usability:** Default help should show only safe, commonly-used commands
- **Accessibility:** Expert users must retain full access to all functionality
- **Zero Breaking Changes:** Existing workflows and scripts must continue working
- **Educational Value:** System should teach users about security implications
- **Gradual Disclosure:** Progressive revelation of functionality based on user intent
- **Harmonic Doctrine Alignment:** Influence through design rather than restriction

## Considered Options

### Option 1: Complete Command Removal
- **Pros:** Maximum security, clean interface
- **Cons:** Breaks existing functionality, prevents legitimate use cases
- **Resonance Score:** Low - Removes capability rather than enhancing it

### Option 2: Configuration-Based Hiding
- **Pros:** User-controlled, persistent settings
- **Cons:** Complex configuration management, discovery friction
- **Resonance Score:** Medium - Good control but adds complexity

### Option 3: Dynamic Help Filtering with Explicit Access
- **Pros:** Clean default UX, maintains full functionality, educational opportunities
- **Cons:** Requires custom parser implementation
- **Resonance Score:** High - Enhances user agency while preserving capability

### Option 4: Separate Binary/Command Structure
- **Pros:** Clear separation of concerns
- **Cons:** Deployment complexity, workflow fragmentation
- **Resonance Score:** Low - Creates unnecessary complexity

## Decision Outcome

**Chosen option:** Dynamic Help Filtering with Explicit Access (Option 3)

**Justification:** This option embodies the Mesopredator principles of dual awareness and cognitive flexibility by:
- **Dual Awareness:** Maintains both hunter (expert) and hunted (novice) perspectives
- **Field Governance:** Shapes the interaction space toward beneficial outcomes
- **Capability Democratization:** Preserves expert access while protecting novice users
- **Conscious Choice Architecture:** Every command execution becomes a deliberate decision
- **Resonant Emergence:** Builds better systems rather than removing existing ones

## Positive Consequences

### **Enhanced User Experience**
- Clean, focused help output for new users
- Reduced cognitive load when discovering PRI functionality
- Educational security messaging builds user awareness

### **Improved Security Posture**
- Dangerous commands not immediately discoverable
- Security warnings appear when using hidden commands
- Existing security gates remain fully functional

### **Preserved Expert Workflow**
- `--show-all` flag reveals all commands instantly
- Hidden commands work exactly as before when explicitly typed
- No workflow disruption for advanced users

### **Educational Value**
- `--help-security` provides comprehensive security education
- Command tier system teaches users about risk levels
- Progressive disclosure builds security awareness

## Negative Consequences

### **Implementation Complexity**
- Required custom ArgumentParser classes
- Additional code maintenance burden
- More sophisticated help formatting logic

### **Discovery Friction**
- Expert users need to know about `--show-all` flag
- Slight increase in command-line verbosity for dangerous operations
- Help system has two different modes to maintain

## Implementation Plan

- [x] **Phase 1:** Core Implementation
  - [x] Create `HiddenCommandArgumentParser` class
  - [x] Implement dynamic help filtering
  - [x] Add `--show-all` and `--help-security` flags
  - [x] Mark dangerous commands as hidden

- [x] **Phase 2:** Security Integration
  - [x] Integrate with existing security warning system
  - [x] Add security notifications for hidden command usage
  - [x] Preserve all existing security gates

- [x] **Phase 3:** Testing & Documentation
  - [x] Comprehensive testing of all command scenarios
  - [x] Verify zero breaking changes
  - [x] Document security tier system

- [ ] **Monitoring:** Measure adoption and usability
  - [ ] Track `--show-all` usage patterns
  - [ ] Monitor user feedback on command discoverability
  - [ ] Assess security incident reduction

- [ ] **Rollback Plan:** Simple reversion strategy
  - [ ] Remove hidden command marking (single line change)
  - [ ] Maintain all existing functionality intact

## Validation Criteria

**Success Metrics:**
- ✅ Default help shows only 7 safe commands (vs. previous 10)
- ✅ Hidden commands (`test`, `validate`, `consolidate`) remain fully functional
- ✅ Security warnings display appropriately for dangerous operations
- ✅ Zero breaking changes to existing workflows
- ✅ Expert users can access all functionality via `--show-all`

**Measurable Outcomes:**
- Reduced accidental usage of dangerous commands
- Improved new user onboarding experience
- Maintained expert user productivity
- Enhanced security awareness through educational messaging

**Review Timeline:**
- **30 days:** Collect user feedback on discoverability
- **90 days:** Assess security incident patterns
- **180 days:** Evaluate long-term usability impact

## Links

- **Security Audit Report:** `/SECURITY_AUDIT_REPORT.md`
- **Security Hardened Status:** `/SECURITY_HARDENED_STATUS.md`
- **Implementation Documentation:** `/COMMAND_HIDING_IMPLEMENTATION.md`
- **Related ADRs:** 
  - ADR-016: Anti-Pattern Identification
  - ADR-037: OpenMW Semantic Bridge
- **Harmonic Doctrine:** `/home/gusfromspace/Development/Standards/harmonic_doctrine.md`
- **Mesopredator Philosophy:** `/home/gusfromspace/Development/Standards/mesopredator_philosophy.md`

---

*This ADR follows the principle of "Conscious Decision Making" - every technical choice must be documented with clear rationale and consideration of alternatives. The dynamic command hiding system represents a harmonious balance between security, usability, and capability preservation, embodying the core principle that we replace before we remove.*