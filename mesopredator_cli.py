import argparse
import json
import shutil
import sys
import logging
from datetime import datetime

from pathlib import Path

# Set up logger for the CLI
logger = logging.getLogger(__name__)

# Add the src directory to the path to allow for module imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from cognitive.persistent_recursion import run_analysis
from cognitive.interactive_approval import (
    InteractiveApprovalSystem, FixProposal, FixSeverity, ApprovalDecision
)
from cognitive.enhanced_patterns.memory_enhanced_false_positive_detector import MemoryEnhancedFalsePositiveDetector
from cognitive.enhanced_patterns.context_analyzer import ContextAnalyzer
from cognitive.enhanced_patterns.memory_pruning_system import MemoryPruningSystem, PruningStrategy
from cognitive.enhanced_patterns.improvement_cycle_tracker import ImprovementCycleTracker
from cognitive.memory.memory.engine import MemoryEngine

def run_fixer(project_path: str, issues_file: str, dynamic_approval: bool = False, conservative_level: float = 0.95):
    """Interactively fixes issues in a project."""
    print(f"🌀 Enhanced PRI: Interactive Fix Application")
    print(f"📁 Project: {project_path}")
    print(f"🎯 Mode: {'Dynamic Approval' if dynamic_approval else 'Automatic'}")
    print(f"🛡️  Auto-approve safe fixes: Yes")
    if dynamic_approval:
        print(f"⚖️  Conservative level: {conservative_level}")

    try:
        with open(issues_file, 'r') as f:
            issues = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading issues file: {e}")
        return

    # If dynamic approval, filter proposals by safety score
    fix_proposals = convert_issues_to_proposals(issues)
    
    if dynamic_approval:
        # Filter based on STRICT conservative level
        original_count = len(fix_proposals)
        # Ensure conservative level is never below 0.9 for dynamic approval
        strict_conservative_level = max(conservative_level, 0.9)
        fix_proposals = [p for p in fix_proposals if calculate_fix_safety_score(p) >= strict_conservative_level]
        print(f"\n📊 STRICT Dynamic Approval: {len(fix_proposals)}/{original_count} fixes meet safety threshold (≥{strict_conservative_level:.1f})")
        if len(fix_proposals) < original_count:
            print(f"🛡️  SAFETY: {original_count - len(fix_proposals)} potentially risky fixes filtered out")
    
    approval_system = InteractiveApprovalSystem(auto_approve_safe=True, interactive_mode=False)
    approved_fixes, rejected_fixes = approval_system.process_fix_batch(fix_proposals)

    if approved_fixes:
        print("\n🔧 Applying approved fixes...")
        applied_count = 0
        for fix in approved_fixes:
            if apply_fix(project_path, fix):
                applied_count += 1
        print(f"✅ Fix application complete: {applied_count} fixes applied")
    else:
        print("\nNo fixes were approved.")

