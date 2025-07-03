#!/usr/bin/env python3
"""
Mesopredator Educational Injection System

Transforms every bug fix into a learning opportunity through intelligent
annotation injection that prevents future occurrences of the same patterns.

This embodies the mesopredator field shaping principle - create an environment
where good practices naturally emerge through knowledge transfer.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class AnnotationStyle(Enum):
    """Different styles of educational annotations"""
    STANDARD = "standard"
    CONCISE = "concise"
    COMPREHENSIVE = "comprehensive"


class CognitivePrinciple(Enum):
    """Mesopredator cognitive principles for learning"""


@dataclass
class FixContext:
    """Context information about a code fix"""
    fix_type: str                # Type of fix applied
    pattern_name: str           # Name of the pattern fixed
    severity: str               # critical, high, medium, low
    category: str               # security, performance, maintainability, etc.
    language: str               # Programming language
    line_number: int            # Where the fix was applied
    old_code: str              # Original problematic code
    new_code: str              # Fixed code
    cognitive_aspect: str       # Which mesopredator principle applies
    ai_generated: bool         # Whether this was likely AI-generated code
    complexity: str            # simple, medium, complex


@dataclass
class EducationalAnnotation:
    """Complete educational annotation for a code fix"""
    fix_explanation: str        # Why this change was needed
    prevention_strategies: List[str]  # How to avoid this in future
    standards_reference: str    # Link to coding standards
    cognitive_insight: str      # Mesopredator principle lesson
    memory_aid: str            # Easy-to-remember tip
    examples: Optional[str]     # Code examples if needed
    next_steps: List[str]      # Actionable follow-up items


class MesopredatorEducationalInjector:
    """
    Core educational injection system for Mesopredator

    Implements field shaping through intelligent learning annotation injection
    """

    def __init__(self, standards_path: str = "/home/gusfromspace/Development/Standards"):
        self.standards_path = Path(standards_path)
        self.pattern_database = self._load_pattern_database()
        self.cognitive_mappings = self._load_cognitive_mappings()

    def inject_learning_annotation(self, fix_context: FixContext, style: AnnotationStyle = AnnotationStyle.STANDARD) -> str:
        """
        Generate educational annotation for a specific fix

        Applies strategic patience - not every fix needs comprehensive annotation
        """
        annotation = self._create_annotation(fix_context)
        return self._format_annotation(annotation, fix_context.language, style)

    def should_inject_annotation(self, fix_context: FixContext, file_context: Dict) -> bool:
        """
        Strategic decision: when to inject educational content

        Embodies executive function - calculate value vs overhead
        """
        # Always annotate security critical fixes
        if fix_context.severity == "critical" and fix_context.category == "security":
            return True

        # Annotate common AI mistakes for learning
        if fix_context.ai_generated and fix_context.pattern_name in self._get_common_ai_patterns():
            return True

        # Annotate complex patterns that are hard to understand
        if fix_context.complexity == "complex":
            return True

        # Apply strategic patience - don"t over-annotate simple files
        if file_context.get("line_count", 0) < 100 and fix_context.complexity == "simple":
            return False

        # Default to annotation for learning value
        return True

    def _create_annotation(self, fix_context: FixContext) -> EducationalAnnotation:
        """Create comprehensive educational annotation"""

        pattern_info = self.pattern_database.get(fix_context.pattern_name, {})

        return EducationalAnnotation(
            fix_explanation=self._explain_fix(fix_context, pattern_info),
            prevention_strategies=self._create_prevention_strategies(fix_context, pattern_info),
            standards_reference=self._link_to_standards(fix_context),
            cognitive_insight=self._extract_cognitive_lesson(fix_context),
            memory_aid=self._create_memory_aid(fix_context, pattern_info),
            examples=self._generate_examples(fix_context) if fix_context.complexity != "simple" else None,
            next_steps=self._suggest_next_steps(fix_context)
        )

    def _explain_fix(self, fix_context: FixContext, pattern_info: Dict) -> str:
        """Explain why this change was necessary"""

        explanations = {
            "security_vulnerability": f"""
