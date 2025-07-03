#!/usr/bin/env python3
"""
Update Package Format and Validation System

This module defines a standardized format for update packages that can be safely
distributed, validated, and integrated using the Auto-Updater system.

Key Features:
- Standardized package structure with metadata
- Cryptographic validation and integrity checking
- Version compatibility and dependency management
- Security scanning and risk assessment
- Automated package generation and publishing
"""

import json
import hashlib
import logging
import tempfile
import tarfile
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, NamedTuple
from dataclasses import dataclass, field
from enum import Enum
import datetime
import semantic_version
import yaml

logger = logging.getLogger(__name__)


class PackageType(Enum):
    """Types of update packages"""
    FEATURE = "feature"           # New functionality
    # IMPROVED: BUGFIX = "bugfix"            # Bug fixes
    ENHANCEMENT = "enhancement"   # Improvements to existing features
    SECURITY = "security"        # Security updates
    LIBRARY = "library"          # Library/dependency updates
    TEMPLATE = "template"        # Code templates and examples


class CompatibilityLevel(Enum):
    """Package compatibility levels"""
    COMPATIBLE = "compatible"     # Fully compatible, safe to auto-integrate
    MINOR_ISSUES = "minor"       # Minor compatibility issues, review recommended
    MAJOR_ISSUES = "major"       # Major compatibility issues, manual review required
    INCOMPATIBLE = "incompatible" # Incompatible, manual adaptation needed


@dataclass
class PackageMetadata:
    """Comprehensive metadata for update packages"""
    
    # Basic information
    name: str
    version: str
    description: str
    package_type: PackageType
    
    # Author and origin
    author: str
    author_email: str
    organization: Optional[str] = None
    source_url: Optional[str] = None
    
    # Compatibility and requirements
    target_frameworks: List[str] = field(default_factory=list)
    python_version_min: str = "3.7"
    python_version_max: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    
    # Integration hints
    integration_strategy: str = "conservative"  # conservative, aggressive, custom
    target_directories: List[str] = field(default_factory=list)
    target_files: List[str] = field(default_factory=list)
    
    # Security and validation
    security_level: str = "standard"  # minimal, standard, strict
    requires_approval: bool = True
    auto_approvable: bool = False
    
    # Timestamps and versioning
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    # Package integrity
    checksum: Optional[str] = None
    signature: Optional[str] = None
    
    # Additional metadata
    tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    documentation_url: Optional[str] = None
    changelog_url: Optional[str] = None


@dataclass
class PackageFile:
    """Information about a file in the update package"""
    path: str
    size: int
    checksum: str
    modification_type: str  # new, modified, deleted
    target_location: Optional[str] = None
    permissions: str = "644"
    executable: bool = False


@dataclass
class PackageManifest:
    """Complete package manifest with all files and metadata"""
    metadata: PackageMetadata
    files: List[PackageFile]
    total_size: int
    file_count: int
    manifest_version: str = "1.0"