def calculate_fix_safety_score(proposal):
    """Calculate a STRICT safety score for a fix proposal."""
    score = 0.1  # MUCH lower base score - assume unsafe until proven otherwise
    
    # STRICT issue type safety categorization
    ultra_safe_types = {'whitespace_cleanup', 'typo_corrections'}  # Only truly cosmetic
    risky_types = {
        'security', 'performance', 'logic', 'syntax_errors', 'exception_handling',
        'missing_imports', 'string_formatting', 'algorithm_changes', 'api_modifications',
        'database_queries', 'concurrency_fixes', 'memory_management'
    }
    
    if proposal.issue_type in ultra_safe_types:
        score += 0.4  # Still conservative
    elif proposal.issue_type in risky_types:
        score -= 0.1  # Penalize risky types more heavily
        return 0.0    # Immediately fail risky types
    
    # STRICT code change analysis
    if proposal.original_code and proposal.proposed_fix:
        # Any structural changes are dangerous
        orig_lines = proposal.original_code.count('\n')
        new_lines = proposal.proposed_fix.count('\n')
        
        if orig_lines != new_lines:
            score -= 0.3  # Line count changes are risky
        
        # Any significant size changes are dangerous
        size_ratio = len(proposal.proposed_fix) / max(len(proposal.original_code), 1)
        if size_ratio > 1.2 or size_ratio < 0.8:  # More than 20% change
            score -= 0.2
        
        # Check for dangerous patterns in the fix - COMPREHENSIVE LIST
        dangerous_code_patterns = [
            'import ', 'def ', 'class ', 'try:', 'except:', 'with ', 'for ', 'while ', 'if ',
            'subprocess', 'os.system', 'eval(', 'exec(', '__import__', 'getattr(',
            'setattr(', 'delattr(', 'globals()', 'locals()', 'vars()', 'dir(',
            'open(', 'file(', 'input()', 'raw_input()', 'compile(', 'memoryview(',
            'user.role =', '.role =', 'admin', 'root', 'password', 'auth',
            'return True', 'return False', '== True', '== False',
            'http://', 'https://', 'ftp://', 'requests.', 'urllib.',
            'rm -rf', 'del ', 'shutil.', 'pathlib.', 'pickle.',
            'yaml.load', 'marshal.', 'shelve.', 'dill.', 'joblib.'
        ]
        
        dangerous_found = [pattern for pattern in dangerous_code_patterns 
                          if pattern in proposal.proposed_fix]
        
        if dangerous_found:
            score = 0.0  # Immediate fail for any dangerous pattern
            # Log what was detected for security audit
            print(f"🚨 SECURITY: Dangerous patterns detected in fix: {dangerous_found}")
        
        # Additional check for assignment/modification patterns
        modification_patterns = [' = ', '+=', '-=', '*=', '/=', '|=', '&=', '^=']
        if any(pattern in proposal.proposed_fix for pattern in modification_patterns):
            # Any assignments in fixes are very risky
            score = min(score, 0.1)
    
    # STRICT context penalties
    if hasattr(proposal, 'context'):
        if proposal.context == 'production':
            score -= 0.2  # Heavy penalty for production
        elif proposal.context == 'config':
            score -= 0.3  # Configuration changes are very risky
    
    # STRICT severity penalties
    if hasattr(proposal, 'severity'):
        if proposal.severity.value in ['high', 'critical']:
            return 0.0  # Immediate fail for high/critical
        elif proposal.severity.value == 'medium':
            score -= 0.2
    
    # Use existing safety score if available, but be more conservative
    if hasattr(proposal, 'safety_score'):
        existing_score = proposal.safety_score / 100
        score = min(score, existing_score * 0.8)  # Take 80% of existing score as maximum
    
    return max(0.0, min(1.0, score))

