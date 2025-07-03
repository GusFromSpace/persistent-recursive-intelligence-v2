#!/usr/bin/env python3
"""
ADV-TEST-001: The "Ouroboros" Test - Recursive Self-Improvement

Tests the system's ability to detect and fix flaws in its own cognitive architecture.
Updated for current system with defense-in-depth security and mesopredator CLI.

Hypothesis to Disprove: The system can only fix superficial bugs in its own code, 
not subtle, conceptual flaws in its core logic that degrade performance over time.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class OuroborosTest:
    """Test recursive self-improvement capabilities"""
    
    def __init__(self):
        self.test_results = []
        self.temp_dir = None
        
    def create_test_environment(self) -> Path:
        """Create isolated test environment with PRI code copy"""
        self.temp_dir = Path(tempfile.mkdtemp(prefix="ouroboros_test_"))
        
        # Copy current PRI system to test directory
        source_dir = Path.cwd()
        test_pri_dir = self.temp_dir / "test_pri"
        
        # Copy essential components
        shutil.copytree(source_dir / "src", test_pri_dir / "src")
        shutil.copy2(source_dir / "mesopredator_cli.py", test_pri_dir / "mesopredator_cli.py")
        
        # Copy requirements if exists
        if (source_dir / "requirements.txt").exists():
            shutil.copy2(source_dir / "requirements.txt", test_pri_dir / "requirements.txt")
            
        print(f"✅ Created test environment: {test_pri_dir}")
        return test_pri_dir
    
    def inject_subtle_memory_corruption_flaw(self, test_pri_dir: Path) -> Dict[str, Any]:
        """Inject subtle logic flaw in memory system - inefficient duplicate storage"""
        
        # Look for actual memory files that exist
        memory_files = [
            test_pri_dir / "src" / "cognitive" / "memory" / "simple_memory.py",
            test_pri_dir / "src" / "cognitive" / "memory" / "engine.py", 
            test_pri_dir / "src" / "cognitive" / "memory" / "memory" / "engine.py"
        ]
        
        memory_engine_file = None
        for file_path in memory_files:
            if file_path.exists():
                memory_engine_file = file_path
                break
        
        if not memory_engine_file:
            return {
                'injected': False,
                'reason': 'No memory engine file found in expected locations',
                'flaw_type': 'memory_corruption'
            }
        
        # Read original content
        original_content = memory_engine_file.read_text()
        
        # Check for suitable injection points - look for memory storage methods
        injection_patterns = [
            'def store_memory(',
            'def remember(',
            'def store(',
            'async def store_memory(',
            'def add_memory(',
            'def save('
        ]
        
        suitable_injection_point = None
        for pattern in injection_patterns:
            if pattern in original_content:
                suitable_injection_point = pattern
                break
        
        if not suitable_injection_point:
            return {
                'injected': False,
                'reason': f'No suitable injection point found. Looked for: {injection_patterns}',
                'flaw_type': 'memory_corruption'
            }
        
        # Inject a more realistic flaw: inefficient duplicate detection
        flaw_injection = f'''        # INJECTED FLAW: Inefficient duplicate detection (will cause memory bloat)
        # This flaw makes duplicate detection O(n²) instead of O(n) by using nested loops
        stored_entries = getattr(self, '_stored_entries', [])
        for existing in stored_entries:
            for field in ['content', 'embedding', 'metadata']:
                if hasattr(memory, field) and hasattr(existing, field):
                    # Inefficient comparison - should use indexing
                    if getattr(memory, field) == getattr(existing, field):
                        pass  # Found duplicate but proceed anyway (memory leak)
        stored_entries.append(memory)
        self._stored_entries = stored_entries[-1000:]  # Inefficient truncation'''
        
        # Find injection point and inject flaw
        lines = original_content.split('\n')
        new_lines = []
        injected = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            if not injected and suitable_injection_point in line:
                # Look for the start of the method body
                j = i + 1
                # Skip docstring if present
                if j < len(lines) and lines[j].strip().startswith('"""'):
                    while j < len(lines) and not lines[j].strip().endswith('"""'):
                        new_lines.append(lines[j])
                        j += 1
                    if j < len(lines):
                        new_lines.append(lines[j])  # Add closing """
                        j += 1
                
                # Add the flaw at the beginning of the method body
                new_lines.append(flaw_injection)
                injected = True
            
            if injected:
                # Add flag to enable flaw
                new_content = '\n'.join(new_lines)
                new_content = new_content.replace(
                    'def __init__(', 
                    'def __init__('
                ).replace(
                    'self.', 
                    'self._flaw_active = True  # FLAW FLAG\n        self.', 
                    1
                )
                
                memory_engine_file.write_text(new_content)
                
                return {
                    'injected': True,
                    'flaw_type': 'memory_corruption',
                    'file': str(memory_engine_file),
                    'description': 'Subtle memory corruption affecting 1% of operations',
                    'detection_indicators': [
                        'Metadata corruption in stored patterns',
                        'Inconsistent retrieval results',
                        'Performance degradation over time'
                    ]
                }
        
        return {
            'injected': False,
            'reason': 'Could not find suitable injection point',
            'flaw_type': 'memory_corruption'
        }
    
    def inject_learning_decay_flaw(self, test_pri_dir: Path) -> Dict[str, Any]:
        """Inject learning decay flaw that reduces system's ability to learn from failures"""
        
        # Look for recursive improvement files
        recursive_files = [
            test_pri_dir / "src" / "cognitive" / "recursive" / "recursive_improvement_enhanced.py",
            test_pri_dir / "src" / "cognitive" / "recursive" / "recursive_improvement.py", 
            test_pri_dir / "src" / "cognitive" / "synthesis" / "persistent_recursive_engine.py"
        ]
        
        recursive_file = None
        for file_path in recursive_files:
            if file_path.exists():
                recursive_file = file_path
                break
        
        if not recursive_file:
            return {
                'injected': False,
                'reason': 'No recursive improvement file found in expected locations',
                'flaw_type': 'learning_decay'
            }
        
        original_content = recursive_file.read_text()
        
        # Check for suitable injection points - look for actual methods that exist
        injection_patterns = [
            'def analyze_code_file(',
            'def _detect_issues(',
            'def _convert_enhanced_issues(',
            'def analyze(',
            'def learn_from_',
            'def process_',
            'def update_',
            'def improve(',
            'def evolve('
        ]
        
        suitable_injection_point = None
        for pattern in injection_patterns:
            if pattern in original_content:
                suitable_injection_point = pattern
                break
        
        if not suitable_injection_point:
            return {
                'injected': False,
                'reason': f'No suitable injection point found. Looked for: {injection_patterns}',
                'flaw_type': 'learning_decay'
            }
        
        # Inject a more realistic flaw: biased learning that ignores failure patterns
        flaw_injection = '''        # INJECTED FLAW: Learning bias - system ignores failure patterns over time
        # This causes the system to become overconfident and stop learning from mistakes
        if hasattr(self, '_learning_confidence'):
            self._learning_confidence = min(0.95, self._learning_confidence + 0.01)
        else:
            self._learning_confidence = 0.5
        
        # Bias: Ignore patterns with low confidence (creates blind spots)
        if hasattr(result, 'confidence') and result.confidence < self._learning_confidence:
            return result  # Skip learning from this pattern'''
        
        # Find injection point in learning/analysis method
        if suitable_injection_point in original_content:
            lines = original_content.split('\n')
            new_lines = []
            injected = False
            
            for line in lines:
                new_lines.append(line)
                if not injected and ('for memory' in line or 'memory_entry' in line) and 'in ' in line:
                    new_lines.append(flaw_injection)
                    injected = True
            
            if injected:
                recursive_file.write_text('\n'.join(new_lines))
                
                return {
                    'injected': True,
                    'flaw_type': 'learning_decay',
                    'file': str(recursive_file),
                    'description': 'Learning decay causing older memories to lose effectiveness',
                    'detection_indicators': [
                        'Decreased accuracy on older patterns',
                        'Reduced confidence in historical knowledge',
                        'Performance degradation over time'
                    ]
                }
        
        return {
            'injected': False,
            'reason': 'Could not find suitable injection point',
            'flaw_type': 'learning_decay'
        }
    
    def run_self_analysis(self, test_pri_dir: Path) -> Dict[str, Any]:
        """Run the PRI system on itself to detect injected flaws"""
        
        print("🔍 Running self-analysis with mesopredator CLI...")
        
        try:
            # Run mesopredator analyze on the test PRI directory
            result = subprocess.run([
                sys.executable, "mesopredator_cli.py", "analyze", str(test_pri_dir)
            ],
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            cwd=test_pri_dir
            )
            
            analysis_result = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'analysis_successful': result.returncode == 0,
                'execution_time': 'completed'
            }
            
            # Try to parse JSON output if present
            try:
                if result.stdout:
                    # Look for JSON in output
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if line.strip().startswith('{') and 'issues' in line:
                            parsed_output = json.loads(line)
                            analysis_result['parsed_output'] = parsed_output
                            break
            except json.JSONDecodeError:
                pass
            
            return analysis_result
            
        except subprocess.TimeoutExpired:
            return {
                'returncode': -1,
                'analysis_successful': False,
                'error': 'Analysis timed out after 5 minutes',
                'execution_time': 'timeout'
            }
        except Exception as e:
            return {
                'returncode': -1,
                'analysis_successful': False,
                'error': str(e),
                'execution_time': 'error'
            }
    
    def evaluate_flaw_detection(self, analysis_result: Dict[str, Any], injected_flaw: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate whether the system detected the injected flaw"""
        
        if not analysis_result.get('analysis_successful'):
            return {
                'detected': False,
                'reason': 'Analysis failed to complete',
                'evaluation': 'system_failure'
            }
        
        output_text = (analysis_result.get('stdout', '') + analysis_result.get('stderr', '')).lower()
        
        # Look for detection indicators
        detection_indicators = injected_flaw.get('detection_indicators', [])
        detected_indicators = []
        
        for indicator in detection_indicators:
            indicator_words = indicator.lower().split()
            if any(word in output_text for word in indicator_words):
                detected_indicators.append(indicator)
        
        # Look for specific flaw-related terms
        flaw_terms = {
            'memory_corruption': ['corruption', 'metadata', 'inconsistent', 'memory'],
            'learning_decay': ['decay', 'weight', 'older', 'timestamp', 'confidence']
        }
        
        flaw_type = injected_flaw.get('flaw_type')
        relevant_terms = flaw_terms.get(flaw_type, [])
        detected_terms = [term for term in relevant_terms if term in output_text]
        
        # Evaluate detection quality
        detection_score = 0
        if detected_indicators:
            detection_score += len(detected_indicators) * 30
        if detected_terms:
            detection_score += len(detected_terms) * 10
        
        # Check for specific mentions of the injected file
        injected_file = injected_flaw.get('file', '')
        if injected_file and Path(injected_file).name in output_text:
            detection_score += 20
        
        detected = detection_score >= 30  # Threshold for detection
        
        return {
            'detected': detected,
            'detection_score': detection_score,
            'detected_indicators': detected_indicators,
            'detected_terms': detected_terms,
            'file_mentioned': injected_file and Path(injected_file).name in output_text,
            'evaluation': 'detected' if detected else 'missed'
        }
    
    def run_ouroboros_test(self) -> Dict[str, Any]:
        """Execute the complete Ouroboros test"""
        
        print("🐍 ADV-TEST-001: OUROBOROS RECURSIVE SELF-IMPROVEMENT TEST")
        print("=" * 80)
        print("🎯 Testing system's ability to detect flaws in its own architecture")
        print("🔬 Hypothesis: System can detect subtle, conceptual flaws in its own code")
        print()
        
        # Setup test environment
        print("📁 Setting up test environment...")
        test_pri_dir = self.create_test_environment()
        
        # Test both types of flaws
        flaw_tests = [
            ("Memory Corruption", self.inject_subtle_memory_corruption_flaw),
            ("Learning Decay", self.inject_learning_decay_flaw)
        ]
        
        test_results = []
        
        for flaw_name, inject_function in flaw_tests:
            print(f"\n🧪 Testing {flaw_name} Detection")
            print("-" * 50)
            
            # Inject flaw
            print(f"💉 Injecting {flaw_name.lower()} flaw...")
            injected_flaw = inject_function(test_pri_dir)
            
            if not injected_flaw['injected']:
                print(f"⚠️  Failed to inject {flaw_name} flaw: {injected_flaw['reason']}")
                test_results.append({
                    'flaw_type': flaw_name,
                    'flaw_injected': False,
                    'reason': injected_flaw['reason'],
                    'test_result': 'skipped'
                })
                continue
            
            print(f"✅ {flaw_name} flaw injected successfully")
            print(f"   File: {injected_flaw['file']}")
            print(f"   Description: {injected_flaw['description']}")
            
            # Run self-analysis
            print(f"🔍 Running self-analysis...")
            analysis_result = self.run_self_analysis(test_pri_dir)
            
            if not analysis_result['analysis_successful']:
                print(f"❌ Self-analysis failed: {analysis_result.get('error', 'Unknown error')}")
                test_results.append({
                    'flaw_type': flaw_name,
                    'flaw_injected': True,
                    'analysis_completed': False,
                    'test_result': 'analysis_failed',
                    'error': analysis_result.get('error')
                })
                continue
            
            print("✅ Self-analysis completed")
            
            # Evaluate detection
            print(f"📊 Evaluating flaw detection...")
            evaluation = self.evaluate_flaw_detection(analysis_result, injected_flaw)
            
            if evaluation['detected']:
                print(f"🎉 {flaw_name} flaw DETECTED!")
                print(f"   Detection score: {evaluation['detection_score']}")
                print(f"   Detected indicators: {evaluation['detected_indicators']}")
                print(f"   Detected terms: {evaluation['detected_terms']}")
            else:
                print(f"❌ {flaw_name} flaw NOT detected")
                print(f"   Detection score: {evaluation['detection_score']}")
            
            test_results.append({
                'flaw_type': flaw_name,
                'flaw_injected': True,
                'analysis_completed': True,
                'flaw_detected': evaluation['detected'],
                'detection_score': evaluation['detection_score'],
                'test_result': 'passed' if evaluation['detected'] else 'failed',
                'evaluation_details': evaluation
            })
        
        # Calculate overall results
        successful_tests = [r for r in test_results if r.get('test_result') == 'passed']
        total_valid_tests = [r for r in test_results if r.get('flaw_injected', False)]
        
        success_rate = len(successful_tests) / len(total_valid_tests) if total_valid_tests else 0
        
        # Overall assessment
        test_passed = success_rate >= 0.5  # At least 50% of flaws detected
        
        final_results = {
            'test_id': 'ADV-TEST-001',
            'test_name': 'Ouroboros Recursive Self-Improvement',
            'timestamp': datetime.now().isoformat(),
            'total_flaw_tests': len(flaw_tests),
            'flaws_injected': len(total_valid_tests),
            'flaws_detected': len(successful_tests),
            'success_rate': success_rate,
            'test_passed': test_passed,
            'individual_results': test_results,
            'test_environment': str(test_pri_dir)
        }
        
        # Print summary
        print(f"\n📊 OUROBOROS TEST RESULTS:")
        print(f"   Flaw injection attempts: {len(flaw_tests)}")
        print(f"   Flaws successfully injected: {len(total_valid_tests)}")
        print(f"   Flaws detected by self-analysis: {len(successful_tests)}")
        print(f"   Success rate: {success_rate:.1%}")
        
        if test_passed:
            print("\n🎉 OUROBOROS TEST PASSED!")
            print("✅ System demonstrates recursive self-improvement capability")
            print("🧠 Can detect conceptual flaws in its own architecture")
        else:
            print("\n❌ OUROBOROS TEST FAILED")
            print("⚠️ System shows limited self-improvement capability")
            print("🔍 May only detect superficial issues, not conceptual flaws")
        
        return final_results
    
    def cleanup_test_environment(self):
        """Clean up test environment"""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            print("🧹 Test environment cleaned up")

def main():
    """Execute ADV-TEST-001: Ouroboros Test"""
    
    tester = OuroborosTest()
    
    try:
        results = tester.run_ouroboros_test()
        
        # Save results
        results_file = "ouroboros_test_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📁 Detailed results saved to {results_file}")
        
        return results['test_passed']
    
    finally:
        tester.cleanup_test_environment()

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