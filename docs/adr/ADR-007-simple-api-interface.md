# Architecture Decision Record - Simple API Interface

**ADR Number:** 006  
**Date:** 2025-06-22  
**Status:** Accepted  
**Deciders:** Development Team, External Integration Requirements

## Context and Problem Statement

The persistent-recursive-intelligence system has powerful cognitive capabilities including memory persistence, recursive improvement, and cross-project pattern transfer. However, external programs cannot easily interact with these capabilities, limiting the system's utility and preventing integration with other tools and workflows.

The existing API in `src/api/rest/app.py` was complex, tightly coupled to specific models, and difficult for external programs to consume effectively.

## Decision Drivers

- **External Integration Need:** Other programs need simple, predictable ways to interact with the intelligence system
- **Simplicity Over Complexity:** External consumers prefer straightforward interfaces over complex model hierarchies
- **Distributed Power Principle:** Enable other systems to leverage intelligence capabilities without tight coupling
- **Maintenance Burden:** Complex APIs require more documentation, testing, and support
- **Developer Experience:** External developers should be able to integrate quickly with minimal setup

## Considered Options

### Option 1: Enhance Existing Complex API
- **Pros:** 
  - Leverages existing code structure
  - Maintains consistency with internal architecture
  - Full feature parity with internal systems
- **Cons:**
  - High complexity barrier for external developers
  - Requires understanding of internal models and structures
  - Difficult to maintain backward compatibility
  - Heavy documentation burden
- **Resonance Score:** Low - creates friction rather than enabling flow

### Option 2: Create Simple REST API
- **Pros:**
  - Clean, minimal interface focused on core use cases
  - Standard HTTP/JSON - works with any programming language
  - Self-documenting with OpenAPI/Swagger
  - Easy to test and debug
  - Follows principle of asymmetric leverage
- **Cons:**
  - Less feature-complete than internal APIs
  - Requires maintaining two API interfaces
  - Some advanced features may not be exposed
- **Resonance Score:** High - enables external systems while maintaining simplicity

### Option 3: GraphQL Interface
- **Pros:**
  - Flexible querying capabilities
  - Single endpoint for all operations
  - Strong typing system
- **Cons:**
  - Higher learning curve for consumers
  - More complex to implement and maintain
  - Overkill for simple integration needs
- **Resonance Score:** Medium - flexible but potentially over-engineered

## Decision Outcome

**Chosen option:** Create Simple REST API (Option 2)

**Justification:** This option embodies the Mesopredator principles by providing dual awareness - internal complexity paired with external simplicity. It demonstrates cognitive flexibility by adapting the interface to external needs while maintaining the sophisticated internal architecture. The simple API creates resonant emergence by enabling other systems to easily leverage intelligence capabilities.

## Positive Consequences

- **Easy Integration:** External programs can integrate with minimal setup
- **Language Agnostic:** Works with Python, JavaScript, Go, Rust, or any HTTP-capable language
- **Self-Documenting:** Automatic OpenAPI documentation reduces support burden
- **Testable:** Simple HTTP interface is easy to test and debug
- **Scalable:** Can be deployed independently and scaled as needed
- **Enables Innovation:** Other developers can build on top of the intelligence system

## Negative Consequences

- **Dual Maintenance:** Need to maintain both internal and external APIs
- **Feature Gap:** Some advanced internal features may not be exposed
- **Abstraction Layer:** Adds another layer between external systems and core functionality
- **Potential Inconsistency:** External and internal APIs might diverge over time

## Implementation Plan

- [x] **Phase 1:** Create `simple_api.py` with core endpoints
  - Memory storage and search
  - Intelligence evolution
  - Pattern transfer
  - System statistics
- [x] **Phase 2:** Add comprehensive documentation
  - API reference with examples
  - Usage patterns for different languages
  - Integration guide
- [ ] **Phase 3:** Add monitoring and rate limiting
  - Request tracking
  - Error monitoring
  - Usage analytics
- [ ] **Monitoring:** Track API usage patterns and error rates
- [ ] **Rollback Plan:** Can disable external API and direct users to internal interfaces

## Validation Criteria

*How will we know if this decision was correct?*
- **Adoption Metrics:** Number of external integrations using the API
- **Developer Feedback:** Ease of integration reports from external developers
- **Support Burden:** Reduced questions about API usage and integration
- **System Reliability:** External API doesn't negatively impact core system performance
- **Review Timeline:** Evaluate success after 3 months of availability

## API Design Principles

The simple API follows these key principles:

1. **Intuitive Endpoints:** URLs clearly indicate functionality (`/memory/store`, `/intelligence/evolve`)
2. **Consistent Responses:** All responses follow standard JSON format with status indicators
3. **Minimal Parameters:** Only essential parameters required, sensible defaults provided
4. **Error Transparency:** Clear error messages with actionable information
5. **Stateless Operations:** Each request is independent, no session management required

## Core Endpoints Implemented

- `POST /api/v1/memory/store` - Store information in memory system
- `POST /api/v1/memory/search` - Search stored memories
- `POST /api/v1/intelligence/evolve` - Run recursive improvement on projects
- `POST /api/v1/intelligence/transfer` - Transfer patterns between projects
- `GET /api/v1/system/stats` - Get system statistics
- `GET /health` - Health check endpoint

## Links

- [Simple API Implementation](../../src/api/rest/simple_api.py)
- [API Documentation](../../API.md)
- [ADR-001: Persistent Recursive Intelligence Merge](ADR-001-persistent-recursive-intelligence-merge.md)
- [ADR-002: Debugging Capabilities Validation](ADR-002-debugging-capabilities-validation.md)

---

*This ADR follows the principle of "Conscious Decision Making" - every technical choice must be documented with clear rationale and consideration of alternatives.*