def apply_fix(project_path, fix):
    """Applies a single fix to a file with emergency safeguards."""
    try:
        file_path = Path(project_path) / fix.file_path
        if not file_path.exists():
            print(f"  ❌ Error: File not found at {file_path}")
            return False

        # Read original file content
        with open(file_path, 'r') as f:
            original_content = f.read()
            original_lines = f.readlines()

        # Calculate what the new content would be
        if fix.line_number - 1 >= len(original_lines):
            print(f"  ❌ Error: Line number {fix.line_number} is out of bounds for file {fix.file_path}")
            return False
        
        new_lines = original_lines.copy()
        new_lines[fix.line_number - 1] = new_lines[fix.line_number - 1].replace(fix.original_code, fix.proposed_fix)
        new_content = ''.join(new_lines)

        # 🚨 EMERGENCY SAFEGUARDS: Pattern-based validation
        print(f"  🛡️ Emergency validation for {fix.file_path}...")
        
        # Import emergency safeguards
        sys.path.insert(0, str(Path(__file__).parent / 'src'))
        from safety.emergency_safeguards import validate_fix_application
        
        is_safe, reason = validate_fix_application(fix, original_content, new_content)
        
        if not is_safe:
            print(f"  🚨 EMERGENCY BLOCK: {reason}")
            print(f"  🛑 Fix blocked by emergency safeguards despite user approval!")
            
            # Log the emergency block
            emergency_log = {
                'timestamp': datetime.now().isoformat(),
                'action': 'EMERGENCY_APPLICATION_BLOCK',
                'file_path': str(file_path),
                'fix_type': fix.issue_type,
                'reason': reason,
                'proposed_fix': fix.proposed_fix
            }
            
            emergency_log_file = Path('emergency_application_blocks.log')
            with open(emergency_log_file, 'a') as f:
                import json
                f.write(json.dumps(emergency_log) + '\n')
            
            return False

        print(f"  ✅ Emergency validation passed")

        # 🏗️ SANDBOX VALIDATION: Ultimate safety test
        print(f"  🏗️ Sandbox validation for {fix.file_path}...")
        
        try:
            from safety.sandboxed_validation import validate_fix_with_sandbox
            
            sandbox_safe, sandbox_reason, sandbox_result = validate_fix_with_sandbox(
                project_path, fix, original_content, new_content
            )
            
            if not sandbox_safe:
                print(f"  🚨 SANDBOX BLOCK: {sandbox_reason}")
                print(f"  🏗️ Build passed: {sandbox_result.build_passed}")
                print(f"  🧪 Tests passed: {sandbox_result.tests_passed}")
                print(f"  🔍 Runtime safe: {sandbox_result.runtime_safe}")
                print(f"  🛑 Fix blocked by sandbox validation despite all other approvals!")
                
                # Log the sandbox block
                sandbox_log = {
                    'timestamp': datetime.now().isoformat(),
                    'action': 'SANDBOX_APPLICATION_BLOCK',
                    'file_path': str(file_path),
                    'fix_type': fix.issue_type,
                    'reason': sandbox_reason,
                    'build_passed': sandbox_result.build_passed,
                    'tests_passed': sandbox_result.tests_passed,
                    'runtime_safe': sandbox_result.runtime_safe,
                    'execution_time': sandbox_result.execution_time,
                    'issues': sandbox_result.issues_found,
                    'security_violations': sandbox_result.security_violations
                }
                
                sandbox_log_file = Path('sandbox_application_blocks.log')
                with open(sandbox_log_file, 'a') as f:
                    f.write(json.dumps(sandbox_log) + '\n')
                
                return False
            
            print(f"  ✅ Sandbox validation passed ({sandbox_result.execution_time:.2f}s)")
            
        except Exception as e:
            print(f"  ⚠️ Sandbox validation unavailable: {e}")
            print(f"  🔄 Proceeding with emergency validation only")

        # Create a backup
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        shutil.copy2(file_path, backup_path)

        # Apply the fix
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print(f"  ✅ Applied fix: {fix.issue_type} in {fix.file_path}")
        return True

    except Exception as e:
        print(f"  ❌ Error applying fix to {fix.file_path}: {e}")
        return False

def generate_fix_for_issue(issue):
    """Generate actual fix code for an issue with safety checks."""
    issue_type = issue.get('type', '')
    file_path = issue.get('file_path', '')
    line_num = issue.get('line', 0)
    description = issue.get('description', '').lower()
    
    # Read the actual line from the file
    actual_line = None
    if file_path and line_num > 0:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 0 < line_num <= len(lines):
                    actual_line = lines[line_num - 1]
        except Exception:
            pass
    
    # If we couldn't read the line, return empty fix
    if not actual_line:
        return '', ''
    
    # Strip only for comparison, preserve original formatting
    actual_line_stripped = actual_line.strip()
    
    # Exception handling fixes
    if issue_type == 'exception_handling':
        if 'bare except' in description:
            if actual_line_stripped == 'except:':
                # Replace bare except with specific exception
                return actual_line, actual_line.replace('except:', 'except Exception as e:')
            elif actual_line_stripped == 'except Exception:':
                # Add variable binding
                return actual_line, actual_line.replace('except Exception:', 'except Exception as e:')
    
    # Debugging statement fixes
    elif issue_type == 'debugging':
        if 'print(' in actual_line:
            # Simple print to logger conversion
            # But first check if logger is imported
            import_needed = check_logger_import(file_path)
            if import_needed:
                # Don't auto-fix if logger import is missing
                return '', ''
            
            # Replace print with logger.info preserving indentation
            new_line = actual_line.replace('print(', 'logger.info(')
            if new_line != actual_line:
                return actual_line, new_line
    
    # Security fixes
    elif issue_type == 'security':
        if 'eval(' in actual_line:
            # Comment out eval usage instead of breaking syntax
            indent = len(actual_line) - len(actual_line.lstrip())
            comment = ' ' * indent + '# SECURITY WARNING: eval() usage detected - consider safer alternatives\n'
            return actual_line, comment + actual_line
    
    # Maintenance/TODO fixes - just acknowledge, don't modify
    elif issue_type == 'maintenance':
        if 'TODO' in actual_line or 'FIXME' in actual_line:
            # Don't modify TODO/FIXME comments
            return '', ''
    
    # No fix available
    return '', ''

