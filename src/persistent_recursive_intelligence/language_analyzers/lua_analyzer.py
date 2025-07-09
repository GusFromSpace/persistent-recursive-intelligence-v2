"""
Lua Language Analyzer for Mesopredator PRI System
Implements the Multi-Language Support Standard for Lua analysis
"""

import os
import re
import json
import subprocess
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

from ..cognitive.enhanced_patterns.base_analyzer import BaseLanguageAnalyzer


class LuaAnalyzer(BaseLanguageAnalyzer):
    """
    Lua-specific analyzer implementing the Multi-Language Support Standard
    
    Supports:
    - OpenMW Lua scripting
    - Standard Lua applications
    - LuaJIT optimizations
    - Game scripting patterns
    """
    
    def __init__(self, memory_engine):
        super().__init__(language="lua", memory_engine=memory_engine)
        
        # Language-specific configuration
        self.file_extensions = ['.lua', '.luau']
        self.language_family = 'scripting'
        self.database_name = 'pri_lua.db'
        
        # Lua-specific pattern categories (following the standard)
        self.pattern_categories = {
            "openmw_patterns": [
                "console_command_registration",
                "engine_handler_structure", 
                "lua_environment_access",
                "cross_script_communication"
            ],
            "performance": [
                "table_creation_inefficiency",
                "string_concatenation_loops",
                "unnecessary_global_access",
                "coroutine_misuse"
            ],
            "security": [
                "loadstring_usage",
                "dofile_path_injection", 
                "unsafe_require_paths",
                "global_namespace_pollution"
            ],
            "lua_idioms": [
                "proper_error_handling",
                "metamethod_usage",
                "closure_patterns",
                "table_as_namespace"
            ],
            "game_scripting": [
                "event_handler_patterns",
                "state_management",
                "npc_behavior_logic",
                "resource_loading"
            ]
        }
        
        # Initialize Lua-specific memory namespace
        if self.memory_engine:
            self._initialize_lua_namespace()
    
    def _initialize_lua_namespace(self):
        """Initialize Lua-specific memory patterns"""
        namespace = 'lua_patterns'
        
        # OpenMW-specific patterns
        openmw_patterns = [
            {
                'content': 'Console functions should be added via I.Console.addToEnvironment() in OpenMW',
                'pattern_category': 'openmw_patterns',
                'language_construct': 'console_registration',
                'severity_level': 'high',
                'suggestion': 'Use I.Console.addToEnvironment("function_name", function_ref) for console access'
            },
            {
                'content': 'Engine handlers should return proper structure with engineHandlers table',
                'pattern_category': 'openmw_patterns', 
                'language_construct': 'module_export',
                'severity_level': 'medium',
                'suggestion': 'Return {engineHandlers = {onUpdate = func, onActivate = func}}'
            },
            {
                'content': 'Global environment access via _G may not work in isolated Lua states',
                'pattern_category': 'openmw_patterns',
                'language_construct': 'global_access',
                'severity_level': 'high',
                'suggestion': 'Use proper OpenMW API instead of _G for cross-script communication'
            }
        ]
        
        # Store patterns in memory
        for pattern in openmw_patterns:
            self.memory_engine.store_memory(f"lua_pattern_{pattern.get('type', 'openmw')}", pattern)
    
    def analyze_file(self, file_path: str) -> List[Dict]:
        """Analyze a Lua file for patterns and issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [{'error': f'Failed to read file: {e}'}]
        
        issues = []
        
        # Run analysis methods
        issues.extend(self._analyze_openmw_patterns(content, file_path))
        issues.extend(self._analyze_performance_patterns(content, file_path))
        issues.extend(self._analyze_security_patterns(content, file_path))
        issues.extend(self._analyze_lua_idioms(content, file_path))
        issues.extend(self._analyze_game_scripting_patterns(content, file_path))
        
        # Add cross-language correlation analysis
        if self.memory_engine and issues:
            cross_correlations = self._analyze_cross_language_patterns(issues)
            if cross_correlations:
                # Add correlation insights as special issue types
                for correlation in cross_correlations:
                    issues.append({
                        'type': 'cross_language_correlation',
                        'line': 1,
                        'severity': 'info',
                        'description': correlation['description'],
                        'suggestion': correlation['recommendation'],
                        'correlation_data': correlation,
                        'file_path': file_path
                    })
        
        return issues
    
    def _analyze_cross_language_patterns(self, local_issues: List[Dict]) -> List[Dict]:
        """
        Analyze cross-language patterns by correlating with related languages
        
        This method implements the principle of letting FAISS scan other language
        databases while working but never writing to them.
        """
        correlations = []
        
        # Get unique issue types from local analysis
        issue_types = set(issue.get('type', 'unknown') for issue in local_issues)
        
        for issue_type in issue_types:
            # Search for patterns in related languages (Python, JavaScript, etc.)
            cross_patterns = self.search_cross_language_patterns(issue_type, 3)
            
            if cross_patterns:
                # Generate correlation insights
                correlation = {
                    'type': 'cross_language_pattern',
                    'issue_type': issue_type,
                    'description': f'Lua pattern "{issue_type}" has correlations in {len(cross_patterns)} related languages',
                    'languages': list(cross_patterns.keys()),
                    'recommendation': self._generate_cross_language_recommendation(issue_type, cross_patterns),
                    'correlation_strength': len(cross_patterns),
                    'patterns': cross_patterns
                }
                correlations.append(correlation)
        
        return correlations
    
    def _generate_cross_language_recommendation(self, issue_type: str, cross_patterns: Dict) -> str:
        """Generate recommendations based on cross-language pattern analysis"""
        recommendations = []
        
        # Check if Python has solutions for this pattern
        if 'python' in cross_patterns:
            recommendations.append("Consider Python approaches for similar issues in AI/scripting integration")
        
        # Check for patterns across multiple scripting languages
        scripting_langs = [lang for lang in cross_patterns.keys() if lang in ['python', 'javascript', 'ruby']]
        if len(scripting_langs) > 1:
            recommendations.append(f"Pattern appears across {len(scripting_langs)} scripting languages - consider industry best practices")
        
        # Lua-specific recommendations based on issue type
        if issue_type == 'performance':
            recommendations.append("Lua performance patterns can often be adapted from Python optimizations")
        elif issue_type == 'error_handling':
            recommendations.append("Error handling patterns from other scripting languages may inform Lua pcall() usage")
        elif issue_type == 'security':
            recommendations.append("Security patterns from web scripting (JavaScript/Python) apply to game scripting")
        
        return "; ".join(recommendations) if recommendations else f"Review {issue_type} patterns in related languages for potential solutions"
    
    def _analyze_openmw_patterns(self, content: str, file_path: str) -> List[Dict]:
        """Analyze OpenMW-specific Lua patterns"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for console function registration issues
            if '_G[' in line and 'function' in line:
                issues.append({
                    'type': 'openmw_console_issue',
                    'severity': 'high',
                    'line': line_num,
                    'description': 'Using _G for console function registration may not work in OpenMW',
                    'suggestion': 'Use I.Console.addToEnvironment() instead',
                    'pattern_category': 'openmw_patterns',
                    'file_path': file_path
                })
            
            # Check for missing engine handler structure
            if 'return {' in line and 'engineHandlers' not in content:
                issues.append({
                    'type': 'missing_engine_handlers',
                    'severity': 'medium', 
                    'line': line_num,
                    'description': 'Module export should include engineHandlers structure',
                    'suggestion': 'Add engineHandlers = {onUpdate = func, onConsoleCommand = func} to return table',
                    'pattern_category': 'openmw_patterns',
                    'file_path': file_path
                })
            
            # Check for console command handling
            if 'onConsoleCommand' in line and 'mode' not in line:
                issues.append({
                    'type': 'console_command_pattern',
                    'severity': 'medium',
                    'line': line_num,
                    'description': 'Console command handler should check mode parameter',
                    'suggestion': 'function onConsoleCommand(mode, cmd, selectedObject)',
                    'pattern_category': 'openmw_patterns',
                    'file_path': file_path
                })
        
        return issues
    
    def _analyze_performance_patterns(self, content: str, file_path: str) -> List[Dict]:
        """Analyze Lua performance patterns"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for string concatenation in loops
            if ('for ' in line or 'while ' in line) and '..' in content[content.find(line):]:
                next_lines = lines[line_num:line_num+10]
                if any('..' in next_line for next_line in next_lines):
                    issues.append({
                        'type': 'string_concat_in_loop',
                        'severity': 'medium',
                        'line': line_num,
                        'description': 'String concatenation in loop can be inefficient',
                        'suggestion': 'Use table.insert() and table.concat() for multiple concatenations',
                        'pattern_category': 'performance',
                        'file_path': file_path
                    })
            
            # Check for unnecessary table creation
            if line.count('{}') > 2:
                issues.append({
                    'type': 'excessive_table_creation',
                    'severity': 'low',
                    'line': line_num,
                    'description': 'Multiple empty table creations on one line',
                    'suggestion': 'Consider reusing tables or creating them when needed',
                    'pattern_category': 'performance', 
                    'file_path': file_path
                })
        
        return issues
    
    def _analyze_security_patterns(self, content: str, file_path: str) -> List[Dict]:
        """Analyze Lua security patterns"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for loadstring usage
            if 'loadstring(' in line:
                issues.append({
                    'type': 'loadstring_usage',
                    'severity': 'high',
                    'line': line_num,
                    'description': 'loadstring() can execute arbitrary code - security risk',
                    'suggestion': 'Validate input or use safer alternatives',
                    'pattern_category': 'security',
                    'file_path': file_path
                })
            
            # Check for dofile with variables
            if 'dofile(' in line and ('".."' in line or "'.." in line):
                issues.append({
                    'type': 'dofile_path_injection',
                    'severity': 'high',
                    'line': line_num,
                    'description': 'dofile() with string concatenation - path injection risk',
                    'suggestion': 'Validate file paths or use whitelist of allowed files',
                    'pattern_category': 'security',
                    'file_path': file_path
                })
            
            # Check for global pollution
            if line.strip().startswith('_G.') and '=' in line:
                issues.append({
                    'type': 'global_namespace_pollution',
                    'severity': 'medium',
                    'line': line_num,
                    'description': 'Direct modification of global namespace',
                    'suggestion': 'Use local variables or module-specific namespaces',
                    'pattern_category': 'security',
                    'file_path': file_path
                })
        
        return issues
    
    def _analyze_lua_idioms(self, content: str, file_path: str) -> List[Dict]:
        """Analyze Lua-specific idioms and best practices"""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for proper error handling
            if 'pcall(' not in content and ('error(' in line or 'assert(' in line):
                issues.append({
                    'type': 'error_handling_pattern',
                    'severity': 'low',
                    'line': line_num,
                    'description': 'Consider using pcall() for error handling',
                    'suggestion': 'local success, result = pcall(function_that_might_fail)',
                    'pattern_category': 'lua_idioms',
                    'file_path': file_path
                })
            
            # Check for proper table usage as namespace
            if 'local ' in line and ' = {}' in line and line.count('local') > 1:
                issues.append({
                    'type': 'table_namespace_pattern',
                    'severity': 'info',
                    'line': line_num,
                    'description': 'Good practice: using table as namespace',
                    'suggestion': 'Continue organizing functions in table namespaces',
                    'pattern_category': 'lua_idioms',
                    'file_path': file_path
                })
        
        return issues
    
    def _analyze_game_scripting_patterns(self, content: str, file_path: str) -> List[Dict]:
        """Analyze game scripting specific patterns"""
        issues = []
        lines = content.split('\n')
        
        # Check for NPC behavior patterns
        if 'npc' in content.lower() or 'character' in content.lower():
            for line_num, line in enumerate(lines, 1):
                if 'math.random(' in line and 'personality' in content.lower():
                    issues.append({
                        'type': 'npc_personality_randomization',
                        'severity': 'info',
                        'line': line_num,
                        'description': 'Good practice: randomizing NPC personality traits',
                        'suggestion': 'Consider seed-based randomization for consistent behavior',
                        'pattern_category': 'game_scripting',
                        'file_path': file_path
                    })
        
        # Check for event handler patterns
        if 'engineHandlers' in content:
            for line_num, line in enumerate(lines, 1):
                if 'onUpdate' in line:
                    issues.append({
                        'type': 'update_handler_found',
                        'severity': 'info',
                        'line': line_num,
                        'description': 'Update handler found - ensure efficient frame processing',
                        'suggestion': 'Use frame counters to limit expensive operations',
                        'pattern_category': 'game_scripting',
                        'file_path': file_path
                    })
        
        return issues
    
    def get_language_metrics(self, project_path: str) -> Dict:
        """Get Lua-specific metrics for the project"""
        lua_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if any(file.endswith(ext) for ext in self.file_extensions):
                    lua_files.append(os.path.join(root, file))
        
        total_lines = 0
        total_functions = 0
        openmw_files = 0
        
        for file_path in lua_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    total_lines += len(lines)
                    total_functions += content.count('function ')
                    
                    # Check if it's OpenMW-specific
                    if any(keyword in content for keyword in ['openmw', 'engineHandlers', 'ui.printToConsole']):
                        openmw_files += 1
            except (FileNotFoundError, IOError, UnicodeDecodeError) as e:
                continue
        
        return {
            'total_lua_files': len(lua_files),
            'total_lines_of_code': total_lines,
            'total_functions': total_functions,
            'openmw_specific_files': openmw_files,
            'average_functions_per_file': total_functions / len(lua_files) if lua_files else 0,
            'language_family': self.language_family
        }
    
    def suggest_improvements(self, analysis_results: List[Dict]) -> List[Dict]:
        """Suggest Lua-specific improvements based on analysis"""
        suggestions = []
        
        # Count pattern types
        pattern_counts = {}
        for result in analysis_results:
            pattern_type = result.get('type', 'unknown')
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        # OpenMW-specific suggestions
        if pattern_counts.get('openmw_console_issue', 0) > 0:
            suggestions.append({
                'type': 'architecture_improvement',
                'priority': 'high',
                'description': 'Consider using OpenMW Console interface instead of _G manipulation',
                'implementation': 'Replace _G assignments with I.Console.addToEnvironment() calls',
                'rationale': 'OpenMW console runs in isolated Lua state - _G access may not work'
            })
        
        # Performance suggestions
        if pattern_counts.get('string_concat_in_loop', 0) > 2:
            suggestions.append({
                'type': 'performance_improvement', 
                'priority': 'medium',
                'description': 'Multiple string concatenation inefficiencies detected',
                'implementation': 'Use table-based string building: table.insert() + table.concat()',
                'rationale': 'Lua string concatenation creates new strings - inefficient in loops'
            })
        
        return suggestions


def create_lua_analyzer(memory_engine) -> LuaAnalyzer:
    """Factory function to create Lua analyzer instance"""
    return LuaAnalyzer(memory_engine)


# Integration with the PRI system
LUA_LANGUAGE_CONFIG = {
    'name': 'lua',
    'family': 'scripting',
    'extensions': ['.lua', '.luau'],
    'analyzer_class': LuaAnalyzer,
    'database_name': 'pri_lua.db',
    'pattern_categories': [
        'openmw_patterns',
        'performance', 
        'security',
        'lua_idioms',
        'game_scripting'
    ],
    'related_languages': ['javascript', 'python'],  # For cross-language correlation
    'specialty_domains': ['game_scripting', 'embedded_scripting', 'configuration']
}