import re
from pathlib import Path
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass
from enum import Enum

from .base_analyzer import BaseLanguageAnalyzer
from src.cognitive.memory.simple_memory import SimpleMemoryEngine as MemoryIntelligence

# Import the new standard interfaces
try:
    from src.cognitive.enhanced_patterns.code_connector import FileCapabilities
except ImportError:
    # Fallback for basic FileCapabilities if not available
    @dataclass
    class FileCapabilities:
        functions: List[Dict] = None
        classes: List[Dict] = None
        constants: List[str] = None
        imports: List[str] = None
        keywords: Set[str] = None
        complexity_score: int = 0
        has_main_guard: bool = False
        file_size: int = 0

# Language specification for C++
class LanguageFamily(Enum):
    SYSTEMS_PROGRAMMING = "systems_programming"
    DYNAMIC_SCRIPTING = "dynamic_scripting"
    FUNCTIONAL = "functional"
    JVM_BASED = "jvm_based"

class MemoryModel(Enum):
    MANUAL_MANAGEMENT = "manual_management"
    GARBAGE_COLLECTED = "garbage_collected"
    OWNERSHIP_SYSTEM = "ownership_system"

@dataclass
class LanguageSpecification:
    name: str
    family: LanguageFamily
    file_extensions: Set[str]
    primary_extension: str
    case_convention: str
    paradigms: List[str]
    memory_model: MemoryModel
    compilation_model: str
    type_system: str
    has_pointers: bool = False
    has_exceptions: bool = True
    has_generics: bool = True
    has_macros: bool = False
    has_ffi: bool = False
    import_syntax: str = ""
    comment_syntax: List[str] = None
    string_delimiters: List[str] = None

