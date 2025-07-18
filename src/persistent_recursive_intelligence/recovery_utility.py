#!/usr/bin/env python3
"""
Recovery Utility - Helps recover from destructive changes

This utility helps identify and recover from damage caused by
the AI diagnostic toolkit running on itself.
"""

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

from safety_validator import SafetyValidator


@dataclass
class DamageReport:
    file_path: Path
    destructive_lines: List[Tuple[int, str]]  # (line_number, content)
    backup_available: bool
    recommended_action: str

class RecoveryUtility:
    """Utility to recover from AI toolkit self-damage"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(".")
        self.validator = SafetyValidator()
        self.damage_reports = []

    def find_backup_files(self) -> List[Path]:
        """Find all backup files in the project"""
        return list(self.project_root.glob("**/*.backup"))

    def analyze_destructive_damage(self, file_path: Path) -> DamageReport:
        """Analyze a file for destructive patterns introduced by the toolkit"""
        destructive_lines = []

        try:
            content = file_path.read_text()
            lines = content.split('\n')

            for line_no, line in enumerate(lines, 1):
                # Check for the destructive _result pattern
                if re.match(r"^\s*(\w+)_result\s*=", line):
                    destructive_lines.append((line_no, line.strip()))

                # Check for indentation issues that commonly occur
                if re.match(r"^[a-zA-Z_]\w*\.\w+\(", line):  # Unindented method calls
                    # This might be damage from fixing indentation incorrectly
                    destructive_lines.append((line_no, line.strip()))

        except Exception as e:
            logger.info(f"Error analyzing {file_path}: {e}")

        backup_path = Path(str(file_path) + ".backup")

        return DamageReport(
            file_path=file_path,
            destructive_lines=destructive_lines,
            backup_available=backup_path.exists(),
            recommended_action=self._get_recommended_action(destructive_lines, backup_path.exists())
        )

    def _get_recommended_action(self, destructive_lines: List, has_backup: bool) -> str:
        """Determine recommended recovery action"""
        if not destructive_lines:
            return "No damage detected"

        if len(destructive_lines) > 10:
            return "Severe damage - restore from backup" if has_backup else "Severe damage - manual repair needed"
        elif len(destructive_lines) > 3:
            return "Moderate damage - compare with backup" if has_backup else "Moderate damage - manual review needed"
        else:
            return "Minor damage - selective fixes possible"

    def scan_project_for_damage(self) -> List[DamageReport]:
        """Scan entire project for damage patterns"""
        python_files = list(self.project_root.glob("**/*.py"))
        damage_reports = []

        for py_file in python_files:
            if py_file.name.endswith(".backup"):
                continue

            report = self.analyze_destructive_damage(py_file)
            if report.destructive_lines:
                damage_reports.append(report)

        self.damage_reports = damage_reports
        return damage_reports

    def generate_recovery_plan(self) -> Dict:
        """Generate a comprehensive recovery plan"""
        if not self.damage_reports:
            self.scan_project_for_damage()

        severe_damage = [r for r in self.damage_reports if len(r.destructive_lines) > 10]
        moderate_damage = [r for r in self.damage_reports if 3 < len(r.destructive_lines) <= 10]
        minor_damage = [r for r in self.damage_reports if 1 <= len(r.destructive_lines) <= 3]

        return {
            "summary": {
                "total_damaged_files": len(self.damage_reports),
                "severe_damage": len(severe_damage),
                "moderate_damage": len(moderate_damage),
                "minor_damage": len(minor_damage),
                "backups_available": sum(1 for r in self.damage_reports if r.backup_available)
            },
            "recovery_steps": self._generate_recovery_steps(severe_damage, moderate_damage, minor_damage),
            "damaged_files": {
                "severe": [str(r.file_path) for r in severe_damage],
                "moderate": [str(r.file_path) for r in moderate_damage],
                "minor": [str(r.file_path) for r in minor_damage]
            }
        }

    def _generate_recovery_steps(self, severe, moderate, minor) -> List[str]:
        """Generate step-by-step recovery instructions"""
        steps = []

        if severe:
            steps.append("1. IMMEDIATE: Restore severely damaged files from backups")
            steps.extend([f"   - Restore {r.file_path}" for r in severe if r.backup_available])

        if moderate:
            steps.append("2. Compare moderately damaged files with backups")
            steps.extend([f"   - Review {r.file_path}" for r in moderate])

        if minor:
            steps.append("3. Selectively fix minor damage")
            steps.extend([f"   - Fix {len(r.destructive_lines)} issues in {r.file_path}" for r in minor])

        steps.append("4. Run syntax validation on all recovered files")
        steps.append("5. Test toolkit functionality after recovery")

        return steps

    def restore_file_from_backup(self, file_path: Path) -> bool:
        """Restore a single file from its backup"""
        backup_path = Path(str(file_path) + ".backup")

        if not backup_path.exists():
            logger.info(f"No backup found for {file_path}")
            return False

        try:
            # Create a safety backup of current (damaged) file
            safety_backup = Path(str(file_path) + ".damaged")
            shutil.copy2(file_path, safety_backup)

            # Restore from backup
            shutil.copy2(backup_path, file_path)
            logger.info(f"Restored {file_path} from backup")
            logger.info(f"Damaged version saved as {safety_backup}")
            return True

        except Exception as e:
            logger.info(f"Error restoring {file_path}: {e}")
            return False

    def auto_fix_destructive_patterns(self, file_path: Path) -> int:
        """Automatically fix known destructive patterns in a file"""
        try:
            content = file_path.read_text()
            lines = content.split("\n")
            fixes_applied = 0

            for i, line in enumerate(lines):
                # Fix the _result pattern
                match = re.match(r"^(\s*)(\w+)_result\s*=\s*(.+)$", line)
                if match:
                    indent, var_prefix, actual_call = match.groups()
                    # Replace with just the actual call, properly indented
                    lines[i] = f"{indent}{actual_call}"
                    fixes_applied += 1

            if fixes_applied > 0:
                # Save the fixed content
                file_path.write_text("\n".join(lines))
                logger.info(f"Applied {fixes_applied} automatic fixes to {file_path}")

            return fixes_applied

        except Exception as e:
            logger.info(f"Error auto-fixing {file_path}: {e}")
            return 0

    def create_recovery_report(self) -> str:
        """Create a detailed recovery report"""
        plan = self.generate_recovery_plan()

        report = f"""# AI Diagnostic Toolkit - Damage Recovery Report

