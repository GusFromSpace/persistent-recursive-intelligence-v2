#!/usr/bin/env python3
"""
Update Package Analyzer - Multi-File Integration Intelligence

This module extends the Code Connector's capabilities to analyze entire update packages
(collections of new/modified files) and understand their collective integration requirements.

Transforms Mesopredator from single-file suggestions to comprehensive package integration mapping.
"""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, NamedTuple, Tuple
from dataclasses import dataclass
from collections import defaultdict
import json

# Import Code Connector foundation
from .code_connector import CodeConnector, FileCapabilities, ConnectionSuggestion

logger = logging.getLogger(__name__)


@dataclass
class PackageFile:
    """Represents a file within an update package"""
    path: Path
    content: str
    capabilities: FileCapabilities
    package_role: str  # 'core', 'utility', 'config', 'test', 'documentation'
    dependencies: Set[str]  # Internal package dependencies
    external_dependencies: Set[str]  # External dependencies


@dataclass
class PackageDependencyGraph:
    """Represents the internal dependency structure of an update package"""
    files: Dict[str, PackageFile]
    internal_edges: Dict[str, Set[str]]  # file -> files it depends on
    external_requirements: Set[str]  # External libraries/modules needed
    entry_points: List[str]  # Files that serve as package entry points
    utility_files: List[str]  # Supporting/helper files


@dataclass
class PackageIntegrationPlan:
    """Complete integration plan for an update package"""
    package_info: PackageDependencyGraph
    target_project_path: str
    integration_order: List[str]  # Optimal order for integration
    connection_suggestions: List[ConnectionSuggestion]
    package_level_modifications: List[Dict]  # Structural changes needed
    conflict_warnings: List[str]
    success_probability: float


