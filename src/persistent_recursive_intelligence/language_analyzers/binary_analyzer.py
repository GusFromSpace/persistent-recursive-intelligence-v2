#!/usr/bin/env python3
"""
Binary File Analyzer for Mesopredator PRI
Analyzes binary file formats including ESM/ESP files, executables, and data files
"""

import struct
import mmap
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
import json

try:
    from .base_language_analyzer import BaseLanguageAnalyzer
except ImportError:
    # Fallback for when running standalone
    from abc import ABC, abstractmethod
    from pathlib import Path as PathType
    
    class BaseLanguageAnalyzer(ABC):
        def __init__(self, language: str, memory_engine):
            self.language = language
            self.memory_engine = memory_engine
            
        @abstractmethod
        def detect_issues(self, file_path: str):
            pass

@dataclass
class BinaryPattern:
    """Pattern found in binary files"""
    pattern_type: str
    offset: int
    size: int
    description: str
    data_sample: bytes
    confidence: float

@dataclass
class BinaryStructure:
    """Identified structure in binary file"""
    name: str
    offset: int
    size: int
    fields: List[Dict[str, Any]]
    format_type: str

class BinaryAnalyzer(BaseLanguageAnalyzer):
    """Analyzes binary file formats with focus on game data files"""
    
    def __init__(self, memory_engine):
        super().__init__(language="binary", memory_engine=memory_engine)
        self.file_extensions = [
            '.esm', '.esp', '.bsa',  # Elder Scrolls
            '.exe', '.dll', '.so',   # Executables 
            '.dat', '.bin', '.pak',  # Data files
            '.db', '.sqlite',        # Databases
            '.img', '.iso',          # Disk images
        ]
        
        # Binary file signatures
        self.file_signatures = {
            # Elder Scrolls formats
            b'TES3': 'morrowind_esm',
            b'TES4': 'oblivion_esp', 
            b'TES5': 'skyrim_esp',
            
            # Archive formats
            b'BSA\x00': 'bethesda_archive',
            b'PK\x03\x04': 'zip_archive',
            b'Rar!': 'rar_archive',
            
            # Executable formats
            b'MZ': 'dos_executable',
            b'\x7fELF': 'linux_executable',
            b'\xca\xfe\xba\xbe': 'macos_universal',
            
            # Database formats
            b'SQLite format 3': 'sqlite_database',
            
            # Image formats
            b'\x89PNG': 'png_image',
            b'\xff\xd8\xff': 'jpeg_image',
            b'GIF8': 'gif_image',
        }
        
        # ESM/ESP record types for Elder Scrolls analysis
        self.tes_record_types = {
            b'CELL': 'cell_data',
            b'REFR': 'object_reference', 
            b'NPC_': 'character_data',
            b'WEAP': 'weapon_data',
            b'ARMO': 'armor_data',
            b'MISC': 'misc_item',
            b'BOOK': 'book_data',
            b'CONT': 'container_data',
            b'DOOR': 'door_data',
            b'FURN': 'furniture_data',
            b'LIGH': 'light_source',
            b'STAT': 'static_object',
            b'TREE': 'vegetation',
            b'CREA': 'creature_data',
            b'DIAL': 'dialog_data',
            b'QUEST': 'quest_data',
            b'SCPT': 'script_data',
        }
        
        self.pattern_categories = {
            "file_format": ["esm_structure", "esp_structure", "archive_format"],
            "game_data": ["cell_records", "object_references", "script_data"],
            "security": ["executable_sections", "embedded_scripts", "suspicious_patterns"],
            "performance": ["large_data_blocks", "unoptimized_structures", "fragmentation"],
            "data_integrity": ["checksum_validation", "reference_consistency", "format_compliance"]
        }
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a binary file and extract patterns"""
        path = Path(file_path)
        
        if not path.exists():
            return {"error": f"File not found: {file_path}"}
        
        if not path.is_file():
            return {"error": f"Not a file: {file_path}"}
        
        try:
            analysis = {
                "file_path": str(path),
                "file_size": path.stat().st_size,
                "file_type": "unknown",
                "format_confidence": 0.0,
                "structures": [],
                "patterns": [],
                "issues": [],
                "metadata": {}
            }
            
            # Read file header to identify format
            with open(path, 'rb') as f:
                header = f.read(min(1024, path.stat().st_size))
            
            # Identify file format
            file_type, confidence = self._identify_file_format(header)
            analysis["file_type"] = file_type
            analysis["format_confidence"] = confidence
            
            # Perform format-specific analysis
            if file_type.endswith('_esm') or file_type.endswith('_esp'):
                analysis.update(self._analyze_tes_file(path))
            elif file_type.endswith('_executable'):
                analysis.update(self._analyze_executable(path))
            elif file_type.endswith('_database'):
                analysis.update(self._analyze_database(path))
            else:
                analysis.update(self._analyze_generic_binary(path))
            
            # Generate hash for integrity checking
            analysis["metadata"]["sha256"] = self._calculate_file_hash(path)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _identify_file_format(self, header: bytes) -> Tuple[str, float]:
        """Identify binary file format from header"""
        for signature, format_type in self.file_signatures.items():
            if header.startswith(signature):
                return format_type, 1.0
        
        # Check for partial matches or patterns
        if b'CELL' in header[:200] and b'REFR' in header[:1000]:
            return 'elder_scrolls_mod', 0.8
        
        if header.startswith(b'\x00\x00') and len(header) > 10:
            return 'binary_data', 0.3
        
        return 'unknown_binary', 0.0
    
    def _analyze_tes_file(self, path: Path) -> Dict[str, Any]:
        """Analyze Elder Scrolls ESM/ESP files"""
        analysis = {
            "tes_records": [],
            "cell_count": 0,
            "object_count": 0,
            "script_count": 0,
            "dialog_count": 0
        }
        
        try:
            with open(path, 'rb') as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    offset = 0
                    
                    while offset < len(mm) - 8:
                        # Read record header
                        try:
                            record_type = mm[offset:offset+4]
                            record_size = struct.unpack('<I', mm[offset+4:offset+8])[0]
                            
                            if record_type in self.tes_record_types:
                                record_info = {
                                    "type": self.tes_record_types[record_type],
                                    "offset": offset,
                                    "size": record_size,
                                    "record_type_raw": record_type.decode('ascii', errors='ignore')
                                }
                                
                                analysis["tes_records"].append(record_info)
                                
                                # Count specific record types
                                if record_type == b'CELL':
                                    analysis["cell_count"] += 1
                                elif record_type == b'REFR':
                                    analysis["object_count"] += 1
                                elif record_type == b'SCPT':
                                    analysis["script_count"] += 1
                                elif record_type == b'DIAL':
                                    analysis["dialog_count"] += 1
                            
                            offset += 8 + record_size
                            
                        except (struct.error, ValueError):
                            offset += 1  # Skip bad data
                        
                        # Prevent infinite loops
                        if len(analysis["tes_records"]) > 10000:
                            break
            
            # Generate patterns based on analysis
            self._generate_tes_patterns(analysis)
            
        except Exception as e:
            analysis["error"] = f"TES analysis failed: {str(e)}"
        
        return analysis
    
    def _generate_tes_patterns(self, analysis: Dict[str, Any]):
        """Generate patterns for TES file analysis"""
        patterns = []
        
        # Cell density pattern
        if analysis["cell_count"] > 0:
            pattern = BinaryPattern(
                pattern_type="esm_structure",
                offset=0,
                size=analysis.get("file_size", 0),
                description=f"ESM file with {analysis['cell_count']} cells and {analysis['object_count']} objects",
                data_sample=b'CELL',
                confidence=0.9
            )
            patterns.append(pattern)
        
        # Script presence
        if analysis["script_count"] > 0:
            pattern = BinaryPattern(
                pattern_type="script_data", 
                offset=0,
                size=0,
                description=f"Contains {analysis['script_count']} embedded scripts",
                data_sample=b'SCPT',
                confidence=0.8
            )
            patterns.append(pattern)
        
        # Performance consideration
        if analysis["object_count"] > 1000:
            pattern = BinaryPattern(
                pattern_type="large_data_blocks",
                offset=0,
                size=0,
                description=f"Large object count ({analysis['object_count']}) may impact loading performance",
                data_sample=b'REFR',
                confidence=0.7
            )
            patterns.append(pattern)
        
        analysis["patterns"] = [p.__dict__ for p in patterns]
    
    def _analyze_executable(self, path: Path) -> Dict[str, Any]:
        """Analyze executable files"""
        analysis = {
            "executable_type": "unknown",
            "sections": [],
            "imports": [],
            "exports": []
        }
        
        try:
            with open(path, 'rb') as f:
                header = f.read(1024)
            
            if header.startswith(b'MZ'):
                analysis["executable_type"] = "pe_executable"
                # Basic PE analysis could be added here
            elif header.startswith(b'\x7fELF'):
                analysis["executable_type"] = "elf_executable"
                # Basic ELF analysis could be added here
                
        except Exception as e:
            analysis["error"] = f"Executable analysis failed: {str(e)}"
        
        return analysis
    
    def _analyze_database(self, path: Path) -> Dict[str, Any]:
        """Analyze database files"""
        analysis = {
            "database_type": "unknown",
            "tables": [],
            "schema_info": {}
        }
        
        try:
            # Basic SQLite detection
            with open(path, 'rb') as f:
                header = f.read(100)
            
            if b'SQLite format 3' in header:
                analysis["database_type"] = "sqlite3"
                # Could add SQLite schema analysis here
                
        except Exception as e:
            analysis["error"] = f"Database analysis failed: {str(e)}"
        
        return analysis
    
    def _analyze_generic_binary(self, path: Path) -> Dict[str, Any]:
        """Analyze generic binary files"""
        analysis = {
            "entropy": 0.0,
            "repeated_patterns": [],
            "null_bytes": 0,
            "ascii_strings": []
        }
        
        try:
            with open(path, 'rb') as f:
                data = f.read(min(65536, path.stat().st_size))  # Read first 64KB
            
            # Calculate entropy
            analysis["entropy"] = self._calculate_entropy(data)
            
            # Count null bytes
            analysis["null_bytes"] = data.count(b'\x00')
            
            # Find ASCII strings
            analysis["ascii_strings"] = self._extract_ascii_strings(data)[:20]  # Limit to 20
            
        except Exception as e:
            analysis["error"] = f"Generic binary analysis failed: {str(e)}"
        
        return analysis
    
    def _calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of binary data"""
        if not data:
            return 0.0
        
        # Count byte frequencies
        frequencies = [0] * 256
        for byte in data:
            frequencies[byte] += 1
        
        # Calculate entropy
        entropy = 0.0
        data_len = len(data)
        
        for freq in frequencies:
            if freq > 0:
                p = freq / data_len
                entropy -= p * (p.bit_length() - 1)  # Approximation of log2(p)
        
        return entropy
    
    def _extract_ascii_strings(self, data: bytes, min_length: int = 4) -> List[str]:
        """Extract printable ASCII strings from binary data"""
        strings = []
        current_string = ""
        
        for byte in data:
            if 32 <= byte <= 126:  # Printable ASCII range
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        # Add final string if valid
        if len(current_string) >= min_length:
            strings.append(current_string)
        
        return strings
    
    def _calculate_file_hash(self, path: Path) -> str:
        """Calculate SHA256 hash of file"""
        hasher = hashlib.sha256()
        
        try:
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return "hash_calculation_failed"
    
    def detect_issues(self, file_path: str) -> List[Dict[str, Any]]:
        """Detect issues in binary files"""
        issues = []
        
        try:
            analysis = self.analyze_file(file_path)
            
            # File format issues
            if analysis.get("format_confidence", 0) < 0.5:
                issues.append({
                    "severity": "medium",
                    "category": "format_recognition",
                    "message": "File format could not be reliably identified",
                    "suggestion": "Verify file integrity and format specifications"
                })
            
            # ESM/ESP specific issues
            if analysis.get("file_type", "").endswith(('_esm', '_esp')):
                if analysis.get("cell_count", 0) == 0:
                    issues.append({
                        "severity": "high", 
                        "category": "data_integrity",
                        "message": "No cell records found in ESM/ESP file",
                        "suggestion": "File may be corrupted or incomplete"
                    })
                
                if analysis.get("object_count", 0) > 5000:
                    issues.append({
                        "severity": "low",
                        "category": "performance",
                        "message": f"High object count ({analysis['object_count']}) may impact game performance",
                        "suggestion": "Consider optimizing object placement or splitting into multiple files"
                    })
            
            # Generic binary issues
            if analysis.get("entropy", 0) < 1.0:
                issues.append({
                    "severity": "low",
                    "category": "data_analysis",
                    "message": "Low entropy suggests highly repetitive data",
                    "suggestion": "File may benefit from compression or optimization"
                })
            
        except Exception as e:
            issues.append({
                "severity": "high",
                "category": "analysis_error",
                "message": f"Binary analysis failed: {str(e)}",
                "suggestion": "File may be corrupted or in an unsupported format"
            })
        
        return issues
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        return self.file_extensions.copy()

def create_binary_analyzer(memory_engine) -> BinaryAnalyzer:
    """Factory function to create binary analyzer"""
    return BinaryAnalyzer(memory_engine)