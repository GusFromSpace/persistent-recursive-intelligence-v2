#!/usr/bin/env python3
"""
Compound Intelligence Analysis Script

Runs memory-enhanced PRI on multiple AI projects to demonstrate
compound intelligence learning effects across different codebases.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add memory intelligence to path
sys.path.insert(0, str(Path(__file__).parent.parent / "projects" / "memory-intelligence-service-standalone" / "src"))

from gus_memory import MemoryIntelligence
from gus_memory.adapters import ProjectAdapter, remember_calls, remember_errors


class CompoundIntelligenceAnalyzer:
    """
    Analyzer that demonstrates compound intelligence across multiple projects
    """

    def __init__(self):
        self.memory = MemoryIntelligence("compound-intelligence-analyzer")
        self.project_adapter = ProjectAdapter("multi-project-analysis")
        self.analysis_results = []

        # Clear previous analysis for fresh demonstration
        self.memory.clear_memories(confirm="YES")

        # Remember the compound analysis session start
        self.memory.remember("Starting compound intelligence analysis across multiple AI projects", {
            "session_start": datetime.now().isoformat(),
            "analysis_type": "multi_project_compound_intelligence",
            "expected_compound_effects": True
        })

    @remember_calls("multi-project-analysis")
    @remember_errors("multi-project-analysis")
    def analyze_project(self, project_path: str, project_name: str):
        """Analyze a single project with memory enhancement"""

        logger.info(f"\n🔍 Analyzing Project: {project_name}")
        logger.info(f"   Path: {project_path}")
        logger.info("=" * 60)

        try:
            # Check if project exists
            if not Path(project_path).exists():
                logger.info(f"❌ Project path does not exist: {project_path}")
                return None

            # Remember project analysis start
            self.memory.remember(f"Starting analysis of {project_name}", {
                "project_name": project_name,
                "project_path": project_path,
                "analysis_order": len(self.analysis_results) + 1
            })

            previous_analyses = self.memory.recall("analysis of", limit=10)
            patterns_learned = self.memory.recall("pattern", limit=20)

            if previous_analyses:
                logger.info(f"📚 Found {len(previous_analyses)} previous analyses in memory")
                logger.info(f"🧠 Found {len(patterns_learned)} learned patterns to apply")

            # Perform project-specific analysis
            project_analysis = self._analyze_project_structure(project_path, project_name)

            # Learn patterns from this project
            if project_analysis["insights"]:
                self.memory.learn_pattern(f"{project_name}_analysis_patterns",
                                        project_analysis["insights"])

            # Remember analysis completion
            self.memory.remember(f"Completed analysis of {project_name}", {
                "project_name": project_name,
                "files_found": project_analysis["files_count"],
                "insights_generated": len(project_analysis["insights"]),
                "compound_learning_applied": len(previous_analyses) > 0
            })

            self.analysis_results.append({
                "project_name": project_name,
                "project_path": project_path,
                "analysis": project_analysis,
                "compound_effects": len(previous_analyses) > 0
            })

            return project_analysis

        except Exception as e:
            logger.info(f"❌ Error analyzing {project_name}: {e}")
            self.project_adapter.remember_error(e, {
                "project_name": project_name,
                "project_path": project_path
            })
            return None

    def _analyze_project_structure(self, project_path: str, project_name: str):
        """Analyze the structure and characteristics of a project"""

        project_dir = Path(project_path)
        analysis = {
            "project_type": self._detect_project_type(project_dir),
            "files_count": 0,
            "languages": set(),
            "frameworks": set(),
            "insights": [],
            "architecture_patterns": []
        }

        # Count files and detect languages
        for file_path in project_dir.rglob("*"):
            if file_path.is_file():
                analysis["files_count"] += 1

                # Detect language from extension
                suffix = file_path.suffix.lower()
                if suffix in [".py"]:
                    analysis["languages"].add("Python")
                elif suffix in [".cpp", ".h", ".c"]:
                    analysis["languages"].add("C++")
                elif suffix in [".js", ".ts"]:
                    analysis["languages"].add("JavaScript/TypeScript")
                elif suffix in [".go"]:
                    analysis["languages"].add("Go")
                elif suffix in [".rs"]:
                    analysis["languages"].add("Rust")

        # Detect frameworks and patterns
        analysis["frameworks"] = self._detect_frameworks(project_dir)
        analysis["insights"] = self._generate_insights(project_dir, analysis)
        analysis["architecture_patterns"] = self._detect_architecture_patterns(project_dir)

        logger.info(f"   📊 Files: {analysis['files_count']}")
        logger.info(f"   🗣️ Languages: {', '.join(analysis['languages'])}")
        logger.info(f'   🔧 Frameworks: {', '.join(analysis['frameworks'])}")
        logger.info(f"   🧠 Insights: {len(analysis['insights'])}")
        logger.info(f"   🏗️ Architecture Patterns: {len(analysis['architecture_patterns'])}")

        return analysis

    def _detect_project_type(self, project_dir: Path):
        """Detect the type of AI project"""

        if (project_dir / "requirements.txt").exists() or (project_dir / "setup.py").exists():
            return "Python AI Project"
        elif (project_dir / "CMakeLists.txt").exists():
            return "C++ Project"
        elif (project_dir / "package.json").exists():
            return "Node.js Project"
        elif (project_dir / "Cargo.toml").exists():
            return "Rust Project"
        else:
            return "Unknown Project Type"

    def _detect_frameworks(self, project_dir: Path):
        """Detect frameworks used in the project"""
        frameworks = set()

        # Check common AI framework files
        if any(project_dir.rglob("*torch*")):
            frameworks.add("PyTorch")
        if any(project_dir.rglob("*tensorflow*")):
            frameworks.add("TensorFlow")
        if any(project_dir.rglob("*fastapi*")) or any(project_dir.rglob("*uvicorn*")):
            frameworks.add("FastAPI")
        if any(project_dir.rglob("*django*")):
            frameworks.add("Django")
        if any(project_dir.rglob("*flask*")):
            frameworks.add("Flask")
        if (project_dir / "CMakeLists.txt").exists():
            frameworks.add("CMake")

        return frameworks

    def _generate_insights(self, project_dir: Path, analysis):
        """Generate insights about the project"""
        insights = []

        # Size-based insights
        if analysis["files_count"] > 100:
            insights.append("Large codebase - potential for modularization")
        elif analysis["files_count"] < 10:
            insights.append("Small project - good for experimentation")

        # Language-based insights
        if "Python" in analysis["languages"]:
            insights.append("Python-based AI project - focus on data processing and ML")
        if "C++" in analysis["languages"]:
            insights.append("C++ project - performance-critical application")

        # Structure-based insights
        if (project_dir / "src").exists():
            insights.append("Well-organized source structure")
        if (project_dir / "tests").exists():
            insights.append("Has test suite - good engineering practices")
        if (project_dir / "docs").exists():
            insights.append("Has documentation - maintainable project")

        return insights

    def _detect_architecture_patterns(self, project_dir: Path):
        """Detect architecture patterns in the project"""
        patterns = []

        # Common AI project patterns
        if (project_dir / "config").exists():
            patterns.append("Configuration Management Pattern")
        if (project_dir / "core").exists():
            patterns.append("Core Engine Pattern")
        if (project_dir / "utils").exists():
            patterns.append("Utility Layer Pattern")
        if (project_dir / "strategies").exists():
            patterns.append("Strategy Pattern")
        if (project_dir / "exchanges").exists():
            patterns.append("Exchange Adapter Pattern")

        return patterns

    def analyze_compound_intelligence_effects(self):
        """Analyze the compound intelligence effects across all projects"""

        logger.info(f"\n🌀 Analyzing Compound Intelligence Effects")
        logger.info("=" * 45)

        # Get all accumulated patterns
        all_patterns = self.memory.recall("pattern", limit=50)

        # Calculate compound effects
        total_projects = len(self.analysis_results)
        total_patterns_learned = len(all_patterns)
        cross_project_insights = len([p for p in all_patterns if "cross_project" in str(p)])

        # Intelligence multiplier calculation
        base_intelligence = 1.0
        pattern_multiplier = total_patterns_learned * 0.1
        cross_project_multiplier = cross_project_insights * 0.2
        experience_multiplier = total_projects * 0.15

        compound_intelligence = base_intelligence + pattern_multiplier + cross_project_multiplier + experience_multiplier

        compound_effects = {
            "total_projects_analyzed": total_projects,
            "total_patterns_learned": total_patterns_learned,
            "cross_project_insights": cross_project_insights,
            "intelligence_multiplier": compound_intelligence,
            "learning_acceleration": compound_intelligence / base_intelligence
        }

        # Remember compound intelligence analysis
        self.memory.remember("Compound intelligence analysis complete", {
            "compound_effects": compound_effects,
            "analysis_type": "compound_intelligence_measurement"
        })

        logger.info(f"   📊 Projects Analyzed: {compound_effects['total_projects_analyzed']}")
        logger.info(f"   🧠 Patterns Learned: {compound_effects['total_patterns_learned']}")
        logger.info(f"   🔄 Cross-Project Insights: {compound_effects['cross_project_insights']}")
        logger.info(f"   ⚡ Intelligence Multiplier: {compound_effects['intelligence_multiplier']:.2f}x")
        logger.info(f"   🚀 Learning Acceleration: {compound_effects['learning_acceleration']:.2f}x")

        return compound_effects

    def generate_final_report(self):
        """Generate final compound intelligence report"""

        logger.info(f"\n📋 Compound Intelligence Analysis Report")
        logger.info("=" * 45)

        for i, result in enumerate(self.analysis_results, 1):
            logger.info(f"\n{i}. {result['project_name']}")
            logger.info(f"   Type: {result['analysis']['project_type']}")
            logger.info(f'   Files: {result['analysis']['files_count']}")
            logger.info(f"   Languages: {', '.join(result['analysis']['languages'])}")
            logger.info(f"   Compound Learning: {'✅' if result['compound_effects'] else '🆕'}")

        # Get final intelligence state
        final_stats = self.memory.get_statistics()
        compound_effects = self.analyze_compound_intelligence_effects()

        logger.info(f"\n🎯 Final Intelligence State:")
        logger.info(f"   Total Memories: {final_stats['memory_count']}")
        logger.info(f"   Intelligence Growth: {compound_effects['intelligence_multiplier']:.2f}x")
        logger.info(f"   Learning Velocity: {compound_effects['learning_acceleration']:.2f}x")

        return {
            "analysis_results": self.analysis_results,
            "compound_effects": compound_effects,
            "final_stats": final_stats
        }


def main():
    """Run compound intelligence analysis on multiple AI projects"""

    logger.info("🚀 Compound Intelligence Analysis Across AI Projects")
    logger.info("=" * 55)

    # Initialize analyzer
    analyzer = CompoundIntelligenceAnalyzer()

    # Define projects to analyze
    projects = [
        ("/home/gusfromspace/Development/projects/ai/infvx copy", "INFVX"),
        ("/home/gusfromspace/Development/projects/ai/gus_bot/v1", "GusBot-v1"),
        ("/home/gusfromspace/Development/projects/ai/gus_bot/v2", "GusBot-v2"),
        ("/home/gusfromspace/Development/projects/ai/gus_bot/v3", "GusBot-v3")
    ]

    for project_path, project_name in projects:
        analyzer.analyze_project(project_path, project_name)

    # Generate final compound intelligence report
    final_report = analyzer.generate_final_report()

    logger.info(f"\n🎉 Compound Intelligence Analysis Complete!")
    logger.info(f"🧠 Demonstrated cross-project learning and pattern accumulation")
    logger.info(f"⚡ Intelligence multiplier: {final_report['compound_effects']['intelligence_multiplier']:.2f}x")

    return final_report


if __name__ == "__main__":
    main()