
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any

from persistent_recursive_intelligence.cognitive.memory.simple_memory import SimpleMemoryEngine as MemoryIntelligence

class BaseLanguageAnalyzer(ABC):
    """
    Abstract base class for language-specific analyzers.
    """

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Return the name of the language this analyzer handles."""
        pass

    @property
    @abstractmethod
    def file_extensions(self) -> List[str]:
        """Return the file extensions this analyzer handles."""
        pass

    @abstractmethod
    def analyze_file(self, file_path: Path, content: str, memory: MemoryIntelligence, global_memory: MemoryIntelligence) -> List[Dict[str, Any]]:
        """
        Analyze a single file and return a list of detected issues.

        Args:
            file_path: The path to the file being analyzed.
            content: The content of the file.
            memory: The language-specific memory instance.
            global_memory: The global memory instance.

        Returns:
            A list of dictionaries, where each dictionary represents an issue.
        """
        pass