def check_logger_import(file_path):
    """Check if logger is properly imported in the file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for common logger imports
            if 'import logging' in content or 'from logging import' in content:
                # Also check if logger is defined
                if 'logger = ' in content or 'logger=' in content:
                    return False  # Logger is available
        return True  # Logger import is needed
    except Exception:
        return True  # Assume import is needed if we can't check

def convert_issues_to_proposals(issues):
    """Converts a list of issues to a list of FixProposal objects."""
    proposals = []
    for issue in issues:
        severity_map = {
            'critical': FixSeverity.CRITICAL,
            'high': FixSeverity.HIGH,
            'medium': FixSeverity.MEDIUM,
            'low': FixSeverity.LOW,
            'cosmetic': FixSeverity.COSMETIC
        }
        # Generate fix if not provided
        original_code = issue.get('original_code', '')
        proposed_fix = issue.get('suggested_fix', '')
        
        if not original_code or not proposed_fix:
            original_code, proposed_fix = generate_fix_for_issue(issue)
        
        # Only create proposal if we have a valid fix
        if original_code and proposed_fix and original_code != proposed_fix:
            proposal = FixProposal(
                file_path=issue.get('file_path'),
                issue_type=issue.get('type'),
                severity=severity_map.get(issue.get('severity'), FixSeverity.MEDIUM),
                description=issue.get('description'),
                original_code=original_code,
                proposed_fix=proposed_fix,
                line_number=issue.get('line'),
                educational_explanation=f"This fix addresses a {issue.get('type')} issue.",
                safety_score=issue.get('safety_score', 50),
                context=issue.get('context', 'unknown'),
                auto_approvable=True
            )
            proposals.append(proposal)
    return proposals

def run_training(issues_file: str, interactive: bool, batch_file: str = None):
    """Train PRI by flagging false positives."""
    print(f"🧠 PRI Training Mode: False Positive Detection")
    print(f"📁 Issues file: {issues_file}")
    print(f"🎯 Mode: {'Interactive' if interactive else 'Batch'}")

    try:
        # Load issues
        with open(issues_file, 'r') as f:
            issues = json.load(f)

        # Initialize memory-enhanced detector
        memory_engine = MemoryEngine()
        context_analyzer = ContextAnalyzer()
        fp_detector = MemoryEnhancedFalsePositiveDetector(memory_engine, context_analyzer)

        if interactive:
            run_interactive_training(issues, fp_detector)
        elif batch_file:
            run_batch_training(issues, batch_file, fp_detector)
        else:
            print("❌ Error: Must specify either --interactive or --batch-file")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading files: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def run_interactive_training(issues: list, fp_detector):
    """Interactive training mode for flagging false positives."""
    print(f"\n🎯 Interactive Training Session")
    print(f"📊 Total issues to review: {len(issues)}")
    print("💡 Commands: (y)es = false positive, (n)o = valid issue, (s)kip, (q)uit")
    print()

    trained_count = 0
    skipped_count = 0

    for i, issue in enumerate(issues, 1):
        print(f"📋 Issue {i}/{len(issues)}")
        print(f"   Type: {issue.get('type', 'unknown')}")
        print(f"   Severity: {issue.get('severity', 'unknown')}")
        print(f"   Description: {issue.get('description', 'No description')}")
        print(f"   Context: {issue.get('context', 'unknown')}")

        if issue.get('suggestion'):
            print(f"   Suggestion: {issue.get('suggestion')}")

        print()

        while True:
            response = input("Is this a false positive? (y/n/s/q): ").lower().strip()

            if response == 'q':
                print(f"\n✅ Training session completed.")
                print(f"📊 Trained on {trained_count} issues, skipped {skipped_count}")
                return

            elif response == 's':
                skipped_count += 1
                print("⏭️  Skipped")
                break

            elif response in ['y', 'n']:
                is_false_positive = (response == 'y')

                # Get user reasoning
                reasoning = input("Brief reason (optional): ").strip()
                if not reasoning:
                    reasoning = "User classification during training"

                # Store the training data
                try:
                    # For training, we'll use a dummy file path based on context
                    file_path = f"training_data/{issue.get('context', 'unknown')}_file.py"

                    # Use asyncio to run the async method
                    import asyncio
                    asyncio.run(fp_detector.learn_from_user_feedback(
                        issue, file_path, is_false_positive, reasoning, confidence=1.0
                    ))

                    trained_count += 1
                    status = "false positive" if is_false_positive else "valid issue"
                    print(f"✅ Learned: {status}")

                except Exception as e:
                    print(f"⚠️  Error storing feedback: {e}")

                break

            else:
                print("Invalid response. Use y/n/s/q")

        print("-" * 50)

    print(f"\n🎉 Training completed!")
    print(f"📊 Final stats: {trained_count} trained, {skipped_count} skipped")

def run_batch_training(issues: list, batch_file: str, fp_detector):
    """Batch training mode using pre-labeled data."""
    print(f"\n📦 Batch Training Mode")
    print(f"📁 Batch file: {batch_file}")

    try:
        with open(batch_file, 'r') as f:
            batch_data = json.load(f)

        print(f"📊 Found {len(batch_data)} labeled examples")

        trained_count = 0
        errors = 0

        for label_data in batch_data:
            try:
                # Find matching issue
                issue_id = label_data.get('issue_id')
                matching_issue = None

                for issue in issues:
                    if (issue.get('line') == issue_id or
                        issue.get('description') == label_data.get('description')):
                        matching_issue = issue
                        break

                if not matching_issue:
                    print(f"⚠️  Could not find matching issue for: {label_data.get('description', 'unknown')}")
                    continue

                # Apply the label
                is_false_positive = label_data.get('is_false_positive', False)
                reasoning = label_data.get('reasoning', 'Batch training data')
                file_path = label_data.get('file_path', 'batch_training_file.py')

                asyncio.run(fp_detector.learn_from_user_feedback(
                    matching_issue, file_path, is_false_positive, reasoning, confidence=0.9
                ))

                trained_count += 1

            except Exception as e:
                print(f"❌ Error processing batch item: {e}")
                errors += 1

        print(f"\n✅ Batch training completed!")
        print(f"📊 Successfully trained: {trained_count}")
        print(f"❌ Errors: {errors}")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading batch file: {e}")

def run_stats(detailed: bool):
    """Show false positive detection statistics."""
    print("📊 PRI False Positive Detection Statistics")
    print("=" * 50)

    try:
        # Initialize detector to get stats
        memory_engine = MemoryEngine()
        context_analyzer = ContextAnalyzer()
        fp_detector = MemoryEnhancedFalsePositiveDetector(memory_engine, context_analyzer)

        stats = asyncio.run(fp_detector.get_false_positive_statistics())

        if "error" in stats:
            print(f"❌ Error getting statistics: {stats['error']}")
            return

        if "message" in stats:
            print(f"💡 {stats['message']}")
            return

        # Display basic statistics
        print(f"🔢 Total Analyses: {stats['total_analyses']}")
        print(f"🚫 False Positives: {stats['total_false_positives']}")
        print(f"📈 False Positive Rate: {stats['overall_fp_rate']:.2%}")
        print(f"👤 User Feedbacks: {stats['user_feedbacks']}")
        print(f"🧠 Learning Effectiveness: {stats['learning_effectiveness']:.2%}")

        if detailed and stats.get('issue_type_statistics'):
            print(f"\n📋 Issue Type Breakdown:")
            print("-" * 30)

            for issue_type, type_stats in stats['issue_type_statistics'].items():
                print(f"  {issue_type}:")
                print(f"    Total: {type_stats['total']}")
                print(f"    False Positives: {type_stats['false_positives']}")
                print(f"    FP Rate: {type_stats['fp_rate']:.2%}")
                print()

        if detailed and stats.get('context_statistics'):
            print(f"📁 Context Breakdown:")
            print("-" * 30)

            for context, context_stats in stats['context_statistics'].items():
                print(f"  {context}:")
                print(f"    Total: {context_stats['total']}")
                print(f"    False Positives: {context_stats['false_positives']}")
                print(f"    FP Rate: {context_stats['fp_rate']:.2%}")
                print()

        print("💡 Use 'python mesopredator_cli.py train --interactive --issues-file <file>' to improve detection")

    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        import traceback
        print(traceback.format_exc())

def run_pruning(strategy: str, dry_run: bool, namespace: str = None, aggressive: bool = False):
    """Run memory pruning with the specified strategy."""
    print("🧹 PRI Memory Pruning")
    print("=" * 40)
    print(f"🎯 Strategy: {strategy}")
    print(f"🔍 Mode: {'Dry run (preview only)' if dry_run else 'Live pruning'}")

    if namespace:
        print(f"📂 Target namespace: {namespace}")
    else:
        print("📂 Target: All namespaces")

    if aggressive:
        print("⚡ Aggressive pruning: Enabled")

    try:
        # Initialize pruning system
        memory_engine = MemoryEngine()
        pruning_system = MemoryPruningSystem(memory_engine)

        # Convert strategy string to enum
        strategy_map = {
            'age_based': PruningStrategy.AGE_BASED,
            'redundancy_based': PruningStrategy.REDUNDANCY_BASED,
            'quality_based': PruningStrategy.QUALITY_BASED,
            'hybrid': PruningStrategy.HYBRID
        }

        strategy_enum = strategy_map.get(strategy, PruningStrategy.HYBRID)

        if dry_run:
            print("\n🔍 DRY RUN - Analyzing what would be pruned...")
            # For dry run, we'd implement a preview mode
            print("💡 Dry run mode not yet implemented - use with caution!")
            return

        print(f"\n🚀 Starting pruning with {strategy} strategy...")


        if namespace:
            # Prune specific namespace
            result = asyncio.run(pruning_system._prune_namespace(namespace, strategy_enum))
            print(f"\n✅ Namespace pruning completed!")
            print(f"📊 Results for {namespace}:")
            print(f"   🗑️  Removed: {result['memories_removed']}")
            print(f"   📦 Consolidated: {result['memories_consolidated']}")
            print(f"   📈 Initial count: {result['initial_count']}")
            print(f"   📉 Final count: {result['final_count']}")
        else:
            # Prune all namespaces
            result = asyncio.run(pruning_system.prune_all_namespaces(strategy_enum))
            print(f"\n✅ Global pruning completed!")
            print(f"📊 Overall Results:")
            print(f"   🗑️  Total removed: {result.memories_removed}")
            print(f"   📦 Total consolidated: {result.memories_consolidated}")
            print(f"   📈 Before: {result.total_memories_before} memories")
            print(f"   📉 After: {result.total_memories_after} memories")
            print(f"   💾 Space saved: {result.space_saved_mb:.2f} MB")
            print(f"   ⏱️  Time taken: {result.pruning_time_seconds:.2f} seconds")

            if result.namespace_results:
                print(f"\n📂 Namespace breakdown:")
                for ns, ns_result in result.namespace_results.items():
                    if isinstance(ns_result, dict) and 'memories_removed' in ns_result:
                        print(f"   {ns}: -{ns_result['memories_removed']}, consolidated: {ns_result['memories_consolidated']}")

        print(f"\n💡 Tip: Use 'python mesopredator_cli.py stats --detailed' to see updated memory statistics")

    except Exception as e:
        print(f"❌ Error during pruning: {e}")
        print(traceback.format_exc())

def run_cycle_tracking(command: str, issues_file: str = None, project_path: str = None, previous_issues_file: str = None):
    """Run improvement cycle tracking operations."""
    print("🔄 PRI Improvement Cycle Tracking")
    print("=" * 45)

    try:
        # Initialize cycle tracker
        memory_engine = MemoryEngine()
        cycle_tracker = ImprovementCycleTracker(memory_engine)


        if command == "manual_fixes":
            if not issues_file or not project_path:
                print("❌ Error: --issues-file and --project-path required for manual fixes detection")
                return

            print(f"🔍 Detecting manual fixes in: {project_path}")
            print(f"📁 Current scan file: {issues_file}")

            # Load current issues
            with open(issues_file, 'r') as f:
                current_issues = json.load(f)

            # Detect manual fixes
            manual_fixes = asyncio.run(cycle_tracker.detect_manual_fixes_in_scan(current_issues, project_path))

            print(f"\n🛠️  Manual Fixes Detected: {len(manual_fixes)}")

            if manual_fixes:
                print("\n📋 Manual Fix Details:")
                for fix in manual_fixes:
                    print(f"   • {fix['issue_type']} in {fix['file_path']}")
                    print(f"     Context: {fix['file_context']}")
                    print(f"     Detected: {fix['manual_fix_detected_date']}")
                    print()
            else:
                print("   No manual fixes detected in recent cycles")

        elif command == "scan_comparison":
            if not issues_file or not project_path or not previous_issues_file:
                print("❌ Error: --issues-file, --previous-issues-file, and --project-path required")
                return

            print(f"📊 Comparing scans for: {project_path}")
            print(f"📁 Previous scan: {previous_issues_file}")
            print(f"📁 Current scan: {issues_file}")

            # Load issues
            with open(previous_issues_file, 'r') as f:
                previous_issues = json.load(f)
            with open(issues_file, 'r') as f:
                current_issues = json.load(f)

            # Track comparison metrics
            metrics = asyncio.run(cycle_tracker.track_scan_comparison_metrics(
                previous_issues, current_issues, project_path
            ))

            if metrics:
                print(f"\n📈 Scan Comparison Results:")
                print(f"   📋 Previous issues: {metrics['previous_issues_count']}")
                print(f"   📋 Current issues: {metrics['current_issues_count']}")
                print(f"   ✅ Total resolved: {metrics['total_resolved']}")
                print(f"   🛠️  Manual fixes: {metrics['manual_fixes_detected']}")
                print(f"   🤖 Automated fixes: {metrics['automated_fixes_estimated']}")
                print(f"   📊 Manual fix rate: {metrics['manual_fix_rate']:.1%}")
                print(f"   📊 Automated fix rate: {metrics['automated_fix_rate']:.1%}")

                if metrics['manual_fix_types_breakdown']:
                    print(f"\n🔧 Manual Fix Types:")
                    for fix_type, count in metrics['manual_fix_types_breakdown'].items():
                        print(f"   • {fix_type}: {count}")

        elif command == "patterns":
            print("🔍 Analyzing manual fix patterns...")

            patterns = asyncio.run(cycle_tracker.get_manual_fix_patterns())

            if "error" in patterns:
                print(f"❌ Error: {patterns['error']}")
                return

            if "message" in patterns:
                print(f"💡 {patterns['message']}")
                return

            print(f"\n📊 Manual Fix Pattern Analysis:")
            print(f"   🔢 Total manual fixes: {patterns['total_manual_fixes']}")

            if patterns['issue_types']:
                print(f"\n🐛 Issue Types Manually Fixed:")
                for issue_type, data in patterns['issue_types'].items():
                    print(f"   • {issue_type}: {data['count']} fixes")
                    print(f"     Contexts: {', '.join(data['contexts'])}")

            if patterns['file_contexts']:
                print(f"\n📁 File Contexts:")
                for context, count in patterns['file_contexts'].items():
                    print(f"   • {context}: {count} fixes")

            if patterns.get('average_manual_fix_time_hours'):
                print(f"\n⏱️  Timing Analysis:")
                print(f"   • Average fix time: {patterns['average_manual_fix_time_hours']:.1f} hours")
                print(f"   • Median fix time: {patterns['median_manual_fix_time_hours']:.1f} hours")

            if patterns['automation_opportunities']:
                print(f"\n🤖 Automation Opportunities:")
                for opp in patterns['automation_opportunities']:
                    print(f"   • {opp['issue_type']} ({opp['frequency']} occurrences)")
                    print(f"     Potential: {opp['automation_potential']}")
                    print(f"     Recommendation: {opp['recommendation']}")
                    print()

        elif command == "cycle_metrics":
            print("📊 Analyzing improvement cycle patterns...")

            cycle_metrics = asyncio.run(cycle_tracker.analyze_cycle_patterns())

            print(f"\n🔄 Cycle Metrics:")
            print(f"   📊 Total cycles: {cycle_metrics.total_cycles}")
            print(f"   ✅ Completed: {cycle_metrics.completed_cycles}")
            print(f"   📈 Success rate: {cycle_metrics.success_rate:.1%}")
            print(f"   ⏱️  Average cycle time: {cycle_metrics.average_cycle_time_hours:.1f} hours")
            print(f"   🚀 Learning velocity: {cycle_metrics.learning_velocity:.2f} cycles/day")
            print(f"   🔧 Fix application rate: {cycle_metrics.fix_application_rate:.1%}")

            if cycle_metrics.common_failure_points:
                print(f"\n⚠️  Common Failure Points:")
                for stage, count in cycle_metrics.common_failure_points.items():
                    print(f"   • {stage}: {count} failures")

            if cycle_metrics.pattern_effectiveness_by_type:
                print(f"\n🎯 Pattern Effectiveness:")
                for pattern, effectiveness in cycle_metrics.pattern_effectiveness_by_type.items():
                    print(f"   • {pattern}: {effectiveness:.1%}")

        else:
            print(f"❌ Unknown cycle tracking command: {command}")
            print("💡 Available commands: manual_fixes, scan_comparison, patterns, cycle_metrics")

    except Exception as e:
        print(f"❌ Error in cycle tracking: {e}")
        print(traceback.format_exc())

def main():
    """Main entry point for the PRI CLI tool."""
    parser = argparse.ArgumentParser(
        description="Persistent Recursive Intelligence (PRI) CLI Tool",
        epilog="A tool for analyzing and improving codebases with self-evolving AI."
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # --- Analyze Command ---
    parser_analyze = subparsers.add_parser('analyze', help='Analyze a project and store insights.')
    parser_analyze.add_argument('project_path', type=str, help='The path to the project directory to analyze.')
    parser_analyze.add_argument('--output-file', type=str, help='Path to save the analysis results as a JSON file.')

    # --- Fix Command ---
    parser_fix = subparsers.add_parser('fix', help='Interactively fix issues in a project.')
    parser_fix.add_argument('project_path', type=str, help='The path to the project directory to fix.')
    parser_fix.add_argument('--issues-file', type=str, required=True, help='JSON file containing the list of issues to address.')
    parser_fix.add_argument('--dynamic-approval', action='store_true', help='Use dynamic approval based on safety scores.')
    parser_fix.add_argument('--conservative-level', type=float, default=0.7, help='Conservative level for dynamic approval (0.0-1.0).')

    # --- Train Command ---
    parser_train = subparsers.add_parser('train', help='Train PRI by flagging false positives.')
    parser_train.add_argument('--issues-file', type=str, required=True, help='JSON file containing analysis results.')
    parser_train.add_argument('--interactive', action='store_true', help='Interactive mode for reviewing and flagging issues.')
    parser_train.add_argument('--batch-file', type=str, help='Batch file with pre-labeled false positives.')

    # --- Stats Command ---
    parser_stats = subparsers.add_parser('stats', help='Show false positive detection statistics.')
    parser_stats.add_argument('--detailed', action='store_true', help='Show detailed statistics by issue type and context.')

    # --- Prune Command ---
    parser_prune = subparsers.add_parser('prune', help='Prune memory system to remove redundant patterns.')
    parser_prune.add_argument('--strategy', choices=['age_based', 'redundancy_based', 'quality_based', 'hybrid'],
                             default='hybrid', help='Pruning strategy to use.')
    parser_prune.add_argument('--dry-run', action='store_true', help='Show what would be pruned without actually doing it.')
    parser_prune.add_argument('--namespace', type=str, help='Prune specific namespace only.')
    parser_prune.add_argument('--aggressive', action='store_true', help='Use aggressive pruning for over-represented patterns.')

    # --- Cycle Tracking Command ---
    parser_cycle = subparsers.add_parser('cycle', help='Track improvement cycles and detect manual fixes.')
    parser_cycle.add_argument('cycle_command', choices=['manual_fixes', 'scan_comparison', 'patterns', 'cycle_metrics'],
                             help='Cycle tracking operation to perform.')
    parser_cycle.add_argument('--issues-file', type=str, help='JSON file with current scan issues.')
    parser_cycle.add_argument('--previous-issues-file', type=str, help='JSON file with previous scan issues (for comparison).')
    parser_cycle.add_argument('--project-path', type=str, help='Path to the project being analyzed.')

    args = parser.parse_args()

    if args.command == 'analyze':
        issues = run_analysis(args.project_path)
        if args.output_file:
            with open(args.output_file, 'w') as f:
                json.dump(issues, f, indent=4)
            print(f"💾 Analysis results saved to {args.output_file}")

    elif args.command == 'fix':
        run_fixer(args.project_path, args.issues_file, args.dynamic_approval, args.conservative_level)

    elif args.command == 'train':
        run_training(args.issues_file, args.interactive, args.batch_file)

    elif args.command == 'stats':
        run_stats(args.detailed)

    elif args.command == 'prune':
        run_pruning(args.strategy, args.dry_run, args.namespace, args.aggressive)

    elif args.command == 'cycle':
        run_cycle_tracking(args.cycle_command, args.issues_file, args.project_path, args.previous_issues_file)

if __name__ == '__main__':
    main()