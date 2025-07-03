# ADR-032: Language Analyzer Standard

**Date:** 2025-07-01  
**Status:** Accepted  
**Deciders:** GusFromSpace, Claude  
**Technical Story:** [Phase 1 C++ Implementation & Language Standard Refinement]  

## Context

Following the successful implementation of the Multi-Language Support Framework (ADR-031) and the enhanced C++ analyzer, we need to establish a formal standard for all language analyzers. This standard ensures consistency, quality, and maintainability across all language implementations while enabling rapid integration of new languages.

The current system has Python and C++ analyzers with different implementation approaches and interfaces. To scale the multi-language system effectively, we need:

1. **Mandatory Interface Compliance** - All analyzers must implement the same BaseAnalyzer interface
2. **Standardized Pattern Format** - Language-agnostic pattern definitions for cross-language learning
3. **Integration Requirements** - Clear steps for adding new analyzers to the orchestrator
4. **Quality Assurance** - Minimum testing and validation requirements

## Decision

We establish the **Language Analyzer Standard** that defines mandatory requirements for all language analyzers in the PRI system.

### Core Standard Components

#### 1. Mandatory BaseAnalyzer Interface

All language analyzers MUST inherit from and fully implement `BaseLanguageAnalyzer`:

```python
class BaseLanguageAnalyzer(ABC):
    def __init__(self):
        self.language_name: str = ""
        self.file_extensions: List[str] = []
        
    @abstractmethod
    def analyze_file(self, file_path: Path, content: str, 
                    memory: MemoryIntelligence, 
                    global_memory: MemoryIntelligence) -> List[Dict[str, Any]]:
        """Analyze a single file and return issues found"""
        pass
    
    @abstractmethod
    def learn_from_analysis(self, findings: List[Dict[str, Any]], 
                           memory: MemoryIntelligence) -> None:
        """Store analysis results for future learning"""
        pass
    
    @abstractmethod
    def get_similar_patterns(self, issue_type: str, 
                           memory: MemoryIntelligence) -> List[str]:
        """Retrieve similar patterns for educational purposes"""
        pass
    
    @abstractmethod
    def get_cross_language_correlations(self) -> List[str]:
        """Return list of related language families for correlation"""
        pass
```

#### 2. Standardized Pattern Definition Format

All analyzers MUST use the standardized JSON pattern format:

```json
{
    "pattern_id": "language_category_specific_name",
    "language": "language_name",
    "category": "security|performance|memory_management|syntax|ai_patterns|general",
    "severity": "critical|high|medium|low",
    "pattern_type": "regex|ast|semantic",
    "detection": {
        "regex": "pattern_string",
        "description": "What this pattern detects",
        "examples": ["code examples that trigger this pattern"]
    },
    "suggestion": "How to fix this issue",
    "educational_content": "Educational explanation of the issue",
    "cross_language_correlation": ["related_patterns_in_other_languages"]
}
```

#### 3. Issue Output Format

All analyzers MUST return issues in this standardized format:

```python
{
    "type": str,                    # Pattern identifier
    "line": int,                    # Line number where issue occurs
    "severity": str,                # critical|high|medium|low
    "description": str,             # Human-readable description
    "file_path": str,              # Absolute path to file
    "educational_content": str,     # Educational explanation
    "similar_patterns": List[str],  # Related patterns from memory
    "suggestion": str               # Optional fix suggestion
}
```

#### 4. Memory Integration Requirements

All analyzers MUST:

- Use language-specific memory namespaces (`pri_{language_name}`)
- Store patterns using `memory.store_memory(content, metadata)`
- Implement pattern retrieval using `memory.search_memories(query, limit)`
- Categorize findings using the standardized category system
- Enable cross-language correlation through metadata

#### 5. Integration Steps for New Analyzers

To add a new language analyzer:

1. **Create Analyzer Class**
   ```python
   # src/cognitive/analyzers/{language}_analyzer.py
   class {Language}Analyzer(BaseLanguageAnalyzer):
       def __init__(self):
           super().__init__()
           self.language_name = "{language}"
           self.file_extensions = [".{ext1}", ".{ext2}"]
   ```

2. **Import in Orchestrator**
   ```python
   # src/cognitive/orchestration/analyzer_orchestrator.py
   from ..analyzers import {language}_analyzer
   # Add to module list in _load_analyzers()
   ```

3. **Create Pattern Definitions**
   ```bash
   # patterns/{language}_patterns.json
   # Following standardized pattern format
   ```

4. **Add Test Coverage**
   ```bash
   # tests/test_{language}_analyzer.py
   # Minimum 85% code coverage required
   ```

5. **Registration Function**
   ```python
   def register_analyzer():
       """Auto-registration for Auto-Updater system"""
       analyzer = {Language}Analyzer()
       orchestrator = AnalyzerOrchestrator()
       return orchestrator.register_language_analyzer(analyzer)
   ```

#### 6. Quality Assurance Requirements

All language analyzers MUST meet:

- **Code Coverage:** Minimum 85% test coverage
- **Pattern Validation:** All patterns tested against known positive/negative cases
- **Integration Testing:** Successfully processes test files and finds expected issues
- **Memory Integration:** Proper storage and retrieval from memory system
- **Documentation:** Pattern descriptions and educational content for all detections

#### 7. Performance Standards

