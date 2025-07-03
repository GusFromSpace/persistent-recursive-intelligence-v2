#!/usr/bin/env python3
"""
Update Package Format System Demonstration

This script demonstrates the complete update package format system:
1. Creating standardized update packages
2. Validating package integrity and security
3. Extracting package metadata
4. Integration with Auto-Updater workflow
"""

import json
import logging
import shutil
import tempfile
from pathlib import Path

# Import the update package format system
from src.cognitive.enhanced_patterns.update_package_format import (
    PackageMetadata, PackageType, UpdatePackageBuilder,
    UpdatePackageValidator, extract_package_metadata
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def create_sample_update_package():
    """Create a sample update package for demonstration"""
    
    # Create temporary source directory
    source_dir = Path(tempfile.mkdtemp(prefix="sample_package_source_"))
    
    # Create sample files
    advanced_logger = source_dir / "advanced_logger.py"
    advanced_logger.write_text('''
import logging
from datetime import datetime
from typing import Optional

class AdvancedLogger:
    """Enhanced logging functionality with timestamp and file handling"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        self._setup_formatter()
    
    def _setup_formatter(self):
        """Setup custom log formatter"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def log_with_timestamp(self, message: str, level: str = "INFO"):
        """Log message with explicit timestamp"""
        timestamp = datetime.now().isoformat()
        formatted_message = f"[{timestamp}] {message}"
        getattr(self.logger, level.lower())(formatted_message)
    
    def configure_file_handler(self, filename: str, max_bytes: int = 1024*1024):
        """Configure rotating file handler"""
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            filename, maxBytes=max_bytes, backupCount=5
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def log_exception(self, exception: Exception, context: Optional[str] = None):
        """Log exception with context"""
        import traceback
        
        context_msg = f" in {context}" if context else ""
        self.logger.error(f"Exception{context_msg}: {exception}")
        self.logger.debug(traceback.format_exc())
''')
    
    config_validator = source_dir / "config_validator.py"
    config_validator.write_text('''
from typing import Dict, Any, List, Callable, Optional
import re

class ConfigValidator:
    """Configuration validation and management system"""
    
    def __init__(self):
        self.required_keys = []
        self.validators = {}
        self.type_validators = {}
    
    def add_required_key(self, key: str, validator: Optional[Callable] = None, key_type: Optional[type] = None):
        """Add required configuration key with optional validator"""
        self.required_keys.append(key)
        
        if validator:
            self.validators[key] = validator
        
        if key_type:
            self.type_validators[key] = key_type
    
    def add_email_validator(self, key: str):
        """Add email validation for a key"""
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$')
        self.validators[key] = lambda value: bool(email_pattern.match(str(value)))
    
    def add_url_validator(self, key: str):
        """Add URL validation for a key"""
        url_pattern = re.compile(r'^https?://[^\\s/$.?#].[^\\s]*$')
        self.validators[key] = lambda value: bool(url_pattern.match(str(value)))
    
    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Check required keys
        for key in self.required_keys:
            if key not in config:
                errors.append(f"Missing required key: {key}")
                continue
            
            value = config[key]
            
            # Type validation
            if key in self.type_validators:
                expected_type = self.type_validators[key]
                if not isinstance(value, expected_type):
                    errors.append(f"Key '{key}' must be of type {expected_type.__name__}")
            
            # Custom validation
            if key in self.validators:
                try:
                    if not self.validators[key](value):
                        errors.append(f"Invalid value for key '{key}': {value}")
                except Exception as e:
                    errors.append(f"Validation error for key '{key}': {e}")
        
        return errors
    
    def get_validated_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Get validated configuration or raise exception"""
        errors = self.validate_config(config)
        if errors:
            raise ValueError(f"Configuration validation failed: {', '.join(errors)}")
        return config.copy()
    
    def suggest_fixes(self, config: Dict[str, Any]) -> Dict[str, str]:
        """Suggest fixes for configuration issues"""
        suggestions = {}
        errors = self.validate_config(config)
        
        for error in errors:
            if "Missing required key" in error:
                key = error.split(": ")[1]
                suggestions[key] = f"Add required key '{key}' to configuration"
            elif "must be of type" in error:
                suggestions["type_fix"] = "Check data types in configuration"
        
        return suggestions
''')
    
    # Create README
    readme = source_dir / "README.md"
    readme.write_text('''
# Advanced Logging and Configuration Package

This package provides enhanced logging capabilities and configuration validation
for Python applications.

## Components

### AdvancedLogger
- Enhanced logging with timestamps
- File rotation support
- Exception logging with context
- Configurable formatters

### ConfigValidator
- Required key validation
- Type checking
- Email and URL validation
- Error reporting and suggestions

## Usage Example

```python
from advanced_logger import AdvancedLogger
from config_validator import ConfigValidator

# Setup logger
logger = AdvancedLogger("myapp")
logger.configure_file_handler("app.log")
logger.log_with_timestamp("Application started")

# Setup config validation
validator = ConfigValidator()
validator.add_required_key("database_url", key_type=str)
validator.add_email_validator("admin_email")

config = {"database_url": "sqlite:///app.db", "admin_email": "admin@example.com"}
validated_config = validator.get_validated_config(config)
```

## Integration

This package integrates well with existing Python applications and provides
drop-in enhancements for logging and configuration management.
''')
    
    # Create requirements
    requirements = source_dir / "requirements.txt"
    requirements.write_text('''
# Core dependencies
typing-extensions>=3.10.0
# No additional dependencies - uses standard library
''')
    
    return source_dir


def demonstrate_package_creation():
    """Demonstrate creating a standardized update package"""
    
    logger.info("🏗️ Creating sample update package...")
    
    # Create sample source
    source_dir = create_sample_update_package()
    
    # Create package metadata
    metadata = PackageMetadata(
        name="advanced-logging-config",
        version="1.2.0",
        description="Enhanced logging and configuration validation utilities",
        package_type=PackageType.FEATURE,
        author="GusFromSpace Development",
        author_email="dev@gusfromspace.com",
        organization="GusFromSpace",
        source_url="https://github.com/gusfromspace/advanced-logging-config",
        target_frameworks=["mesopredator", "general-python"],
        python_version_min="3.8",
        dependencies=["typing-extensions>=3.10.0"],
        integration_strategy="conservative",
        target_directories=["src/", "utils/", "logging/"],
        target_files=["main.py", "config.py", "logger.py"],
        security_level="standard",
        requires_approval=True,
        auto_approvable=False,
        tags=["logging", "configuration", "validation", "utilities"],
        keywords=["log", "config", "validate", "timestamp", "rotation"],
        documentation_url="https://docs.gusfromspace.com/advanced-logging-config"
    )
    
    # Build package
    output_dir = Path(tempfile.mkdtemp(prefix="update_package_"))
    package_path = output_dir / "advanced-logging-config"
    
    builder = UpdatePackageBuilder(output_format="directory")
    created_package = builder.build_package(source_dir, package_path, metadata)
    
    logger.info(f"✅ Package created at: {created_package}")
    
    # Clean up source
    shutil.rmtree(source_dir)
    
    return created_package


def demonstrate_package_validation(package_path: Path):
    """Demonstrate package validation and security scanning"""
    
    logger.info("🔍 Validating update package...")
    
    # Create validator
    validator = UpdatePackageValidator(strict_mode=True)
    
    # Validate package
    results = validator.validate_package(package_path)
    
    logger.info(f"📊 Validation Results:")
    logger.info(f"   ✅ Valid: {results['valid']}")
    logger.info(f"   🛡️ Compatibility: {results['compatibility'].value}")
    logger.info(f"   ⚠️ Warnings: {len(results['warnings'])}")
    logger.info(f"   ❌ Errors: {len(results['errors'])}")
    logger.info(f"   🚨 Security Issues: {len(results['security_issues'])}")
    
    # Display details
    if results['warnings']:
        logger.info("   Warning Details:")
        for warning in results['warnings']:
            logger.info(f"     • {warning}")
    
    if results['errors']:
        logger.info("   Error Details:")
        for error in results['errors']:
            logger.info(f"     • {error}")
    
    if results['security_issues']:
        logger.info("   Security Issue Details:")
        for issue in results['security_issues']:
            severity_emoji = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}
            emoji = severity_emoji.get(issue.get('severity', 'low'), '⚠️')
            logger.info(f"     {emoji} {issue.get('description', 'Unknown issue")}")
    
    return results


