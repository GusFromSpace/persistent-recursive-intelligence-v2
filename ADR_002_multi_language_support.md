# Architecture Decision Record: Multi-Language Support

**ADR Number:** 002  
**Date:** 2025-06-30  
**Status:** Accepted  
**Deciders:** Gus, Gemini

## Context and Problem Statement

The Persistent Recursive Intelligence (PRI) tool was originally designed to analyze a single language (Python). To expand its capabilities and utility across a wider range of projects, it needed to support multiple languages, starting with C++. The primary architectural challenge was to integrate new language analyzers in a way that was scalable, maintainable, and, most importantly, prevented "memory pollution," where linguistic patterns and rules from one language could contaminate the analysis of another, thereby reducing accuracy.

## Decision Drivers

- **Functional Requirement:** The immediate need to analyze C++ codebases.
- **Scalability:** The architecture needed to be easily extensible to support other languages (e.g., Java, Go, Rust) in the future without significant refactoring.
- **Analysis Quality:** The need to maintain high-fidelity, language-specific analysis, avoiding the dilution of knowledge that would come from a single, monolithic model.
- **Cognitive Flexibility:** The solution had to align with the Mesopredator principle of preserving cognitive flexibility by avoiding a rigid, hard-to-modify structure.
- **Harmonic Doctrine:** The desire for a coherent system composed of specialized, decentralized components (analyzers) working in harmony.

## Considered Options

### Option 1: Monolithic Engine with Conditional Logic
- **Description:** Keep the existing `MemoryEnhancedRecursiveImprovement` engine and add conditional blocks (`if/elif/else` based on file extension) to handle language-specific analysis logic. A single database would be used for all learned patterns.
- **Pros:** 
    - Faster to implement for the first additional language (C++).
- **Cons:**
    - Leads to a complex, tightly-coupled, and difficult-to-maintain codebase as more languages are added.
    - High risk of knowledge pollution in the central memory database.
    - Poor scalability; each new language increases the complexity of the core engine.
- **Resonance Score:** Low. This approach violates the principles of modularity and creates a rigid system, reducing cognitive flexibility.

### Option 2: Modular Analyzer Architecture with Language-Specific Databases
- **Description:** Refactor the core engine to use a modular, plugin-style architecture. This involves creating a `BaseLanguageAnalyzer` abstract class that defines a common interface for all analyzers. Each language is implemented as a separate analyzer class. Crucially, each analyzer uses its own dedicated database for learning language-specific patterns, with an additional global database for universal, language-agnostic patterns.
- **Pros:**
    - Creates a clean, decoupled, and highly scalable architecture.
    - Prevents knowledge pollution, leading to higher-quality analysis for each language.
    - Simplifies the addition of new languages.
    - Embodies the Harmonic Doctrine by creating a system of specialized, coherent, and decentralized components.
- **Cons:**
    - Requires a larger upfront investment in refactoring the core engine.
    - Introduces a small amount of complexity in managing multiple database instances.
- **Resonance Score:** High. This design perfectly embodies the Mesopredator principles. It has "dual awareness" (language-specific and global knowledge) and high cognitive flexibility (new analyzers can be added easily).

## Decision Outcome

**Chosen option:** Option 2: Modular Analyzer Architecture with Language-Specific Databases

**Justification:** This option was selected for its superior scalability, maintainability, and alignment with our core doctrines. By isolating language-specific logic and knowledge, it prevents the degradation of analysis quality and creates a robust foundation for future expansion. The architecture reflects the Mesopredator philosophy by enabling both specialized, deep analysis and generalized, cross-domain learning, preserving the system's ability to adapt and evolve.

## Positive Consequences

- **Extensibility:** The system can now be easily extended to support new programming languages by simply creating a new analyzer class.
- **Improved Accuracy:** Language-specific databases prevent knowledge contamination, leading to more accurate and relevant analysis for each supported language.
- **Maintainability:** The decoupled architecture makes the codebase cleaner, easier to understand, and safer to modify.
- **C++ Support:** The immediate goal of supporting C++ has been achieved.

## Negative Consequences

- **Increased Complexity:** The system now manages multiple memory databases, which adds a layer of complexity to the memory management system.
- **Minor Overhead:** There is a slight performance overhead associated with loading the appropriate analyzer and connecting to multiple databases.

## Implementation Plan

- [x] **Phase 1: Core Refactoring:**
    - [x] Create `BaseLanguageAnalyzer` abstract class.
    - [x] Implement `CppAnalyzer` by adapting logic from the `ai-diagnostic-toolkit`.
    - [x] Refactor existing Python checks into a dedicated `PythonAnalyzer`.
    - [x] Create an `AnalyzerOrchestrator` to manage and select the correct analyzer based on file type.
    - [x] Integrate the orchestrator into the main `MemoryEnhancedRecursiveImprovement` engine.
- [x] **Phase 2: Memory Segregation:**
    - [x] Modify the main engine to create and manage separate `MemoryIntelligence` instances for each language (`pri_python`, `pri_cpp`) and one for global patterns (`pri_global`).
    - [x] Update the analyzer interface to accept and use the dedicated memory instances.
    - [x] Refactor all memory calls to use the correct language-specific or global database.
- [ ] **Monitoring:**
    - [ ] Monitor the accuracy of C++ analysis on real-world projects.
    - [ ] Track the growth and quality of the language-specific databases.
    - [ ] Measure the performance overhead of the new architecture.
- [ ] **Rollback Plan:**
    - [ ] The previous monolithic version is available in the git history. A rollback would involve reverting the commits related to the analyzer and memory refactoring.

## Validation Criteria

- **Success Metric:** The tool successfully analyzes C++ projects and identifies common AI-generated errors with over 90% accuracy.
- **Success Metric:** The false positive rate for both C++ and Python analysis remains below 5%.
- **Verification:** The language-specific databases (`pri_cpp.db`, `pri_python.db`) are created and populated with relevant, language-specific data.
- **Verification:** Adding a new, simple language analyzer (e.g., for Markdown) can be done in under 2 hours with minimal changes to the core engine.
- **Review Timeline:** The effectiveness of this architecture will be reviewed after analyzing 10 real-world C++ projects.

## Links

- ADR_001_claude_wrapper_integration.md