class UpdatePackageValidator:
    """
    Validates update packages for security, integrity, and compatibility.
    """
    
    def __init__(self, strict_mode: bool = True):
        self.strict_mode = strict_mode
        
        # Security patterns to check
        self.dangerous_patterns = [
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__\s*\(',
            r'subprocess\.',
            r'os\.system',
            r'shell=True',
        ]
        
        # Required files for different package types
        self.required_files = {
            PackageType.FEATURE: ["manifest.json"],
            # IMPROVED: PackageType.BUGFIX: ["manifest.json"],
            PackageType.SECURITY: ["manifest.json", "SECURITY.md"],
            PackageType.LIBRARY: ["manifest.json", "requirements.txt"],
        }
    
    def validate_package(self, package_path: Path) -> Dict[str, Any]:
        """
        Comprehensive package validation.
        
        Args:
            package_path: Path to the update package
            
        Returns:
            Validation results with warnings, errors, and compatibility assessment
        """
        results = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "security_issues": [],
            "compatibility": CompatibilityLevel.INCOMPATIBLE,
            "package_info": None,
            "validation_time": datetime.datetime.now().isoformat()
        }
        
        try:
            logger.info(f"🔍 Validating update package: {package_path}")
            
            # Step 1: Basic structure validation
            structure_valid, structure_issues = self._validate_structure(package_path)
            if not structure_valid:
                results["errors"].extend(structure_issues)
                return results
            
            # Step 2: Load and validate manifest
            manifest = self._load_manifest(package_path)
            if not manifest:
                results["errors"].append("Invalid or missing manifest file")
                return results
            
            results["package_info"] = manifest.metadata
            
            # Step 3: File integrity validation
            integrity_valid, integrity_issues = self._validate_file_integrity(package_path, manifest)
            if not integrity_valid:
                results["errors"].extend(integrity_issues)
                if self.strict_mode:
                    return results
                else:
                    results["warnings"].extend(integrity_issues)
            
            # Step 4: Security scanning
            security_issues = self._scan_security_issues(package_path, manifest)
            results["security_issues"] = security_issues
            
            if security_issues and self.strict_mode:
                results["errors"].append(f"Security issues found: {len(security_issues)} issues")
                return results
            
            # Step 5: Compatibility assessment
            compatibility = self._assess_compatibility(manifest)
            results["compatibility"] = compatibility
            
            # Step 6: Dependency validation
            dependency_issues = self._validate_dependencies(manifest)
            results["warnings"].extend(dependency_issues)
            
            # Overall validation result
            has_errors = bool(results["errors"])
            has_critical_security = any(issue["severity"] == "critical" for issue in security_issues)
            
            results["valid"] = not has_errors and not has_critical_security
            
            logger.info(f"✅ Package validation complete: {'Valid' if results['valid'] else 'Invalid'}")
            
        except Exception as e:
            logger.error(f"💥 Package validation failed: {e}")
            results["errors"].append(f"Validation error: {str(e)}")
        
        return results
    
    def _validate_structure(self, package_path: Path) -> tuple[bool, List[str]]:
        """Validate basic package structure"""
        issues = []
        
        # Check if package exists and is accessible
        if not package_path.exists():
            return False, ["Package path does not exist"]
        
        if not package_path.is_dir():
            return False, ["Package path is not a directory"]
        
        # Check for manifest file
        manifest_path = package_path / "manifest.json"
        if not manifest_path.exists():
            # Try alternate locations
            alt_manifest = package_path / "package.json"
            if not alt_manifest.exists():
                return False, ["No manifest.json or package.json found"]
        
        # Check for basic structure
        has_code_files = any(package_path.rglob("*.py"))
        if not has_code_files:
            issues.append("No Python files found in package")
        
        return True, issues
    
    def _load_manifest(self, package_path: Path) -> Optional[PackageManifest]:
        """Load and parse package manifest"""
        try:
            manifest_path = package_path / "manifest.json"
            if not manifest_path.exists():
                manifest_path = package_path / "package.json"
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert to structured format
            metadata = PackageMetadata(**data.get("metadata", {}))
            
            files = []
            for file_data in data.get("files", []):
                files.append(PackageFile(**file_data))
            
            manifest = PackageManifest(
                metadata=metadata,
                files=files,
                total_size=data.get("total_size", 0),
                file_count=data.get("file_count", len(files)),
                manifest_version=data.get("manifest_version", "1.0")
            )
            
            return manifest
            
        except Exception as e:
            logger.error(f"Error loading manifest: {e}")
            return None
    
    def _validate_file_integrity(self, package_path: Path, manifest: PackageManifest) -> tuple[bool, List[str]]:
        """Validate file integrity using checksums"""
        issues = []
        
        for file_info in manifest.files:
            file_path = package_path / file_info.path
            
            if not file_path.exists():
                issues.append(f"Missing file: {file_info.path}")
                continue
            
            # Check file size
            actual_size = file_path.stat().st_size
            if actual_size != file_info.size:
                issues.append(f"Size mismatch for {file_info.path}: expected {file_info.size}, got {actual_size}")
            
            # Check checksum
            if file_info.checksum:
                actual_checksum = self._calculate_file_checksum(file_path)
                if actual_checksum != file_info.checksum:
                    issues.append(f"Checksum mismatch for {file_info.path}")
        
        return len(issues) == 0, issues
    
    def _scan_security_issues(self, package_path: Path, manifest: PackageManifest) -> List[Dict[str, Any]]:
        """Scan for security issues in package files"""
        security_issues = []
        
        for file_info in manifest.files:
            if not file_info.path.endswith('.py'):
                continue
                
            file_path = package_path / file_info.path
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for pattern in self.dangerous_patterns:
                    import re
                    matches = re.findall(pattern, content)
                    if matches:
                        security_issues.append({
                            "file": file_info.path,
                            "pattern": pattern,
                            "matches": len(matches),
                            "severity": "high" if pattern in ['exec\\s*\\(', 'eval\\s*\\('] else "medium",
                            "description": f"Potentially dangerous pattern found: {pattern}"
                        })
            
            except Exception as e:
                security_issues.append({
                    "file": file_info.path,
                    "error": str(e),
                    "severity": "low",
                    "description": f"Could not scan file for security issues"
                })
        
        return security_issues
    
    def _assess_compatibility(self, manifest: PackageManifest) -> CompatibilityLevel:
        """Assess package compatibility with target system"""
        
        # Check Python version compatibility
        try:
            min_version = semantic_version.Version(manifest.metadata.python_version_min)
            current_version = semantic_version.Version("3.8.0")  # Example current version
            
            if min_version > current_version:
                return CompatibilityLevel.INCOMPATIBLE
        except Exception as e:
            pass
        
        # Check for security package requirements
        if manifest.metadata.package_type == PackageType.SECURITY:
            if not manifest.metadata.requires_approval:
                return CompatibilityLevel.MAJOR_ISSUES
        
        # Check for auto-approvable packages
        if manifest.metadata.auto_approvable and manifest.metadata.security_level == "minimal":
            return CompatibilityLevel.COMPATIBLE
        
        # Default assessment based on package type
        compatibility_map = {
            PackageType.TEMPLATE: CompatibilityLevel.COMPATIBLE,
            # IMPROVED: PackageType.BUGFIX: CompatibilityLevel.MINOR_ISSUES,
            PackageType.FEATURE: CompatibilityLevel.MINOR_ISSUES,
            PackageType.SECURITY: CompatibilityLevel.MAJOR_ISSUES,
            PackageType.LIBRARY: CompatibilityLevel.MAJOR_ISSUES,
        }
        
        return compatibility_map.get(manifest.metadata.package_type, CompatibilityLevel.MINOR_ISSUES)
    
    def _validate_dependencies(self, manifest: PackageManifest) -> List[str]:
        """Validate package dependencies"""
        warnings = []
        
        # Check for common problematic dependencies
        problematic_deps = ['os', 'subprocess', 'eval', 'exec']
        
        for dep in manifest.metadata.dependencies:
            if any(prob in dep.lower() for prob in problematic_deps):
                warnings.append(f"Potentially problematic dependency: {dep}")
        
        # Check for missing version specifications
        for dep in manifest.metadata.dependencies:
            if not any(op in dep for op in ['==', '>=', '<=', '>', '<', '~=']):
                warnings.append(f"Dependency without version specification: {dep}")
        
        return warnings
    
    def _calculate_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum for a file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()