def demonstrate_metadata_extraction(package_path: Path):
    """Demonstrate metadata extraction and inspection"""
    
    logger.info("📋 Extracting package metadata...")
    
    metadata = extract_package_metadata(str(package_path))
    
    if metadata:
        logger.info(f"📦 Package Information:")
        logger.info(f"   Name: {metadata.name}")
        logger.info(f"   Version: {metadata.version}")
        logger.info(f"   Type: {metadata.package_type.value}")
        logger.info(f"   Author: {metadata.author}")
        logger.info(f"   Description: {metadata.description}")
        logger.info(f"   Python Version: {metadata.python_version_min}+")
        logger.info(f"   Dependencies: {len(metadata.dependencies)}")
        logger.info(f"   Security Level: {metadata.security_level}")
        logger.info(f"   Auto-Approvable: {metadata.auto_approvable}")
        logger.info(f"   Tags: {', '.join(metadata.tags)}")
    else:
        logger.error("❌ Could not extract metadata")
    
    return metadata


def demonstrate_integration_with_auto_updater(package_path: Path):
    """Demonstrate integration with Auto-Updater system"""
    
    logger.info("🤖 Testing Auto-Updater integration...")
    
    try:
        # Import Auto-Updater components
        from src.cognitive.enhanced_patterns.update_package_analyzer import UpdatePackageAnalyzer
        from src.cognitive.enhanced_patterns.integration_mapper import IntegrationMapGenerator
        
        # Create test project directory
        test_project = Path(tempfile.mkdtemp(prefix="test_integration_"))
        
        # Create simple test project files
        main_file = test_project / "main.py"
        main_file.write_text('''
def main():
    print("Test application")
    # Add better logging
    # Add configuration management

if __name__ == "__main__":
    main()
''')
        
        config_file = test_project / "config.py"
        config_file.write_text('''
# Simple configuration
# IMPROVED: DEBUG = True
LOG_LEVEL = "INFO"
# Add configuration validation
''')
        
        # Analyze package for integration
        analyzer = UpdatePackageAnalyzer(str(test_project))
        integration_plan = analyzer.analyze_update_package(str(package_path))
        
        logger.info(f"🔗 Integration Analysis:")
        logger.info(f"   Files in Package: {len(integration_plan.package_info.files)}")
        logger.info(f"   Connection Suggestions: {len(integration_plan.connection_suggestions)}")
        logger.info(f"   Success Probability: {integration_plan.success_probability:.1%}")
        logger.info(f"   Conflict Warnings: {len(integration_plan.conflict_warnings)}")
        
        # Generate integration map
        mapper = IntegrationMapGenerator(str(test_project))
        integration_map = mapper.generate_integration_map(str(package_path))
        
        logger.info(f"🗺️ Integration Mapping:")
        logger.info(f"   Integration Steps: {len(integration_map.integration_steps)}")
        logger.info(f"   Total Modifications: {integration_map.modification_count}")
        logger.info(f"   Risk Assessment: {integration_map.risk_assessment}")
        logger.info(f"   Estimated Time: {integration_map.total_estimated_time:.1f}s")
        
        # Clean up test project
        shutil.rmtree(test_project)
        
        logger.info("✅ Auto-Updater integration test successful")
        
    except Exception as e:
        logger.error(f"❌ Auto-Updater integration test failed: {e}")


