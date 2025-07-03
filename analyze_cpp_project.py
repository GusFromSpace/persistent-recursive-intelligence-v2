#!/usr/bin/env python3
"""
Mesopredator C++ Project Analyzer
Applies recursive intelligence to C++ codebases with orchestrated analysis
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re
import logging

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Enhanced imports with orchestrator integration
from gus_memory import MemoryIntelligence
from cognitive.orchestration.analyzer_orchestrator import AnalyzerOrchestrator

class CppMesopredatorAnalyzer:
    """Apply Mesopredator recursive intelligence to C++ projects with orchestrated analysis"""
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.memory = MemoryIntelligence("cpp-recursive-analysis")
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize orchestrator for enhanced analysis
        self.orchestrator = AnalyzerOrchestrator()
        
        # C++ specific patterns
        self.cpp_extensions = {'.cpp', '.cxx', '.cc', '.c', '.h', '.hpp', '.hxx'}
        self.issues_found = []
        self.recursive_depth = 0
        
    def find_cpp_files(self):
        """Find all C++ source files in the project"""
        cpp_files = []
        exclude_dirs = {'build', 'third_party', '.git', '__pycache__'}
        
        for root, dirs, files in os.walk(self.project_path):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if Path(file).suffix in self.cpp_extensions:
                    file_path = Path(root) / file
                    if file_path.stat().st_size < 1024 * 1024:  # Skip very large files
                        cpp_files.append(file_path)
        
        return cpp_files
    
    def analyze_cpp_file(self, file_path: Path):
        """Analyze a single C++ file with recursive intelligence and orchestrated analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            self.logger.warning(f"Could not read {file_path}: {e}")
            return []
        
        issues = []
        
        # Use orchestrator for enhanced analysis
        analyzer = self.orchestrator.get_analyzer_for_file(file_path)
        if analyzer:
            try:
                orchestrated_issues = analyzer.analyze_file(file_path, content)
                issues.extend(orchestrated_issues)
                self.logger.info(f"Orchestrator found {len(orchestrated_issues)} issues in {file_path}")
            except Exception as e:
                self.logger.warning(f"Orchestrator analysis failed for {file_path}: {e}")
        
        # Continue with legacy analysis for comparison
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Memory leak detection
            if 'new ' in line and 'delete' not in content:
                issues.append({
                    'type': 'memory_leak',
                    'line': i + 1,
                    'severity': 'high',
                    'description': f"Potential memory leak: 'new' without corresponding 'delete'",
                    'file_path': str(file_path)
                })
            
            # Buffer overflow risks
            if any(func in line for func in ['strcpy(', 'strcat(', 'sprintf(', 'gets(']):
                issues.append({
                    'type': 'buffer_overflow',
                    'line': i + 1,
                    'severity': 'critical',
                    'description': f"Unsafe function usage: potential buffer overflow",
                    'file_path': str(file_path)
                })
            
            # Null pointer dereference
            if '->' in line and 'if' not in line and 'nullptr' not in line:
                # Simple heuristic for potential null pointer dereference
                if not any(check in line for check in ['assert', 'check', 'verify', 'ensure']):
                    issues.append({
                        'type': 'null_pointer',
                        'line': i + 1,
                        'severity': 'medium',
                        'description': f"Potential null pointer dereference without check",
                        'file_path': str(file_path)
                    })
            
            # TODO/FIXME comments
            if any(keyword in line_stripped for keyword in ['TODO', 'FIXME', 'XXX', 'HACK']):
                issues.append({
                    'type': 'maintenance',
                    'line': i + 1,
                    'severity': 'low',
                    'description': f"Maintenance comment: {line_stripped[:100]}",
                    'file_path': str(file_path)
                })
            
            # Missing const correctness
            if re.search(r'^\s*\w+\s*\*\s*\w+\s*=', line) and 'const' not in line:
                issues.append({
                    'type': 'const_correctness',
                    'line': i + 1,
                    'severity': 'low',
                    'description': f"Consider const correctness for pointer declaration",
                    'file_path': str(file_path)
                })
        
        # Store patterns in memory for recursive learning
        if issues:
            pattern_descriptions = [issue['description'] for issue in issues]
            self.memory.learn_pattern(f"cpp_issues_{file_path.suffix}", 
                                    pattern_descriptions, 
                                    {"file_type": file_path.suffix, 
                                     "analysis_date": datetime.now().isoformat()})
        
        return issues
    
    def recursive_analysis(self, max_depth: int = 7):
        """Perform recursive analysis with increasing sophistication"""
        self.logger.info(f"🌀 Mesopredator C++ Recursive Analysis - Depth {max_depth}")
        self.logger.info("=" * 60)
        
        all_issues = []
        cpp_files = self.find_cpp_files()
        
        self.logger.info(f"📁 Found {len(cpp_files)} C++ files to analyze")
        
        for depth in range(1, max_depth + 1):
            self.logger.info(f"\n🔍 Recursive Depth {depth}/{max_depth}")
            self.recursive_depth = depth
            
            depth_issues = []
            for file_path in cpp_files:
                issues = self.analyze_cpp_file(file_path)
                depth_issues.extend(issues)
                
                # Remember analysis
                self.memory.remember(f"Analyzed {file_path.name} at depth {depth}", {
                    "depth": depth,
                    "issues_found": len(issues),
                    "file_path": str(file_path)
                })
            
            all_issues.extend(depth_issues)
            
            # Apply recursive learning - each depth builds on previous knowledge
            if depth > 1:
                previous_patterns = self.memory.recall(f"cpp analysis depth {depth-1}", limit=10)
                self.logger.info(f"   🧠 Learning from {len(previous_patterns)} previous patterns")
            
            self.logger.info(f"   📊 Depth {depth}: {len(depth_issues)} issues found")
            
            # Store depth-specific intelligence
            self.memory.remember(f"Recursive depth {depth} complete", {
                "depth": depth,
                "total_issues": len(depth_issues),
                "analysis_timestamp": datetime.now().isoformat()
            })
        
        return all_issues
    
    def generate_report(self, issues):
        """Generate comprehensive analysis report"""
        self.logger.info(f"\n📊 Mesopredator C++ Analysis Results")
        self.logger.info("=" * 50)
        
        # Categorize issues
        critical = [i for i in issues if i.get('severity') == 'critical']
        high = [i for i in issues if i.get('severity') == 'high']
        medium = [i for i in issues if i.get('severity') == 'medium']
        low = [i for i in issues if i.get('severity') == 'low']
        
        self.logger.info(f"🔥 Issue Breakdown:")
        self.logger.info(f"   Critical: {len(critical)}")
        self.logger.info(f"   High: {len(high)}")
        self.logger.info(f"   Medium: {len(medium)}")
        self.logger.info(f"   Low: {len(low)}")
        self.logger.info(f"   Total: {len(issues)}")
        
        # Show top priority issues
        priority_issues = critical + high
        if priority_issues:
            self.logger.info(f"\n⚠️  Top Priority Issues:")
            for i, issue in enumerate(priority_issues[:10], 1):
                file_name = Path(issue['file_path']).name
                self.logger.info(f"   {i}. {issue['type'].upper()} ({issue['severity'].upper()})")
                self.logger.info(f"      {file_name}:{issue['line']} - {issue['description']}")
        
        # Memory intelligence insights
        patterns = self.memory.recall("cpp", limit=5)
        self.logger.info(f"\n🧠 Intelligence Insights:")
        self.logger.info(f"   Patterns learned: {len(patterns)}")
        self.logger.info(f"   Recursive depth achieved: {self.recursive_depth}")
        
        return {
            'total_issues': len(issues),
            'critical': len(critical),
            'high': len(high),
            'medium': len(medium),
            'low': len(low),
            'recursive_depth': self.recursive_depth
        }

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Mesopredator C++ Recursive Intelligence Analyzer")
    parser.add_argument("--project", required=True, help="Path to C++ project")
    parser.add_argument("--max-depth", type=int, default=7, help="Maximum recursive depth")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        # IMPROVED: logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    project_path = Path(args.project).resolve()
    if not project_path.exists():
        logger.info(f"❌ Project path does not exist: {project_path}")
        return 1
    
    analyzer = CppMesopredatorAnalyzer(project_path)
    issues = analyzer.recursive_analysis(args.max_depth)
    results = analyzer.generate_report(issues)
    
    logger.info(f"\n✅ Analysis complete! {results['total_issues']} issues found across {args.max_depth} recursive layers")
    return 0

if __name__ == "__main__":
    sys.exit(main())