class UpdatePackageBuilder:
    """
    Builds standardized update packages from source directories.
    """
    
    def __init__(self, output_format: str = "directory"):
        self.output_format = output_format  # directory, zip, tar.gz
    
    def build_package(self, source_path: Path, output_path: Path, 
                     metadata: PackageMetadata) -> Path:
        """
        Build an update package from source directory.
        
        Args:
            source_path: Source directory containing files to package
            output_path: Output path for the package
            metadata: Package metadata
            
        Returns:
            Path to the created package
        """
        logger.info(f"📦 Building update package: {metadata.name} v{metadata.version}")
        
        # Create temporary build directory
        with tempfile.TemporaryDirectory(prefix="package_build_") as temp_dir:
            build_dir = Path(temp_dir) / metadata.name
            build_dir.mkdir()
            
            # Copy source files
            self._copy_source_files(source_path, build_dir, metadata)
            
            # Generate file list and checksums
            files = self._generate_file_list(build_dir)
            
            # Create manifest
            manifest = PackageManifest(
                metadata=metadata,
                files=files,
                total_size=sum(f.size for f in files),
                file_count=len(files)
            )
            
            # Write manifest
            self._write_manifest(build_dir, manifest)
            
            # Create final package
            final_package = self._create_final_package(build_dir, output_path)
            
            logger.info(f"✅ Package built successfully: {final_package}")
            return final_package
    
    def _copy_source_files(self, source_path: Path, build_dir: Path, metadata: PackageMetadata):
        """Copy source files to build directory"""
        
        # Copy all Python files
        for py_file in source_path.rglob("*.py"):
            rel_path = py_file.relative_to(source_path)
            target_path = build_dir / rel_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(py_file, target_path)
        
        # Copy additional files if specified
        additional_files = [
            "README.md", "LICENSE", "requirements.txt", 
            "setup.py", "pyproject.toml", "CHANGELOG.md"
        ]
        
        for filename in additional_files:
            source_file = source_path / filename
            if source_file.exists():
                shutil.copy2(source_file, build_dir / filename)
    
    def _generate_file_list(self, build_dir: Path) -> List[PackageFile]:
        """Generate list of files with metadata"""
        files = []
        
        for file_path in build_dir.rglob("*"):
            if file_path.is_file() and file_path.name != "manifest.json":
                rel_path = file_path.relative_to(build_dir)
                
                file_info = PackageFile(
                    path=str(rel_path),
                    size=file_path.stat().st_size,
                    checksum=self._calculate_checksum(file_path),
                    modification_type="new",
                    permissions="644",
                    executable=file_path.suffix in ['.sh', '.bat']
                )
                files.append(file_info)
        
        return files
    
    def _write_manifest(self, build_dir: Path, manifest: PackageManifest):
        """Write package manifest"""
        manifest_path = build_dir / "manifest.json"
        
        manifest_data = {
            "manifest_version": manifest.manifest_version,
            "metadata": {
                "name": manifest.metadata.name,
                "version": manifest.metadata.version,
                "description": manifest.metadata.description,
                "package_type": manifest.metadata.package_type.value,
                "author": manifest.metadata.author,
                "author_email": manifest.metadata.author_email,
                "organization": manifest.metadata.organization,
                "source_url": manifest.metadata.source_url,
                "target_frameworks": manifest.metadata.target_frameworks,
                "python_version_min": manifest.metadata.python_version_min,
                "python_version_max": manifest.metadata.python_version_max,
                "dependencies": manifest.metadata.dependencies,
                "dev_dependencies": manifest.metadata.dev_dependencies,
                "integration_strategy": manifest.metadata.integration_strategy,
                "target_directories": manifest.metadata.target_directories,
                "target_files": manifest.metadata.target_files,
                "security_level": manifest.metadata.security_level,
                "requires_approval": manifest.metadata.requires_approval,
                "auto_approvable": manifest.metadata.auto_approvable,
                "created_at": manifest.metadata.created_at,
                "updated_at": manifest.metadata.updated_at,
                "tags": manifest.metadata.tags,
                "keywords": manifest.metadata.keywords,
                "documentation_url": manifest.metadata.documentation_url,
                "changelog_url": manifest.metadata.changelog_url
            },
            "files": [
                {
                    "path": f.path,
                    "size": f.size,
                    "checksum": f.checksum,
                    "modification_type": f.modification_type,
                    "target_location": f.target_location,
                    "permissions": f.permissions,
                    "executable": f.executable
                }
                for f in manifest.files
            ],
            "total_size": manifest.total_size,
            "file_count": manifest.file_count
        }
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2)
    
    def _create_final_package(self, build_dir: Path, output_path: Path) -> Path:
        """Create final package in specified format"""
        
        if self.output_format == "directory":
            if output_path.exists():
                shutil.rmtree(output_path)
            shutil.copytree(build_dir, output_path)
            return output_path
        
        elif self.output_format == "zip":
            zip_path = output_path.with_suffix('.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in build_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(build_dir)
                        zipf.write(file_path, arcname)
            return zip_path
        
        elif self.output_format == "tar.gz":
            tar_path = output_path.with_suffix('.tar.gz')
            with tarfile.open(tar_path, 'w:gz') as tar:
                tar.add(build_dir, arcname=build_dir.name)
            return tar_path
        
        else:
            raise ValueError(f"Unsupported output format: {self.output_format}")
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()


# Utility functions for package management

def create_package_from_directory(source_dir: str, output_path: str, 
                                package_name: str, version: str, 
                                description: str, author: str, 
                                author_email: str, **kwargs) -> Path:
    """
    Convenience function to create an update package from a directory.
    """
    metadata = PackageMetadata(
        name=package_name,
        version=version,
        description=description,
        package_type=PackageType.FEATURE,
        author=author,
        author_email=author_email,
        **kwargs
    )
    
    builder = UpdatePackageBuilder()
    return builder.build_package(Path(source_dir), Path(output_path), metadata)


def validate_package_directory(package_path: str, strict: bool = True) -> Dict[str, Any]:
    """
    Convenience function to validate an update package.
    """
    validator = UpdatePackageValidator(strict_mode=strict)
    return validator.validate_package(Path(package_path))


def extract_package_metadata(package_path: str) -> Optional[PackageMetadata]:
    """
    Extract metadata from an update package.
    """
    try:
        manifest_path = Path(package_path) / "manifest.json"
        if not manifest_path.exists():
            return None
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return PackageMetadata(**data.get("metadata", {}))
    
    except Exception as e:
        logger.error(f"Error extracting metadata: {e}")
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Package Format Tools")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Build package command
    build_parser = subparsers.add_parser('build', help='Build update package')
    build_parser.add_argument('source', help='Source directory')
    build_parser.add_argument('output', help='Output path')
    build_parser.add_argument('--name', required=True, help='Package name')
    build_parser.add_argument('--version', required=True, help='Package version')
    build_parser.add_argument('--description', required=True, help='Package description')
    build_parser.add_argument('--author', required=True, help='Author name')
    build_parser.add_argument('--email', required=True, help='Author email')
    build_parser.add_argument('--format', choices=['directory', 'zip', 'tar.gz'], 
                             default='directory', help='Output format')
    
    # Validate package command
    validate_parser = subparsers.add_parser('validate', help='Validate update package')
    validate_parser.add_argument('package', help='Package path')
    validate_parser.add_argument('--strict', action='store_true', help='Strict validation mode')
    
    # Extract metadata command
    metadata_parser = subparsers.add_parser('metadata', help='Extract package metadata')
    metadata_parser.add_argument('package', help='Package path')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        try:
            builder = UpdatePackageBuilder(output_format=args.format)
            metadata = PackageMetadata(
                name=args.name,
                version=args.version,
                description=args.description,
                package_type=PackageType.FEATURE,
                author=args.author,
                author_email=args.email
            )
            
            package_path = builder.build_package(
                Path(args.source), Path(args.output), metadata
            )
            logger.info(f"✅ Package built: {package_path}")
            
        except Exception as e:
            logger.info(f"❌ Build failed: {e}")
    
    elif args.command == 'validate':
        try:
            results = validate_package_directory(args.package, args.strict)
            
            logger.info(f"Package validation: {'✅ Valid' if results['valid'] else '❌ Invalid'}")
            logger.info(f"Compatibility: {results['compatibility'].value}")
            
            if results['errors']:
                logger.info(f"\nErrors ({len(results['errors'])}):")
                for error in results['errors']:
                    logger.info(f"  ❌ {error}")
            
            if results['warnings']:
                logger.info(f"\nWarnings ({len(results['warnings'])}):")
                for warning in results['warnings']:
                    logger.info(f"  ⚠️  {warning}")
            
            if results['security_issues']:
                logger.info(f"\nSecurity Issues ({len(results['security_issues'])}):")
                for issue in results['security_issues']:
                    severity_emoji = {"critical": "🚨", "high": "🔴", "medium": "🟡", "low": "🟢"}
                    logger.info(f"  {severity_emoji.get(issue['severity'], '⚠️')} {issue['description']}")
        
        except Exception as e:
            logger.info(f"❌ Validation failed: {e}")
    
    elif args.command == 'metadata':
        try:
            metadata = extract_package_metadata(args.package)
            if metadata:
                logger.info(f"Package: {metadata.name} v{metadata.version}")
                logger.info(f"Type: {metadata.package_type.value}")
                logger.info(f"Author: {metadata.author}")
                logger.info(f"Description: {metadata.description}")
                logger.info(f"Dependencies: {len(metadata.dependencies)}")
                logger.info(f"Security Level: {metadata.security_level}")
            else:
                logger.info("❌ Could not extract metadata")
        
        except Exception as e:
            logger.info(f"❌ Metadata extraction failed: {e}")
    
    else:
        parser.print_help()