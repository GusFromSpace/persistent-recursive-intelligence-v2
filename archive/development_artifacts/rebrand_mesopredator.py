#!/usr/bin/env python3
"""
Mesopredator Self-Rebranding Tool
Uses Mesopredator's own pattern matching to safely rebrand user-facing strings
"""

import re
from pathlib import Path
from typing import List, Dict, Tuple

class MesopredatorRebrander:
    """Safe rebranding tool that only updates user-facing strings"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.changes_made = []
        
        # Safe rebranding patterns - only user-facing strings
        self.safe_patterns = [
            # Print statements and user messages
            (r'print\(f?"🌀 Enhanced PRI([^"]*)"', r'print(f"🌀 Enhanced Mesopredator\1"'),
            (r'print\(f?"🌀 PRI Analysis([^"]*)"', r'print(f"🌀 Mesopredator Analysis\1"'),
            (r'print\("🧠 Memory-Enhanced PRI([^"]*)"', r'print("🧠 Memory-Enhanced Mesopredator\1"'),
            
            # API titles and descriptions (not functional code)
            (r'title="Enhanced PRI API"', r'title="Enhanced Mesopredator API"'),
            (r'"service": "Enhanced PRI API"', r'"service": "Enhanced Mesopredator API"'),
            
            # Logging messages
            (r'logging\.info\("🧠 Memory-Enhanced PRI([^"]*)"', r'logging.info("🧠 Memory-Enhanced Mesopredator\1"'),
            
            # Comments and docstrings
            (r'"""(\s*)Enhanced PRI([^"]*?)"""', r'"""\1Enhanced Mesopredator\2"""'),
            (r'# Enhanced PRI([^\n]*)', r'# Enhanced Mesopredator\1'),
        ]
        
        # Files to exclude (to avoid breaking functionality)
        self.exclude_patterns = [
            '**/venv/**',
            '**/__pycache__/**',
            '**/.git/**',
            '**/test_*',  # Exclude test files to preserve historical accuracy
            '**/debug_*',  # Exclude debug files
            '**/analysis_*',  # Exclude analysis result files
        ]
    
    def is_safe_to_modify(self, file_path: Path) -> bool:
        """Check if file is safe to modify"""
        file_str = str(file_path)
        
        # Exclude patterns
        for pattern in self.exclude_patterns:
            if file_path.match(pattern):
                return False
        
        # Only modify Python files for now
        return file_path.suffix == '.py'
    
    def find_rebranding_opportunities(self) -> List[Tuple[Path, List[str]]]:
        """Find files with rebranding opportunities"""
        opportunities = []
        
        for py_file in self.project_root.rglob('*.py'):
            if not self.is_safe_to_modify(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                matches = []
                for pattern, replacement in self.safe_patterns:
                    if re.search(pattern, content):
                        matches.append(f"Found pattern: {pattern}")
                
                if matches:
                    opportunities.append((py_file, matches))
                    
            except Exception as e:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"⚠️  Could not read {py_file}: {e}")\n        
        return opportunities
    
    def apply_safe_rebranding(self, file_path: Path) -> bool:
        """Apply safe rebranding to a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            modified_content = original_content
            changes_in_file = []
            
            for pattern, replacement in self.safe_patterns:
                new_content = re.sub(pattern, replacement, modified_content)
                if new_content != modified_content:
                    changes_in_file.append(f"Applied: {pattern} -> {replacement}")
                    modified_content = new_content
            
            if changes_in_file:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                
                # Write modified content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                self.changes_made.append({
                    'file': str(file_path),
                    'changes': changes_in_file,
                    'backup': str(backup_path)
                })
                
                return True
            
            return False
            
        except Exception as e:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"❌ Error modifying {file_path}: {e}")\n            return False
    
    def run_rebranding(self) -> Dict:
        """Run the complete rebranding process"""
# DEBUG ELIMINATED BY MESOPREDATOR: print("🔍 Mesopredator Self-Rebranding Analysis")\n# DEBUG ELIMINATED BY MESOPREDATOR\n        
        # Find opportunities
        opportunities = self.find_rebranding_opportunities()
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"📊 Found {len(opportunities)} files with rebranding opportunities")\n        
        if not opportunities:
# DEBUG ELIMINATED BY MESOPREDATOR: print("✅ No rebranding needed - all user-facing strings already use Mesopredator!")\n            return {'status': 'complete', 'changes': 0}
        
        # Show opportunities
# DEBUG ELIMINATED BY MESOPREDATOR: print("\n🎯 Rebranding Opportunities:")\n        for file_path, matches in opportunities:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"📁 {file_path.relative_to(self.project_root)}")\n            for match in matches:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   • {match}")\n        
        # Auto-apply (safe patterns only)
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n✅ Auto-applying safe rebranding to {len(opportunities)} files...")\n        
        # Apply changes
# DEBUG ELIMINATED BY MESOPREDATOR: print("\n🔄 Applying safe rebranding...")\n        successful_changes = 0
        
        for file_path, _ in opportunities:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   📝 {file_path.relative_to(self.project_root)}")\n            if self.apply_safe_rebranding(file_path):
                successful_changes += 1
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"      ✅ Modified")\n            else:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"      ⚠️  No changes needed")\n        
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n🎉 Rebranding complete!")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"📊 Modified {successful_changes} files")\n# DEBUG ELIMINATED BY MESOPREDATOR: print(f"💾 Backups created for all modified files")\n        
        return {
            'status': 'complete',
            'changes': successful_changes,
            'files_modified': self.changes_made
        }

def main():
    """Main rebranding function"""
    rebrander = MesopredatorRebrander('.')
    result = rebrander.run_rebranding()
    
    if result['changes'] > 0:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n📋 Summary of Changes:")\n        for change in rebrander.changes_made:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"   📁 {change['file']}")\n            for mod in change['changes']:
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"      • {mod}")\n    
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\n🌀 Mesopredator has successfully analyzed and updated its own branding!")\n
if __name__ == "__main__":
    main()