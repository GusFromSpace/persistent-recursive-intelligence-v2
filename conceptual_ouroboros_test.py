#!/usr/bin/env python3
"""
ADV-TEST-001: The "Ouroboros" Test - CONCEPTUAL FLAW INJECTION

This test validates the system's ability to detect and fix SUBTLE, CONCEPTUAL FLAWS
in its core cognitive architecture, not superficial syntax errors.

Target Claim: PRI can detect and fix performance-degrading flaws in its own logic
Hypothesis to Disprove: System can only fix superficial bugs, not subtle cognitive flaws

Test Flaws Designed:
1. Memory Corruption: Subtle metadata corruption that degrades memory accuracy over time
2. Learning Decay: Artificial reduction in pattern weights that causes "forgetting"
3. Recursive Depth Limitation: Subtle logic that prevents deep cognitive analysis

These are CONCEPTUAL flaws that would degrade performance but not cause crashes.
"""

import sys
import time
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

class ConceptualFlawInjector:
    """Inject subtle, performance-degrading conceptual flaws into cognitive architecture"""
    
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.injected_flaws = []
        self.performance_baseline = None
    
    def inject_memory_corruption_flaw(self):
        """
        FLAW IDEA 1: Memory Corruption
        Inject subtle metadata corruption in memory engine that occasionally 
        omits key metadata, degrading memory accuracy over time
        """
        engine_file = self.target_dir / "src/cognitive/memory/memory/engine.py"
        
        if not engine_file.exists():
            print(f"⚠️ Target file not found: {engine_file}")
            return False
        
        # Read the original file
        original_content = engine_file.read_text()
        
        # Create the subtle flaw injection
        memory_corruption_flaw = '''
        # ADV-TEST-001 CONCEPTUAL FLAW: Subtle memory corruption
        # This flaw occasionally corrupts metadata, degrading accuracy over time
        import random
        import time
        
        # Inject corruption during memory storage operations
        if hasattr(self, '_memory_operations_count'):
            self._memory_operations_count += 1
        else:
            self._memory_operations_count = 1
            
        # Corruption probability increases with usage (simulating memory wear)
        corruption_probability = min(0.05, self._memory_operations_count * 0.0001)
        
        if random.random() < corruption_probability:
            # Subtle corruption: occasionally drop metadata fields
            if 'metadata' in locals() and isinstance(metadata, dict):
                corruption_keys = ['timestamp', 'confidence', 'source', 'type']
                key_to_corrupt = random.choice([k for k in corruption_keys if k in metadata])
                if key_to_corrupt:
                    # Corrupt by slightly altering the value, not removing it
                    if key_to_corrupt == 'confidence' and isinstance(metadata[key_to_corrupt], (int, float)):
                        metadata[key_to_corrupt] *= random.uniform(0.8, 0.95)  # Reduce confidence
                    elif key_to_corrupt == 'timestamp':
                        metadata[key_to_corrupt] = metadata[key_to_corrupt] + "corrupted"
                        
        '''
        
        # Find the store/remember method to inject after
        lines = original_content.split('\n')
        injected_lines = []
        injection_done = False
        
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # Look for memory storage method
            if not injection_done and ('def store(' in line or 'def remember(' in line):
                # Skip the method signature and docstring, inject in the method body
                j = i + 1
                while j < len(lines) and (lines[j].strip().startswith('"""') or 
                                        lines[j].strip().startswith('"""') or
                                        lines[j].strip() == '' or
                                        '"""' in lines[j]):
                    injected_lines.append(lines[j])
                    j += 1
                    if '"""' in lines[j-1] and not lines[j-1].strip().startswith('"""'):
                        break
                
                # Inject the flaw
                injected_lines.extend(memory_corruption_flaw.split('\n'))
                injection_done = True
        
        if injection_done:
            engine_file.write_text('\n'.join(injected_lines))
            self.injected_flaws.append({
                'type': 'memory_corruption',
                'file': str(engine_file),
                'description': 'Subtle memory corruption: Progressive metadata degradation',
                'performance_impact': 'high',
                'detection_difficulty': 'very_hard'
            })
            print(f"✅ Injected memory corruption flaw into {engine_file}")
            return True
        else:
            print(f"⚠️ Could not find injection point in {engine_file}")
            return False
    
    def inject_learning_decay_flaw(self):
        """
        FLAW IDEA 2: Learning Decay
        Inject artificial reduction in memory pattern weights, 
        causing the system to "forget" valuable lessons over time
        """
        recursive_file = self.target_dir / "src/cognitive/recursive/recursive_improvement.py"
        
        if not recursive_file.exists():
            print(f"⚠️ Target file not found: {recursive_file}")
            return False
        
        # Read the original file
        original_content = recursive_file.read_text()
        
        # Create the learning decay flaw
        learning_decay_flaw = '''
        # ADV-TEST-001 CONCEPTUAL FLAW: Learning decay
        # This causes the system to artificially "forget" older patterns
        import time
        import math
        
        # Apply decay to any improvement patterns or learnings
        current_time = time.time()
        
        # Decay factor increases over time - simulating cognitive degradation
        if hasattr(self, '_pattern_weights') and isinstance(self._pattern_weights, dict):
            for pattern_id in list(self._pattern_weights.keys()):
                pattern_data = self._pattern_weights[pattern_id]
                
                # Get pattern age
                pattern_timestamp = pattern_data.get('created_at', current_time)
                age_hours = (current_time - pattern_timestamp) / 3600
                
                # Apply exponential decay - older patterns lose weight
                if age_hours > 1:  # Start decay after 1 hour
                    decay_factor = math.exp(-age_hours * 0.1)  # 10% decay per hour
                    
                    if 'weight' in pattern_data:
                        pattern_data['weight'] *= decay_factor
                        
                    if 'confidence' in pattern_data:
                        pattern_data['confidence'] *= decay_factor
                        
                    # Remove patterns that decay too much
                    if pattern_data.get('weight', 1.0) < 0.1:
                        del self._pattern_weights[pattern_id]
                        
        # Also decay any stored results or metrics
        if hasattr(self, 'improvement_log') and isinstance(self.improvement_log, list):
            # Corrupt improvement scores over time
            for entry in self.improvement_log:
                if isinstance(entry, dict) and 'score' in entry:
                    entry_age = (current_time - entry.get('timestamp', current_time)) / 3600
                    if entry_age > 0.5:  # Start corruption after 30 minutes
                        corruption = random.uniform(0.9, 0.99)
                        entry['score'] *= corruption
        '''
        
        # Inject into the improvement iteration method
        lines = original_content.split('\n')
        injected_lines = []
        injection_done = False
        
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # Look for improvement iteration methods
            if not injection_done and ('def improve_' in line or 'def recursive_' in line or 'def iteration' in line):
                # Skip method signature and docstring
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or 
                                        lines[j].strip().startswith('"""') or
                                        '"""' in lines[j]):
                    injected_lines.append(lines[j])
                    j += 1
                    if '"""' in lines[j-1] and not lines[j-1].strip().startswith('"""'):
                        break
                
                # Inject the learning decay flaw
                injected_lines.extend(learning_decay_flaw.split('\n'))
                injection_done = True
        
        if injection_done:
            recursive_file.write_text('\n'.join(injected_lines))
            self.injected_flaws.append({
                'type': 'learning_decay',
                'file': str(recursive_file),
                'description': 'Learning decay: Artificial forgetting of valuable patterns',
                'performance_impact': 'very_high',
                'detection_difficulty': 'extremely_hard'
            })
            print(f"✅ Injected learning decay flaw into {recursive_file}")
            return True
        else:
            print(f"⚠️ Could not find injection point in {recursive_file}")
            return False
    
    def inject_recursive_depth_limitation_flaw(self):
        """
        FLAW IDEA 3: Recursive Depth Limitation
        Inject subtle logic that artificially limits recursive analysis depth,
        preventing the system from achieving deep cognitive insights
        """
        recursive_file = self.target_dir / "src/cognitive/recursive/recursive_improvement.py"
        
        if not recursive_file.exists():
            return False
        
        original_content = recursive_file.read_text()
        
        # Create the depth limitation flaw
        depth_limitation_flaw = '''
        # ADV-TEST-001 CONCEPTUAL FLAW: Recursive depth limitation
        # Subtly limits cognitive depth to prevent deep analysis
        
        # Check if we're in a recursive context and artificially limit depth
        if hasattr(self, 'iteration_count'):
            current_depth = getattr(self, '_current_depth', 0)
            
            # Artificial limitation: start reducing effectiveness after depth 2
            if current_depth > 2:
                effectiveness_reduction = 0.7 ** (current_depth - 2)
                
                # Corrupt any depth-related parameters
                if 'max_depth' in locals():
                    max_depth = int(max_depth * effectiveness_reduction)
                    max_depth = max(1, max_depth)  # Ensure at least 1
                    
                if 'iterations' in locals():
                    iterations = int(iterations * effectiveness_reduction)
                    iterations = max(1, iterations)
                    
                # Also limit batch processing
                if 'batch_size' in locals():
                    batch_size = int(batch_size * effectiveness_reduction)
                    batch_size = max(1, batch_size)
                    
            # Track depth artificially
            self._current_depth = current_depth + 1
        '''
        
        # Inject at the beginning of recursive methods
        lines = original_content.split('\n')
        injected_lines = []
        injection_done = False
        
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # Look for recursive improvement methods
            if not injection_done and 'def improve_recursively' in line:
                # Find method body start
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or 
                                        lines[j].strip().startswith('"""') or
                                        '"""' in lines[j]):
                    injected_lines.append(lines[j])
                    j += 1
                    if '"""' in lines[j-1] and not lines[j-1].strip().startswith('"""'):
                        break
                
                # Inject the depth limitation flaw
                injected_lines.extend(depth_limitation_flaw.split('\n'))
                injection_done = True
        
        if injection_done:
            recursive_file.write_text('\n'.join(injected_lines))
            self.injected_flaws.append({
                'type': 'recursive_depth_limitation',
                'file': str(recursive_file),
                'description': 'Depth limitation: Artificial constraint on cognitive depth',
                'performance_impact': 'high',
                'detection_difficulty': 'hard'
            })
            print(f"✅ Injected recursive depth limitation flaw into {recursive_file}")
            return True
        else:
            print(f"⚠️ Could not find injection point for depth limitation")
            return False

