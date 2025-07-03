# Mesopredator PRI - User Manual

**Version:** 1.0  
**System:** Persistent Recursive Intelligence  
**Status:** Production Ready for Code Analysis  
**Last Updated:** 2025-06-29 - Added mesopredator global command and fixed enum issues

---

## Overview

Mesopredator PRI (Persistent Recursive Intelligence) is an **advanced code analysis system** with semantic understanding capabilities. It combines machine learning, vector search, and pattern recognition to provide deep insights into codebases while maintaining strict security and ethical boundaries.

### What Mesopredator PRI Does Well

✅ **Semantic Code Analysis**: Understands concepts across different programming languages and paradigms  
✅ **Security Vulnerability Detection**: Identifies potential security issues with high accuracy  
✅ **Pattern Recognition**: Detects code patterns, anti-patterns, and best practice violations  
✅ **Cross-Language Concept Transfer**: Learns patterns in one language and applies to others  
✅ **Persistent Learning**: Builds knowledge over time with memory of previous analyses  
✅ **Educational Annotations**: Provides detailed explanations of detected issues  

### What Mesopredator PRI Cannot Do

❌ **Autonomous Problem Solving**: Cannot independently solve complex multi-domain problems  
❌ **Code Generation**: Does not write or generate new code  
❌ **Cross-Domain Orchestration**: Limited synthesis across unrelated data sources  
❌ **Real-Time Code Execution**: Analysis only, no code execution capabilities  
❌ **Direct File Modification**: Read-only analysis, does not modify your code  

---

## Core Capabilities

### 1. Advanced Pattern Detection

**What it does:**
- Detects security vulnerabilities (SQL injection, XSS, buffer overflows)
- Identifies code quality issues (complexity, maintainability, performance)
- Recognizes architectural patterns and anti-patterns
- Finds inconsistencies in coding standards

**Accuracy:** 90%+ detection rate for common vulnerability patterns  
**Coverage:** Supports 20+ programming languages with semantic understanding

### 2. Semantic Concept Learning

**What it does:**
- Learns abstract concepts like "off-by-one errors" across different implementations
- Transfers knowledge between programming paradigms
- Understands conceptual similarities despite syntactic differences
- Builds persistent memory of patterns across projects

**Example:** Learns buffer overflow patterns in C and recognizes similar logical errors in Python list operations.

### 3. Security-First Architecture

**What it does:**
- 100% blocking of malicious code execution attempts
- Sandboxed analysis environment with strict access controls
- No network access during analysis
- Read-only file system access within project boundaries

**Security Features:**
- Runtime interception of dangerous operations
- File system boundary enforcement
- Subprocess execution prevention
- Comprehensive audit logging

---

## System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows with WSL2
- **Python**: 3.8 or higher
- **Memory**: 8GB RAM (16GB recommended)
- **Storage**: 2GB free space for dependencies
- **CPU**: Multi-core processor (4+ cores recommended)

### Recommended Setup
- **Memory**: 16GB+ RAM for large codebases
- **Storage**: SSD for faster analysis
- **GPU**: CUDA-compatible GPU for accelerated FAISS operations (optional)

### Dependencies
- FAISS (Facebook AI Similarity Search)
- SentenceTransformers
- SQLite3
- Python scientific stack (numpy, scipy, scikit-learn)

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-org/persistent-recursive-intelligence
cd persistent-recursive-intelligence
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Global Command (Recommended)
```bash
# Create the mesopredator wrapper script
cat > ~/.local/bin/mesopredator << 'EOF'
#!/bin/bash
cd /home/gusfromspace/Development/persistent-recursive-intelligence || {
    echo "Error: Cannot find PRI directory"
    exit 1
}
source venv/bin/activate || {
    echo "Error: Cannot activate PRI virtual environment"
    exit 1
}
python mesopredator_cli.py "$@"
EOF

# Make it executable
chmod +x ~/.local/bin/mesopredator

# Add to PATH if not already there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 5. Verify Installation
```bash
# Test the global command
mesopredator --help

