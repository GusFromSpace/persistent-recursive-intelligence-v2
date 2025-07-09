from pathlib import Path
from typing import List, Dict, Any, Set

from .base_analyzer import BaseLanguageAnalyzer

from persistent_recursive_intelligence.cognitive.memory.simple_memory import SimpleMemoryEngine as MemoryIntelligence

class PythonAnalyzer(BaseLanguageAnalyzer):
    """
    Python language analyzer for common issues.
    """

    @property
    def language_name(self) -> str:
        return "python"

    @property
    def file_extensions(self) -> Set[str]:
        return {".py"}

    def analyze_file(self, file_path: Path, content: str, memory: MemoryIntelligence, global_memory: MemoryIntelligence) -> List[Dict[str, Any]]:
        """Analyze a single Python file."""
        issues = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            if any(keyword in line_stripped for keyword in ["TODO", "FIXME", "XXX", "HACK", "BUG"]):
                issues.append({
                    "type": "maintenance",
                    "line": i + 1,
                    "severity": "medium",
                    "description": f"Maintenance comment: {line_stripped[:100]}",
                    "file_path": str(file_path)
                })

            elif line_stripped.startswith("print(") and not self._is_test_file(file_path):
                issues.append({
                    "type": "debugging",
                    "line": i + 1,
                    "severity": "low",
                    "description": f"Debug print statement in production code",
                    "file_path": str(file_path)
                })

            elif "import *" in line_stripped and "from" in line_stripped:
                issues.append({
                    "type": "code_quality",
                    "line": i + 1,
                    "severity": "medium",
                    "description": f"Wildcard import: {line_stripped}",
                    "file_path": str(file_path)
                })

            elif line_stripped == "except Exception as e:" or "except Exception as e:" in line_stripped:
                issues.append({
                    "type": "exception_handling",
                    "line": i + 1,
                    "severity": "high",
                    "description": f"Bare except clause catches all exceptions",
                    "file_path": str(file_path)
                })

            elif any(sec_pattern in line_lower for sec_pattern in ["password", "secret", "key", "token"]) and "=" in line_stripped and ("'" in line_stripped or '"' in line_stripped):
                if not any(safe_pattern in line_lower for safe_pattern in ["getenv", "environ", "config", "input"]):
                    issues.append({
                        "type": "security",
                        "line": i + 1,
                        "severity": "critical",
                        "description": f"Potential hardcoded credential",
                        "file_path": str(file_path)
                    })

            elif any(sql_word in line_lower for sql_word in ["execute(", "cursor.execute", "query"]) and ("+" in line_stripped or "%" in line_stripped):
                issues.append({
                    "type": "security",
                    "line": i + 1,
                    "severity": "critical",
                    "description": f"Potential SQL injection vulnerability",
                    "file_path": str(file_path)
                })
        return issues

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file"""
        return (file_path.name.startswith("test_") or \
                "/test" in str(file_path) or \
                "tests/" in str(file_path) or \
                file_path.name.endswith("_test.py"))