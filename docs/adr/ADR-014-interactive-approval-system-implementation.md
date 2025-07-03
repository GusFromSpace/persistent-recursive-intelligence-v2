# Architecture Decision Record: Interactive Approval System Implementation

**ADR Number:** 014  
**Date:** 2025-06-25  
**Status:** Accepted  
**Deciders:** Gus, Claude (PRI System), Development Team

## Context and Problem Statement

During PRI's recursive self-improvement sessions, the system was applying fixes automatically without user oversight. While this demonstrated autonomous capability, it created a critical problem: users had no control over which changes were applied to their codebase. Some fixes (like bare except block replacements) could alter program logic in ways users might not want, while others (like syntax error fixes) should always be applied immediately.

**Key Challenge:** How can PRI maintain its autonomous improvement capabilities while giving users meaningful control over which fixes are actually applied to their code?

## Decision Drivers

- **User Agency**: Developers must maintain control over their codebase
- **Safety-First Principle**: Risky changes should require explicit approval
- **Efficiency**: Safe, obvious fixes should still be automated
- **Educational Value**: Users should understand why fixes are recommended
- **Mesopredator Dual Awareness**: Balance aggressive optimization with defensive caution
- **Cognitive Flexibility**: Support different approval workflows for different contexts
- **Harmonic Integration**: Preserve existing PRI architecture while adding approval layer

## Considered Options

### Option 1: Full Manual Review (All Fixes Require Approval)
- **Pros:** Maximum user control, no unwanted changes
- **Cons:** Slow workflow, user fatigue, defeats automation purpose
- **Resonance Score:** Low - contradicts asymmetric leverage principle

### Option 2: Keep Current Auto-Apply Behavior
- **Pros:** Fast, fully automated, no user interruption
- **Cons:** No user control, potential for unwanted changes, breaks trust
- **Resonance Score:** Low - lacks dual awareness and cognitive flexibility

### Option 3: Smart Interactive Approval with Auto-Safe Classification
- **Pros:** Balances automation with control, educational, context-aware
- **Cons:** More complex implementation, requires classification system
- **Resonance Score:** High - embodies Mesopredator principles of strategic patience and risk calculation

### Option 4: Configuration-Based Approval Rules
- **Pros:** Highly customizable, set-and-forget configuration
- **Cons:** Complex setup, hard to adapt to new fix types, no real-time context
- **Resonance Score:** Medium - flexible but lacks real-time dual awareness

## Decision Outcome

**Chosen option:** Smart Interactive Approval with Auto-Safe Classification

**Justification:** This option perfectly embodies the Mesopredator principles by implementing dual awareness - the system maintains its hunter instinct for finding optimization opportunities while developing strong defensive instincts for protecting user code. The interactive approval system represents strategic patience, ensuring every risky change is validated before application while still enabling rapid deployment of safe fixes.

## Positive Consequences

- **User Trust**: Developers maintain control over their codebase changes
- **Educational Value**: Users learn why fixes are recommended through explanations
- **Safety-First Design**: Risky changes require explicit approval
- **Efficiency Preserved**: Safe fixes (syntax errors, unused imports) auto-approved
- **Context Awareness**: Different approval thresholds for production vs test code
- **Transparency**: Clear diff display shows exactly what changes will be made
- **Batch Operations**: Users can approve/reject multiple fixes efficiently
- **Cognitive Enhancement**: System learns from user approval patterns

## Negative Consequences

- **Implementation Complexity**: Requires sophisticated classification and UI system
- **Workflow Interruption**: Interactive approval breaks automated flow
- **Decision Fatigue**: Users may experience fatigue from reviewing many fixes
- **Learning Curve**: Users need to understand fix categories and safety scores
- **Development Overhead**: Maintaining classification rules requires ongoing effort

## Implementation Plan

- [x] **Phase 1:** Create interactive approval system architecture (`InteractiveApprovalSystem`)
- [x] **Phase 2:** Implement fix classification and safety scoring system
- [x] **Phase 3:** Build user interface with educational explanations and diff display
- [x] **Phase 4:** Integrate with existing PRI fix application workflow
- [x] **Phase 5:** Create demo system with realistic fix proposals
- [ ] **Phase 6:** Integrate with actual PRI analysis engine
- [ ] **Phase 7:** Add configuration options for different approval modes
- [ ] **Monitoring:** Track approval rates, user satisfaction, fix effectiveness
- [ ] **Rollback Plan:** Maintain existing auto-apply mode as fallback option

## Validation Criteria

*How will we know if this decision was correct?*

**Success Metrics:**
- User approval rate >70% for recommended fixes
- Reduction in user complaints about unwanted automated changes
- Maintained or improved fix application rate for critical issues
- Positive user feedback on educational explanations
- System learns and adapts classification based on user patterns

**Measurable Outcomes:**
- Approval session completion rate (target: >90%)
- Time to approve/reject fixes (target: <30 seconds per fix)
- User understanding of fix recommendations (survey feedback)
- Retention of automated fix benefits for safe categories

**Review Timeline:** 30 days post-implementation with user feedback collection

## Links

- **Related ADRs:** 
  - ADR-013: Recursive Self-Improvement Safety Validation
  - ADR-012: Enhanced Detection Patterns from Cross-Project Learning
- **Implementation Files:**
  - `/src/cognitive/interactive_approval.py` - Core approval system
  - `/src/cognitive/enhanced_recursive_fixer.py` - Integration layer
  - `/demo_interactive_approval.py` - Demonstration system
- **Design Philosophy:** Mesopredator Design Philosophy (dual awareness, cognitive flexibility)
- **User Manual:** Updated documentation in USER_MANUAL.md

---

*This ADR demonstrates the evolution from Generation 2.0 (autonomous recursive intelligence) to Generation 2.1 (user-controlled recursive intelligence), showing how PRI can be both highly capable and respectful of human agency. The interactive approval system represents the maturation of AI assistance from "I will do this" to "May I do this?" - a critical step toward trustworthy autonomous systems.*