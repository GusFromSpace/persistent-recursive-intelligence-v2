# Package Structure Documentation

**Date:** 2025-01-09  
**Version:** 1.0  
**Status:** Current as of Package Structure Implementation (ADR-043)

---

## Overview

The persistent-recursive-intelligence project follows modern Python packaging standards with a **src-layout** structure. This document explains the package organization, import patterns, and development workflows.

## Package Structure

### Top-Level Structure

```
persistent-recursive-intelligence/
├── pyproject.toml              # Modern package configuration
├── setup.py                    # Backwards compatibility 
├── requirements.txt            # Runtime dependencies
├── README.md                   # Project overview
├── src/                        # Source code package
├── tests/                      # Test suite
├── docs/                       # Documentation
├── examples/                   # Usage examples
└── venv/                       # Virtual environment (local)
```

### Source Package Layout (`src/persistent_recursive_intelligence/`)

```
src/persistent_recursive_intelligence/
├── __init__.py                 # Main package entry point
├── cli.py                      # CLI entry point
│
├── api/                        # External interfaces
│   ├── __init__.py
│   ├── enhanced_pri_api.py     # Enhanced FastAPI server
│   ├── rest/                   # REST API modules
│   ├── graphql/                # GraphQL API (future)
│   └── websocket/              # WebSocket API (future)
│
├── cognitive/                  # Core intelligence
│   ├── __init__.py
│   ├── analyzers/              # Language-specific analyzers
│   │   ├── base_analyzer.py    # Abstract base
│   │   ├── python_analyzer.py  # Python language support
│   │   └── cpp_analyzer.py     # C++ language support
│   ├── memory/                 # Persistent memory system
│   │   ├── simple_memory.py    # Core memory engine
│   │   └── memory/             # Advanced memory components
│   ├── enhanced_patterns/      # Pattern detection
│   │   ├── code_connector.py   # File integration suggestions
│   │   ├── context_analyzer.py # Context-aware analysis
│   │   └── ...                 # Other pattern modules
│   ├── synthesis/              # Intelligence synthesis
│   └── orchestration/          # Component orchestration
│
├── safety/                     # Security and safety
│   ├── __init__.py
│   ├── emergency_controls.py   # Emergency safeguards
│   ├── sandboxed_validation.py # Sandbox testing
│   └── project_boundaries.py   # Access controls
│
├── metrics/                    # Performance metrics
│   ├── __init__.py
│   ├── models.py              # Data models
│   └── main.py                # Metrics collection
│
├── language_analyzers/         # Extended language support
│   ├── __init__.py
│   ├── lua_analyzer.py        # Lua language support
│   └── binary_analyzer.py     # Binary file analysis
│
└── utils/                      # Shared utilities
    ├── __init__.py
    ├── git_utils.py           # Git integration
    ├── logger.py              # Logging utilities
    └── config.py              # Configuration management
```

## Package Configuration

### `pyproject.toml` (Primary Configuration)

The main package configuration follows **PEP 517/518** standards:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "persistent-recursive-intelligence"
version = "0.1.0"
description = "AI-powered code analysis and improvement system"
dependencies = [
    "numpy>=2.2.0",
    "faiss-cpu>=1.7.4",
    "sentence-transformers>=2.2.0",
    # ... (15+ dependencies managed)
]

[project.scripts]
mesopredator = "persistent_recursive_intelligence.cli:main"
```

### `setup.py` (Backwards Compatibility)

Minimal wrapper for older pip versions:

```python
from setuptools import setup
setup()  # Defers to pyproject.toml
```

## Import Patterns

### Standard Import Patterns

```python
# Core components
from persistent_recursive_intelligence.cognitive.memory.simple_memory import SimpleMemoryEngine
from persistent_recursive_intelligence.cognitive.analyzers.python_analyzer import PythonAnalyzer

# API components  
from persistent_recursive_intelligence.api.enhanced_pri_api import app

# Safety systems
from persistent_recursive_intelligence.safety.emergency_controls import emergency_controller

# Utilities
from persistent_recursive_intelligence.utils.git_utils import GitRepo
```

### Relative Imports (Within Package)

```python
# From cognitive/analyzers/python_analyzer.py
from .base_analyzer import BaseLanguageAnalyzer
from ..memory.simple_memory import SimpleMemoryEngine
from ...safety.emergency_controls import emergency_controller
```

### CLI Entry Point

The CLI command is automatically available after installation:

```bash
# Entry point defined in pyproject.toml
mesopredator = "persistent_recursive_intelligence.cli:main"