def demonstrate_cli_usage(package_path: Path):
    """Demonstrate CLI usage of the package format system"""
    
    logger.info("💻 CLI Usage Examples:")
    
    # Show CLI commands that would be used
    commands = [
        f"# Validate package",
        f"python -m src.cognitive.enhanced_patterns.update_package_format validate {package_path}",
        f"",
        f"# Extract metadata", 
        f"python -m src.cognitive.enhanced_patterns.update_package_format metadata {package_path}",
        f"",
        f"# Build new package",
        f"python -m src.cognitive.enhanced_patterns.update_package_format build ./source ./output \\",
        f"  --name 'my-package' --version '1.0.0' --description 'My package' \\",
        f"  --author 'Developer' --email 'dev@example.com'"
    ]
    
    for command in commands:
        logger.info(f"   {command}")


def main():
    """Main demonstration function"""
    
    logger.info("🚀 Update Package Format System Demonstration")
    logger.info("=" * 60)
    
    try:
        # Step 1: Create a sample update package
        package_path = demonstrate_package_creation()
        
        # Step 2: Validate the package
        validation_results = demonstrate_package_validation(package_path)
        
        # Step 3: Extract and display metadata
        metadata = demonstrate_metadata_extraction(package_path)
        
        # Step 4: Test Auto-Updater integration
        demonstrate_integration_with_auto_updater(package_path)
        
        # Step 5: Show CLI usage
        demonstrate_cli_usage(package_path)
        
        # Save demonstration results
        results_file = Path("/tmp/package_format_demo_results.json")
        demo_results = {
            "package_path": str(package_path),
            "validation_valid": validation_results['valid'],
            "validation_compatibility": validation_results['compatibility'].value,
            "metadata_name": metadata.name if metadata else None,
            "metadata_version": metadata.version if metadata else None,
            "demo_timestamp": "2025-07-01T12:00:00Z"
        }
        
        with open(results_file, 'w') as f:
            json.dump(demo_results, f, indent=2)
        
        logger.info(f"\n💾 Demonstration results saved to: {results_file}")
        
        # Clean up
        shutil.rmtree(package_path.parent)
        
        logger.info("\n🎉 Update Package Format demonstration complete!")
        logger.info("✅ All components working correctly")
        
    except Exception as e:
        logger.error(f"💥 Demonstration failed: {e}")
        raise


if __name__ == "__main__":
    main()