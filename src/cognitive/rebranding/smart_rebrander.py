#!/usr/bin/env python3
"""
Smart Rebranding Tool
Intelligent code analysis and safe rebranding for any project
Uses pattern matching and context analysis to safely rebrand codebases
"""

import json
import logging
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import yaml


class RebrandingRisk(Enum):
    """Risk levels for rebranding operations"""
    SAFE = "safe"           # User-facing strings, comments, docs
    MEDIUM = "medium"       # Variable names, function names  
    HIGH = "high"          # Class names, imports, APIs
    CRITICAL = "critical"  # Core functionality, file paths

@dataclass
class RebrandingPattern:
    """Represents a rebranding pattern with safety analysis"""
    pattern: str
    replacement: str
    risk_level: RebrandingRisk
    description: str
    file_types: List[str]
    exclude_contexts: List[str] = None

@dataclass
class RebrandingResult:
    """Result of a rebranding operation"""
    file_path: Path
    changes_made: List[str]
    backup_path: Optional[Path]
    success: bool
    error_message: Optional[str] = None

class SmartRebrander:
    """
    Intelligent rebranding tool that analyzes code context and applies safe transformations
    """
    
    def __init__(self, project_root: str, config_file: Optional[str] = None):
        self.project_root = Path(project_root)
        self.results = []
        self.setup_logging()
        
        # Load configuration
        if config_file and Path(config_file).exists():
            self.config = self.load_config(config_file)
        else:
            self.config = self.get_default_config()
    
    def setup_logging(self):
        """Setup logging for the rebranding process"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.project_root / 'rebranding.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, config_file: str) -> Dict:
        """Load rebranding configuration from file"""
        config_path = Path(config_file)
        
        if config_path.suffix.lower() == '.json':
            with open(config_path, 'r') as f:
                return json.load(f)
        elif config_path.suffix.lower() in ['.yml', '.yaml']:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported config format: {config_path.suffix}")
    
    def get_default_config(self) -> Dict:
        """Get default rebranding configuration"""
        return {
            "rebranding_rules": [
                {
                    "old_brand": "PRI",
                    "new_brand": "Mesopredator",
                    "patterns": [
                        {
                            "pattern": r'print\(f?"🌀 Enhanced {old_brand}([^"]*)"',
                            "replacement": r'print(f"🌀 Enhanced {new_brand}\1"',
                            "risk_level": "safe",
                            "description": "User-facing print statements",
                            "file_types": ["*.py"]
                        },
                        {
                            "pattern": r'print\(f?"🌀 {old_brand} Analysis([^"]*)"',
                            "replacement": r'print(f"🌀 {new_brand} Analysis\1"',
                            "risk_level": "safe", 
                            "description": "Analysis output messages",
                            "file_types": ["*.py"]
                        },
                        {
                            "pattern": r'title="{old_brand} API"',
                            "replacement": r'title="{new_brand} API"',
                            "risk_level": "safe",
                            "description": "API titles",
                            "file_types": ["*.py"]
                        },
                        {
                            "pattern": r'"""(\s*)Enhanced {old_brand}([^"]*?)"""',
                            "replacement": r'"""\1Enhanced {new_brand}\2"""',
                            "risk_level": "safe",
                            "description": "Docstring titles",
                            "file_types": ["*.py"]
                        },
                        {
                            "pattern": r'# {old_brand}([^\n]*)',
                            "replacement": r'# {new_brand}\1',
                            "risk_level": "safe",
                            "description": "Comment references",
                            "file_types": ["*.py", "*.md", "*.txt"]
                        }
                    ]
                }
            ],
            "safety_settings": {
                "create_backups": True,
                "max_risk_level": "medium",
                "exclude_patterns": [
                    "**/venv/**",
                    "**/__pycache__/**", 
                    "**/.git/**",
                    "**/node_modules/**",
                    "**/*.pyc"
                ],
                "exclude_test_files": True,
                "exclude_history_files": True
            },
            "analysis_settings": {
                "analyze_context": True,
                "check_syntax": True,
                "validate_imports": True
            }
        }
    
    def create_rebranding_patterns(self, old_brand: str, new_brand: str) -> List[RebrandingPattern]:
        """Create rebranding patterns from config"""
        patterns = []
        
        for rule in self.config["rebranding_rules"]:
            if rule["old_brand"] == old_brand and rule["new_brand"] == new_brand:
                for pattern_config in rule["patterns"]:
                    pattern = RebrandingPattern(
                        pattern=pattern_config["pattern"].format(old_brand=old_brand, new_brand=new_brand),
                        replacement=pattern_config["replacement"].format(old_brand=old_brand, new_brand=new_brand),
                        risk_level=RebrandingRisk(pattern_config["risk_level"]),
                        description=pattern_config["description"],
                        file_types=pattern_config["file_types"],
                        exclude_contexts=pattern_config.get("exclude_contexts", [])
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def is_safe_to_modify(self, file_path: Path) -> bool:
        """Check if file is safe to modify based on configuration"""
        file_str = str(file_path.relative_to(self.project_root))
        
        # Check exclude patterns
        for pattern in self.config["safety_settings"]["exclude_patterns"]:
            if file_path.match(pattern):
                return False
        
        # Check test files
        if self.config["safety_settings"]["exclude_test_files"]:
            if any(part.startswith('test_') for part in file_path.parts):
                return False
        
        # Check history files
        if self.config["safety_settings"]["exclude_history_files"]:
            history_keywords = ['history', 'changelog', 'analysis', 'findings', 'report']
            if any(keyword in file_path.name.lower() for keyword in history_keywords):
                return False
        
        return True
    
    def analyze_context(self, file_path: Path, line_content: str, line_number: int) -> Dict:
        """Analyze the context around a potential change"""
        context = {
            "is_comment": line_content.strip().startswith('#'),
            "is_docstring": '"""' in line_content or "'''" in line_content,
            "is_print_statement": 'print(' in line_content,
            "is_logging": any(log_func in line_content for log_func in ['logging.', 'logger.', 'log.']),
            "is_string_literal": '"' in line_content or "'" in line_content,
            "is_function_def": line_content.strip().startswith('def '),
            "is_class_def": line_content.strip().startswith('class '),
            "is_import": line_content.strip().startswith(('import ', 'from '))
        }
        
        return context
    
    def find_rebranding_opportunities(self, old_brand: str, new_brand: str) -> List[Tuple[Path, List[Dict]]]:
        """Find rebranding opportunities in the project"""
        patterns = self.create_rebranding_patterns(old_brand, new_brand)
        opportunities = []
        max_risk = RebrandingRisk(self.config["safety_settings"]["max_risk_level"])
        
        for file_path in self.project_root.rglob('*'):
            if not file_path.is_file() or not self.is_safe_to_modify(file_path):
                continue
            
            # Check if file matches any pattern file types
            file_matches_patterns = []
            for pattern in patterns:
                if any(file_path.match(ft) for ft in pattern.file_types):
                    if pattern.risk_level.value <= max_risk.value:
                        file_matches_patterns.append(pattern)
            
            if not file_matches_patterns:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                matches = []
                lines = content.split('\n')
                
                for pattern in file_matches_patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern.pattern, line):
                            context = self.analyze_context(file_path, line, line_num)
                            
                            matches.append({
                                'pattern': pattern,
                                'line_number': line_num,
                                'line_content': line.strip(),
                                'context': context,
                                'risk_level': pattern.risk_level.value
                            })
                
                if matches:
                    opportunities.append((file_path, matches))
                    
            except Exception as e:
                self.logger.warning(f"Could not read {file_path}: {e}")
        
        return opportunities
    
    def apply_rebranding(self, file_path: Path, patterns: List[RebrandingPattern]) -> RebrandingResult:
        """Apply rebranding patterns to a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            modified_content = original_content
            changes_made = []
            backup_path = None
            
            for pattern in patterns:
                new_content = re.sub(pattern.pattern, pattern.replacement, modified_content)
                if new_content != modified_content:
                    changes_made.append(f"{pattern.description}: {pattern.pattern}")
                    modified_content = new_content
            
            if changes_made:
                # Create backup if enabled
                if self.config["safety_settings"]["create_backups"]:
                    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                # Write modified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                return RebrandingResult(
                    file_path=file_path,
                    changes_made=changes_made,
                    backup_path=backup_path,
                    success=True
                )
            
            return RebrandingResult(
                file_path=file_path,
                changes_made=[],
                backup_path=None,
                success=True
            )
            
        except Exception as e:
            return RebrandingResult(
                file_path=file_path,
                changes_made=[],
                backup_path=None,
                success=False,
                error_message=str(e)
            )
    
    def run_rebranding(self, old_brand: str, new_brand: str, dry_run: bool = False) -> Dict:
        """Run the complete rebranding process"""
        self.logger.info(f"🔄 Smart Rebranding: {old_brand} → {new_brand}")
        self.logger.info("=" * 60)
        
        # Find opportunities
        opportunities = self.find_rebranding_opportunities(old_brand, new_brand)
        self.logger.info(f"📊 Found {len(opportunities)} files with rebranding opportunities")
        
        if not opportunities:
            self.logger.info("✅ No rebranding needed!")
            return {'status': 'complete', 'changes': 0}
        
        # Show opportunities
        self.logger.info("\n🎯 Rebranding Opportunities:")
        total_changes = 0
        for file_path, matches in opportunities:
            self.logger.info(f"📁 {file_path.relative_to(self.project_root)}")
            for match in matches:
                self.logger.info(f"   • Line {match['line_number']}: {match['pattern'].description} (Risk: {match['risk_level']})")
                total_changes += 1
        
        if dry_run:
            self.logger.info(f"\n🧪 Dry run complete - {total_changes} potential changes identified")
            return {'status': 'dry_run', 'changes': total_changes}
        
        # Apply changes
        self.logger.info(f"\n🔄 Applying rebranding to {len(opportunities)} files...")
        successful_changes = 0
        
        for file_path, matches in opportunities:
            patterns = [match['pattern'] for match in matches]
            result = self.apply_rebranding(file_path, patterns)
            self.results.append(result)
            
            if result.success:
                if result.changes_made:
                    successful_changes += 1
                    self.logger.info(f"   ✅ {file_path.relative_to(self.project_root)} - {len(result.changes_made)} changes")
                else:
                    self.logger.info(f"   ⚪ {file_path.relative_to(self.project_root)} - no changes needed")
            else:
                self.logger.error(f"   ❌ {file_path.relative_to(self.project_root)} - {result.error_message}")
        
        self.logger.info(f"\n🎉 Rebranding complete!")
        self.logger.info(f"📊 Modified {successful_changes} files")
        
        return {
            'status': 'complete',
            'changes': successful_changes,
            'total_files': len(opportunities),
            'results': self.results
        }
    
    def generate_config_template(self, output_path: str):
        """Generate a configuration template file"""
        template = {
            "rebranding_rules": [
                {
                    "old_brand": "OLD_BRAND_NAME",
                    "new_brand": "NEW_BRAND_NAME", 
                    "patterns": [
                        {
                            "pattern": r'print\(f?"🌀 {old_brand}([^"]*)"',
                            "replacement": r'print(f"🌀 {new_brand}\1"',
                            "risk_level": "safe",
                            "description": "Print statements",
                            "file_types": ["*.py"]
                        }
                    ]
                }
            ],
            "safety_settings": {
                "create_backups": True,
                "max_risk_level": "medium",
                "exclude_patterns": ["**/venv/**", "**/__pycache__/**"],
                "exclude_test_files": True,
                "exclude_history_files": True
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(template, f, indent=2)
        
        self.logger.info(f"📄 Configuration template created: {output_path}")

def main():
    """Command line interface for the smart rebrander"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart Rebranding Tool")
    parser.add_argument("project_path", help="Path to project root")
    parser.add_argument("old_brand", help="Old brand name to replace")
    parser.add_argument("new_brand", help="New brand name")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("--generate-config", help="Generate config template at path")
    
    args = parser.parse_args()
    
    rebrander = SmartRebrander(args.project_path, args.config)
    
    if args.generate_config:
        rebrander.generate_config_template(args.generate_config)
        return
    
    result = rebrander.run_rebranding(args.old_brand, args.new_brand, args.dry_run)
    
    logger.info(f"\n🌀 Smart Rebranding Complete!")
    logger.info(f"Status: {result['status']}")
    logger.info(f"Changes: {result['changes']}")

if __name__ == "__main__":
    main()