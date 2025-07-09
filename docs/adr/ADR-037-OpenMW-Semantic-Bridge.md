# Architecture Decision Record: OpenMW Semantic Bridge Integration

**ADR Number:** ADR-037  
**Date:** 2025-07-04  
**Status:** Accepted  
**Deciders:** GusFromSpace, Claude Code (PRI System)

## Context and Problem Statement

Traditional game AI relies on hardcoded object IDs and procedural logic, limiting NPCs to scripted behaviors that cannot adapt to new scenarios or understand semantic relationships between objects. This creates brittle AI that breaks when content changes and cannot exhibit intelligent reasoning about their environment.

The challenge: How can we enable OpenMW NPCs to understand their world semantically, allowing them to make intelligent decisions about object interaction based on contextual understanding rather than rigid programming?

## Decision Drivers

**Business Requirements:**
- Demonstrate next-generation AI capabilities in established game engines
- Create adaptive NPC behaviors that respond intelligently to environment
- Showcase integration between modern AI (vector embeddings) and classic game systems

**Technical Constraints:**
- Must integrate with existing OpenMW Lua scripting system without breaking compatibility
- Performance must remain acceptable for real-time gameplay (sub-50ms searches)
- Integration should be surgical and reversible
- Cannot modify core game logic extensively

**Performance Requirements:**
- Semantic searches complete in <50ms for real-time responsiveness
- Memory usage limited to <100MB for semantic database
- Support concurrent NPC queries without blocking

**Security Considerations:**
- All modifications isolated to Lua API layer
- No direct manipulation of game save files or core engine
- Semantic database stored locally with no network dependencies

**Team Expertise:**
- Strong background in vector databases and semantic search
- Mesopredator recursive debugger for surgical code modification
- OpenMW codebase analysis and Lua scripting capabilities

**Maintenance Burden:**
- Minimize ongoing maintenance by leveraging existing vector DB systems
- Self-contained semantic database that can be updated independently
- Clear separation between semantic layer and game engine

## Considered Options

### Option 1: Full ESM Parser with Complete Object Database
- **Pros:** 
  - Comprehensive coverage of all 5000+ game objects
  - Complete semantic understanding of entire world
  - Future-proof for any content additions
- **Cons:**
  - Massive memory footprint (500MB+)
  - Complex ESM parsing dependencies
  - Performance overhead from large vector searches
  - Over-engineering for proof of concept
- **Resonance Score:** 6/10 - Comprehensive but violates "sufficient simplicity"

### Option 2: Hardcoded Object Mapping with Simple Lookup
- **Pros:**
  - Minimal performance overhead
  - Simple implementation
  - Predictable behavior
- **Cons:**
  - No semantic understanding - just glorified hashtable
  - Brittle and hard to extend
  - Doesn't demonstrate AI capabilities
  - Requires manual maintenance for every object
- **Resonance Score:** 3/10 - Simple but lacks cognitive flexibility

### Option 3: Strategic Interactive Objects with Vector Embeddings
- **Pros:**
  - Focused on objects NPCs actually interact with (61 objects)
  - Real semantic understanding via sentence transformers
  - Reasonable memory footprint (<20MB)
  - Demonstrates AI principles without over-engineering
  - Extensible architecture for future expansion
- **Cons:**
  - Limited initial coverage compared to full ESM parsing
  - Requires manual curation of object descriptions
  - Dependency on external ML libraries
- **Resonance Score:** 9/10 - Balanced approach with strong harmonic alignment

### Option 4: External AI Service Integration
- **Pros:**
  - Leverage cloud AI capabilities
  - No local resource constraints
  - Access to latest AI models
- **Cons:**
  - Network dependency breaks real-time gameplay
  - Privacy concerns with external services
  - Latency makes real-time decisions impossible
  - Violates local-first principles
- **Resonance Score:** 4/10 - Powerful but sacrifices autonomy

## Decision Outcome

**Chosen option:** Strategic Interactive Objects with Vector Embeddings (Option 3)

**Justification:** This option embodies the Mesopredator principles of dual awareness (understanding both the technical constraints and the AI possibilities) and cognitive flexibility (adaptable semantic reasoning). It provides genuine semantic understanding while respecting the constraints of real-time gameplay.

