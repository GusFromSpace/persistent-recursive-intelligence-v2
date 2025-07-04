#!/usr/bin/env python3
"""
OpenMW Real Bloodlust Cycles - Scan, Bloodlust Eliminate, Learn, Repeat

This actually eliminates issues between cycles using the bloodlust hunter
instead of the conservative mesopredator fix command.
"""

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class OpenMWBloodlustCycles:
    """Execute real hunting cycles with bloodlust elimination on OpenMW"""
    
    def __init__(self, openmw_path: str = "/home/gusfromspace/Development/persistent-recursive-intelligence/openmw_metrics_integration"):
        self.openmw_path = Path(openmw_path)
        self.cycles_complete = 0
        self.total_eliminations = 0
        self.cycle_results = []
        self.hunt_start_time = time.time()
        
    def execute_bloodlust_hunt(self, max_cycles: int = 7) -> Dict[str, Any]:
        """Execute real hunting cycles with bloodlust elimination between scans"""
        print("🔥" * 70)
        print("🦅 OPENMW REAL BLOODLUST CYCLES - SCAN, ELIMINATE, LEARN, REPEAT")
        print("🔥" * 70)
        print(f"📁 Target: {self.openmw_path}")
        print(f"🎯 Max Cycles: {max_cycles}")
        print(f"🧠 Strategy: Bloodlust elimination between cycles")
        print(f"⚡ Expected: Decreasing issues per cycle (actual learning)")
        print(f"💀 Elimination Tool: Mesopredator Bloodlust Hunter")
        print("🔥" * 70)
        
        for cycle in range(1, max_cycles + 1):
            print(f"\n🌀 CYCLE {cycle}/{max_cycles} - {self._get_cycle_name(cycle)}")
            print("=" * 50)
            
            # Step 1: Scan for issues
            scan_result = self._scan_for_issues(cycle)
            
            if scan_result["issues_found"] == 0:
                print("🏆 No more issues found - Hunt complete!")
                break
                
            # Step 2: Bloodlust eliminate issues
            elimination_result = self._bloodlust_eliminate(cycle, scan_result)
            
            # Step 3: Combine results
            cycle_result = {**scan_result, **elimination_result}
            self.cycle_results.append(cycle_result)
            self.cycles_complete = cycle
            
            # Show cycle summary
            self._display_cycle_summary(cycle, cycle_result)
            
            # Check if we actually eliminated issues
            if elimination_result.get("eliminations_completed", 0) == 0:
                print("⚠️  No eliminations - switching to maintenance mode")
                break
            
            # Brief pause for file system
            if cycle < max_cycles:
                print("⏳ Preparing next cycle...")
                time.sleep(2)
        
        # Final analysis
        final_results = self._generate_final_analysis()
        self._save_results(final_results)
        
        return final_results
    
    def _get_cycle_name(self, cycle: int) -> str:
        """Get thematic name for each cycle"""
        cycle_names = {
            1: "Genesis Scan & Bloodlust",
            2: "Consciousness Purge", 
            3: "Pattern Hunt & Kill",
            4: "Aggressive Elimination",
            5: "Precision Strike",
            6: "Final Cleanup",
            7: "Perfection Achievement"
        }
        return cycle_names.get(cycle, f"Bloodlust Cycle {cycle}")
    
    def _scan_for_issues(self, cycle: int) -> Dict[str, Any]:
        """Scan for issues using mesopredator"""
        print(f"🔍 Scanning for issues...")
        cycle_start = time.time()
        
        try:
            # Run mesopredator analysis
            output_file = f"openmw_bloodlust_cycle_{cycle}_scan.json"
            cmd = ["mesopredator", "analyze", str(self.openmw_path), "--output-file", output_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Parse results
            issues_found = self._extract_issues_count(result.stdout.split('\n'))
            scan_time = time.time() - cycle_start
            
            return {
                "cycle": cycle,
                "cycle_name": self._get_cycle_name(cycle),
                "timestamp": datetime.now().isoformat(),
                "scan_time_seconds": scan_time,
                "issues_found": issues_found,
                "scan_output_file": output_file,
                "scan_status": "success"
            }
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Scan failed: {e}")
            return {
                "cycle": cycle,
                "scan_status": "failed",
                "error": str(e)
            }
    
    def _bloodlust_eliminate(self, cycle: int, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Use bloodlust hunter to actually eliminate issues"""
        print(f"💀 Unleashing bloodlust hunter on {scan_result['issues_found']} issues...")
        
        if scan_result.get("scan_status") != "success":
            return {"elimination_status": "skipped", "eliminations": 0}
            
        eliminate_start = time.time()
        
        try:
            # Use bloodlust hunter for real elimination
            issues_file = scan_result["scan_output_file"]
            cmd = ["python3", "mesopredator_bloodlust_hunter.py", 
                   str(self.openmw_path), issues_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            eliminate_time = time.time() - eliminate_start
            
            # Parse bloodlust results from output
            eliminations = self._count_bloodlust_kills(result.stdout)
            
            self.total_eliminations += eliminations
            
            return {
                "eliminate_time_seconds": eliminate_time,
                "eliminations_attempted": scan_result['issues_found'],
                "eliminations_completed": eliminations,
                "elimination_rate": eliminations / eliminate_time if eliminate_time > 0 else 0,
                "elimination_status": "success" if eliminations > 0 else "no_targets",
                "total_eliminations": self.total_eliminations,
                "elimination_tool": "bloodlust_hunter"
            }
            
        except subprocess.TimeoutExpired:
            print("⏰ Bloodlust hunt timed out - proceeding to next cycle")
            return {
                "elimination_status": "timeout",
                "eliminations_completed": 0
            }
        except Exception as e:
            print(f"❌ Bloodlust hunt failed: {e}")
            return {
                "elimination_status": "failed", 
                "eliminations_completed": 0,
                "error": str(e)
            }
    
    def _extract_issues_count(self, output_lines: List[str]) -> int:
        """Extract issues count from mesopredator output"""
        for line in output_lines:
            if "issues" in line.lower() and "found" in line.lower():
                try:
                    # Extract number from "Found X issues" or "X issues found"
                    words = line.split()
                    for i, word in enumerate(words):
                        if word.isdigit():
                            return int(word)
                except:
                    pass
        return 0
    
    def _count_bloodlust_kills(self, output: str) -> int:
        """Count actual eliminations from bloodlust hunter output"""
        # Look for the final kill count
        lines = output.split('\n')
        
        for line in lines:
            if "TOTAL KILLS:" in line:
                try:
                    # Extract number from "💀 TOTAL KILLS: X"
                    kills = int(line.split("TOTAL KILLS:")[1].strip())
                    return kills
                except:
                    pass
        
        return 0
    
    def _display_cycle_summary(self, cycle: int, result: Dict[str, Any]):
        """Display summary for completed cycle"""
        print(f"✅ {result['cycle_name']} Complete!")
        print(f"   🔍 Issues Found: {result.get('issues_found', 0)}")
        print(f"   💀 Issues Eliminated: {result.get('eliminations_completed', 0)}")
        print(f"   ⏱️  Scan Time: {result.get('scan_time_seconds', 0):.2f}s")
        print(f"   ⚡ Elimination Time: {result.get('eliminate_time_seconds', 0):.2f}s")
        
        if result.get('eliminations_completed', 0) > 0:
            rate = result.get('elimination_rate', 0)
            print(f"   🔥 Kill Rate: {rate:.1f} eliminations/second")
        
        total_elims = result.get('total_eliminations', 0)
        print(f"   🎯 Total Eliminations: {total_elims}")
        
        # Progress indicator
        issues_remaining = result.get('issues_found', 0) - result.get('eliminations_completed', 0)
        if issues_remaining <= 0:
            print(f"   🏆 CODEBASE CLEAN!")
        else:
            print(f"   📊 Issues Remaining: ~{issues_remaining}")
            
        # Learning progress
        if len(self.cycle_results) > 1:
            prev_issues = self.cycle_results[-2].get('issues_found', 0)
            current_issues = result.get('issues_found', 0)
            if current_issues < prev_issues:
                improvement = prev_issues - current_issues
                print(f"   📈 LEARNING: {improvement} fewer issues than last cycle!")
    
    def _generate_final_analysis(self) -> Dict[str, Any]:
        """Generate comprehensive analysis of the bloodlust hunt"""
        hunt_end_time = time.time()
        total_hunt_time = hunt_end_time - self.hunt_start_time
        
        successful_cycles = [r for r in self.cycle_results if r.get("scan_status") == "success"]
        
        if successful_cycles:
            total_issues_found = sum(r.get("issues_found", 0) for r in successful_cycles)
            total_eliminations = sum(r.get("eliminations_completed", 0) for r in successful_cycles)
            
            # Calculate improvement trend
            issue_trend = [r.get("issues_found", 0) for r in successful_cycles]
            elimination_trend = [r.get("eliminations_completed", 0) for r in successful_cycles]
        else:
            total_issues_found = 0
            total_eliminations = 0
            issue_trend = []
            elimination_trend = []
        
        final_analysis = {
            "hunt_summary": {
                "total_cycles": self.cycles_complete,
                "successful_cycles": len(successful_cycles),
                "total_hunt_time_seconds": total_hunt_time,
                "total_issues_found": total_issues_found,
                "total_eliminations": total_eliminations,
                "net_improvement": total_eliminations,
                "hunt_efficiency": (total_eliminations / total_issues_found * 100) if total_issues_found > 0 else 0,
                "elimination_tool": "bloodlust_hunter"
            },
            "learning_metrics": {
                "issue_trend": issue_trend,
                "elimination_trend": elimination_trend,
                "learning_demonstrated": len(issue_trend) > 1 and issue_trend[-1] < issue_trend[0],
                "improvement_rate": (issue_trend[0] - issue_trend[-1]) / len(issue_trend) if len(issue_trend) > 1 else 0
            },
            "cycle_results": self.cycle_results
        }
        
        return final_analysis
    
    def _save_results(self, results: Dict[str, Any]):
        """Save hunt results to file"""
        results_file = f"openmw_bloodlust_cycles_{int(time.time())}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {results_file}")
    
    def display_final_results(self, results: Dict[str, Any]):
        """Display final hunt results"""
        print("\n" + "🔥" * 70)
        print("🏆 OPENMW REAL BLOODLUST CYCLES - FINAL RESULTS")
        print("🔥" * 70)
        
        summary = results["hunt_summary"]
        learning = results["learning_metrics"]
        
        print(f"📊 HUNT SUMMARY:")
        print(f"   🎯 Cycles Completed: {summary['total_cycles']}")
        print(f"   ⏱️  Total Hunt Time: {summary['total_hunt_time_seconds']:.2f}s")
        print(f"   🔍 Total Issues Found: {summary['total_issues_found']:,}")
        print(f"   💀 Total Eliminations: {summary['total_eliminations']:,}")
        print(f"   📈 Net Improvement: {summary['net_improvement']:,} issues eliminated")
        print(f"   🎯 Hunt Efficiency: {summary['hunt_efficiency']:.1f}%")
        print(f"   🔧 Elimination Tool: {summary['elimination_tool']}")
        
        print(f"\n🧠 LEARNING METRICS:")
        if learning["issue_trend"]:
            print(f"   📉 Issue Trend: {' → '.join(map(str, learning['issue_trend']))}")
        if learning["elimination_trend"]:
            print(f"   💀 Elimination Trend: {' → '.join(map(str, learning['elimination_trend']))}")
        print(f"   🎓 Learning Demonstrated: {'✅ YES' if learning['learning_demonstrated'] else '❌ NO'}")
        print(f"   📊 Improvement Rate: {learning['improvement_rate']:.1f} issues/cycle")
        
        if learning["learning_demonstrated"]:
            print(f"\n🏆 REAL BLOODLUST HUNTING ACHIEVED!")
            print(f"   The mesopredator bloodlust hunter successfully reduced issues over time!")
            print(f"   This demonstrates actual learning and code improvement!")
        else:
            print(f"\n⚠️  NO LEARNING DETECTED")
            print(f"   The hunt did not show improvement - consider different elimination strategies")
        
        print("\n" + "🔥" * 70)


def main():
    """Execute real bloodlust hunting cycles on OpenMW"""
    
    print("🦅 OPENMW REAL BLOODLUST CYCLES")
    print("This uses the bloodlust hunter to actually eliminate issues between scans!")
    print("Each cycle should find fewer issues as the codebase gets cleaner.")
    
    hunter = OpenMWBloodlustCycles()
    
    try:
        results = hunter.execute_bloodlust_hunt(max_cycles=7)
        hunter.display_final_results(results)
        
        print(f"\n🦅 Real bloodlust hunting complete.")
        print(f"💀 Check the results to see if issues actually decreased!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Hunt interrupted by user")
        print(f"🔥 Cycles completed: {hunter.cycles_complete}")
    except Exception as e:
        print(f"\n❌ Hunt failed: {e}")
        print(f"🔥 Cycles completed: {hunter.cycles_complete}")


if __name__ == "__main__":
    main()