class UpdatePackageAnalyzer:
    """
    Analyzes update packages and generates comprehensive integration plans.
    
    Extends Code Connector intelligence to handle multi-file collections with
    internal dependencies and complex integration requirements.
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.code_connector = CodeConnector(str(self.project_path))
        
        # Package role classification patterns
        self.role_patterns = {
            'core': [
                r'.*/(main|core|engine|processor|manager|controller)\.py$',
                r'.*/.*_engine\.py$',
                r'.*/.*_manager\.py$',
                r'.*/.*_controller\.py$'
            ],
            'utility': [
                r'.*/(util|utils|helper|helpers|common|shared)\.py$',
                r'.*/.*_util\.py$',
                r'.*/.*_helper\.py$',
                r'.*/.*_common\.py$'
            ],
            'config': [
                r'.*/(config|settings|constants|defaults)\.py$',
                r'.*/.*_config\.py$',
                r'.*/.*_settings\.py$'
            ],
            'test': [
                r'.*/test_.*\.py$',
                r'.*_test\.py$',
                r'.*/tests/.*\.py$'
            ],
            'documentation': [
                r'.*\.md$',
                r'.*\.rst$',
                r'.*\.txt$'
            ]
        }
    
    def analyze_update_package(self, package_path: str, 
                             target_files: Optional[List[str]] = None) -> PackageIntegrationPlan:
        """
        Main entry point for update package analysis.
        
        Args:
            package_path: Path to the update package directory
            target_files: Optional list of target project files to focus on
            
        Returns:
            Complete integration plan for the package
        """
        logger.info(f"🔍 Analyzing update package: {package_path}")
        
        package_path = Path(package_path)
        
        # Phase 1: Analyze package structure and capabilities
        logger.info("📦 Phase 1: Package structure analysis...")
        package_info = self._analyze_package_structure(package_path)
        
        # Phase 2: Build internal dependency graph
        logger.info("🔗 Phase 2: Building dependency graph...")
        self._build_internal_dependency_graph(package_info)
        
        # Phase 3: Determine integration order
        logger.info("📋 Phase 3: Computing integration order...")
        integration_order = self._compute_integration_order(package_info)
        
        # Phase 4: Generate connection suggestions using Code Connector
        logger.info("🧠 Phase 4: Generating connection suggestions...")
        if target_files is None:
            target_files = self._discover_target_files()
        
        connection_suggestions = self._generate_package_connections(
            package_info, target_files
        )
        
        # Phase 5: Detect conflicts and generate warnings
        logger.info("⚠️ Phase 5: Conflict detection...")
        conflict_warnings = self._detect_integration_conflicts(
            package_info, target_files
        )
        
        # Phase 6: Calculate success probability
        success_probability = self._calculate_integration_probability(
            package_info, connection_suggestions, conflict_warnings
        )
        
        integration_plan = PackageIntegrationPlan(
            package_info=package_info,
            target_project_path=str(self.project_path),
            integration_order=integration_order,
            connection_suggestions=connection_suggestions,
            package_level_modifications=self._generate_package_modifications(package_info),
            conflict_warnings=conflict_warnings,
            success_probability=success_probability
        )
        
        logger.info(f"✅ Package analysis complete: {len(package_info.files)} files, "
                   f"{len(connection_suggestions)} connections, "
                   f"{success_probability:.1%} success probability")
        
        return integration_plan
    
    def _analyze_package_structure(self, package_path: Path) -> PackageDependencyGraph:
        """Analyze the structure and capabilities of an update package"""
        files = {}
        
        # Find all Python files in the package
        python_files = list(package_path.rglob("*.py"))
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse and analyze capabilities using Code Connector's infrastructure
                ast_tree = ast.parse(content)
                capabilities = self.code_connector._analyze_file_capabilities(
                    ast_tree, content, file_path
                )
                
                # Determine package role
                role = self._classify_package_role(file_path)
                
                # Extract dependencies
                internal_deps, external_deps = self._extract_dependencies(
                    ast_tree, content, package_path
                )
                
                package_file = PackageFile(
                    path=file_path,
                    content=content,
                    capabilities=capabilities,
                    package_role=role,
                    dependencies=internal_deps,
                    external_dependencies=external_deps
                )
                
                rel_path = str(file_path.relative_to(package_path))
                files[rel_path] = package_file
                
            except Exception as e:
                logger.warning(f"Error analyzing package file {file_path}: {e}")
        
        return PackageDependencyGraph(
            files=files,
            internal_edges={},  # Will be built in next phase
            external_requirements=set(),  # Will be computed
            entry_points=[],  # Will be identified
            utility_files=[]  # Will be classified
        )
    
    def _classify_package_role(self, file_path: Path) -> str:
        """Classify the role of a file within the package"""
        file_str = str(file_path)
        
        for role, patterns in self.role_patterns.items():
            for pattern in patterns:
                import re
                if re.match(pattern, file_str, re.IGNORECASE):
                    return role
        
        return 'core'  # Default classification
    
    def _extract_dependencies(self, ast_tree: ast.AST, content: str, 
                            package_path: Path) -> Tuple[Set[str], Set[str]]:
        """Extract internal package dependencies and external dependencies"""
        internal_deps = set()
        external_deps = set()
        
        for node in ast.walk(ast_tree):
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    module_parts = node.module.split('.')
                    
                    # Check if it's a relative import within the package
                    if node.level > 0:  # Relative import (from .module import ...)
                        internal_deps.add(node.module or "")
                    else:
                        # Check if it refers to a file in the package
                        potential_file = package_path / f"{module_parts[-1]}.py"
                        if potential_file.exists():
                            internal_deps.add(module_parts[-1])
                        else:
                            external_deps.add(node.module)
            
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_parts = alias.name.split('.')
                    potential_file = package_path / f"{module_parts[0]}.py"
                    if potential_file.exists():
                        internal_deps.add(module_parts[0])
                    else:
                        external_deps.add(alias.name)
        
        return internal_deps, external_deps
    
    def _build_internal_dependency_graph(self, package_info: PackageDependencyGraph):
        """Build the internal dependency graph for the package"""
        # Create dependency edges
        for file_path, package_file in package_info.files.items():
            dependencies = set()
            
            for dep in package_file.dependencies:
                # Find actual files that match this dependency
                for other_path in package_info.files.keys():
                    if dep in other_path or other_path.replace('.py', '') == dep:
                        dependencies.add(other_path)
            
            package_info.internal_edges[file_path] = dependencies
        
        # Identify entry points (files with minimal dependencies)
        entry_points = []
        for file_path, deps in package_info.internal_edges.items():
            if len(deps) <= 1 and package_info.files[file_path].package_role in ['core', 'config']:
                entry_points.append(file_path)
        
        # Identify utility files
        utility_files = [
            file_path for file_path, package_file in package_info.files.items()
            if package_file.package_role == 'utility'
        ]
        
        # Compute external requirements
        all_external_deps = set()
        for package_file in package_info.files.values():
            all_external_deps.update(package_file.external_dependencies)
        
        package_info.entry_points = entry_points
        package_info.utility_files = utility_files
        package_info.external_requirements = all_external_deps
    
    def _compute_integration_order(self, package_info: PackageDependencyGraph) -> List[str]:
        """Compute the optimal order for integrating package files"""
        # Topological sort based on internal dependencies
        visited = set()
        temp_visited = set()
        result = []
        
        def visit(file_path: str):
            if file_path in temp_visited:
                # Circular dependency - handle gracefully
                return
            if file_path in visited:
                return
            
            temp_visited.add(file_path)
            
            # Visit dependencies first
            for dep in package_info.internal_edges.get(file_path, []):
                if dep in package_info.files:  # Ensure dependency exists in package
                    visit(dep)
            
            temp_visited.remove(file_path)
            visited.add(file_path)
            result.append(file_path)
        
        # Start with entry points and utility files
        for entry_point in package_info.entry_points:
            visit(entry_point)
        
        for utility_file in package_info.utility_files:
            if utility_file not in visited:
                visit(utility_file)
        
        # Add any remaining files
        for file_path in package_info.files.keys():
            if file_path not in visited:
                visit(file_path)
        
        return result
    
    def _discover_target_files(self) -> List[str]:
        """Discover target files in the project for integration"""
        target_files = []
        
        # Find main Python files in the project
        for python_file in self.project_path.rglob("*.py"):
            # Skip common exclusions
            if any(skip in str(python_file) for skip in ["venv", "__pycache__", ".git", "test_"]):
                continue
            
            target_files.append(str(python_file))
        
        return target_files[:20]  # Limit for performance
    
    def _generate_package_connections(self, package_info: PackageDependencyGraph,
                                    target_files: List[str]) -> List[ConnectionSuggestion]:
        """Generate connection suggestions for the entire package"""
        all_suggestions = []
        
        # Convert package files to the format expected by Code Connector
        package_file_paths = [
            package_info.files[rel_path].path 
            for rel_path in package_info.files.keys()
        ]
        
        target_file_paths = [Path(f) for f in target_files]
        
        # Use Code Connector to generate suggestions
        suggestions = self.code_connector.analyze_orphaned_files(
            package_file_paths, target_file_paths
        )
        
        # Enhance suggestions with package-level context
        enhanced_suggestions = []
        for suggestion in suggestions:
            # Add package context to reasoning
            package_file_rel = None
            for rel_path, package_file in package_info.files.items():
                if str(package_file.path) in suggestion.orphaned_file:
                    package_file_rel = rel_path
                    break
            
            if package_file_rel:
                package_file = package_info.files[package_file_rel]
                enhanced_reasoning = list(suggestion.reasoning)
                enhanced_reasoning.append(
                    f"Package role: {package_file.package_role} - "
                    f"integrates as part of {len(package_info.files)}-file update package"
                )
                
                # Create enhanced suggestion
                enhanced_suggestion = ConnectionSuggestion(
                    orphaned_file=suggestion.orphaned_file,
                    target_file=suggestion.target_file,
                    connection_score=suggestion.connection_score,
                    connection_type=suggestion.connection_type,
                    integration_suggestions=suggestion.integration_suggestions,
                    reasoning=enhanced_reasoning
                )
                enhanced_suggestions.append(enhanced_suggestion)
            else:
                enhanced_suggestions.append(suggestion)
        
        return enhanced_suggestions
    
    def _detect_integration_conflicts(self, package_info: PackageDependencyGraph,
                                    target_files: List[str]) -> List[str]:
        """Detect potential conflicts during package integration"""
        warnings = []
        
        # Check for name conflicts
        package_names = set()
        for package_file in package_info.files.values():
            for func in package_file.capabilities.functions:
                package_names.add(func['name'])
            for cls in package_file.capabilities.classes:
                package_names.add(cls['name'])
        
        # Check against target project
        for target_file in target_files[:5]:  # Sample check
            try:
                with open(target_file, 'r', encoding='utf-8') as f:
                    target_content = f.read()
                
                target_ast = ast.parse(target_content)
                target_capabilities = self.code_connector._analyze_file_capabilities(
                    target_ast, target_content, Path(target_file)
                )
                
                target_names = set()
                for func in target_capabilities.functions:
                    target_names.add(func['name'])
                for cls in target_capabilities.classes:
                    target_names.add(cls['name'])
                
                conflicts = package_names.intersection(target_names)
                if conflicts:
                    warnings.append(
                        f"Name conflicts detected with {Path(target_file).name}: {', '.join(list(conflicts)[:3])}"
                    )
            
            except Exception:
                continue
        
        # Check for missing external dependencies
        for ext_dep in package_info.external_requirements:
            # This is a simplified check - in reality would verify import availability
            if '.' not in ext_dep and len(ext_dep) > 2:
                warnings.append(f"External dependency required: {ext_dep}")
        
        return warnings
    
    def _calculate_integration_probability(self, package_info: PackageDependencyGraph,
                                         connection_suggestions: List[ConnectionSuggestion],
                                         conflict_warnings: List[str]) -> float:
        """Calculate the probability of successful integration"""
        base_probability = 0.7  # Base assumption
        
        # Boost for high-quality connections
        if connection_suggestions:
            avg_score = sum(s.connection_score for s in connection_suggestions) / len(connection_suggestions)
            score_boost = min(0.2, (avg_score - 0.5) * 0.4)
            base_probability += score_boost
        
        # Penalty for conflicts
        conflict_penalty = min(0.3, len(conflict_warnings) * 0.05)
        base_probability -= conflict_penalty
        
        # Boost for clean package structure
        if package_info.entry_points and package_info.utility_files:
            base_probability += 0.1
        
        # Penalty for complex internal dependencies
        avg_internal_deps = sum(len(deps) for deps in package_info.internal_edges.values())
        if avg_internal_deps > len(package_info.files) * 0.5:
            base_probability -= 0.1
        
        return max(0.1, min(1.0, base_probability))
    
    def _generate_package_modifications(self, package_info: PackageDependencyGraph) -> List[Dict]:
        """Generate package-level modifications needed for integration"""
        modifications = []
        
        # Import path adjustments
        if package_info.files:
            modifications.append({
                "type": "import_path_adjustment",
                "description": f"Adjust import paths for {len(package_info.files)} package files",
                "affected_files": list(package_info.files.keys())
            })
        
        # External dependency installation
        if package_info.external_requirements:
            modifications.append({
                "type": "dependency_installation",
                "description": f"Install external dependencies: {', '.join(list(package_info.external_requirements)[:3])}",
                "requirements": list(package_info.external_requirements)
            })
        
        # Configuration updates
        config_files = [
            rel_path for rel_path, package_file in package_info.files.items()
            if package_file.package_role == 'config'
        ]
        if config_files:
            modifications.append({
                "type": "configuration_integration",
                "description": f"Integrate configuration from {len(config_files)} config files",
                "config_files": config_files
            })
        
        return modifications


def analyze_update_package(package_path: str, project_path: str, 
                         target_files: Optional[List[str]] = None) -> PackageIntegrationPlan:
    """
    Main API function for update package analysis.
    
    Args:
        package_path: Path to the update package directory
        project_path: Path to the target project
        target_files: Optional list of specific target files to consider
    
    Returns:
        Complete integration plan for the package
    """
    analyzer = UpdatePackageAnalyzer(project_path)
    return analyzer.analyze_update_package(package_path, target_files)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Package Analyzer - Multi-File Integration Intelligence")
    parser.add_argument("package_path", help="Path to the update package directory")
    parser.add_argument("project_path", help="Path to the target project")
    parser.add_argument("--target-files", nargs="+", help="Specific target files to consider")
    parser.add_argument("--output", help="Output JSON file for integration plan")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    # Analyze the update package
    integration_plan = analyze_update_package(
        args.package_path,
        args.project_path,
        args.target_files
    )
    
    # Output results
    if args.output:
        # Convert to serializable format
        plan_dict = {
            "package_info": {
                "files": list(integration_plan.package_info.files.keys()),
                "entry_points": integration_plan.package_info.entry_points,
                "utility_files": integration_plan.package_info.utility_files,
                "external_requirements": list(integration_plan.package_info.external_requirements)
            },
            "target_project_path": integration_plan.target_project_path,
            "integration_order": integration_plan.integration_order,
            "connection_suggestions": [
                {
                    "orphaned_file": s.orphaned_file,
                    "target_file": s.target_file,
                    "connection_score": s.connection_score,
                    "connection_type": s.connection_type,
                    "integration_suggestions": s.integration_suggestions,
                    "reasoning": s.reasoning
                }
                for s in integration_plan.connection_suggestions
            ],
            "package_level_modifications": integration_plan.package_level_modifications,
            "conflict_warnings": integration_plan.conflict_warnings,
            "success_probability": integration_plan.success_probability
        }
        
        with open(args.output, 'w') as f:
            json.dump(plan_dict, f, indent=2)
        
        logger.info(f"💾 Integration plan saved to {args.output}")
    else:
        # Console output
        logger.info(f"\n📦 Update Package Integration Analysis")
        logger.info("=" * 50)
        logger.info(f"📁 Package: {args.package_path}")
        logger.info(f"🎯 Target: {args.project_path}")
        logger.info(f"📊 Files: {len(integration_plan.package_info.files)}")
        logger.info(f"🔗 Connections: {len(integration_plan.connection_suggestions)}")
        logger.info(f"⚠️ Warnings: {len(integration_plan.conflict_warnings)}")
        logger.info(f"📈 Success Probability: {integration_plan.success_probability:.1%}")
        
        if integration_plan.integration_order:
            logger.info(f"\n📋 Integration Order:")
            for i, file_path in enumerate(integration_plan.integration_order):
                logger.info(f"   {i+1}. {file_path}")
        
        if integration_plan.connection_suggestions:
            logger.info(f"\n🔗 Top Connection Suggestions:")
            for suggestion in integration_plan.connection_suggestions[:3]:
                logger.info(f"   📁 {suggestion.orphaned_file}")
                logger.info(f"   → {suggestion.target_file} (score: {suggestion.connection_score:.3f})")
                if suggestion.reasoning:
                    logger.info(f"   📝 {suggestion.reasoning[0]}")
                logger.info()
        
        if integration_plan.conflict_warnings:
            logger.info(f"\n⚠️ Integration Warnings:")
            for warning in integration_plan.conflict_warnings:
                logger.info(f"   • {warning}")