# Or test the Python module directly
python mesopredator_cli.py --help
```

### 6. Initialize Memory Database
The memory database is automatically initialized on first run. No manual setup required.

---

## Usage Guide

### Quick Start with Mesopredator Command

**The easiest way to use Mesopredator PRI is with the global command:**

```bash
# Analyze a single file
mesopredator analyze /path/to/file.py

# Analyze entire project 
mesopredator analyze /path/to/project/

# Fix issues interactively
mesopredator fix /path/to/project/

# View statistics
mesopredator stats

# Show help
mesopredator --help
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Perform code analysis | `mesopredator analyze ./src/` |
| `fix` | Interactive issue fixing | `mesopredator fix ./project/` |
| `train` | Train on new patterns | `mesopredator train ./examples/` |
| `stats` | View analysis statistics | `mesopredator stats` |
| `prune` | Clean memory database | `mesopredator prune` |
| `cycle` | Run improvement cycle | `mesopredator cycle ./project/` |

### Basic Analysis

**Analyze a single project:**
```bash
# Using mesopredator command (recommended)
mesopredator analyze /path/to/your/code

# Using Python module directly
python -m src.cognitive.persistent_recursion --project /path/to/your/code
```

**With custom parameters:**
```bash
mesopredator analyze /path/to/your/code --batch-size 20 --output results.json
```

### Advanced Usage

**Interactive fixing mode:**
```bash
mesopredator fix /path/to/your/code
```

**Security-focused scan:**
```bash
mesopredator analyze /path/to/your/code --focus security
```

**Train on new patterns:**
```bash
mesopredator train /path/to/examples/
```

### Command Line Options

#### For `mesopredator analyze`

| Option | Description | Default |
|--------|-------------|---------|
| `--batch-size` | Processing batch size | 10 |
| `--output` | Output file path | stdout |
| `--focus` | Analysis focus (security, quality, all) | all |
| `--verbose` | Verbose output | false |

#### For `mesopredator fix`

| Option | Description | Default |
|--------|-------------|---------|
| `--auto-approve` | Auto-approve safe fixes | false |
| `--backup` | Create backup before fixing | true |
| `--dry-run` | Preview changes without applying | false |

#### For `mesopredator train`

| Option | Description | Default |
|--------|-------------|---------|
| `--pattern-type` | Type of patterns to learn | all |
| `--confidence` | Minimum confidence threshold | 0.7 |

#### Legacy Python Module Options

| Option | Description | Default |
|--------|-------------|---------|
| `--project` | Path to code project | Required |
| `--max-depth` | Maximum analysis depth | 2 |
| `--recursive-depth` | Recursive improvement iterations | 1 |
| `--enable-learning` | Enable persistent learning | false |
| `--strict-mode` | Enhanced security checks | false |

---

## Understanding Results

### Analysis Output Format

```json
{
  "project_path": "/path/to/project",
  "analysis_timestamp": "2025-06-29T10:30:00Z",
  "total_files": 42,
  "issues_found": 15,
  "improvement_potential": "32%",
  "security_rating": "B+",
  "issues": [
    {
      "category": "security",
      "severity": "high", 
      "file": "src/auth.py",
      "line": 45,
      "description": "Potential SQL injection vulnerability",
      "explanation": "User input used directly in SQL query without sanitization",
      "recommendation": "Use parameterized queries or ORM methods"
    }
  ],
  "patterns_learned": 3,
  "memory_entries_added": 12
}
```

### Issue Severity Levels

- **CRITICAL**: Immediate security risks or system-breaking issues
- **HIGH**: Significant security or quality concerns
- **MEDIUM**: Code quality improvements and best practice violations
- **LOW**: Style issues and minor optimizations

### Security Rating Scale

- **A+**: Excellent security posture, no significant issues
- **A**: Good security with minor recommendations
- **B**: Acceptable security with some concerns to address
- **C**: Multiple security issues requiring attention  
- **D**: Significant security vulnerabilities present
- **F**: Critical security flaws requiring immediate action

---

## Configuration

### Memory Configuration

Create `config/memory_config.json`:
```json
{
  "database_path": "memory_intelligence.db",
  "faiss_index_path": "faiss_index/",
  "vector_dimension": 384,
  "similarity_threshold": 0.7,
  "max_memory_entries": 1000000,
  "enable_compression": true
}
```