SECURITY FIX: {pattern_info.get("vulnerability_type", "Security issue")} resolved

THE PROBLEM:
{fix_context.old_code}

This code pattern creates security risks because:
{pattern_info.get("security_explanation", "it allows potential exploitation")}

THE SOLUTION:
{fix_context.new_code}

This fix prevents the vulnerability by:
{pattern_info.get("fix_explanation", "implementing secure alternatives")}
""",

            "performance_issue": f"""
PERFORMANCE FIX: {pattern_info.get("performance_type", "Performance optimization")} applied

THE BOTTLENECK:
{fix_context.old_code}

This pattern causes performance problems because:
{pattern_info.get("performance_explanation", "it uses inefficient algorithms or data structures")}

THE OPTIMIZATION:
{fix_context.new_code}

This improvement enhances performance by:
{pattern_info.get("optimization_explanation", "using more efficient approaches")}
""",

            "maintainability_problem": f"""
MAINTAINABILITY FIX: {pattern_info.get("maintainability_type", "Code clarity improvement")}

THE ISSUE:
{fix_context.old_code}

This pattern makes code hard to maintain because:
{pattern_info.get("maintainability_explanation", "it obscures intent and increases complexity")}

THE IMPROVEMENT:
{fix_context.new_code}

This change improves maintainability by:
{pattern_info.get("improvement_explanation", "making the code clearer and more predictable")}
""",

            "ai_common_mistake": f"""
AI PATTERN FIX: {pattern_info.get("ai_mistake_type", "Common AI-generated antipattern")} corrected

THE AI MISTAKE:
{fix_context.old_code}

AI tools commonly generate this antipattern because:
{pattern_info.get("ai_explanation", "they lack project context and best practices knowledge")}

THE CORRECTED PATTERN:
{fix_context.new_code}

This follows best practices by:
{pattern_info.get("best_practice_explanation", "adhering to established patterns and conventions")}
"""
        }

        return explanations.get(fix_context.category, f"Code improvement: {fix_context.pattern_name}")

    def _create_prevention_strategies(self, fix_context: FixContext, pattern_info: Dict) -> List[str]:
        """Generate actionable prevention strategies"""

        base_strategies = pattern_info.get("prevention_strategies", [])

        # Add language-specific strategies
        language_strategies = {
            "python": {
                "security_vulnerability": [
                    "Use ast.literal_eval() instead of eval()",
                    "Validate all user inputs with strong typing",
                    "Use parameterized queries for database access",
                    "Avoid subprocess with shell=True"
                ],
                "performance_issue": [
                    "Use list comprehensions for simple transformations",
                    "Choose appropriate data structures (set vs list for lookups)",
                    "Profile code before optimizing",
                    "Use generators for large datasets"
                ]
            },
            "cpp": {
                "security_vulnerability": [
                    "Use smart pointers to prevent memory leaks",
                    "Validate input bounds before array access",
                    "Use const correctness throughout",
                    "Avoid C-style strings in favor of std::string"
                ],
                "performance_issue": [
                    "Use references to avoid unnecessary copying",
                    "Reserve vector capacity when size is known",
                    "Use const& for function parameters",
                    "Profile with tools like perf or gprof"
                ]
            }
        }

        strategies = base_strategies.copy()
        lang_specific = language_strategies.get(fix_context.language, {}).get(fix_context.category, [])
        strategies.extend(lang_specific)

        return [f"✅ {strategy}" for strategy in strategies]

    def _link_to_standards(self, fix_context: FixContext) -> str:
        """Reference relevant coding standards"""

        standards_map = {
            "security": f"{self.standards_path}/PROJECT_STANDARDS.md#security--reliability",
            "performance": f"{self.standards_path}/PROJECT_STANDARDS.md#metrics--monitoring",
            "architecture": f"{self.standards_path}/PROJECT_STANDARDS.md#architecture-standards",
            "maintainability": f"{self.standards_path}/PROJECT_STANDARDS.md#code-standards",
            "ai_common_mistake": f"{self.standards_path}/The Mesopredator Design Philosophy.md"
        }

        base_reference = standards_map.get(fix_context.category, f"{self.standards_path}/PROJECT_STANDARDS.md")

        return f"""