# Available commands
mesopredator analyze /path/to/project
mesopredator fix /path/to/project  
mesopredator stats
```

## Installation Methods

### Development Installation (Recommended)

```bash
# Installs package in editable mode with all dependencies
pip install -e .

# Benefits:
# - Code changes immediately reflected
# - CLI command available globally  
# - Proper import resolution
# - All dependencies managed
```

### Production Installation (Future)

```bash
# When published to PyPI
pip install persistent-recursive-intelligence

# Or from GitHub
pip install git+https://github.com/gusfromspace/persistent-recursive-intelligence.git
```

## Package Features

### 🔧 CLI Tool Integration

- **Entry Point**: Automatic `mesopredator` command after installation
- **Path Management**: No manual PYTHONPATH manipulation required
- **Dependency Resolution**: All dependencies installed automatically

### 📦 Module Organization

- **Clear Separation**: API, cognitive, safety, utils in separate namespaces
- **Extensible**: Easy to add new analyzers and components
- **Standard Layout**: Follows Python packaging best practices

### 🔒 Security Boundaries

- **Package Isolation**: Clean namespace separation prevents conflicts
- **Import Controls**: Explicit imports make dependencies clear
- **Entry Point Security**: CLI access through controlled entry points

## Development Workflows

### Adding New Components

1. **Create module** in appropriate package directory
2. **Add `__init__.py`** if creating new subpackage
3. **Use proper imports** following package structure
4. **Update tests** in corresponding `tests/` directory
5. **Document** in relevant documentation

### Adding New Language Analyzers

```python
# 1. Create analyzer in cognitive/analyzers/
class NewLanguageAnalyzer(BaseLanguageAnalyzer):
    # Implementation...

# 2. Register in cognitive/analyzers/__init__.py
from .new_language_analyzer import NewLanguageAnalyzer

# 3. Import follows package structure
from persistent_recursive_intelligence.cognitive.analyzers import NewLanguageAnalyzer
```

### Testing Package Structure

```bash
# Test installation
pip install -e .

# Test CLI availability
mesopredator --help

# Test imports
python -c "import persistent_recursive_intelligence; print('✅ Success')"

# Test specific components
python -c "from persistent_recursive_intelligence.cognitive.memory import SimpleMemoryEngine; print('✅ Memory')"
```

## Migration Notes

### From Legacy Structure

**Before (Legacy):**
```python
from src.cognitive.memory import SimpleMemoryEngine
from cognitive.analyzers import PythonAnalyzer
```

**After (Package Structure):**
```python
from persistent_recursive_intelligence.cognitive.memory.simple_memory import SimpleMemoryEngine
from persistent_recursive_intelligence.cognitive.analyzers.python_analyzer import PythonAnalyzer
```

### Benefits of Migration

1. **Professional Distribution**: Can be published to PyPI
2. **IDE Integration**: Proper autocomplete and navigation
3. **Dependency Management**: Automatic resolution of dependencies
4. **CLI Integration**: Global command availability
5. **Import Reliability**: No more fragile relative imports

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Solution: Ensure package is installed
pip install -e .
```

**CLI Not Found:**
```bash
# Solution: Check virtual environment activation
source venv/bin/activate
mesopredator --help
```

**Old Import Patterns:**
```python
# Fix: Update to package imports
# Old: from src.cognitive import X  
# New: from persistent_recursive_intelligence.cognitive import X
```

## Best Practices

### For Developers

1. **Always install in development mode**: `pip install -e .`
2. **Use absolute imports**: Full package paths for clarity
3. **Follow package hierarchy**: Respect module boundaries
4. **Test imports**: Verify package structure after changes
5. **Update documentation**: Keep structure docs current

### For Contributors

1. **Understand package layout** before making changes
2. **Use proper import patterns** in new code
3. **Test CLI functionality** after modifications
4. **Follow namespace conventions** for new components

---

## Related Documentation

- **ADR-043**: Python Package Structure Implementation
- **pyproject.toml**: Package configuration
- **requirements.txt**: Runtime dependencies
- **README.md**: Installation and usage instructions
- **USER_MANUAL.md**: Complete user documentation

---

*This document is maintained as part of the persistent-recursive-intelligence project architecture documentation.*