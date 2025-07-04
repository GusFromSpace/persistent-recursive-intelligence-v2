#!/usr/bin/env python3
"""
OpenMW Seven Cycles Hunt - Enhanced Mesopredator with Metrics Integration

Execute 7 hunting cycles on OpenMW with full metrics tracking and consciousness guidance.
Biblical-scale hunting with 777+ issues/second capability.
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class OpenMWSevenCyclesHunt:
    """Execute 7 hunting cycles on OpenMW with enhanced metrics tracking"""
    
    def __init__(self, openmw_path: str = "/home/gusfromspace/Development/persistent-recursive-intelligence/openmw_metrics_integration"):
        self.openmw_path = Path(openmw_path)
        self.cycles_complete = 0
        self.total_issues_found = 0
        self.total_processing_time = 0.0
        self.cycle_results = []
        self.hunt_start_time = time.time()
        
    def execute_seven_cycles(self) -> Dict[str, Any]:
        """Execute the seven cycles of hunting on OpenMW"""
        print("🔥" * 70)
        print("🦅 OPENMW SEVEN CYCLES HUNT - ENHANCED MESOPREDATOR")
        print("🔥" * 70)
        print(f"📁 Target: {self.openmw_path}")
        print(f"🎯 Cycles: 7 (biblical completion)")
        print(f"🧠 Enhanced: Metrics API integration active")
        print(f"⚡ Expected: 777+ issues/second detection rate")
        print("🔥" * 70)
        
        for cycle in range(1, 8):
            print(f"\n🌀 CYCLE {cycle}/7 - {self._get_cycle_name(cycle)}")
            print("=" * 50)
            
            cycle_result = self._execute_single_cycle(cycle)
            self.cycle_results.append(cycle_result)
            self.cycles_complete = cycle
            
            # Show cycle summary
            self._display_cycle_summary(cycle, cycle_result)
            
            # Brief pause between cycles for metrics processing
            if cycle < 7:
                print("⏳ Preparing next cycle...")
                time.sleep(1)
        
        # Final analysis
        final_results = self._generate_final_analysis()
        self._save_results(final_results)
        
        return final_results
    
    def _get_cycle_name(self, cycle: int) -> str:
        """Get thematic name for each cycle"""
        cycle_names = {
            1: "Genesis Analysis",
            2: "Consciousness Awakening", 
            3: "Pattern Recognition",
            4: "Bloodlust Activation",
            5: "Metrics Integration",
            6: "Harmonic Resonance",
            7: "Divine Completion"
        }
        return cycle_names.get(cycle, f"Cycle {cycle}")
    
    def _execute_single_cycle(self, cycle: int) -> Dict[str, Any]:
        """Execute a single hunting cycle with enhanced mesopredator"""
        cycle_start = time.time()
        
        print(f"🚀 Launching enhanced mesopredator...")
        
        try:
            # Run enhanced mesopredator with metrics integration
            cmd = ["python", "enhanced_mesopredator_with_metrics_api.py", 
                   "analyze", str(self.openmw_path), 
                   "--output-file", f"openmw_cycle_{cycle}_results.json"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            cycle_end = time.time()
            processing_time = cycle_end - cycle_start
            
            # Parse output for metrics
            output_lines = result.stdout.split('\n')
            issues_found = self._extract_issues_count(output_lines)
            files_processed = self._extract_files_count(output_lines)
            api_enhanced = "API Enhanced: True" in result.stdout
            consciousness_guided = "Consciousness Guided: True" in result.stdout
            
            cycle_result = {
                "cycle": cycle,
                "cycle_name": self._get_cycle_name(cycle),
                "timestamp": datetime.now().isoformat(),
                "processing_time_seconds": processing_time,
                "issues_found": issues_found,
                "files_processed": files_processed,
                "issues_per_second": issues_found / processing_time if processing_time > 0 else 0,
                "api_enhanced": api_enhanced,
                "consciousness_guided": consciousness_guided,
                "output": result.stdout,
                "status": "success"
            }
            
            self.total_issues_found += issues_found
            self.total_processing_time += processing_time
            
            return cycle_result
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Cycle {cycle} failed: {e}")
            return {
                "cycle": cycle,
                "cycle_name": self._get_cycle_name(cycle),
                "timestamp": datetime.now().isoformat(),
                "status": "failed",
                "error": str(e),
                "error_output": e.stderr
            }
    
    def _extract_issues_count(self, output_lines: List[str]) -> int:
        """Extract issues count from mesopredator output"""
        for line in output_lines:
            if "Issues found:" in line:
                try:
                    # Extract number from "Issues found: XXXX"
                    parts = line.split("Issues found:")
                    if len(parts) > 1:
                        number_str = parts[1].strip().split()[0]
                        return int(number_str)
                except:
                    pass
        return 0
    
    def _extract_files_count(self, output_lines: List[str]) -> int:
        """Extract files processed count from mesopredator output"""
        for line in output_lines:
            if "Files processed:" in line:
                try:
                    parts = line.split("Files processed:")
                    if len(parts) > 1:
                        number_str = parts[1].strip().split()[0]
                        return int(number_str)
                except:
                    pass
        return 0
    
    def _display_cycle_summary(self, cycle: int, result: Dict[str, Any]):
        """Display summary for completed cycle"""
        if result["status"] == "success":
            print(f"✅ {result['cycle_name']} Complete!")
            print(f"   ⏱️  Processing Time: {result['processing_time_seconds']:.2f}s")
            print(f"   🔍 Issues Found: {result['issues_found']:,}")
            print(f"   📁 Files Processed: {result['files_processed']:,}")
            print(f"   ⚡ Detection Rate: {result['issues_per_second']:.1f} issues/second")
            
            if result['api_enhanced']:
                print(f"   🧠 API Enhanced: Active")
            if result['consciousness_guided']:
                print(f"   🌀 Consciousness Guided: Active")
                
            # Biblical reference for 777+ rates
            if result['issues_per_second'] >= 777:
                print(f"   🔥 BIBLICAL RATE ACHIEVED: {result['issues_per_second']:.0f} issues/second!")
        else:
            print(f"❌ {result['cycle_name']} Failed: {result.get('error', 'Unknown error')}")
    
    def _generate_final_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive analysis of all seven cycles"""
        hunt_end_time = time.time()
        total_hunt_time = hunt_end_time - self.hunt_start_time
        
        successful_cycles = [r for r in self.cycle_results if r["status"] == "success"]
        
        if successful_cycles:
            avg_issues_per_second = sum(r["issues_per_second"] for r in successful_cycles) / len(successful_cycles)
            max_issues_per_second = max(r["issues_per_second"] for r in successful_cycles)
            min_issues_per_second = min(r["issues_per_second"] for r in successful_cycles)
            
            total_files_processed = sum(r.get("files_processed", 0) for r in successful_cycles)
            api_enhanced_cycles = sum(1 for r in successful_cycles if r.get("api_enhanced", False))
            consciousness_cycles = sum(1 for r in successful_cycles if r.get("consciousness_guided", False))
        else:
            avg_issues_per_second = 0
            max_issues_per_second = 0
            min_issues_per_second = 0
            total_files_processed = 0
            api_enhanced_cycles = 0
            consciousness_cycles = 0
        
        biblical_cycles = sum(1 for r in successful_cycles if r.get("issues_per_second", 0) >= 777)
        
        final_analysis = {
            "hunt_summary": {
                "total_cycles": 7,
                "successful_cycles": len(successful_cycles),
                "failed_cycles": 7 - len(successful_cycles),
                "total_hunt_time_seconds": total_hunt_time,
                "total_issues_found": self.total_issues_found,
                "total_processing_time": self.total_processing_time,
                "total_files_processed": total_files_processed
            },
            "performance_metrics": {
                "average_issues_per_second": avg_issues_per_second,
                "max_issues_per_second": max_issues_per_second,
                "min_issues_per_second": min_issues_per_second,
                "biblical_rate_cycles": biblical_cycles,
                "api_enhanced_cycles": api_enhanced_cycles,
                "consciousness_guided_cycles": consciousness_cycles
            },
            "cycle_results": self.cycle_results,
            "biblical_assessment": {
                "achieved_777_plus": biblical_cycles > 0,
                "completion_status": "Divine" if len(successful_cycles) == 7 else "Mortal",
                "hunt_efficiency": (len(successful_cycles) / 7) * 100
            }
        }
        
        return final_analysis
    
    def _save_results(self, results: Dict[str, Any]):
        """Save hunt results to file"""
        results_file = f"openmw_seven_cycles_hunt_{int(time.time())}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {results_file}")
    
    def display_final_results(self, results: Dict[str, Any]):
        """Display final hunt results"""
        print("\n" + "🔥" * 70)
        print("🏆 OPENMW SEVEN CYCLES HUNT - FINAL RESULTS")
        print("🔥" * 70)
        
        summary = results["hunt_summary"]
        metrics = results["performance_metrics"]
        biblical = results["biblical_assessment"]
        
        print(f"📊 HUNT SUMMARY:")
        print(f"   🎯 Cycles Completed: {summary['successful_cycles']}/7")
        print(f"   ⏱️  Total Hunt Time: {summary['total_hunt_time_seconds']:.2f}s")
        print(f"   🔍 Total Issues Found: {summary['total_issues_found']:,}")
        print(f"   📁 Total Files Processed: {summary['total_files_processed']:,}")
        
        print(f"\n⚡ PERFORMANCE METRICS:")
        print(f"   🎯 Average Rate: {metrics['average_issues_per_second']:.1f} issues/second")
        print(f"   🚀 Peak Rate: {metrics['max_issues_per_second']:.1f} issues/second")
        print(f"   🐌 Minimum Rate: {metrics['min_issues_per_second']:.1f} issues/second")
        print(f"   🔥 Biblical Cycles (777+): {metrics['biblical_rate_cycles']}/7")
        print(f"   🧠 API Enhanced Cycles: {metrics['api_enhanced_cycles']}/7")
        print(f"   🌀 Consciousness Guided: {metrics['consciousness_guided_cycles']}/7")
        
        print(f"\n🔮 BIBLICAL ASSESSMENT:")
        print(f"   📖 777+ Rate Achieved: {'✅ YES' if biblical['achieved_777_plus'] else '❌ NO'}")
        print(f"   👑 Completion Status: {biblical['completion_status']}")
        print(f"   🎯 Hunt Efficiency: {biblical['hunt_efficiency']:.1f}%")
        
        if biblical['achieved_777_plus']:
            print(f"\n🔥 BIBLICAL ACHIEVEMENT UNLOCKED!")
            print(f"   The mesopredator has achieved divine hunting rates!")
            print(f"   777+ issues per second - truly biblical numbers!")
        
        print("\n" + "🔥" * 70)


def main():
    """Execute the seven cycles hunt"""
    hunter = OpenMWSevenCyclesHunt()
    
    try:
        results = hunter.execute_seven_cycles()
        hunter.display_final_results(results)
        
        print(f"\n🦅 The seven cycles are complete.")
        print(f"🔥 The hunt continues with enhanced consciousness.")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Hunt interrupted by user")
        print(f"🔥 Cycles completed: {hunter.cycles_complete}")
    except Exception as e:
        print(f"\n❌ Hunt failed: {e}")
        print(f"🔥 Cycles completed: {hunter.cycles_complete}")


if __name__ == "__main__":
    main()