STANDARDS REFERENCE:
See: {base_reference}
Principle: "{self._get_relevant_principle(fix_context)}"

For comprehensive guidelines, review:
{self.standards_path}/PROJECT_STANDARDS.md
"""

    def _extract_cognitive_lesson(self, fix_context: FixContext) -> str:
        """Connect fix to mesopredator cognitive principles"""

        cognitive_lessons = {
            "security_vulnerability": """
MESOPREDATOR HUNTED MODE INSIGHT:
This fix demonstrates threat awareness - the ability to recognize
potential vulnerabilities before they become actual attacks.

COGNITIVE PATTERN: Always scan for dangerous functions and patterns:
• eval(), exec(), subprocess with shell=True (Python)
• Direct memory access, C-style strings (C++)
• User input without validation (All languages)

DUAL AWARENESS TIP:
When you see user input, simultaneously think:
🎯 HUNTER: "What opportunities does this enable?"
🛡️ HUNTED: "What threats does this introduce?"
""",

            "performance_issue": """
MESOPREDATOR HUNTER MODE INSIGHT:
This fix demonstrates opportunity recognition - identifying
optimization potential that improves system efficiency.

COGNITIVE PATTERN: Look for efficiency multipliers:
• O(n²) algorithms that could be O(n log n)
• Repeated computations that could be cached
• Data structures optimized for access patterns

STRATEGIC PATIENCE LESSON:
Not all optimizations are worth immediate action.
Profile first, optimize bottlenecks, measure impact.
""",

            "ai_common_mistake": """
MESOPREDATOR FIELD SHAPING INSIGHT:
This fix demonstrates environment modification - creating
conditions where good patterns naturally emerge.

COGNITIVE PATTERN: AI tools make predictable mistakes:
• Lack of project context (relative imports, architecture)
• Missing edge case handling (error conditions, input validation)
• Pattern repetition without abstraction

PREVENTION STRATEGY:
Create templates and examples that guide AI toward better patterns.
Feed AI tools with project-specific context and standards.
""",

            "maintainability_problem": """
MESOPREDATOR EXECUTIVE FUNCTION INSIGHT:
This fix demonstrates strategic decision-making - choosing
maintainability over short-term convenience.

COGNITIVE PATTERN: Think long-term when writing code:
• Will this be clear to someone in 6 months?
• Does this follow the principle of least surprise?
• Can this be easily modified or extended?

TEMPORAL PATIENCE LESSON:
Taking time to write clear code saves more time later
in debugging, modification, and team collaboration.
"""
        }

        return cognitive_lessons.get(fix_context.category, f"""
MESOPREDATOR COGNITIVE INSIGHT:
This fix embodies {fix_context.cognitive_aspect} - demonstrating
the value of systematic code improvement and learning.
""")

    def _create_memory_aid(self, fix_context: FixContext, pattern_info: Dict) -> str:
        """Create memorable tip for the pattern"""

        memory_aids = {
            "eval_usage": "MEMORY AID: \"eval() = evil() - never trust user input with code execution\"",
            "mutable_defaults": "MEMORY AID: \"Mutable defaults = Shared surprises\"",
            "relative_imports": "MEMORY AID: \"Relative paths break when files move - anchor to project root\"",
            "command_injection": "MEMORY AID: \"Shell=True, Security=False\"",
            "sql_injection": "MEMORY AID: \"Concatenated queries = Hacker's playground\"",
            "buffer_overflow": "MEMORY AID: \"Check bounds before you bound into trouble\"",
            "memory_leak": "MEMORY AID: \"Every new needs a delete, every malloc needs a free\"",
            "performance_o2": "MEMORY AID: \"Nested loops = Performance swoops (downward)\"",
            "string_concat_loop": "MEMORY AID: \"String concat in loops = Performance poops\""
        }

        return pattern_info.get("memory_aid",
                               memory_aids.get(fix_context.pattern_name,
                                             f"MEMORY AID: \"Good patterns prevent {fix_context.category} problems\""))

    def _generate_examples(self, fix_context: FixContext) -> str:
        """Generate helpful code examples"""

        if fix_context.complexity == "simple":
            return None

        # For complex patterns, provide additional examples
        examples_template = f"""
