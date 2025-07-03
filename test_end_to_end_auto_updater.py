#!/usr/bin/env python3
"""
End-to-End Auto-Updater Workflow Proof-of-Concept

This script demonstrates the complete Auto-Updater pipeline:
1. Code Connector Analysis (orphaned file discovery and connection suggestions)
2. Update Package Analysis (multi-file dependency analysis) 
3. Integration Map Generation (comprehensive planning with safety features)
4. Automated Patching (safe execution with rollback capabilities)

This showcases the transformation of Mesopredator from a strategic coordinator
to a creative architect capable of intelligent code integration.
"""

import logging
import tempfile
import shutil
import json
import time
from pathlib import Path
from typing import Dict, List, Any

# Import the complete Auto-Updater pipeline
from src.cognitive.enhanced_patterns.code_connector import CodeConnector
from src.cognitive.enhanced_patterns.update_package_analyzer import UpdatePackageAnalyzer
from src.cognitive.enhanced_patterns.integration_mapper import IntegrationMapGenerator
from src.cognitive.enhanced_patterns.automated_patcher import AutomatedPatcher

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class AutoUpdaterWorkflowDemo:
    """
    Complete Auto-Updater workflow demonstration.
    
    Showcases the end-to-end process from orphaned code discovery
    to safe automated integration.
    """
    
    def __init__(self, test_project_path: str, update_package_path: str):
        self.test_project_path = Path(test_project_path)
        self.update_package_path = Path(update_package_path)
        
        # Initialize components
        self.code_connector = CodeConnector(str(self.test_project_path))
        self.package_analyzer = UpdatePackageAnalyzer(str(self.test_project_path))
        self.integration_mapper = IntegrationMapGenerator(str(self.test_project_path))
        self.automated_patcher = AutomatedPatcher(str(self.test_project_path))
        
        # Tracking
        self.workflow_results = {}
        self.start_time = time.time()
    
    def run_complete_workflow(self, dry_run: bool = True, interactive: bool = False) -> Dict[str, Any]:
        """
        Execute the complete Auto-Updater workflow.
        
        Args:
            dry_run: If True, simulate changes without making them
            interactive: If True, require user approval for modifications
            
        Returns:
            Complete workflow results with metrics and analysis
        """
        logger.info("🚀 Starting End-to-End Auto-Updater Workflow")
        logger.info(f"   📁 Project: {self.test_project_path}")
        logger.info(f"   📦 Update Package: {self.update_package_path}")
        logger.info(f"   🔍 Mode: {'Dry Run' if dry_run else 'Live Execution'}")
        
        try:
            # Phase 1: Code Connector Analysis
            logger.info("\n" + "="*60)
            logger.info("📊 PHASE 1: Code Connector Analysis")
            logger.info("="*60)
            
            phase1_results = self._phase1_code_connector_analysis()
            self.workflow_results['phase1'] = phase1_results
            
            # Phase 2: Update Package Analysis
            logger.info("\n" + "="*60)
            logger.info("📦 PHASE 2: Update Package Analysis")
            logger.info("="*60)
            
            phase2_results = self._phase2_package_analysis()
            self.workflow_results['phase2'] = phase2_results
            
            # Phase 3: Integration Map Generation
            logger.info("\n" + "="*60)
            logger.info("🗺️ PHASE 3: Integration Map Generation")
            logger.info("="*60)
            
            phase3_results = self._phase3_integration_mapping(phase2_results)
            self.workflow_results['phase3'] = phase3_results
            
            # Phase 4: Automated Patching
            logger.info("\n" + "="*60)
            logger.info("🤖 PHASE 4: Automated Patching")
            logger.info("="*60)
            
            phase4_results = self._phase4_automated_patching(
                phase3_results['integration_map'], dry_run, interactive
            )
            self.workflow_results['phase4'] = phase4_results
            
            # Workflow Summary
            self._generate_workflow_summary()
            
            return self.workflow_results
            
        except Exception as e:
            logger.error(f"💥 Workflow failed: {e}")
            self.workflow_results['error'] = str(e)
            return self.workflow_results
    
    def _phase1_code_connector_analysis(self) -> Dict[str, Any]:
        """Phase 1: Discover orphaned files and generate connection suggestions"""
        
        # Discover orphaned files (files in update package)
        orphaned_files = list(self.update_package_path.rglob("*.py"))
        logger.info(f"🔍 Discovered {len(orphaned_files)} orphaned files")
        
        # Discover main project files
        main_files = [f for f in self.test_project_path.rglob("*.py") 
                     if not any(skip in str(f) for skip in ["__pycache__", "test_", ".git"])]
        logger.info(f"📁 Found {len(main_files)} main project files")
        
        # Generate connection suggestions
        start_time = time.time()
        suggestions = self.code_connector.analyze_orphaned_files(orphaned_files, main_files)
        analysis_time = time.time() - start_time
        
        logger.info(f"✅ Generated {len(suggestions)} connection suggestions in {analysis_time:.2f}s")
        
        # Log top suggestions
        for i, suggestion in enumerate(suggestions[:3]):
            logger.info(f"   🔗 {i+1}. {suggestion.orphaned_file} → {suggestion.target_file}")
            logger.info(f"      Score: {suggestion.connection_score:.3f}, Type: {suggestion.connection_type}")
        
        return {
            'orphaned_files_count': len(orphaned_files),
            'main_files_count': len(main_files),
            'suggestions_count': len(suggestions),
            'analysis_time_seconds': analysis_time,
            'top_suggestions': [
                {
                    'orphaned_file': s.orphaned_file,
                    'target_file': s.target_file,
                    'connection_score': s.connection_score,
                    'connection_type': s.connection_type,
                    'reasoning': s.reasoning[:2] if s.reasoning else []
                }
                for s in suggestions[:5]
            ],
            'suggestions': suggestions  # Full suggestions for next phase
        }
    
    def _phase2_package_analysis(self) -> Dict[str, Any]:
        """Phase 2: Analyze update package structure and dependencies"""
        
        start_time = time.time()
        integration_plan = self.package_analyzer.analyze_update_package(
            str(self.update_package_path)
        )
        analysis_time = time.time() - start_time
        
        logger.info(f"✅ Package analysis completed in {analysis_time:.2f}s")
        logger.info(f"   📊 Files: {len(integration_plan.package_info.files)}")
        logger.info(f"   🔗 Connections: {len(integration_plan.connection_suggestions)}")
        logger.info(f"   📈 Success Probability: {integration_plan.success_probability:.1%}")
        logger.info(f"   ⚠️ Warnings: {len(integration_plan.conflict_warnings)}")
        
        # Log integration order
        logger.info(f"   📋 Integration Order:")
        for i, file_path in enumerate(integration_plan.integration_order):
            logger.info(f"      {i+1}. {file_path}")
        
        return {
            'analysis_time_seconds': analysis_time,
            'package_files_count': len(integration_plan.package_info.files),
            'connection_suggestions_count': len(integration_plan.connection_suggestions),
            'success_probability': integration_plan.success_probability,
            'conflict_warnings_count': len(integration_plan.conflict_warnings),
            'integration_order': integration_plan.integration_order,
            'external_requirements': list(integration_plan.package_info.external_requirements),
            'integration_plan': integration_plan  # Full plan for next phase
        }
    
    def _phase3_integration_mapping(self, phase2_results: Dict[str, Any]) -> Dict[str, Any]:
        """Phase 3: Generate detailed integration map with safety features"""
        
        integration_plan = phase2_results['integration_plan']
        
        start_time = time.time()
        # Use the update package path, not the integration plan object
        integration_map = self.integration_mapper.generate_integration_map(str(self.update_package_path))
        mapping_time = time.time() - start_time
        
        logger.info(f"✅ Integration map generated in {mapping_time:.2f}s")
        logger.info(f"   📋 Steps: {len(integration_map.integration_steps)}")
        logger.info(f"   🔧 Modifications: {integration_map.modification_count}")
        logger.info(f"   ⏱️ Estimated Time: {integration_map.total_estimated_time:.1f}s")
        logger.info(f"   🛡️ Risk Level: {integration_map.risk_assessment}")
        
        # Log integration steps
        logger.info(f"   📝 Integration Steps:")
        for step in integration_map.integration_steps:
            logger.info(f"      {step.step_number}. {step.description} ({step.step_type})")
        
        return {
            'mapping_time_seconds': mapping_time,
            'integration_steps_count': len(integration_map.integration_steps),
            'modification_count': integration_map.modification_count,
            'estimated_time_seconds': integration_map.total_estimated_time,
            'risk_assessment': integration_map.risk_assessment,
            'complexity_score': integration_map.complexity_score,
            'integration_map': integration_map  # Full map for execution
        }
    
    def _phase4_automated_patching(self, integration_map, dry_run: bool, 
                                 interactive: bool) -> Dict[str, Any]:
        """Phase 4: Execute integration map with automated patching"""
        
        start_time = time.time()
        execution_results = self.automated_patcher.execute_integration_map(
            integration_map, dry_run, interactive
        )
        execution_time = time.time() - start_time
        
        status = execution_results.get('status', 'unknown')
        logger.info(f"✅ Automated patching completed: {status}")
        logger.info(f"   ⏱️ Execution Time: {execution_time:.2f}s")
        logger.info(f"   📊 Steps Executed: {execution_results.get('steps_executed', 0)}")
        logger.info(f"   🔧 Modifications: {execution_results.get('modifications_successful', 0)}")
        
        if execution_results.get('rollback_initiated'):
            logger.warning(f"   🔄 Rollback was initiated")
        
        if execution_results.get('backup_directory'):
            logger.info(f"   💾 Backup: {execution_results['backup_directory']}")
        
        return {
            'execution_time_seconds': execution_time,
            'status': status,
            'steps_executed': execution_results.get('steps_executed', 0),
            'modifications_attempted': execution_results.get('modifications_attempted', 0),
            'modifications_successful': execution_results.get('modifications_successful', 0),
            'rollback_initiated': execution_results.get('rollback_initiated', False),
            'backup_directory': execution_results.get('backup_directory'),
            'execution_results': execution_results
        }
    
    def _generate_workflow_summary(self):
        """Generate comprehensive workflow summary"""
        
        total_time = time.time() - self.start_time
        
        logger.info("\n" + "="*60)
        logger.info("📈 AUTO-UPDATER WORKFLOW SUMMARY")
        logger.info("="*60)
        
        logger.info(f"⏱️ Total Workflow Time: {total_time:.2f}s")
        
        # Phase summaries
        if 'phase1' in self.workflow_results:
            p1 = self.workflow_results['phase1']
            logger.info(f"📊 Phase 1 - Code Connector: {p1['suggestions_count']} suggestions ({p1['analysis_time_seconds']:.2f}s)")
        
        if 'phase2' in self.workflow_results:
            p2 = self.workflow_results['phase2']
            logger.info(f"📦 Phase 2 - Package Analysis: {p2['success_probability']:.1%} success ({p2['analysis_time_seconds']:.2f}s)")
        
        if 'phase3' in self.workflow_results:
            p3 = self.workflow_results['phase3']
            logger.info(f"🗺️ Phase 3 - Integration Mapping: {p3['modification_count']} modifications ({p3['mapping_time_seconds']:.2f}s)")
        
        if 'phase4' in self.workflow_results:
            p4 = self.workflow_results['phase4']
            logger.info(f"🤖 Phase 4 - Automated Patching: {p4['status']} ({p4['execution_time_seconds']:.2f}s)")
        
        # Overall assessment
        if all(phase in self.workflow_results for phase in ['phase1', 'phase2', 'phase3', 'phase4']):
            if self.workflow_results['phase4']['status'] == 'success':
                logger.info("✅ WORKFLOW COMPLETED SUCCESSFULLY")
            else:
                logger.info("⚠️ WORKFLOW COMPLETED WITH ISSUES")
        else:
            logger.info("❌ WORKFLOW INCOMPLETE")
        
        self.workflow_results['summary'] = {
            'total_time_seconds': total_time,
            'completed_phases': len([k for k in self.workflow_results.keys() if k.startswith('phase')]),
            'overall_status': 'success' if self.workflow_results.get('phase4', {}).get('status') == 'success' else 'incomplete'
        }