All analyzers MUST:

- Process files in batches using the orchestrator's batch system
- Complete analysis of 1000-line file in under 2 seconds
- Handle encoding errors gracefully with fallback strategies
- Provide progress indicators for large file processing
- Support concurrent execution without resource conflicts

## Implementation Plan

### Phase 1: Standardize Existing Analyzers

1. **Update BaseLanguageAnalyzer** - Ensure interface matches standard
2. **Refactor PythonAnalyzer** - Make 100% compliant with standard
3. **Refactor CppAnalyzer** - Make 100% compliant with standard
4. **Create Pattern Libraries** - Convert existing patterns to standard format

### Phase 2: Enhanced Integration

1. **Auto-Registration System** - Implement `register_language_analyzer()` in orchestrator
2. **Pattern Validation** - Create validation system for pattern definitions
3. **Testing Framework** - Standardized test suite for all analyzers
4. **Documentation Generator** - Auto-generate docs from pattern definitions

### Phase 3: Community Support

1. **Analyzer Template** - Cookiecutter template for new language analyzers
2. **Validation CLI** - Command to validate analyzer compliance
3. **Pattern Marketplace** - System for sharing language-specific patterns
4. **Auto-Updater Integration** - Language analyzers as installable packages

## Benefits

### For Developers
- **Consistent Interface** - Same API across all languages
- **Rapid Integration** - Clear steps for adding new languages
- **Quality Assurance** - Built-in standards ensure reliability
- **Educational Value** - Standardized educational content and cross-language learning

### For System Architecture
- **Scalability** - Unlimited language support with consistent performance
- **Maintainability** - Standardized code structure and testing
- **Memory Efficiency** - Optimized storage and retrieval patterns
- **Cross-Language Intelligence** - Systematic correlation and learning

### for Production Use
- **Reliability** - Minimum quality standards ensure stability
- **Performance** - Standardized performance requirements
- **Monitoring** - Consistent metrics and health checks
- **Extensibility** - Community can contribute new language support

## Compliance Validation

Each analyzer must pass this validation checklist:

```bash
# Interface Compliance
✓ Inherits from BaseLanguageAnalyzer
✓ Implements all abstract methods
✓ Uses standardized memory interface
✓ Returns issues in standard format

# Pattern Standards
✓ All patterns follow JSON schema
✓ Categories use standard taxonomy
✓ Educational content provided
✓ Cross-language correlations defined

# Integration Requirements
✓ Proper import in orchestrator
✓ Registration function implemented
✓ Memory namespace configured
✓ Batch processing supported

# Quality Assurance
✓ 85%+ code coverage
✓ Integration tests pass
✓ Performance benchmarks met
✓ Documentation complete
```

## Examples

### Compliant Analyzer Structure
```
src/cognitive/analyzers/
├── base_analyzer.py           # Abstract base class
├── python_analyzer.py         # Python implementation
├── cpp_analyzer.py           # C++ implementation
└── javascript_analyzer.py    # Future implementation

patterns/
├── python_patterns.json      # Python-specific patterns
├── cpp_patterns.json        # C++ specific patterns
└── universal_patterns.json   # Cross-language patterns

tests/
├── test_python_analyzer.py   # Python analyzer tests
├── test_cpp_analyzer.py     # C++ analyzer tests
└── test_analyzer_standard.py # Standard compliance tests
```

### Standard-Compliant Pattern
```json
{
    "pattern_id": "cpp_memory_buffer_overflow",
    "language": "cpp",
    "category": "security",
    "severity": "critical",
    "pattern_type": "regex",
    "detection": {
        "regex": "strcpy\\s*\\(.*\\)",
        "description": "Unsafe string copy that can cause buffer overflow",
        "examples": ["strcpy(dest, src);", "strcpy(buffer, input);"]
    },
    "suggestion": "Use strncpy() or std::string for safe string operations",
    "educational_content": "Buffer overflows occur when data exceeds allocated memory boundaries, potentially allowing code execution attacks.",
    "cross_language_correlation": ["python_string_buffer_issues", "java_string_vulnerabilities"]
}
```

## Consequences

### Positive
- **Standardized Development** - All language analyzers follow same patterns
- **Quality Assurance** - Minimum standards ensure reliability and performance
- **Rapid Scaling** - New languages can be added quickly following standard
- **Community Contribution** - Clear guidelines enable external contributions
- **Cross-Language Learning** - Systematic correlation improves analysis quality

### Negative
- **Initial Refactoring Effort** - Existing analyzers need updates for compliance
- **Complexity for Simple Languages** - Standard may be overkill for basic language support
- **Maintenance Overhead** - Standard needs to evolve with new requirements

### Risks
- **Standard Lock-in** - May limit innovation in analyzer design
- **Performance Overhead** - Compliance requirements may impact speed
- **Migration Complexity** - Updating existing analyzers to new standard

## Mitigation Strategies

1. **Gradual Migration** - Phase compliance updates over multiple releases
2. **Performance Monitoring** - Continuous benchmarking to ensure standards don't impact speed
3. **Standard Evolution** - Regular review and updates based on community feedback
4. **Escape Hatches** - Allow experimental analyzers to deviate with justification

---

This standard establishes the foundation for a truly polyglot intelligent analysis platform, enabling rapid expansion while maintaining quality and consistency across all supported languages.