ADDITIONAL EXAMPLES:

❌ Other ways this pattern commonly appears:
{self._get_antipattern_variations(fix_context)}

✅ Recommended alternatives:
{self._get_good_pattern_examples(fix_context)}

🧪 Test your understanding:
{self._create_practice_scenario(fix_context)}
"""
        return examples_template

    def _suggest_next_steps(self, fix_context: FixContext) -> List[str]:
        """Suggest actionable follow-up items"""

        base_steps = [
            "Review similar code patterns in this project",
            "Update team coding guidelines if needed",
            "Share this pattern in next code review"
        ]

        if fix_context.severity == "critical":
            base_steps.insert(0, "Audit entire codebase for similar vulnerabilities")

        if fix_context.ai_generated:
            base_steps.append("Update AI prompts/templates to prevent this pattern")

        return base_steps

    def _format_annotation(self, annotation: EducationalAnnotation, language: str, style: AnnotationStyle) -> str:
        """Format annotation according to language and style"""

        comment_styles = {
            "python": {"start": "# ", "block_start": """"", "block_end": """""},
            "cpp": {"start": "// ", "block_start": "/*", "block_end": "*/"},
            "javascript": {"start": "// ", "block_start": "/*", "block_end": "*/"},
            "rust": {"start": "// ", "block_start": "/*", "block_end": "*/"}
        }

        style_config = comment_styles.get(language, comment_styles["python"])

        if style == AnnotationStyle.CONCISE:
            return self._format_concise_annotation(annotation, style_config)
        elif style == AnnotationStyle.COMPREHENSIVE:
            return self._format_comprehensive_annotation(annotation, style_config)
        else:
            return self._format_standard_annotation(annotation, style_config)

    def _format_standard_annotation(self, annotation: EducationalAnnotation, style_config: Dict) -> str:
        """Format standard educational annotation"""

        start = style_config["start"]

        formatted = f"""
{start}🦾 MESOPREDATOR LEARNING ANNOTATION 🦾
{start}
{self._indent_text(annotation.fix_explanation, start)}
{start}
{start}PREVENTION STRATEGY:
{self._format_list_items(annotation.prevention_strategies, start)}
{start}
{annotation.standards_reference}
{start}
{self._indent_text(annotation.cognitive_insight, start)}
{start}
{annotation.memory_aid}
"""

        if annotation.next_steps:
            formatted += f"""
{start}
{start}🎯 NEXT STEPS:
{self._format_checklist_items(annotation.next_steps, start)}
"""

        return formatted.strip()

    def _format_concise_annotation(self, annotation: EducationalAnnotation, style_config: Dict) -> str:
        """Format concise annotation for simple fixes"""

        start = style_config["start"]

        return f"""
{start}🦾 MESOPREDATOR FIX: {annotation.fix_explanation.split(":")[1].split('\\n')[0].strip()}
{start}PREVENTION: {annotation.prevention_strategies[0].replace("✅ ", "")}
{start}{annotation.memory_aid}
""".strip()

    def _format_comprehensive_annotation(self, annotation: EducationalAnnotation, style_config: Dict) -> str:
        """Format comprehensive annotation for critical fixes"""

        start = style_config["start"]

        formatted = self._format_standard_annotation(annotation, style_config)

        if annotation.examples:
            formatted += f"""
{start}
{self._indent_text(annotation.examples, start)}
"""

        return formatted

    def _indent_text(self, text: str, prefix: str) -> str:
        """Indent multi-line text with comment prefix"""
        return "\n".join(f"{prefix}{line}" for line in text.split("\n"))

    def _format_list_items(self, items: List[str], prefix: str) -> str:
        """Format list items with comment prefix"""
        return "\n".join(f"{prefix}{item}" for item in items)

    def _format_checklist_items(self, items: List[str], prefix: str) -> str:
        """Format checklist items with comment prefix"""
        return "\n".join(f"{prefix}[ ] {item}" for item in items)

    # Helper methods for pattern database and mappings

    def _load_pattern_database(self) -> Dict:
        """Load pattern information database"""
        # This would load from a JSON file in production
        return {
            "eval_usage": {
                "vulnerability_type": "Arbitrary Code Execution",
                "security_explanation": "eval() executes any Python code from user input",
                "prevention_strategies": ["Use ast.literal_eval() for safe evaluation", "Create explicit parsing functions"],
                "memory_aid": "eval() = evil() - never trust user input with code execution"
            },
            "mutable_defaults": {
                "maintainability_type": "Shared State Bug",
                "maintainability_explanation": "Mutable defaults are shared between function calls",
                "prevention_strategies": ["Use None and create new objects inside function", "Use dataclasses with field(default_factory=...)"],
                "memory_aid": "Mutable defaults = Shared surprises"
            },
            # Add more patterns as needed
        }

    def _load_cognitive_mappings(self) -> Dict:
        """Load mappings between fix types and cognitive principles"""
        return {
            "security_vulnerability": CognitivePrinciple.HUNTED_MODE,
            "performance_issue": CognitivePrinciple.HUNTER_MODE,
            "ai_common_mistake": CognitivePrinciple.FIELD_SHAPING,
            "maintainability_problem": CognitivePrinciple.EXECUTIVE_FUNCTION
        }

    def _get_common_ai_patterns(self) -> List[str]:
        """Get list of common AI-generated antipatterns"""
        return ["eval_usage", "mutable_defaults", "relative_imports", "command_injection", "bare_except"]

    def _get_relevant_principle(self, fix_context: FixContext) -> str:
        """Get relevant coding principle for the fix"""
        principles = {
            "security": "Zero Trust - Verify everything, trust nothing",
            "performance": "Measure First, Optimize Second",
            "maintainability": "Explicit is better than implicit",
            "architecture": "Clear boundaries prevent confusion"
        }
        return principles.get(fix_context.category, "Code quality over quick fixes")

    def _get_antipattern_variations(self, fix_context: FixContext) -> str:
        """Get variations of the antipattern"""
        return "// Additional antipattern examples would be generated here"

    def _get_good_pattern_examples(self, fix_context: FixContext) -> str:
        """Get good pattern examples"""
        return "// Good pattern examples would be generated here"

    def _create_practice_scenario(self, fix_context: FixContext) -> str:
        """Create practice scenario for learning"""
        return "// Practice scenario would be generated here"


# Usage example integration point
def create_educational_fix_context(pattern_name: str, old_code: str, new_code: str, **kwargs) -> FixContext:
    """Helper function to create FixContext for educational injection"""
    return FixContext(
        fix_type=kwargs.get("fix_type", "pattern_fix"),
        pattern_name=pattern_name,
        severity=kwargs.get("severity", "medium"),
        category=kwargs.get("category", "maintainability_problem"),
        language=kwargs.get("language", "python"),
        line_number=kwargs.get("line_number", 1),
        old_code=old_code,
        new_code=new_code,
        cognitive_aspect=kwargs.get("cognitive_aspect", "executive_function"),
        ai_generated=kwargs.get("ai_generated", False),
        complexity=kwargs.get("complexity", "medium")
    )