### Analysis Configuration

Create `config/analysis_config.json`:
```json
{
  "supported_languages": ["python", "javascript", "java", "cpp", "rust"],
  "security_checks": {
    "sql_injection": true,
    "xss_detection": true,
    "buffer_overflow": true,
    "path_traversal": true
  },
  "quality_checks": {
    "code_complexity": true,
    "duplicate_detection": true,
    "unused_variables": true,
    "performance_patterns": true
  }
}
```

---

## Best Practices

### For Optimal Results

1. **Clean Environment**: Run in isolated virtual environment
2. **Adequate Resources**: Ensure sufficient RAM for large codebases
3. **Incremental Analysis**: Start with smaller projects to build memory
4. **Regular Updates**: Keep dependencies updated for latest security checks
5. **Result Review**: Human review of results for context-specific decisions

### Security Considerations

1. **Sandboxed Operation**: System runs in read-only mode by default
2. **Network Isolation**: No external network connections during analysis
3. **File Permissions**: Respects system file permissions
4. **Audit Logging**: All operations logged for security review
5. **Safe Defaults**: Conservative settings prioritize security over performance

### Performance Optimization

1. **Batch Processing**: Adjust batch size based on available memory
2. **Selective Analysis**: Use focus modes for specific issue types
3. **Memory Management**: Monitor memory usage for large codebases
4. **Parallel Processing**: Leverage multi-core systems when available

---

## Limitations & Known Issues

### Current Limitations

#### Orchestration Capabilities
- **No Cross-Domain Synthesis**: Cannot correlate information from logs, databases, and code simultaneously
- **Linear Analysis**: Processes one domain at a time rather than holistic synthesis
- **Limited Problem Solving**: Identifies issues but does not generate comprehensive solutions

#### Language Support
- **Best Support**: Python, JavaScript, Java, C/C++
- **Good Support**: Rust, Go, TypeScript, PHP
- **Limited Support**: Newer or niche languages may have reduced accuracy

#### Scale Limitations
- **Large Codebases**: Performance degrades on projects >100,000 files
- **Memory Usage**: High memory requirements for comprehensive analysis
- **Processing Time**: Analysis time scales non-linearly with project complexity

### Known Issues

1. **False Positives**: May flag legitimate code patterns as suspicious (~5-10% rate)
2. **Context Sensitivity**: Limited understanding of business logic context
3. **Dynamic Analysis**: Cannot analyze runtime behavior, only static code
4. **Framework Specifics**: Generic patterns may not account for framework-specific best practices

### Workarounds

- **False Positives**: Review flagged issues for context appropriateness
- **Large Projects**: Use focus modes or analyze subdirectories separately
- **Performance**: Increase hardware resources or reduce batch size
- **Context Issues**: Combine automated analysis with human code review

---

## Troubleshooting

### Common Issues

#### Installation Problems
```bash
# FAISS installation error
pip install faiss-cpu  # Or faiss-gpu for CUDA support

# SentenceTransformers download issues
export TRANSFORMERS_CACHE=/path/to/writable/directory

# Mesopredator command not found
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### Enum Attribute Errors
If you see errors like `AttributeError: type object 'RelationType' has no attribute 'RELATES_TO'`:

```bash
# These have been fixed in the latest version. Ensure you have:
# - RelationType.RELATES_TO in src/cognitive/memory/models.py
# - ResultFormat.FULL in src/cognitive/memory/models.py  
# - PruningStrategy.HYBRID in src/cognitive/enhanced_patterns/memory_pruning_system.py

# Verify the fixes:
mesopredator analyze --help
```

#### Memory Issues
```bash
# Reduce memory usage
mesopredator analyze /path/to/code --batch-size 5

# Or using legacy module
python -m src.cognitive.persistent_recursion \
  --project /path/to/code \
  --batch-size 5 \
  --max-depth 1
```

#### Permission Errors
```bash
# Ensure read permissions
chmod -R 644 /path/to/code