## Summary
- Total damaged files: {plan["summary"]["total_damaged_files"]}
- Severe damage: {plan["summary"]["severe_damage"]} files
- Moderate damage: {plan["summary"]["moderate_damage"]} files
- Minor damage: {plan["summary"]["minor_damage"]} files
- Backups available: {plan["summary"]["backups_available"]} files

## Damaged Files by Severity

### Severe Damage (10+ issues per file)
"""

        for file_path in plan["damaged_files"]["severe"]:
            report += f"- {file_path}\n"

        report += "\n### Moderate Damage (3-10 issues per file)\n"
        for file_path in plan["damaged_files"]["moderate"]:
            report += f"- {file_path}\n"

        report += "\n### Minor Damage (1-3 issues per file)\n"
        for file_path in plan["damaged_files"]["minor"]:
            report += f"- {file_path}\n"

        report += "\n## Recovery Steps\n"
        for step in plan["recovery_steps"]:
            report += f"{step}\n"

        return report

def main():
    """Main recovery utility interface"""
    recovery = RecoveryUtility()

    logger.info("AI Diagnostic Toolkit - Recovery Utility")
    logger.info("=" * 50)

    # Scan for damage
    logger.info("Scanning project for damage...")
    damage_reports = recovery.scan_project_for_damage()

    if not damage_reports:
        logger.info("✅ No damage detected in project!")
        return

    # Generate and display recovery plan
    plan = recovery.generate_recovery_plan()

    logger.info(f"\n📊 Damage Summary:")
    logger.info(f"   Total damaged files: {plan['summary']['total_damaged_files']}")
    logger.info(f"   Severe damage: {plan['summary']['severe_damage']}")
    logger.info(f"   Moderate damage: {plan['summary']['moderate_damage']}")
    logger.info(f"   Minor damage: {plan['summary']['minor_damage']}")
    logger.info(f"   Backups available: {plan['summary']['backups_available']}")

    logger.info(f'\n🔧 Recovery Steps:')
    for step in plan['recovery_steps']:
        logger.info(f"   {step}")

    # Offer to generate detailed report
    response = input("\nGenerate detailed recovery report? (y/n): ")
    if response.lower() == "y":
        report = recovery.create_recovery_report()
        report_path = Path("RECOVERY_REPORT.md")
        report_path.write_text(report)
        logger.info(f"📋 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    main()