# Architecture Decision Record: PRI CLI Refactoring

**ADR Number:** 003
**Date:** 2025-06-25
**Status:** Accepted
**Deciders:** Gemini, gusfromspace

## Context and Problem Statement

The Persistent Recursive Intelligence (PRI) tool was becoming a collection of disparate Python scripts, each with its own command-line interface. This created a confusing and inconsistent user experience, and made the tool difficult to maintain and extend. The lack of a single, coherent entry point violated the "Coherence as Currency" and "Surgical Efficiency" principles of the GUS development framework.

## Decision Drivers

*   **User Experience:** The tool was not user-friendly. A single, unified CLI would be much easier to use and understand.
*   **Maintainability:** A collection of separate scripts is difficult to maintain. A single entry point with a clear command structure would be much easier to manage.
*   **Extensibility:** Adding new commands and features would be much easier with a single, well-structured CLI.
*   **Alignment with GUS Principles:** The refactoring aligns the tool with the core principles of the GUS framework, particularly "Coherence as Currency" and "Surgical Efficiency."

## Considered Options

### Option 1: Continue with separate scripts

*   **Pros:** No immediate effort required.
*   **Cons:** The tool would remain difficult to use, maintain, and extend. This would violate the core principles of the GUS framework.
*   **Resonance Score:** Low.

### Option 2: Refactor to a single, unified CLI

*   **Pros:** A much more user-friendly, maintainable, and extensible tool. Aligns with the core principles of the GUS framework.
*   **Cons:** Requires up-front effort to refactor the existing scripts.
*   **Resonance Score:** High.

## Decision Outcome

**Chosen option:** Refactor to a single, unified CLI.

**Justification:** This option was chosen because it aligns with the core principles of the GUS framework and will result in a much better tool in the long run. The up-front effort is a worthwhile investment.

## Positive Consequences

*   A more user-friendly, maintainable, and extensible tool.
*   Better alignment with the GUS development framework.
*   A solid foundation for future development.

## Negative Consequences

*   Requires up-front effort to refactor the existing scripts.

## Implementation Plan

*   [x] Create a new `pri_cli.py` script to serve as the single entry point for the tool.
*   [x] Refactor the existing scripts (`persistent_recursion.py`, `enhanced_recursive_fixer.py`) to be importable and callable by the new CLI.
*   [ ] Integrate the refactored scripts into the new CLI.
*   [ ] Update the documentation to reflect the new CLI.

## Validation Criteria

*   The new CLI is easy to use and understand.
*   The tool is easier to maintain and extend.
*   The tool is more aligned with the GUS development framework.

## Links

*   [Code Review of the PRI Tool](#)