@contextmanager
def isolated_test_environment():
    """Create isolated test environment for conceptual flaw testing"""
    original_dir = Path.cwd()
    temp_dir = Path(tempfile.mkdtemp(prefix="pri_conceptual_test_"))
    
    try:
        print(f"🧪 Creating isolated test environment at {temp_dir}")
        
        # Copy the entire PRI system
        for item in original_dir.iterdir():
            if item.name not in ['.git', '__pycache__', 'venv', '.venv', 'node_modules']:
                if item.is_dir():
                    shutil.copytree(item, temp_dir / item.name, 
                                  ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.git'))
                else:
                    shutil.copy2(item, temp_dir / item.name)
        
        yield temp_dir, original_dir
        
    finally:
        print(f"🧹 Cleaning up test environment {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)

def measure_performance_baseline(test_dir: Path):
    """Measure baseline performance before flaw injection"""
    print("📊 Measuring performance baseline...")
    
    # Run a limited analysis to measure performance
    start_time = time.time()
    
    try:
        # Run analysis on a small subset to get baseline metrics
        result = subprocess.run([
            sys.executable, "-m", "src.cognitive.persistent_recursion",
            "--project", str(test_dir / "test_hello_world"),
            "--max-depth", "2",
            "--batch-size", "5"
        ], cwd=test_dir, capture_output=True, text=True, timeout=120)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Extract performance metrics from output
        issues_found = 0
        lines = result.stdout.split('\n')
        for line in lines:
            if "Found" in line and "issues" in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word == "Found" and i + 1 < len(words):
                        try:
                            issues_found = int(words[i + 1])
                            break
                        except ValueError:
                            continue
        
        return {
            'success': result.returncode == 0,
            'duration': duration,
            'issues_found': issues_found,
            'analysis_rate': issues_found / duration if duration > 0 else 0,
            'output_size': len(result.stdout)
        }
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'baseline_timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def measure_performance_after_flaws(test_dir: Path):
    """Measure performance after flaw injection"""
    print("📉 Measuring performance after flaw injection...")
    
    start_time = time.time()
    
    try:
        # Run the same analysis with flaws present
        result = subprocess.run([
            sys.executable, "-m", "src.cognitive.persistent_recursion",
            "--project", str(test_dir / "test_hello_world"),
            "--max-depth", "2", 
            "--batch-size", "5"
        ], cwd=test_dir, capture_output=True, text=True, timeout=120)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Extract performance metrics
        issues_found = 0
        lines = result.stdout.split('\n')
        for line in lines:
            if "Found" in line and "issues" in line:
                words = line.split()
                for i, word in enumerate(words):
                    if word == "Found" and i + 1 < len(words):
                        try:
                            issues_found = int(words[i + 1])
                            break
                        except ValueError:
                            continue
        
        return {
            'success': result.returncode == 0,
            'duration': duration,
            'issues_found': issues_found,
            'analysis_rate': issues_found / duration if duration > 0 else 0,
            'output_size': len(result.stdout),
            'stdout': result.stdout,
            'stderr': result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'performance_timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def run_ouroboros_self_analysis(test_dir: Path):
    """Run the Ouroboros self-analysis to detect injected flaws"""
    print("🐍 Running Ouroboros self-analysis...")
    
    try:
        # Run self-analysis on the entire modified system
        result = subprocess.run([
            sys.executable, "-m", "src.cognitive.persistent_recursion",
            "--project", ".",
            "--max-depth", "3",
            "--batch-size", "10"
        ], cwd=test_dir, capture_output=True, text=True, timeout=300)
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'issues_detected': extract_issues_from_output(result.stdout)
        }
        
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'ouroboros_timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def extract_issues_from_output(output):
    """Extract detailed issues from analysis output"""
    issues = []
    lines = output.split('\n')
    
    # Look for error patterns and issue reports
    for line in lines:
        if any(keyword in line.lower() for keyword in 
               ['error', 'corruption', 'decay', 'limitation', 'degradation', 'performance']):
            issues.append(line.strip())
    
    return issues

def analyze_ouroboros_detection_capability(baseline, post_flaw, ouroboros_result, injected_flaws):
    """Analyze the Ouroboros cycle's ability to detect conceptual flaws"""
    print("🔍 Analyzing Ouroboros detection capability...")
    
    # Performance degradation analysis
    if baseline['success'] and post_flaw['success']:
        performance_degradation = {
            'duration_increase': post_flaw['duration'] / baseline['duration'] - 1,
            'analysis_rate_decrease': 1 - (post_flaw['analysis_rate'] / baseline['analysis_rate']) if baseline['analysis_rate'] > 0 else 0,
            'issues_found_change': post_flaw['issues_found'] - baseline['issues_found']
        }
    else:
        performance_degradation = {'analysis_failed': True}
    
    # Flaw detection analysis
    detected_flaws = []
    if ouroboros_result['success']:
        issues_detected = ouroboros_result['issues_detected']
        
        for flaw in injected_flaws:
            flaw_indicators = {
                'memory_corruption': ['corruption', 'metadata', 'memory', 'integrity'],
                'learning_decay': ['decay', 'forgetting', 'pattern', 'weight', 'confidence'],
                'recursive_depth_limitation': ['depth', 'limitation', 'recursive', 'constraint']
            }
            
            indicators = flaw_indicators.get(flaw['type'], [])
            
            # Check if any detected issues mention this flaw type
            for issue in issues_detected:
                if any(indicator in issue.lower() for indicator in indicators):
                    detected_flaws.append({
                        'flaw': flaw,
                        'detection_evidence': issue,
                        'confidence': 'high' if len([i for i in indicators if i in issue.lower()]) > 1 else 'medium'
                    })
                    break
    
    # Overall detection assessment
    detection_rate = len(detected_flaws) / len(injected_flaws) if injected_flaws else 0
    
    return {
        'performance_degradation': performance_degradation,
        'detected_flaws': detected_flaws,
        'detection_rate': detection_rate,
        'total_flaws_injected': len(injected_flaws),
        'ouroboros_success': ouroboros_result['success']
    }

def main():
    """Execute ADV-TEST-001: Conceptual Ouroboros Test"""
    
    print("🐍 ADV-TEST-001: CONCEPTUAL OUROBOROS TEST")
    print("=" * 80)
    print("🎯 Testing recursive self-improvement on CONCEPTUAL FLAWS")
    print("🔬 Hypothesis: System can only fix superficial bugs, not cognitive flaws")
    print()
    
    with isolated_test_environment() as (test_dir, original_dir):
        
        # Step 1: Measure baseline performance
        print("📊 Step 1: Measuring Baseline Performance")
        baseline = measure_performance_baseline(test_dir)
        
        if not baseline['success']:
            print(f"❌ Baseline measurement failed: {baseline.get('error', 'Unknown error")}")
            return False
        
        print(f"✅ Baseline: {baseline['issues_found']} issues in {baseline['duration']:.2f}s")
        print(f"   Analysis rate: {baseline['analysis_rate']:.2f} issues/second")
        print()
        
        # Step 2: Inject conceptual flaws
        print("💉 Step 2: Injecting Conceptual Flaws")
        injector = ConceptualFlawInjector(test_dir)
        
        injection_results = [
            injector.inject_memory_corruption_flaw(),
            injector.inject_learning_decay_flaw(),
            injector.inject_recursive_depth_limitation_flaw()
        ]
        
        if not any(injection_results):
            print("❌ Failed to inject any conceptual flaws")
            return False
        
        print(f"✅ Successfully injected {len(injector.injected_flaws)} conceptual flaws:")
        for flaw in injector.injected_flaws:
            print(f"  • {flaw['type']}: {flaw['description']}")
            print(f"    Impact: {flaw['performance_impact']}, Difficulty: {flaw['detection_difficulty']}")
        print()
        
        # Step 3: Measure degraded performance
        print("📉 Step 3: Measuring Performance Degradation")
        post_flaw = measure_performance_after_flaws(test_dir)
        
        if post_flaw['success']:
            duration_change = (post_flaw['duration'] / baseline['duration'] - 1) * 100
            rate_change = (post_flaw['analysis_rate'] / baseline['analysis_rate'] - 1) * 100 if baseline['analysis_rate'] > 0 else 0
            
            print(f"📈 Post-flaw: {post_flaw['issues_found']} issues in {post_flaw['duration']:.2f}s")
            print(f"   Duration change: {duration_change:+.1f}%")
            print(f"   Analysis rate change: {rate_change:+.1f}%")
        else:
            print(f"⚠️ Post-flaw analysis had issues: {post_flaw.get('error', 'Unknown")}")
        print()
        
        # Step 4: Run Ouroboros self-analysis
        print("🐍 Step 4: Running Ouroboros Self-Analysis")
        ouroboros_result = run_ouroboros_self_analysis(test_dir)
        
        if not ouroboros_result['success']:
            print(f"❌ Ouroboros analysis failed: {ouroboros_result.get('error', 'Unknown error")}")
            return False
        
        print(f"✅ Ouroboros analysis completed")
        print(f"   Issues detected: {len(ouroboros_result['issues_detected'])}")
        print()
        
        # Step 5: Analyze detection capability
        print("🔍 Step 5: Analyzing Detection Capability")
        analysis = analyze_ouroboros_detection_capability(
            baseline, post_flaw, ouroboros_result, injector.injected_flaws
        )
        
        print(f"📊 Detection Results:")
        print(f"   Flaws detected: {len(analysis['detected_flaws'])}/{analysis['total_flaws_injected']}")
        print(f"   Detection rate: {analysis['detection_rate']:.1%}")
        
        for detection in analysis['detected_flaws']:
            print(f"   ✅ Detected {detection['flaw']['type']}: {detection['confidence']} confidence")
            print(f"      Evidence: {detection['detection_evidence'][:100]}...")
        
        print()
        print("=" * 80)
        
        # Evaluation
        success_threshold = 0.5  # At least 50% of conceptual flaws detected
        test_passed = analysis['detection_rate'] >= success_threshold
        
        if test_passed:
            print("🎉 ADV-TEST-001 PASSED!")
            print("✅ System successfully detected conceptual flaws in its own architecture")
            print("🧠 Ouroboros cycle demonstrates true recursive self-improvement")
            print(f"🎯 Detection rate: {analysis['detection_rate']:.1%}")
        else:
            print("❌ ADV-TEST-001 FAILED!")
            print("⚠️ System failed to detect conceptual flaws")
            print("🔍 Hypothesis CONFIRMED: System only fixes superficial bugs")
            print(f"🎯 Detection rate: {analysis['detection_rate']:.1%}")
        
        # Save comprehensive results
        test_results = {
            'test_id': 'ADV-TEST-001',
            'test_name': 'Conceptual Ouroboros Test',
            'timestamp': datetime.now().isoformat(),
            'success': test_passed,
            'baseline_performance': baseline,
            'post_flaw_performance': post_flaw,
            'injected_flaws': injector.injected_flaws,
            'analysis_results': analysis,
            'detection_rate': analysis['detection_rate']
        }
        
        results_file = original_dir / "conceptual_ouroboros_results.json"
        with open(results_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"📁 Detailed results saved to {results_file}")
        
        return test_passed

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)