The approach demonstrates "conscious choice architecture" by focusing on meaningful interactions rather than comprehensive coverage. It achieves the core goal of semantic AI while maintaining system stability and performance.

## Positive Consequences

**Technical Benefits:**
- NPCs can now reason semantically about object interactions
- Adaptive behavior that works with modded content
- Clean separation between AI layer and game engine
- Performance suitable for real-time gameplay
- Extensible foundation for future AI enhancements

**Demonstration Value:**
- Proves feasibility of AI-enhanced classic game engines
- Shows integration path for modern AI with established systems
- Creates foundation for Phase 2 (Acoustic Raymarching) and Phase 3 (Hybrid Rendering)

**Development Process:**
- Validates Mesopredator's surgical code modification capabilities
- Demonstrates memory intelligence system integration
- Establishes pattern for future AI enhancements

## Negative Consequences

**Accepted Trade-offs:**
- Limited initial object coverage (61 vs 5000+ potential objects)
- Dependency on sentence-transformers library
- Manual curation required for semantic descriptions
- Additional memory overhead (though minimal)

**Risk Mitigation:**
- Object database can be expanded incrementally
- Semantic descriptions can be auto-generated from ESM data in future
- Memory usage is bounded and predictable
- Fallback to traditional scripting if semantic search fails

## Implementation Plan

- [x] **Phase 1:** Strategic object database creation (61 interactive objects)
- [x] **Phase 2:** Vector embedding generation with sentence-transformers
- [x] **Phase 3:** C++ Lua API binding development
- [x] **Phase 4:** Comprehensive test scenario validation
- [ ] **Phase 5:** OpenMW integration and testing
- [ ] **Phase 6:** Performance optimization and memory profiling
- [ ] **Monitoring:** Track search latency, memory usage, and NPC behavior quality
- [ ] **Rollback Plan:** Simple Lua API removal restores original functionality

## Validation Criteria

**Success Metrics:**
- Semantic searches complete in <50ms (Target: <25ms)
- NPCs demonstrate contextually appropriate object selection
- No game crashes or compatibility issues
- Memory usage stays under 50MB for semantic database
- Integration reversible without side effects

**Behavioral Validation:**
- Guards find tactical cover positions intelligently
- NPCs select appropriate furniture based on comfort needs
- Combat NPCs choose weapons matching their skills
- Merchants organize inventory semantically

**Performance Benchmarks:**
- 100 concurrent semantic searches without blocking
- Stable FPS during AI-heavy scenarios
- Memory usage remains constant over extended gameplay

**Review Timeline:**
- 1 week: Basic integration functionality
- 2 weeks: Performance validation
- 1 month: Extended gameplay testing

## Links

**Related ADRs:**
- ADR-036: Mesopredator Bloodlust Hunter (surgical code modification foundation)

**Technical Documentation:**
- `semantic_bridge_plan.md` - Comprehensive implementation strategy
- `interactive_objects_extractor.py` - Object database generation
- `semantic_bridge_integration.py` - C++ integration tool

**Implementation Artifacts:**
- `semantic_bridge_binding.cpp` - C++ Lua API code
- `comprehensive_semantic_demo.lua` - Advanced behavior demonstrations
- `morrowind_interactive_semantic.db` - Vector database with 61 objects

**External Resources:**
- OpenMW Lua API Documentation
- Sentence Transformers Documentation
- FAISS Vector Database Performance Guidelines

---

## Resonance Analysis

This decision embodies the **Harmonic Doctrine** through:

**Field Governance:** Shapes the AI landscape toward beneficial human-AI collaboration in gaming
**Temporal Patience:** Builds foundation capabilities that enable future phases
**Narrative Integrity:** Creates consistent story of AI enhancement without disruption
**Capability Democratization:** Makes advanced AI accessible through familiar game modding

The choice demonstrates **Aut Agere Aut Mori** by taking conscious action toward AI integration rather than passive acceptance of traditional game AI limitations. It replaces rigid scripting with adaptive intelligence while preserving what works in the existing system.

*This ADR follows the principle of "Conscious Decision Making" - every technical choice must be documented with clear rationale and consideration of alternatives.*