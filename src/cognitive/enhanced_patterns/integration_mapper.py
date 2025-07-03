#!/usr/bin/env python3
"""
Integration Map Generator - Comprehensive Integration Planning

This module creates detailed integration maps that specify exactly how to integrate
update packages into target projects. It bridges the gap between Code Connector
suggestions and executable integration plans.

Core of the Auto-Updater workflow - transforms analysis into actionable plans.
"""

import ast
import re
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional, NamedTuple, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import json

# Import foundation components
from .update_package_analyzer import (
    UpdatePackageAnalyzer, PackageIntegrationPlan, PackageFile, PackageDependencyGraph
)
from .code_connector import ConnectionSuggestion

logger = logging.getLogger(__name__)


@dataclass
class FileModification:
    """Represents a specific modification to a file"""
    target_file: str
    modification_type: str  # 'import_add', 'function_call', 'config_update', 'structure_change'
    line_number: Optional[int]
    original_content: Optional[str]
    new_content: str
    reasoning: str
    safety_level: str  # 'safe', 'caution', 'review_required'
    rollback_info: Dict


@dataclass 
class IntegrationStep:
    """Represents a single step in the integration process"""
    step_number: int
    description: str
    step_type: str  # 'file_copy', 'modification', 'dependency_install', 'validation'
    target_files: List[str]
    modifications: List[FileModification]
    prerequisites: List[int]  # Step numbers that must complete first
    validation_commands: List[str]
    estimated_time_seconds: float


@dataclass
class IntegrationMap:
    """Complete integration map with all steps and modifications"""
    package_name: str
    target_project: str
    integration_steps: List[IntegrationStep]
    total_estimated_time: float
    risk_assessment: str  # 'low', 'medium', 'high'
    rollback_plan: List[str]
    validation_strategy: Dict
    success_criteria: List[str]
    
    # Metrics and tracking
    complexity_score: float
    modification_count: int
    file_count: int


