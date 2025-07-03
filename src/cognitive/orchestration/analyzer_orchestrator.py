import inspect
from pathlib import Path
from typing import List, Dict, Any

from ..analyzers import cpp_analyzer, python_analyzer
from ..analyzers.base_analyzer import BaseLanguageAnalyzer
from ..memory.simple_memory import SimpleMemoryEngine as MemoryIntelligence


class AnalyzerOrchestrator:
    """
    Loads and manages all available language analyzers.
    """

    def __init__(self):
        self.analyzers = self._load_analyzers()

    def _load_analyzers(self) -> List[BaseLanguageAnalyzer]:
        """Dynamically load all analyzer classes from the analyzers module."""
        analyzers = []
        # Manual import for now, can be made dynamic later
        for module in [cpp_analyzer, python_analyzer]:
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseLanguageAnalyzer) and obj is not BaseLanguageAnalyzer:
                    analyzers.append(obj())
        return analyzers

    def get_analyzer_for_file(self, file_path: Path) -> BaseLanguageAnalyzer | None:
        """Get the appropriate analyzer for a given file path."""
        file_extension = file_path.suffix
        for analyzer in self.analyzers:
            if file_extension in analyzer.file_extensions:
                return analyzer
        return None

    def analyze_file(self, file_path: Path, content: str, memory: MemoryIntelligence, global_memory: MemoryIntelligence) -> List[Dict[str, Any]]:
        """Analyze a file with the appropriate analyzer."""
        analyzer = self.get_analyzer_for_file(file_path)
        if analyzer:
            return analyzer.analyze_file(file_path, content, memory, global_memory)
        return []

    def register_language_analyzer(self, analyzer):
        pass
