#!/usr/bin/env python3
"""
Mesopredator Educational Injection System - Working Demo

This demonstrates how the educational injection system transforms ordinary
bug fixes into learning opportunities, embodying the field shaping principle.
"""

import tempfile
import logging
from pathlib import Path
from educational_injector import (
    MesopredatorEducationalInjector,
    create_educational_fix_context,
    AnnotationStyle
)
from safe_workflow_manager import SafeWorkflowManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def demo_security_fix_injection():
    """Demonstrate educational injection for a security vulnerability fix"""

    logging.info("🦾 MESOPREDATOR EDUCATIONAL INJECTION DEMO")
    logging.info("=" * 60)
    logging.info("🛡️ SECURITY FIX DEMONSTRATION")

    # Original problematic code
    original_code = """def process_user_command(user_input):
    '''Process user command - UNSAFE VERSION'''
    import subprocess
    result = subprocess.run(["ls", user_input], shell=False, capture_output=True, text=True)
    return result.stdout"""

    # Fixed code
    fixed_code = """def process_user_command(user_input):
    '''Process user command - SECURE VERSION'''
    import shlex

    # Validate input contains only alphanumeric and safe characters
    if not user_input.replace("_", "").replace("-", "").replace(".", "").isalnum():
        raise ValueError("Invalid input: only alphanumeric characters, underscore, hyphen, and dot allowed")

    result = subprocess.run(["ls", user_input], capture_output=True, text=True)
    return result.stdout"""

    # Create educational injection
    injector = MesopredatorEducationalInjector()

    fix_context = create_educational_fix_context(
        pattern_name="command_injection",
        old_code=original_code,
        new_code=fixed_code,
        language="python",
        severity="critical",
        category="security_vulnerability",
        ai_generated=True,
        complexity="complex"
    )

    # Generate educational annotation
    annotation = injector.inject_learning_annotation(fix_context, AnnotationStyle.COMPREHENSIVE)

    logger.info("BEFORE (Problematic Code):")
    logger.info("-" * 30)
    logger.info(original_code)
    logger.info()

    logger.info("AFTER (With Educational Annotation):")
    logger.info("-" * 30)
    logger.info(annotation)
    logger.info()
    logger.info(fixed_code)
    logger.info()

    return annotation

def demo_ai_pattern_fix_injection():
    """Demonstrate educational injection for common AI mistake"""

    logger.info("🤖 AI PATTERN FIX DEMONSTRATION")
    logger.info("-" * 40)

    # AI-generated antipattern
    ai_mistake = '''def process_items(items=[]):
    """Process list of items - AI COMMON MISTAKE"""
    items.append("processed")
    return items'''

    # Corrected pattern
    corrected_code = '''def process_items(items=None):
    """Process list of items - CORRECTED PATTERN"""
    if items is None:
        items = []
    items.append("processed")
    return items'''

    injector = MesopredatorEducationalInjector()

    fix_context = create_educational_fix_context(
        pattern_name="mutable_defaults",
        old_code=ai_mistake,
        new_code=corrected_code,
        language="python",
        severity="medium",
        category="ai_common_mistake",
        ai_generated=True,
        complexity="medium"
    )

    annotation = injector.inject_learning_annotation(fix_context, AnnotationStyle.STANDARD)

    logger.info("AI-GENERATED MISTAKE:")
    logger.info(ai_mistake)
    logger.info()
    logger.info("MESOPREDATOR EDUCATIONAL FIX:")
    logger.info(annotation)
    logger.info()
    logger.info(corrected_code)
    logger.info()

def demo_performance_optimization_injection():
    """Demonstrate educational injection for performance improvement"""

    logger.info("⚡ PERFORMANCE OPTIMIZATION DEMONSTRATION")
    logger.info("-" * 45)

    # Inefficient code
    slow_code = '''def find_duplicates(items):
    """Find duplicate items - SLOW VERSION"""
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates'''

    # Optimized code
    fast_code = '''def find_duplicates(items):
    """Find duplicate items - OPTIMIZED VERSION"""
    seen = set()
    duplicates = set()

    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return list(duplicates)'''

    injector = MesopredatorEducationalInjector()

    fix_context = create_educational_fix_context(
        pattern_name="performance_o2",
        old_code=slow_code,
        new_code=fast_code,
        language="python",
        severity="medium",
        category="performance_issue",
        ai_generated=False,
        complexity="complex"
    )

    annotation = injector.inject_learning_annotation(fix_context, AnnotationStyle.DETAILED)

    logger.info("SLOW ALGORITHM (O(n²)):")
    logger.info(slow_code)
    logger.info()
    logger.info("MESOPREDATOR HUNTER MODE OPTIMIZATION:")
    logger.info(annotation)
    logger.info()
    logger.info(fast_code)
    logger.info()

def demo_safe_workflow_integration():
    """Demonstrate integration with SafeWorkflowManager"""

    logger.info("🔧 SAFE WORKFLOW INTEGRATION DEMONSTRATION")
    logger.info("-" * 50)

    # Create temporary test file
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test_code.py"

        # Write problematic code
        problematic_code = """import subprocess

def execute_command(cmd):
    return subprocess.run(shlex.split(cmd), shell=False)  # Security fixed
"""

        test_file.write_text(problematic_code)

        # Create safe workflow manager with educational injection enabled
        workflow = SafeWorkflowManager(
            source_directory=Path(temp_dir),
            enable_educational_injection=True,
            interactive=False
        )

        # Demonstrate educational fix application
        old_code = "subprocess.run(cmd, shell=True)"
        new_code = "subprocess.run(shlex.split(cmd), shell=False)"

        enhanced_code = workflow.apply_educational_fix(
            file_path=test_file,
            pattern_name="command_injection",
            old_code=old_code,
            new_code=new_code,
            fix_context={
                "severity": "critical",
                "category": "security_vulnerability"
            }
        )

        logger.info("ENHANCED CODE WITH EDUCATIONAL ANNOTATION:")
        logger.info(enhanced_code)
        logger.info()

        # Generate learning report
        learning_report = workflow.generate_learning_report()
        logger.info("LEARNING EFFECTIVENESS REPORT:")
        logger.info(f"📊 Educational annotations injected: {learning_report['educational_annotations']}")
        logger.info(f"🎯 Patterns addressed: {learning_report['patterns_addressed']}")
        logger.info(f"📁 Files enhanced: {learning_report['files_enhanced']}")
        logger.info(f"🌊 Field shaping metrics: {learning_report['field_shaping_metrics']}")

def main():
    """Run all educational injection demonstrations"""

    logger.info("🦾 MESOPREDATOR EDUCATIONAL INJECTION SYSTEM")
    logger.info("🎯 Transforming Bug Fixes into Learning Opportunities")
    logger.info("=" * 70)
    logger.info()

    # Run demonstrations
    demo_security_fix_injection()
    demo_ai_pattern_fix_injection()
    demo_performance_optimization_injection()
    demo_safe_workflow_integration()

    logger.info("🎊 FIELD SHAPING COMPLETE!")
    logger.info("=" * 70)
    logger.info("Every fix becomes a learning opportunity.")
    logger.info("Every mistake becomes prevention knowledge.")
    logger.info("Every pattern becomes team wisdom.")
    logger.info()
    logger.info("🧠 Mesopredator cognitive development accelerated! 🚀")

if __name__ == "__main__":
    main()