def create_test_environment():
    """Create a test environment for the Auto-Updater workflow"""
    
    # Create test project directory
    test_project = Path("/tmp/auto_updater_test_project")
    if test_project.exists():
        shutil.rmtree(test_project)
    
    test_project.mkdir(parents=True)
    
    # Create some main project files
    (test_project / "main.py").write_text('''
def main():
    print("Main application")
    # Add better logging
    # Add configuration management

if __name__ == "__main__":
    main()
''')
    
    (test_project / "utils.py").write_text('''
def simple_helper():
    return "basic utility"

# Add more utility functions
''')
    
    (test_project / "config.py").write_text('''
import os

# Simple configuration
# IMPROVED: DEBUG = True
LOG_LEVEL = "INFO"

# Add configuration validation
''')
    
    # Create update package directory  
    update_package = Path("/tmp/auto_updater_update_package")
    if update_package.exists():
        shutil.rmtree(update_package)
    
    update_package.mkdir(parents=True)
    
    # Create package files that could integrate with main project
    (update_package / "advanced_logger.py").write_text('''
import logging
from datetime import datetime

class AdvancedLogger:
    """Enhanced logging functionality"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        
    def log_with_timestamp(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().isoformat()
        getattr(self.logger, level.lower())(f"[{timestamp}] {message}")
        
    def configure_file_handler(self, filename: str):
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
''')
    
    (update_package / "config_validator.py").write_text('''
from typing import Dict, Any, List

class ConfigValidator:
    """Configuration validation and management"""
    
    def __init__(self):
        self.required_keys = []
        self.validators = {}
    
    def add_required_key(self, key: str, validator=None):
        self.required_keys.append(key)
        if validator:
            self.validators[key] = validator
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        errors = []
        
        for key in self.required_keys:
            if key not in config:
                errors.append(f"Missing required key: {key}")
            elif key in self.validators:
                try:
                    self.validators[key](config[key])
                except Exception as e:
                    errors.append(f"Invalid value for {key}: {e}")
        
        return errors
    
    def get_validated_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        errors = self.validate_config(config)
        if errors:
            raise ValueError(f"Configuration validation failed: {errors}")
        return config
''')
    
    logger.info(f"✅ Test environment created:")
    logger.info(f"   📁 Test Project: {test_project}")
    logger.info(f"   📦 Update Package: {update_package}")
    
    return str(test_project), str(update_package)


