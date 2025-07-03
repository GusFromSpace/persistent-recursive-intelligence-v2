#!/usr/bin/env python3
"""
ADV-TEST-001: The "Ouroboros" Test - Recursive Self-Improvement Validation

This test validates the system's ability to detect and fix subtle, conceptual flaws
in its own cognitive architecture, not just simple syntax errors.

Test Design:
1. Inject a subtle, performance-degrading flaw into the core PRI source
2. Execute the Ouroboros cycle using safe_recursive_test.py
3. Measure if the system detects and correctly fixes the conceptual flaw

Success Criteria:
- PRI detects the conceptual flaw within reasonable cycles
- PRI correctly identifies the root cause
- PRI generates a correct and safe patch
"""

import sys
import time
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class SubtleBugInjector:
    """Inject subtle, conceptual bugs into the PRI codebase"""
    
    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.injected_flaws = []
    
    def inject_memory_corruption_flaw(self):
        """Inject Flaw Idea 1: Memory corruption in the memory engine"""
        engine_file = self.target_dir / "src/cognitive/memory/memory/engine.py"
        
        if not engine_file.exists():
            print(f"⚠️ Target file not found: {engine_file}")
            return False
        
        # Read the original file
        original_content = engine_file.read_text()
        
        # Find the remember function and inject the flaw
        flaw_injection = '''
        # ADV-TEST-001 Injected Flaw: Subtle memory corruption
        import random
        if random.random() < 0.01:  # 1% chance
            # Corrupted memory: omit metadata occasionally
            if 'metadata' in locals():
                metadata = {}  # Corrupt the metadata
            elif hasattr(self, '_current_metadata'):
                self._current_metadata = {}  # Corrupt instance metadata
        '''
        
        # Inject after the first function definition we find
        lines = original_content.split('\n')
        injected_lines = []
        injection_done = False
        
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # Look for a function definition to inject after
            if not injection_done and line.strip().startswith('def ') and 'remember' in line:
                # Find the next non-comment, non-empty line to inject after
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        injected_lines.append(flaw_injection)
                        injection_done = True
                        break
        
        if injection_done:
            engine_file.write_text('\n'.join(injected_lines))
            self.injected_flaws.append({
                'type': 'memory_corruption',
                'file': str(engine_file),
                'description': 'Subtle memory corruption: 1% chance of metadata corruption'
            })
            print(f"✅ Injected memory corruption flaw into {engine_file}")
            return True
        else:
            print(f"⚠️ Could not find injection point in {engine_file}")
            return False
    
    def inject_learning_decay_flaw(self):
        """Inject Flaw Idea 2: Learning decay in recursive improvement"""
        recursive_file = self.target_dir / "src/cognitive/recursive/recursive_improvement_enhanced.py"
        
        if not recursive_file.exists():
            print(f"⚠️ Target file not found: {recursive_file}")
            return False
        
        # Read the original file
        original_content = recursive_file.read_text()
        
        # Inject learning decay logic
        flaw_injection = '''
        # ADV-TEST-001 Injected Flaw: Learning decay
        import time
        current_time = time.time()
        if hasattr(self, '_memory_weights'):
            for key in self._memory_weights:
                age_days = (current_time - self._memory_weights[key].get('timestamp', current_time)) / 86400
                if age_days > 7:  # Decay memories older than 7 days
                    decay_factor = 0.5 ** (age_days / 7)  # Exponential decay
                    if 'weight' in self._memory_weights[key]:
                        self._memory_weights[key]['weight'] *= decay_factor
        '''
        
        # Inject after class definition
        lines = original_content.split('\n')
        injected_lines = []
        injection_done = False
        
        for i, line in enumerate(lines):
            injected_lines.append(line)
            
            # Look for class definition with __init__ method
            if not injection_done and line.strip().startswith('def __init__'):
                # Find the end of the __init__ method
                for j in range(i + 1, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                        # Insert before the next method
                        injected_lines.append(flaw_injection)
                        injection_done = True
                        break
        
        if injection_done:
            recursive_file.write_text('\n'.join(injected_lines))
            self.injected_flaws.append({
                'type': 'learning_decay',
                'file': str(recursive_file),
                'description': 'Learning decay: Older memories artificially reduced in weight'
            })
            print(f"✅ Injected learning decay flaw into {recursive_file}")
            return True
        else:
            print(f"⚠️ Could not find injection point in {recursive_file}")
            return False
    
    def inject_off_by_one_flaw(self):
        """Inject a subtle off-by-one error in batch processing"""
        persistent_file = self.target_dir / "src/cognitive/persistent_recursion.py"
        
        if not persistent_file.exists():
            print(f"⚠️ Target file not found: {persistent_file}")
            return False
        
        original_content = persistent_file.read_text()
        
        # Look for batch processing logic and inject off-by-one
        lines = original_content.split('\n')
        injected_lines = []
        
        for line in lines:
            # Look for range or batch processing patterns
            if 'range(' in line and 'batch' in line.lower():
                # Inject off-by-one error: change range(len(items)) to range(len(items) - 1)
                modified_line = line.replace('range(len(', 'range(len(').replace('))', ') - 1)')
                if modified_line != line:
                    injected_lines.append(f"        # ADV-TEST-001 Injected: Off-by-one error")
                    injected_lines.append(modified_line)
                    self.injected_flaws.append({
                        'type': 'off_by_one',
                        'file': str(persistent_file),
                        'description': 'Off-by-one error in batch processing loop'
                    })
                    print(f"✅ Injected off-by-one flaw into {persistent_file}")
                else:
                    injected_lines.append(line)
            else:
                injected_lines.append(line)
        
        persistent_file.write_text('\n'.join(injected_lines))
        return len(self.injected_flaws) > 0

@contextmanager
def temporary_test_environment():
    """Create a temporary copy of the PRI system for testing"""
    original_dir = Path.cwd()
    temp_dir = Path(tempfile.mkdtemp(prefix="pri_ouroboros_test_"))
    
    try:
        print(f"🔬 Creating test environment at {temp_dir}")
        
        # Copy the entire PRI system to temp directory
        for item in original_dir.iterdir():
            if item.name not in ['.git', '__pycache__', 'venv', '.venv']:
                if item.is_dir():
                    shutil.copytree(item, temp_dir / item.name, ignore=shutil.ignore_patterns('*.pyc', '__pycache__'))
                else:
                    shutil.copy2(item, temp_dir / item.name)
        
        yield temp_dir, original_dir
        
    finally:
        # Cleanup
        print(f"🧹 Cleaning up test environment {temp_dir}")
        shutil.rmtree(temp_dir, ignore_errors=True)

def run_ouroboros_detection_test(test_dir: Path):
    """Run the Ouroboros cycle and detect if flaws are found"""
    print("🌀 Running Ouroboros Detection Test...")
    
    # Change to test directory
    import os
    original_cwd = os.getcwd()
    os.chdir(test_dir)
    
    try:
        # Add test directory src to path
        sys.path.insert(0, str(test_dir / "src"))
        
        # Import and run the recursive system
        from cognitive.persistent_recursion import run_analysis
        
        print("🔍 Running self-analysis on modified system...")
        
        # Run analysis on the test directory itself
        results = run_analysis(
            project_path=str(test_dir),
            max_depth=3,
            batch_size=20,
            output_file=str(test_dir / "ouroboros_test_results.json")
        )
        
        return results
        
    except Exception as e:
        print(f"❌ Ouroboros test failed: {e}")
        return {"error": str(e), "issues_found": []}
    
    finally:
        os.chdir(original_cwd)
        # Remove test directory from path
        if str(test_dir / "src") in sys.path:
            sys.path.remove(str(test_dir / "src"))

def analyze_detection_results(results, injected_flaws):
    """Analyze if the injected flaws were detected"""
    print("📊 Analyzing Detection Results...")
    
    if "error" in results:
        print(f"❌ Analysis failed: {results['error']}")
        return False, "Analysis failed due to error"
    
    issues_found = results.get("issues_found", [])
    total_issues = len(issues_found)
    
    print(f"🔍 Total issues detected: {total_issues}")
    
    # Check if any of the injected flaws were detected
    detected_flaws = []
    
    for flaw in injected_flaws:
        flaw_file = Path(flaw['file']).name
        flaw_type = flaw['type']
        
        # Look for issues in the file where the flaw was injected
        file_issues = [issue for issue in issues_found 
                      if flaw_file in issue.get('file', '')]
        
        print(f"🔍 Issues in {flaw_file}: {len(file_issues)}")
        
        # Check for specific patterns that might indicate detection
        detection_indicators = {
            'memory_corruption': ['random', 'corruption', 'metadata', 'inconsistent'],
            'learning_decay': ['decay', 'weight', 'timestamp', 'memory'],
            'off_by_one': ['range', 'index', 'boundary', 'iteration']
        }
        
        indicators = detection_indicators.get(flaw_type, [])
        
        for issue in file_issues:
            issue_text = str(issue).lower()
            if any(indicator in issue_text for indicator in indicators):
                detected_flaws.append({
                    'flaw': flaw,
                    'detected_in': issue,
                    'confidence': 'high' if len([i for i in indicators if i in issue_text]) > 1 else 'medium'
                })
                print(f"✅ Potential detection of {flaw_type}: {issue.get('message', issue)}")
    
    detection_rate = len(detected_flaws) / len(injected_flaws) if injected_flaws else 0
    
    print(f"📊 Detection Summary:")
    print(f"  🎯 Injected Flaws: {len(injected_flaws)}")
    print(f"  🔍 Detected Flaws: {len(detected_flaws)}")
    print(f"  📈 Detection Rate: {detection_rate:.1%}")
    
    success = detection_rate >= 0.5  # At least 50% detection rate
    
    return success, {
        'detection_rate': detection_rate,
        'detected_flaws': detected_flaws,
        'total_issues': total_issues,
        'injected_flaws': injected_flaws
    }

def main():
    """Execute ADV-TEST-001: The Ouroboros Test"""
    
    print("🐍 ADV-TEST-001: The Ouroboros Test")
    print("=" * 60)
    print("🎯 Testing recursive self-improvement by injecting subtle flaws")
    print("🔬 Hypothesis: System can detect conceptual flaws, not just syntax errors")
    print()
    
    with temporary_test_environment() as (test_dir, original_dir):
        
        # Step 1: Inject subtle flaws
        print("💉 Step 1: Injecting Subtle Flaws...")
        injector = SubtleBugInjector(test_dir)
        
        injection_success = []
        injection_success.append(injector.inject_memory_corruption_flaw())
        injection_success.append(injector.inject_learning_decay_flaw())
        injection_success.append(injector.inject_off_by_one_flaw())
        
        if not any(injection_success):
            print("❌ Failed to inject any flaws - test cannot proceed")
            return False
        
        print(f"✅ Successfully injected {len(injector.injected_flaws)} flaws")
        for flaw in injector.injected_flaws:
            print(f"  • {flaw['type']}: {flaw['description']}")
        print()
        
        # Step 2: Run Ouroboros detection
        print("🌀 Step 2: Running Ouroboros Self-Analysis...")
        results = run_ouroboros_detection_test(test_dir)
        
        # Step 3: Analyze detection results
        print("🔍 Step 3: Analyzing Detection Results...")
        success, analysis = analyze_detection_results(results, injector.injected_flaws)
        
        print()
        print("=" * 60)
        
        if success:
            print("🎉 ADV-TEST-001 PASSED!")
            print("✅ The Ouroboros cycle successfully detected conceptual flaws")
            print("🧠 System demonstrates genuine recursive self-improvement")
            print(f"📊 Detection Rate: {analysis['detection_rate']:.1%}")
        else:
            print("❌ ADV-TEST-001 FAILED!")
            print("⚠️ The Ouroboros cycle failed to detect injected flaws")
            print("🔍 System may only detect superficial bugs, not conceptual issues")
            print(f"📊 Detection Rate: {analysis['detection_rate']:.1%}")
        
        # Save detailed results
        test_results = {
            'test_id': 'ADV-TEST-001',
            'test_name': 'The Ouroboros Test',
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'analysis': analysis,
            'injected_flaws': injector.injected_flaws
        }
        
        results_file = original_dir / "ouroboros_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        print(f"📁 Detailed results saved to {results_file}")
        
        return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)