class IntegrationMapGenerator:
    """
    Generates comprehensive integration maps from package analysis results.
    
    Transforms Code Connector suggestions and package analysis into detailed,
    executable integration plans with safety guarantees and rollback capabilities.
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.package_analyzer = UpdatePackageAnalyzer(str(self.project_path))
        
        # Safety classification patterns
        self.safety_patterns = {
            'safe': [
                r'^import\s+\w+$',  # Simple imports
                r'^from\s+\w+\s+import\s+\w+$',  # Simple from imports
                r'^\s*#.*$',  # Comments
            ],
            'caution': [
                r'.*\.append\(',  # List modifications
                r'.*\.update\(',  # Dict updates
                r'.*=.*\+.*',  # Additive assignments
            ],
            'review_required': [
                r'.*exec\(',  # Code execution
                r'.*eval\(',  # Expression evaluation
                r'.*__.*__',  # Dunder methods
                r'.*\.replace\(',  # String/content replacement
            ]
        }
    
    def generate_integration_map(self, package_path: str, 
                               target_files: Optional[List[str]] = None,
                               integration_strategy: str = 'conservative') -> IntegrationMap:
        """
        Generate a comprehensive integration map for an update package.
        
        Args:
            package_path: Path to the update package
            target_files: Optional specific target files
            integration_strategy: 'conservative', 'moderate', or 'aggressive'
            
        Returns:
            Complete integration map with step-by-step instructions
        """
        logger.info(f"🗺️ Generating integration map for: {package_path}")
        
        # Phase 1: Analyze the update package
        logger.info("📦 Phase 1: Package analysis...")
        package_plan = self.package_analyzer.analyze_update_package(package_path, target_files)
        
        # Phase 2: Generate integration steps
        logger.info("📋 Phase 2: Generating integration steps...")
        integration_steps = self._generate_integration_steps(package_plan, integration_strategy)
        
        # Phase 3: Create detailed file modifications
        logger.info("✏️ Phase 3: Creating file modifications...")
        self._populate_file_modifications(integration_steps, package_plan)
        
        # Phase 4: Calculate metrics and assessments
        logger.info("📊 Phase 4: Risk assessment and metrics...")
        risk_assessment, complexity_score = self._assess_integration_risk(integration_steps)
        
        # Phase 5: Generate rollback and validation plans
        logger.info("🛡️ Phase 5: Safety planning...")
        rollback_plan = self._generate_rollback_plan(integration_steps)
        validation_strategy = self._generate_validation_strategy(package_plan)
        
        # Create final integration map
        integration_map = IntegrationMap(
            package_name=Path(package_path).name,
            target_project=str(self.project_path),
            integration_steps=integration_steps,
            total_estimated_time=sum(step.estimated_time_seconds for step in integration_steps),
            risk_assessment=risk_assessment,
            rollback_plan=rollback_plan,
            validation_strategy=validation_strategy,
            success_criteria=self._generate_success_criteria(package_plan),
            complexity_score=complexity_score,
            modification_count=sum(len(step.modifications) for step in integration_steps),
            file_count=len(set(f for step in integration_steps for f in step.target_files))
        )
        
        logger.info(f"✅ Integration map complete: {len(integration_steps)} steps, "
                   f"{integration_map.modification_count} modifications, "
                   f"risk: {risk_assessment}")
        
        return integration_map
    
    def _generate_integration_steps(self, package_plan: PackageIntegrationPlan,
                                   strategy: str) -> List[IntegrationStep]:
        """Generate the sequence of integration steps"""
        steps = []
        step_number = 1
        
        # Step 1: Dependency validation
        if package_plan.package_info.external_requirements:
            steps.append(IntegrationStep(
                step_number=step_number,
                description="Validate external dependencies",
                step_type="dependency_install",
                target_files=[],
                modifications=[],
                prerequisites=[],
                validation_commands=[
                    f"python -c 'import {dep}'" for dep in list(package_plan.package_info.external_requirements)[:3]
                ],
                estimated_time_seconds=30.0
            ))
            step_number += 1
        
        # Step 2: Create package directory structure  
        if package_plan.package_info.files:
            steps.append(IntegrationStep(
                step_number=step_number,
                description="Create package directory structure",
                step_type="file_copy",
                target_files=list(package_plan.package_info.files.keys()),
                modifications=[],
                prerequisites=list(range(1, step_number)),
                validation_commands=["ls -la {package_dir}"],
                estimated_time_seconds=10.0
            ))
            step_number += 1
        
        # Step 3-N: Integration based on dependency order
        for file_rel_path in package_plan.integration_order:
            if file_rel_path in package_plan.package_info.files:
                package_file = package_plan.package_info.files[file_rel_path]
                
                # Find relevant connection suggestions for this file
                relevant_connections = [
                    conn for conn in package_plan.connection_suggestions
                    if str(package_file.path) in conn.orphaned_file
                ]
                
                if relevant_connections:
                    steps.append(IntegrationStep(
                        step_number=step_number,
                        description=f"Integrate {file_rel_path} ({package_file.package_role})",
                        step_type="modification",
                        target_files=[conn.target_file for conn in relevant_connections],
                        modifications=[],  # Will be populated later
                        prerequisites=list(range(1, step_number)),
                        validation_commands=[f"python -m py_compile {package_file.path}"],
                        estimated_time_seconds=60.0 + len(relevant_connections) * 30.0
                    ))
                    step_number += 1
        
        # Final step: Comprehensive validation
        steps.append(IntegrationStep(
            step_number=step_number,
            description="Comprehensive integration validation",
            step_type="validation",
            target_files=[],
            modifications=[],
            prerequisites=list(range(1, step_number)),
            validation_commands=[
                "python -m py_compile {target_file}" for step in steps 
                for target_file in step.target_files
            ],
            estimated_time_seconds=120.0
        ))
        
        return steps
    
    def _populate_file_modifications(self, integration_steps: List[IntegrationStep],
                                   package_plan: PackageIntegrationPlan):
        """Populate detailed file modifications for each integration step"""
        
        for step in integration_steps:
            if step.step_type == "modification":
                # Find connection suggestions relevant to this step
                step_connections = []
                for conn in package_plan.connection_suggestions:
                    if any(target in step.target_files for target in [conn.target_file]):
                        step_connections.append(conn)
                
                # Generate modifications for each connection
                for connection in step_connections:
                    modifications = self._generate_file_modifications_from_connection(
                        connection, package_plan
                    )
                    step.modifications.extend(modifications)
    
    def _generate_file_modifications_from_connection(self, connection: ConnectionSuggestion,
                                                   package_plan: PackageIntegrationPlan) -> List[FileModification]:
        """Generate specific file modifications from a connection suggestion"""
        modifications = []
        
        try:
            # Read the target file to understand its structure
            with open(connection.target_file, 'r', encoding='utf-8') as f:
                target_content = f.read()
                target_lines = target_content.splitlines()
            
            # Process integration suggestions
            for suggestion in connection.integration_suggestions:
                if suggestion.startswith('import ') or suggestion.startswith('from '):
                    # Import modification
                    modification = self._create_import_modification(
                        connection.target_file, suggestion, target_lines, connection.reasoning
                    )
                    modifications.append(modification)
                
                elif 'Consider integrating at line' in suggestion:
                    # Function integration modification
                    modification = self._create_function_integration_modification(
                        connection.target_file, suggestion, target_lines, connection.reasoning
                    )
                    modifications.append(modification)
        
        except Exception as e:
            logger.warning(f"Error generating modifications for {connection.target_file}: {e}")
        
        return modifications
    
    def _create_import_modification(self, target_file: str, import_statement: str,
                                  target_lines: List[str], reasoning: List[str]) -> FileModification:
        """Create an import modification"""
        
        # Find the best place to insert the import
        import_line_number = self._find_import_insertion_point(target_lines)
        
        # Determine safety level
        safety_level = self._classify_modification_safety(import_statement)
        
        return FileModification(
            target_file=target_file,
            modification_type="import_add",
            line_number=import_line_number,
            original_content=None,
            new_content=import_statement,
            reasoning=f"Import integration: {reasoning[0] if reasoning else 'Code Connector suggestion'}",
            safety_level=safety_level,
            rollback_info={
                "action": "remove_line",
                "line_number": import_line_number,
                "original_line_count": len(target_lines)
            }
        )
    
    def _create_function_integration_modification(self, target_file: str, suggestion: str,
                                                target_lines: List[str], reasoning: List[str]) -> FileModification:
        """Create a function integration modification"""
        
        # Extract line number from suggestion
        import re
        line_match = re.search(r'line (\d+)', suggestion)
        line_number = int(line_match.group(1)) if line_match else len(target_lines)
        
        # Create a comment suggesting integration
        integration_comment = f"# Consider integration - {reasoning[0] if reasoning else 'suggested by Code Connector'}"
        
        return FileModification(
            target_file=target_file,
            modification_type="function_call",
            line_number=line_number,
            original_content=target_lines[line_number - 1] if line_number <= len(target_lines) else None,
            new_content=integration_comment,
            reasoning=f"Function integration opportunity: {suggestion}",
            safety_level="safe",  # Comments are always safe
            rollback_info={
                "action": "remove_line",
                "line_number": line_number,
                "original_content": target_lines[line_number - 1] if line_number <= len(target_lines) else None
            }
        )
    
    def _find_import_insertion_point(self, target_lines: List[str]) -> int:
        """Find the optimal line number to insert an import statement"""
        
        # Look for existing imports
        last_import_line = 0
        for i, line in enumerate(target_lines):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                last_import_line = i + 1
            elif stripped and not stripped.startswith('#') and last_import_line > 0:
                # Found non-import, non-comment line after imports
                break
        
        # Insert after the last import, or at the beginning if no imports found
        return max(1, last_import_line + 1)
    
    def _classify_modification_safety(self, modification_content: str) -> str:
        """Classify the safety level of a modification"""
        
        for safety_level, patterns in self.safety_patterns.items():
            for pattern in patterns:
                if re.match(pattern, modification_content.strip()):
                    return safety_level
        
        return 'caution'  # Default to caution for unclassified modifications
    
    def _assess_integration_risk(self, integration_steps: List[IntegrationStep]) -> Tuple[str, float]:
        """Assess the overall risk and complexity of the integration"""
        
        total_modifications = sum(len(step.modifications) for step in integration_steps)
        review_required_count = sum(
            1 for step in integration_steps 
            for mod in step.modifications 
            if mod.safety_level == 'review_required'
        )
        
        # Calculate complexity score
        complexity_score = (
            len(integration_steps) * 0.1 +
            total_modifications * 0.05 +
            review_required_count * 0.3
        )
        
        # Determine risk level
        if complexity_score < 0.5 and review_required_count == 0:
            risk_level = "low"
        elif complexity_score < 1.0 and review_required_count <= 2:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return risk_level, complexity_score
    
    def _generate_rollback_plan(self, integration_steps: List[IntegrationStep]) -> List[str]:
        """Generate a comprehensive rollback plan"""
        rollback_steps = [
            "1. Stop any running processes that depend on the integrated package",
            "2. Create backup of current state if not already done",
        ]
        
        # Add specific rollback steps for each modification
        for step in reversed(integration_steps):
            if step.modifications:
                rollback_steps.append(f"3.{step.step_number}. Revert modifications in step {step.step_number}: {step.description}")
        
        rollback_steps.extend([
            "4. Remove any new files created during integration",
            "5. Validate project functionality with comprehensive tests",
            "6. Confirm rollback success with original validation commands"
        ])
        
        return rollback_steps
    
    def _generate_validation_strategy(self, package_plan: PackageIntegrationPlan) -> Dict:
        """Generate a comprehensive validation strategy"""
        return {
            "pre_integration": [
                "Run existing test suite to establish baseline",
                "Verify all external dependencies are available",
                "Create complete project backup"
            ],
            "during_integration": [
                "Validate each step before proceeding to next",
                "Run syntax checks after each file modification",
                "Monitor for import errors and dependency issues"
            ],
            "post_integration": [
                "Run complete test suite to detect regressions",
                "Validate all new functionality works as expected",
                "Perform security scan for new vulnerabilities",
                "Check performance impact of integration"
            ],
            "success_indicators": [
                "All tests pass (existing + new)",
                "No import errors or syntax issues",
                "No security vulnerabilities introduced",
                "Performance within acceptable thresholds"
            ]
        }
    
    def _generate_success_criteria(self, package_plan: PackageIntegrationPlan) -> List[str]:
        """Generate success criteria for the integration"""
        criteria = [
            "All package files successfully integrated into target project",
            "All connection suggestions successfully implemented",
            "No syntax errors or import failures in modified files",
            "All external dependencies properly resolved"
        ]
        
        if package_plan.connection_suggestions:
            criteria.append(f"All {len(package_plan.connection_suggestions)} connection suggestions validated")
        
        if package_plan.package_info.external_requirements:
            criteria.append(f"All {len(package_plan.package_info.external_requirements)} external dependencies accessible")
        
        criteria.append(f"Integration probability target ({package_plan.success_probability:.1%}) achieved or exceeded")
        
        return criteria


def generate_integration_map(package_path: str, project_path: str,
                           target_files: Optional[List[str]] = None,
                           strategy: str = 'conservative') -> IntegrationMap:
    """
    Main API function for integration map generation.
    
    Args:
        package_path: Path to the update package
        project_path: Path to the target project
        target_files: Optional specific target files
        strategy: Integration strategy ('conservative', 'moderate', 'aggressive')
    
    Returns:
        Complete integration map
    """
    generator = IntegrationMapGenerator(project_path)
    return generator.generate_integration_map(package_path, target_files, strategy)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Integration Map Generator - Comprehensive Integration Planning")
    parser.add_argument("package_path", help="Path to the update package")
    parser.add_argument("project_path", help="Path to the target project")
    parser.add_argument("--target-files", nargs="+", help="Specific target files")
    parser.add_argument("--strategy", choices=['conservative', 'moderate', 'aggressive'], 
                       default='conservative', help="Integration strategy")
    parser.add_argument("--output", help="Output JSON file for integration map")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    # Generate integration map
    integration_map = generate_integration_map(
        args.package_path,
        args.project_path,
        args.target_files,
        args.strategy
    )
    
    # Output results
    if args.output:
        # Convert to serializable format
        map_dict = {
            "package_name": integration_map.package_name,
            "target_project": integration_map.target_project,
            "total_estimated_time": integration_map.total_estimated_time,
            "risk_assessment": integration_map.risk_assessment,
            "complexity_score": integration_map.complexity_score,
            "modification_count": integration_map.modification_count,
            "file_count": integration_map.file_count,
            "integration_steps": [
                {
                    "step_number": step.step_number,
                    "description": step.description,
                    "step_type": step.step_type,
                    "target_files": step.target_files,
                    "estimated_time_seconds": step.estimated_time_seconds,
                    "modifications": [
                        {
                            "target_file": mod.target_file,
                            "modification_type": mod.modification_type,
                            "line_number": mod.line_number,
                            "new_content": mod.new_content,
                            "reasoning": mod.reasoning,
                            "safety_level": mod.safety_level
                        }
                        for mod in step.modifications
                    ]
                }
                for step in integration_map.integration_steps
            ],
            "rollback_plan": integration_map.rollback_plan,
            "validation_strategy": integration_map.validation_strategy,
            "success_criteria": integration_map.success_criteria
        }
        
        with open(args.output, 'w') as f:
            json.dump(map_dict, f, indent=2)
            
        logger.info(f"💾 Integration map saved to {args.output}")
    else:
        # Console output
        logger.info(f"\n🗺️ Integration Map")
        logger.info("=" * 50)
        logger.info(f"📦 Package: {integration_map.package_name}")
        logger.info(f"🎯 Target: {integration_map.target_project}")
        logger.info(f"📊 Steps: {len(integration_map.integration_steps)}")
        logger.info(f"✏️ Modifications: {integration_map.modification_count}")
        logger.info(f"📁 Files affected: {integration_map.file_count}")
        logger.info(f"⏱️ Estimated time: {integration_map.total_estimated_time:.0f}s")
        logger.info(f"⚠️ Risk: {integration_map.risk_assessment}")
        logger.info(f"🧮 Complexity: {integration_map.complexity_score:.2f}")
        
        logger.info(f"\n📋 Integration Steps:")
        for step in integration_map.integration_steps:
            logger.info(f"   {step.step_number}. {step.description} ({step.step_type})")
            logger.info(f"      Time: {step.estimated_time_seconds:.0f}s, Modifications: {len(step.modifications)}")
        
        logger.info(f"\n✅ Success Criteria:")
        for criterion in integration_map.success_criteria:
            logger.info(f"   • {criterion}")
        
        if integration_map.risk_assessment != "low":
            logger.info(f"\n🛡️ Rollback Plan Available: {len(integration_map.rollback_plan)} steps")