def main():
    """Main demonstration function"""
    
    logger.info("🧪 Auto-Updater End-to-End Workflow Demonstration")
    logger.info("=" * 60)
    
    try:
        # Create test environment
        test_project_path, update_package_path = create_test_environment()
        
        # Initialize workflow demo
        demo = AutoUpdaterWorkflowDemo(test_project_path, update_package_path)
        
        # Run complete workflow (dry run by default for safety)
        results = demo.run_complete_workflow(dry_run=True, interactive=False)
        
        # Save results for analysis
        results_file = Path("/tmp/auto_updater_workflow_results.json")
        with open(results_file, 'w') as f:
            # Convert complex objects to serializable format
            serializable_results = {}
            for phase, data in results.items():
                if isinstance(data, dict):
                    serializable_results[phase] = {
                        k: v for k, v in data.items() 
                        if not k.endswith(('_plan', '_map', 'suggestions', 'integration_plan', 'execution_results'))
                    }
                else:
                    serializable_results[phase] = data
            
            json.dump(serializable_results, f, indent=2)
        
        logger.info(f"\n💾 Results saved to: {results_file}")
        
        # Cleanup
        shutil.rmtree(test_project_path)
        shutil.rmtree(update_package_path)
        
        logger.info("🧹 Test environment cleaned up")
        logger.info("\n🎉 Auto-Updater Workflow Demonstration Complete!")
        
        return results
        
    except Exception as e:
        logger.error(f"💥 Demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()