class CppAnalyzer(BaseLanguageAnalyzer):
    """
    Enhanced C++ language analyzer compliant with Multi-Language Support Standard.
    
    Features:
    - AI-generated code pattern detection
    - Memory management analysis
    - Performance pattern recognition
    - Cross-language correlation with C and systems languages
    - Educational content generation
    """
    
    def __init__(self):
        super().__init__()
        self._specification = self.get_language_specification()

    @property
    def language_name(self) -> str:
        return "cpp"

    @property
    def file_extensions(self) -> Set[str]:
        return self._specification.file_extensions
    
    def get_language_specification(self) -> LanguageSpecification:
        """Complete C++ language specification"""
        return LanguageSpecification(
            name="cpp",
            family=LanguageFamily.SYSTEMS_PROGRAMMING,
            file_extensions={".cpp", ".hpp", ".h", ".c", ".cc", ".cxx", ".hxx"},
            primary_extension=".cpp",
            case_convention="snake_case",  # or camelCase depending on style
            paradigms=["procedural", "object_oriented", "generic", "functional"],
            memory_model=MemoryModel.MANUAL_MANAGEMENT,
            compilation_model="compiled",
            type_system="static",
            has_pointers=True,
            has_exceptions=True,
            has_generics=True,
            has_macros=True,
            has_ffi=True,
            import_syntax="#include <{module}>",
            comment_syntax=["/", "//", "/* */"],
            string_delimiters=['"', "'"]
        )
    
    @property
    def language_family(self) -> LanguageFamily:
        return self._specification.family

    def analyze_file(self, file_path: Path, content: str, memory: MemoryIntelligence, global_memory: MemoryIntelligence) -> List[Dict[str, Any]]:
        """Enhanced C++ file analysis with memory intelligence integration"""
        issues = []
        
        # Core analysis methods
        issues.extend(self._detect_ai_patterns(content, file_path))
        issues.extend(self._analyze_cpp_syntax(content, file_path))
        issues.extend(self._analyze_namespace_structure(content, file_path))
        issues.extend(self._analyze_include_structure(content, file_path))
        
        # Enhanced analysis methods
        issues.extend(self.analyze_security_patterns(content, file_path))
        issues.extend(self.analyze_performance_patterns(content, file_path))
        issues.extend(self._analyze_memory_management(content, file_path))
        
        # Learn from analysis for future improvements
        self.learn_from_analysis(issues, memory)
        
        # Add educational content
        for issue in issues:
            issue['educational_content'] = self.generate_educational_content(issue)
            issue['similar_patterns'] = self.get_similar_patterns(issue['type'], memory)
        
        return issues

    def _detect_ai_patterns(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Common AI mistake patterns in C++"""
        issues = []
        patterns = {
            "incorrect_include_paths": {
                "pattern": r'"\.\./\.\./\.\./[^\"]*"',
                "severity": "high",
                "description": "AI creates incorrect relative include paths due to lack of project structure context",
            },
            "double_namespace": {
                "pattern": r'namespace\s+(\w+)\s*\{\s*namespace\s+\1\s*\{',
                "severity": "high",
                "description": "AI creates double namespace declarations",
            },
            "const_duplication": {
                "pattern": r'\bconst\s+const\b',
                "severity": "medium",
                "description": "AI duplicates const keyword",
            },
            "static_duplication": {
                "pattern": r'\bstatic\s+static\b',
                "severity": "medium",
                "description": "AI duplicates static keyword",
            },
            "platform_specific_includes": {
                "pattern": r'#include\s+<OpenGL/gl3\.h>',
                "severity": "medium",
                "description": "AI uses platform-specific includes without guards",
            },
            "namespace_pollution": {
                "pattern": r'using\s+namespace\s+std\s*;\s*namespace',
                "severity": "medium",
                "description": "AI places using statements in wrong scope",
            },
        }

        for issue_type, pattern_info in patterns.items():
            for match in re.finditer(pattern_info["pattern"], content):
                issues.append({
                    "type": f"cpp_{issue_type}",
                    "line": content[:match.start()].count('\n') + 1,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "file_path": str(file_path),
                })
        return issues

    def _analyze_cpp_syntax(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze C++ syntax issues"""
        issues = []
        syntax_patterns = {
            "missing_semicolon": {
                "pattern": r'\}\s*$(?!\s*;)',
                "severity": "high",
                "description": "Possible missing semicolon after class/struct definition"
            },
        }

        for issue_type, pattern_info in syntax_patterns.items():
            for match in re.finditer(pattern_info["pattern"], content, re.MULTILINE):
                issues.append({
                    "type": f"cpp_syntax_{issue_type}",
                    "line": content[:match.start()].count('\n') + 1,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "file_path": str(file_path),
                })
        return issues

    def _analyze_namespace_structure(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze namespace structure issues"""
        issues = []
        brace_opens = content.count('{')
        brace_closes = content.count('}')

        if brace_opens != brace_closes:
            issues.append({
                "type": "cpp_brace_imbalance",
                "severity": "high",
                "file_path": str(file_path),
                "line": None,
                "description": f"Brace imbalance: {brace_opens} opens, {brace_closes} closes",
            })

        nested_pattern = r'namespace\s+\w+\s*\{\s*namespace\s+\w+\s*\{\s*namespace\s+\w+\s*\{'
        if re.search(nested_pattern, content):
            issues.append({
                "type": "cpp_excessive_namespace_nesting",
                "severity": "medium",
                "file_path": str(file_path),
                "line": None,
                "description": "Excessive namespace nesting detected - consider flattening",
            })
        return issues

    def _analyze_include_structure(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze include structure issues"""
        issues = []
        includes = re.findall(r'#include\s+[<\"][^>\"]*[>\"]', content)
        seen_includes = set()
        for include in includes:
            if include in seen_includes:
                line_num = content.find(include, content.find(include) + 1)
                line_num = content[:line_num].count('\n') + 1 if line_num != -1 else None
                issues.append({
                    "type": "cpp_duplicate_include",
                    "severity": "low",
                    "file_path": str(file_path),
                    "line": line_num,
                    "description": f"Duplicate include: {include}",
                })
            seen_includes.add(include)

        system_after_local = re.search(r'#include\s+"[^\"]*"\s*\n.*#include\s+<[^>]*>', content, re.DOTALL)
        if system_after_local:
            issues.append({
                "type": "cpp_include_order",
                "severity": "low",
                "file_path": str(file_path),
                "line": None,
                "description": "System includes should come before local includes",
            })
        return issues
    
    # Enhanced Analysis Methods (Multi-Language Standard Compliance)
    
    def extract_basic_capabilities(self, content: str, file_path: Path) -> FileCapabilities:
        """Extract C++ file capabilities using text patterns"""
        
        # Extract functions
        functions = []
        function_pattern = r'(?:^|\n)\s*(?:[\w:]+\s+)*(\w+)\s*\([^)]*\)\s*(?:const)?\s*(?:override)?\s*(?:\{|;)'
        for match in re.finditer(function_pattern, content):
            functions.append({
                "name": match.group(1),
                "line": content[:match.start()].count('\n') + 1,
                "signature": match.group(0).strip()
            })
        
        # Extract classes and structs
        classes = []
        class_pattern = r'(?:class|struct)\s+(\w+)(?:\s*:\s*[^{]*)?(?:\s*\{|;)'
        for match in re.finditer(class_pattern, content):
            classes.append({
                "name": match.group(1),
                "line": content[:match.start()].count('\n') + 1,
                "type": "class" if "class" in match.group(0) else "struct"
            })
        
        # Extract includes (imports)
        imports = re.findall(r'#include\s+[<"][^>"]*[>"]', content)
        
        # Extract preprocessor constants
        constants = re.findall(r'#define\s+(\w+)', content)
        
        # Extract keywords for semantic analysis
        cpp_keywords = {
            'virtual', 'override', 'const', 'static', 'inline', 'template',
            'namespace', 'class', 'struct', 'enum', 'union', 'typedef',
            'public', 'private', 'protected', 'friend', 'extern',
            'new', 'delete', 'malloc', 'free', 'smart_ptr', 'unique_ptr', 'shared_ptr'
        }
        
        found_keywords = set()
        content_lower = content.lower()
        for keyword in cpp_keywords:
            if keyword in content_lower:
                found_keywords.add(keyword)
        
        # Calculate complexity score
        complexity_score = (
            len(functions) * 2 +
            len(classes) * 3 +
            content.count('if') +
            content.count('for') +
            content.count('while') +
            content.count('switch') +
            content.count('try')
        )
        
        # Check for main function
        has_main_guard = bool(re.search(r'int\s+main\s*\(', content))
        
        return FileCapabilities(
            functions=functions,
            classes=classes,
            constants=constants,
            imports=imports,
            keywords=found_keywords,
            complexity_score=complexity_score,
            has_main_guard=has_main_guard,
            file_size=len(content)
        )
    
    def analyze_security_patterns(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze C++ security vulnerabilities and anti-patterns"""
        issues = []
        
        security_patterns = {
            "buffer_overflow_risk": {
                "pattern": r'\b(strcpy|strcat|sprintf|gets)\s*\(',
                "severity": "high",
                "description": "Unsafe C string function that can cause buffer overflow",
                "suggestion": "Use safer alternatives like strcpy_s, strcat_s, snprintf, or std::string"
            },
            "null_pointer_dereference": {
                "pattern": r'(\w+)\s*->\s*\w+.*(?:delete|free)\s+\1',
                "severity": "high", 
                "description": "Potential null pointer dereference after deletion",
                "suggestion": "Set pointer to nullptr after deletion and check for null before use"
            },
            "memory_leak_risk": {
                "pattern": r'\bnew\s+\w+(?!\s*\[)(?!.*delete)',
                "severity": "medium",
                "description": "Dynamic allocation without corresponding delete",
                "suggestion": "Use RAII or smart pointers (unique_ptr, shared_ptr) to manage memory automatically"
            },
            "unsafe_cast": {
                "pattern": r'\([\w\s\*]+\)\s*\w+',
                "severity": "medium",
                "description": "C-style cast detected, may be unsafe",
                "suggestion": "Use C++ style casts (static_cast, dynamic_cast, const_cast, reinterpret_cast)"
            },
            "macro_safety": {
                "pattern": r'#define\s+\w+\([^)]*\)(?!.*do\s*\{.*\}\s*while\s*\(0\))',
                "severity": "low",
                "description": "Function-like macro without do-while(0) wrapper",
                "suggestion": "Wrap multi-statement macros in do-while(0) or use inline functions"
            }
        }
        
        for issue_type, pattern_info in security_patterns.items():
            for match in re.finditer(pattern_info["pattern"], content):
                issues.append({
                    "type": f"cpp_security_{issue_type}",
                    "line": content[:match.start()].count('\n') + 1,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "suggestion": pattern_info["suggestion"],
                    "file_path": str(file_path),
                })
        
        return issues
    
    def analyze_performance_patterns(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze C++ performance patterns and optimization opportunities"""
        issues = []
        
        performance_patterns = {
            "inefficient_string_concat": {
                "pattern": r'std::string\s+\w+\s*=\s*[^;]*\+[^;]*\+',
                "severity": "medium",
                "description": "Inefficient string concatenation with multiple + operators",
                "suggestion": "Use std::stringstream or reserve() with += for multiple concatenations"
            },
            "pass_by_value_large": {
                "pattern": r'void\s+\w+\s*\(\s*std::(?:vector|string|map|set)\s+\w+\s*\)',
                "severity": "medium", 
                "description": "Passing large objects by value instead of const reference",
                "suggestion": "Pass large objects by const reference: const std::vector<T>& param"
            },
            "vector_reallocation": {
                "pattern": r'std::vector<[^>]+>\s+\w+(?!.*\.reserve\()',
                "severity": "low",
                "description": "Vector declared without reserve() - may cause reallocations",
                "suggestion": "Call reserve() if you know the approximate final size"
            },
            "iostream_sync": {
                "pattern": r'std::cout|std::cin|std::endl',
                "severity": "low",
                "description": "Using std::endl flushes buffer unnecessarily",
                "suggestion": "Use '\\n' instead of std::endl for better performance, or disable iostream sync"
            }
        }
        
        for issue_type, pattern_info in performance_patterns.items():
            for match in re.finditer(pattern_info["pattern"], content):
                issues.append({
                    "type": f"cpp_performance_{issue_type}",
                    "line": content[:match.start()].count('\n') + 1,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "suggestion": pattern_info["suggestion"],
                    "file_path": str(file_path),
                })
        
        return issues
    
    def _analyze_memory_management(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze memory management patterns in C++"""
        issues = []
        
        memory_patterns = {
            "raw_pointer_usage": {
                "pattern": r'\b(?:int|char|float|double|void|struct\s+\w+)\s*\*\s*\w+\s*=\s*new\b',
                "severity": "medium",
                "description": "Raw pointer with new - consider RAII",
                "suggestion": "Use smart pointers (std::unique_ptr, std::shared_ptr) for automatic memory management"
            },
            "missing_virtual_destructor": {
                "pattern": r'class\s+\w+[^{]*\{(?:[^}]*virtual[^}]*)?(?![^}]*virtual[^}]*~)',
                "severity": "high",
                "description": "Class with virtual functions but no virtual destructor",
                "suggestion": "Add virtual destructor to base classes with virtual functions"
            },
            "array_delete_mismatch": {
                "pattern": r'new\s*\[[^\]]*\](?:[^;]*;[^}]*(?:delete\s+(?!\[\])|\bfree\s*\())',
                "severity": "high",
                "description": "Array allocated with new[] but not deleted with delete[]",
                "suggestion": "Use delete[] for arrays allocated with new[], or use std::vector/std::array"
            }
        }
        
        for issue_type, pattern_info in memory_patterns.items():
            for match in re.finditer(pattern_info["pattern"], content, re.DOTALL):
                issues.append({
                    "type": f"cpp_memory_{issue_type}",
                    "line": content[:match.start()].count('\n') + 1,
                    "severity": pattern_info["severity"],
                    "description": pattern_info["description"],
                    "suggestion": pattern_info["suggestion"],
                    "file_path": str(file_path),
                })
        
        return issues
    
    # Framework Compliance Methods
    
    def get_validation_commands(self) -> List[str]:
        """Get C++ validation commands"""
        return [
            "g++ -fsyntax-only {file}",
            "clang++ -fsyntax-only {file}",
            "cppcheck --enable=all {file}"
        ]
    
    def get_formatting_command(self) -> Optional[str]:
        """Get C++ formatting command"""
        return "clang-format -i {file}"
    
    def generate_import_statement(self, module: str, items: List[str]) -> str:
        """Generate C++ include statement"""
        if module.startswith('<') and module.endswith('>'):
            return f"#include {module}"
        elif not (module.startswith('"') and module.endswith('"')):
            return f'#include "{module}"'
        else:
            return f"#include {module}"
    
    def get_cross_language_correlations(self) -> List[str]:
        """Languages this C++ analyzer can correlate patterns with"""
        return ["c", "rust", "go"]  # Systems programming languages
    
    def generate_educational_content(self, issue: Dict[str, Any]) -> str:
        """Generate educational explanations for C++ issues"""
        issue_type = issue.get('type', '')
        description = issue.get('description', '')
        suggestion = issue.get('suggestion', '')
        
        educational_content = f"C++ Issue: {description}\\n"
        
        if suggestion:
            educational_content += f"Recommendation: {suggestion}\\n"
        
        # Add language-specific educational context
        if 'memory' in issue_type:
            educational_content += "\\nMemory Management in C++:\\n"
            educational_content += "C++ uses manual memory management. Following RAII (Resource Acquisition Is Initialization) "
            educational_content += "principle helps prevent memory leaks and ensures exception safety."
            
        elif 'security' in issue_type:
            educational_content += "\\nC++ Security Best Practices:\\n"
            educational_content += "Use modern C++ features like smart pointers, range-based loops, and standard library "
            educational_content += "containers to avoid common security vulnerabilities."
            
        elif 'performance' in issue_type:
            educational_content += "\\nC++ Performance Optimization:\\n"
            educational_content += "C++ provides zero-cost abstractions. Understanding move semantics, const correctness, "
            educational_content += "and memory locality can significantly improve performance."
        
        return educational_content
    
    # Memory Intelligence Integration
    
    def learn_from_analysis(self, findings: List[Dict[str, Any]], memory: MemoryIntelligence) -> None:
        """Store C++ analysis results in memory for future learning"""
        
        for finding in findings:
            pattern_description = f"{finding['type']}: {finding['description']}"
            metadata = {
                "language": self.language_name,
                "pattern_type": finding['type'],
                "severity": finding['severity'],
                "file_extension": finding.get('file_path', '').split('.')[-1],
                "suggestion": finding.get('suggestion', ''),
                "category": self._categorize_finding(finding['type'])
            }
            
            # Use the correct SimpleMemoryEngine interface
            memory.store_memory(pattern_description, metadata)
    
    def get_similar_patterns(self, issue_type: str, memory: MemoryIntelligence) -> List[str]:
        """Retrieve similar C++ patterns from memory for educational purposes"""
        query = f"{issue_type} {self.language_name}"
        
        try:
            # Use the correct SimpleMemoryEngine interface
            memories = memory.search_memories(query, limit=5)
            return [mem.get('content', '') for mem in memories if isinstance(mem, dict)]
        except Exception as e:
            # Fallback if memory interface has issues
            return [f"Similar pattern search unavailable: {str(e)}"]
    
    def _categorize_finding(self, finding_type: str) -> str:
        """Categorize findings for better memory organization"""
        if 'security' in finding_type:
            return 'security'
        elif 'performance' in finding_type:
            return 'performance'
        elif 'memory' in finding_type:
            return 'memory_management'
        elif 'syntax' in finding_type:
            return 'syntax'
        elif 'ai' in finding_type or any(x in finding_type for x in ['incorrect', 'double', 'duplication']):
            return 'ai_patterns'
        else:
            return 'general'


# Auto-Registration Function for Multi-Language Support Standard
def register_analyzer():
    """
    Auto-registration function called by Auto-Updater system.
    This demonstrates the standardized language analyzer installation process.
    """
    try:
        from src.cognitive.orchestration.analyzer_orchestrator import AnalyzerOrchestrator
        
        # Instantiate the enhanced C++ analyzer
        analyzer = CppAnalyzer()
        
        # Register with orchestrator
        orchestrator = AnalyzerOrchestrator()
        success = orchestrator.register_language_analyzer(analyzer)
        
        # Setup dedicated memory namespace for C++
        if success:
            from src.cognitive.memory.simple_memory import SimpleMemoryEngine
            memory = SimpleMemoryEngine(namespace=f"pri_{analyzer.language_name}")
            
            # Store initialization information
            memory.store_memory(
                f"C++ Language Intelligence initialized",
                {
                    "language_family": "systems_programming",
                    "correlates_with": analyzer.get_cross_language_correlations(),
                    "memory_quota_mb": 200,
                    "pattern_categories": ["memory_management", "performance", "security", "ai_patterns", "syntax"]
                }
            )
            
            logger.info(f"✅ C++ Analyzer registered successfully with dedicated memory namespace: {namespace}")
        
        return success
        
    except Exception as e:
        logger.info(f"❌ Failed to register C++ analyzer: {e}")
        return False
