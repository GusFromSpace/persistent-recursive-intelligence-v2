# Architecture Decision Record - Git Integration and File-Specific Analysis

**ADR Number:** ADR-042  
**Date:** 2025-07-06  
**Status:** Accepted  
**Deciders:** GusFromSpace, Claude Code Analysis

## Context and Problem Statement

The Mesopredator PRI tool required enhanced developer workflow integration to be practically useful in daily development. Developers needed the ability to:
1. Analyze only the files they've changed (git-aware analysis)
2. Focus analysis on specific files without processing entire projects
3. Integrate seamlessly with git-based workflows for pre-commit checks and targeted debugging

The existing full-project analysis was comprehensive but impractical for iterative development where developers want immediate feedback on their changes.

## Decision Drivers

- **Developer Velocity**: Enable rapid feedback loops for code changes
- **Git Integration**: Leverage existing developer workflows around git
- **Focused Analysis**: Allow targeting specific files or changesets
- **Performance**: Avoid analyzing unchanged code repeatedly
- **Workflow Integration**: Support pre-commit hooks and CI/CD integration
- **Mesopredator Principles**: Maintain dual awareness (hunter/hunted) by focusing analysis where threats are most likely (recent changes)

## Considered Options

### Option 1: External Git Integration via Shell Scripts
- **Pros:** 
  - Simple to implement
  - Leverages existing git commands
  - No Python git dependencies needed
- **Cons:**
  - Fragile cross-platform compatibility
  - Poor error handling
  - Limited integration with PRI's semantic analysis
- **Resonance Score:** Low - lacks the cognitive integration that embodies conscious choice

### Option 2: Python Git Library Integration (GitPython)
- **Pros:**
  - Rich Python API for git operations
  - Comprehensive git functionality
  - Good error handling and cross-platform support
- **Cons:**
  - Additional heavy dependency
  - Over-engineered for our specific needs
  - Complexity overhead for simple operations
- **Resonance Score:** Medium - powerful but potentially wasteful of cognitive resources

### Option 3: Minimal Git Utils with Subprocess Integration
- **Pros:**
  - Lightweight and focused on specific needs
  - Direct subprocess control for reliability
  - Easy to understand and maintain
  - Graceful fallback to full analysis
- **Cons:**
  - Requires careful subprocess error handling
  - Limited to basic git operations
- **Resonance Score:** High - embodies "replace before you remove" by building exactly what's needed

### Option 4: File-Specific Analysis via Temporary Directory Isolation
- **Pros:**
  - Reuses existing analysis engine without modification
  - Clean isolation of single files
  - Maintains all existing filtering and reporting
- **Cons:**
  - Temporary file overhead
  - Slightly more complex file handling
- **Resonance Score:** High - leverages existing strengths while enabling new capabilities

## Decision Outcome

**Chosen option:** Option 3 + Option 4 - Minimal Git Utils with File Analysis via Temporary Isolation

**Justification:** This combination embodies the Mesopredator principle of dual awareness by maintaining both the hunter's focus (targeted analysis) and the hunted's caution (graceful fallback). It demonstrates conscious choice by building precisely what's needed without over-engineering, and enables the "Aut Agere Aut Mori" principle by providing immediate actionable feedback on recent changes.

## Positive Consequences

- **Immediate Developer Feedback**: Developers can analyze only their changes in seconds
- **Git Workflow Integration**: Natural fit with existing git-based development processes
- **Focused Problem Solving**: Single-file analysis enables rapid debugging and iteration
- **Performance Benefits**: Dramatic reduction in analysis time for targeted use cases
- **Maintained Semantic Capabilities**: Full FAISS and semantic analysis on filtered file sets
- **Graceful Degradation**: Falls back to full analysis if git operations fail

## Negative Consequences

- **Additional Code Complexity**: New git utilities and file handling logic
- **Platform Dependencies**: Subprocess git calls may vary across platforms
- **Temporary File Overhead**: Single-file analysis creates temporary directories
- **Context Loss**: Analyzing files in isolation may miss cross-file dependencies

## Implementation Plan

- [x] **Phase 1:** Create minimal git utilities module with basic repository operations
- [x] **Phase 2:** Add git-aware CLI options (--git-diff, --staged-only, --since-commit)
- [x] **Phase 3:** Implement file-specific analysis via temporary directory isolation
- [x] **Phase 4:** Integrate new analysis modes with existing filtering and reporting
- [x] **Phase 5:** Add comprehensive error handling and fallback mechanisms
- [x] **Monitoring:** Track usage patterns and performance improvements
- [ ] **Rollback Plan:** Can disable git-aware features via CLI flags if issues arise

## Validation Criteria

**How will we know if this decision was correct?**
- **Measurable outcomes:**
  - Git-diff analysis completes in <10 seconds for typical changesets
  - Single-file analysis completes in <5 seconds
  - Zero false negatives in git change detection
- **Success metrics:**
  - Developer adoption of git-aware analysis modes
  - Reduced time-to-feedback in development workflows
  - Integration with CI/CD pre-commit hooks
- **Review timeline:** 1 month post-implementation

## Links

- Related to ADR-041 (PRI Usability Improvements) - builds on smart filtering foundation
- Supports ADR-033 (Feedback Loop Architecture) - enables rapid iteration cycles
- Integrates with existing persistent memory and semantic analysis architecture

---

*This ADR follows the principle of "Conscious Decision Making" - every technical choice must be documented with clear rationale and consideration of alternatives. The git integration embodies the Mesopredator approach of focused intelligence applied where it's most needed - on the code that's actively changing.*