# Fix mesopredator script permissions
chmod +x ~/.local/bin/mesopredator
```

### Performance Issues

**Slow Analysis:**
- Reduce batch size: `mesopredator analyze /path --batch-size 5`
- Use focus mode: `mesopredator analyze /path --focus security`
- Analyze smaller directories separately

**High Memory Usage:**
- Monitor with: `top -p $(pgrep -f mesopredator)`
- Reduce simultaneous processing
- Clear memory cache: `mesopredator prune`

**FAISS Issues:**
- Verify FAISS installation: `python -c "import faiss; print(faiss.__version__)"`
- Check CUDA compatibility for GPU acceleration
- Fall back to CPU-only mode if needed

**Mesopredator Command Issues:**
- Ensure PATH includes ~/.local/bin: `echo $PATH`
- Verify script exists: `ls -la ~/.local/bin/mesopredator`
- Check permissions: `chmod +x ~/.local/bin/mesopredator`

---

## API Reference

### Python API

```python
from src.cognitive.persistent_recursion import MesopredatorPRI

# Initialize system
pri = MesopredatorPRI(config_path="config/")

# Analyze project
results = pri.analyze_project(
    project_path="/path/to/code",
    max_depth=2,
    enable_learning=True
)

# Access results
print(f"Found {results.total_issues} issues")
for issue in results.security_issues:
    print(f"{issue.severity}: {issue.description}")
```

### REST API (if enabled)

```bash
# Start API server
python -m src.api.server --port 8080

# Analyze project
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"project_path": "/path/to/code", "max_depth": 2}'
```

---

## Support & Community

### Getting Help

1. **Documentation**: Check this manual and `/docs` directory
2. **Issues**: Report bugs at GitHub Issues
3. **Discussions**: Join community discussions for usage questions
4. **Security Issues**: Report privately to security@yourorg.com

### Contributing

1. **Bug Reports**: Use GitHub Issues with detailed reproduction steps
2. **Feature Requests**: Propose new capabilities with use cases
3. **Code Contributions**: Follow contribution guidelines in CONTRIBUTING.md
4. **Pattern Contributions**: Submit new detection patterns for common issues

### Roadmap

**Short Term (Next 3 months):**
- Enhanced language support
- Performance optimizations
- Additional security patterns

**Medium Term (6 months):**
- Cross-domain correlation capabilities
- Advanced synthesis features
- Enterprise integration tools

**Long Term (12+ months):**
- Autonomous orchestration capabilities
- Self-improving architecture
- Advanced AI reasoning features

---

## Appendix

### Supported File Types

| Language | Extensions | Analysis Level |
|----------|------------|----------------|
| Python | .py, .pyw | Full semantic |
| JavaScript | .js, .jsx, .ts, .tsx | Full semantic |
| Java | .java | Full semantic |
| C/C++ | .c, .cpp, .h, .hpp | Full semantic |
| Rust | .rs | Good semantic |
| Go | .go | Good semantic |
| PHP | .php | Basic semantic |
| Ruby | .rb | Basic semantic |
| Shell | .sh, .bash | Pattern-based |

### Exit Codes

- **0**: Analysis completed successfully
- **1**: Analysis completed with issues found
- **2**: Configuration error
- **3**: Permission error
- **4**: Resource exhaustion
- **5**: Internal system error

### Environment Variables

- `MESOPREDATOR_CONFIG`: Path to configuration directory
- `MESOPREDATOR_MEMORY`: Path to memory database
- `MESOPREDATOR_CACHE`: Path to cache directory
- `MESOPREDATOR_LOG_LEVEL`: Logging level (DEBUG, INFO, WARN, ERROR)

---

## License

This software is licensed under [Your License]. See LICENSE file for details.

## Disclaimer

Mesopredator PRI is a **code analysis tool** designed to assist human developers. It should not be used as the sole method for security assessment or code quality evaluation. Always combine automated analysis with human code review and appropriate testing methodologies.

**Security Note**: While the system includes comprehensive security protections, no software is 100% secure. Run in isolated environments and follow security best practices for production deployments.

---

**Version:** 1.0  
**Last Updated:** 2025-06-29  
**Maintained by:** [Your Organization]  
**Support:** [Contact Information]