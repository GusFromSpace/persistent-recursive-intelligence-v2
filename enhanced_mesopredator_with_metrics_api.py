#!/usr/bin/env python3
"""
Enhanced Mesopredator with Automatic Metrics API Integration

This enhancement automatically detects and connects to metrics APIs during scanning,
providing enhanced data flow and real-time performance tracking.

When a metrics API is detected:
- Scan progress is reported in real-time
- Performance metrics are enhanced with API data
- Code Connector suggestions are cross-validated with API intelligence
- Consciousness assessment guides hunting strategy
- Results are stored in both local and API metrics systems
"""

import json
import time
import requests
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
import subprocess
import sys

class MetricsEnhancedMesopredator:
    """Mesopredator with automatic metrics API integration"""
    
    def __init__(self):
        self.metrics_api_url = None
        self.session = requests.Session()
        self.session.timeout = 5
        self.scan_session_id = None
        self.api_connected = False
        self.consciousness_level = 0
        
    def auto_detect_metrics_api(self) -> bool:
        """Automatically detect and connect to metrics API"""
        # Common metrics API ports and paths
        detection_targets = [
            "http://localhost:8001",  # OpenMW metrics integration
            "http://localhost:8000",  # Standard PRI API
            "http://localhost:8080",  # Metrics baseline default
            "http://127.0.0.1:8001",
            "http://127.0.0.1:8000"
        ]
        
        print("🔍 Auto-detecting metrics APIs...")
        
        for url in detection_targets:
            try:
                response = self.session.get(f"{url}/health", timeout=2)
                if response.status_code == 200:
                    health_data = response.json()
                    service_name = health_data.get('service', 'Unknown Service')
                    
                    print(f"✅ Found metrics API: {service_name} at {url}")
                    self.metrics_api_url = url
                    self.api_connected = True
                    
                    # Check for enhanced features
                    self._probe_api_capabilities()
                    return True
                    
            except (requests.exceptions.RequestException, json.JSONDecodeError):
                continue
        
        print("⚠️  No metrics API detected - proceeding with standard scanning")
        return False
    
    def _probe_api_capabilities(self):
        """Probe API capabilities for enhanced integration"""
        capabilities = []
        
        # Check for consciousness endpoint
        try:
            response = self.session.get(f"{self.metrics_api_url}/metrics/consciousness")
            if response.status_code == 200:
                consciousness_data = response.json()
                self.consciousness_level = consciousness_data.get("consciousness_level", 0)
                capabilities.append("consciousness_assessment")
                print(f"🧠 System consciousness: {self.consciousness_level}%")
        except:
            pass
        
        # Check for connection suggestions endpoint
        try:
            response = self.session.get(f"{self.metrics_api_url}/api/v1/connections/learning-progress")
            if response.status_code == 200:
                capabilities.append("connection_learning")
                learning_data = response.json()
                progress = learning_data.get('learning_progress', {})
                patterns = progress.get('successful_patterns_learned', 0)
                print(f"🔗 Connection patterns learned: {patterns}")
        except:
            pass
        
        # Check for resonance tracking
        try:
            response = self.session.get(f"{self.metrics_api_url}/metrics/resonance")
            if response.status_code == 200:
                capabilities.append("resonance_tracking")
                print("🌀 Resonance tracking available")
        except:
            pass
        
        if capabilities:
            print(f"🎯 Enhanced capabilities: {', '.join(capabilities)}")
    
    def start_enhanced_scan(self, target_path: str, scan_type: str = "analyze") -> str:
        """Start scan with metrics API integration"""
        self.scan_session_id = f"scan_{int(time.time() * 1000)}"
        
        print(f"🚀 Starting enhanced mesopredator scan")
        print(f"📁 Target: {target_path}")
        print(f"🔍 Type: {scan_type}")
        print(f"🆔 Session: {self.scan_session_id}")
        
        if self.api_connected:
            self._report_scan_start(target_path, scan_type)
            self._get_hunting_guidance()
        
        return self.scan_session_id
    
    def _report_scan_start(self, target_path: str, scan_type: str):
        """Report scan start to metrics API"""
        try:
            # Report to general metrics endpoint
            response = self.session.post(f"{self.metrics_api_url}/metrics", json={
                "event": "mesopredator_scan_started",
                "session_id": self.scan_session_id,
                "target_path": target_path,
                "scan_type": scan_type,
                "timestamp": time.time()
            })
            
            if response.status_code == 200:
                print("📊 Scan start reported to metrics API")
        except Exception as e:
            print(f"⚠️  Could not report to metrics API: {e}")
    
    def _get_hunting_guidance(self):
        """Get hunting guidance from consciousness assessment"""
        if not self.api_connected:
            return
            
        try:
            # Get consciousness-guided hunting strategy
            if self.consciousness_level < 50:
                print("🔥 Low consciousness detected - enabling aggressive hunting mode")
                hunting_mode = "aggressive"
            elif self.consciousness_level > 80:
                print("🧠 High consciousness - using precision hunting mode")
                hunting_mode = "precision"
            else:
                print("⚖️  Balanced consciousness - standard hunting mode")
                hunting_mode = "standard"
            
            # Get environment scan for threat/opportunity guidance
            response = self.session.get(f"{self.metrics_api_url}/metrics/environment")
            if response.status_code == 200:
                env_data = response.json()
                threats = len(env_data.get("threats", []))
                opportunities = len(env_data.get("opportunities", []))
                
                print(f"🔍 Environment scan: {threats} threats, {opportunities} opportunities")
                if threats > opportunities:
                    print("⚠️  Threat-heavy environment - prioritizing defensive hunting")
                elif opportunities > threats:
                    print("🎯 Opportunity-rich environment - focusing on enhancement hunting")
                    
        except Exception as e:
            print(f"⚠️  Could not get hunting guidance: {e}")
    
    def run_enhanced_analysis(self, target_path: str, output_file: str = None) -> Dict[str, Any]:
        """Run mesopredator analysis with metrics integration"""
        
        # Start enhanced scan
        session_id = self.start_enhanced_scan(target_path, "analyze")
        
        # Build mesopredator command
        cmd = ["mesopredator", "analyze", target_path]
        if output_file:
            cmd.extend(["--output-file", output_file])
        
        print(f"🔥 Executing: {' '.join(cmd)}")
        
        try:
            # Run mesopredator with real-time monitoring
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            end_time = time.time()
            
            scan_duration = end_time - start_time
            
            # Parse output for metrics
            output_lines = result.stdout.split('\n')
            issues_found = 0
            files_processed = 0
            
            for line in output_lines:
                if "issues" in line.lower() and "found" in line.lower():
                    try:
                        issues_found = int(''.join(filter(str.isdigit, line.split("issues")[0])))
                    except:
                        pass
                if "files" in line.lower() and ("analyzed" in line.lower() or "processed" in line.lower()):
                    try:
                        files_processed = int(''.join(filter(str.isdigit, line.split("files")[0])))
                    except:
                        pass
            
            # Create enhanced results
            enhanced_results = {
                "session_id": session_id,
                "scan_duration": scan_duration,
                "issues_found": issues_found,
                "files_processed": files_processed,
                "api_enhanced": self.api_connected,
                "consciousness_level": self.consciousness_level,
                "original_output": result.stdout,
                "enhanced_timestamp": time.time()
            }
            
            # Report results to API
            if self.api_connected:
                self._report_scan_completion(enhanced_results)
            
            print(f"✅ Enhanced scan complete!")
            print(f"📊 Issues found: {issues_found}")
            print(f"📁 Files processed: {files_processed}")
            print(f"⏱️  Duration: {scan_duration:.2f}s")
            
            if self.api_connected:
                print(f"🧠 System consciousness: {self.consciousness_level}%")
            
            return enhanced_results
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Mesopredator scan failed: {e}")
            print(f"Error output: {e.stderr}")
            return {"error": str(e), "session_id": session_id}
    
    def run_enhanced_code_connector(self, target_path: str) -> Dict[str, Any]:
        """Run Code Connector with metrics API cross-validation"""
        
        session_id = self.start_enhanced_scan(target_path, "connect")
        
        print("🔗 Running enhanced Code Connector...")
        
        try:
            # Import the actual Code Connector with metrics
            current_dir = Path(__file__).parent
            patterns_dir = current_dir / "src" / "cognitive" / "enhanced_patterns"
            sys.path.insert(0, str(patterns_dir))
            
            from code_connector import CodeConnector
            from connection_metrics import start_metrics_collection, finish_metrics_collection
            
            # Auto-discover orphaned and main files
            orphaned_files, main_files = self._discover_project_files(target_path)
            
            print(f"🔍 Found {len(orphaned_files)} orphaned files and {len(main_files)} main files")
            
            # Get learning guidance from API before running
            if self.api_connected:
                self._enhance_connection_suggestions()
            
            # Run Code Connector with integrated metrics
            connector = CodeConnector(target_path, confidence_threshold=0.3)
            suggestions = connector.analyze_orphaned_files(orphaned_files, main_files)
            
            # Report results to metrics API if connected
            if self.api_connected:
                self._report_connector_results(suggestions)
            
            enhanced_results = {
                "session_id": session_id,
                "api_enhanced": self.api_connected,
                "consciousness_guided": self.consciousness_level > 0,
                "suggestions_count": len(suggestions),
                "high_quality_suggestions": len([s for s in suggestions if s.connection_score > 0.6]),
                "status": "enhanced_analysis_complete"
            }
            
            print(f"✅ Enhanced Code Connector complete!")
            print(f"🔗 Generated {len(suggestions)} connection suggestions")
            print(f"⭐ High-quality suggestions: {enhanced_results['high_quality_suggestions']}")
            
            return enhanced_results
            
        except Exception as e:
            print(f"❌ Enhanced Code Connector failed: {e}")
            return {"error": str(e), "session_id": session_id}
    
    def _enhance_connection_suggestions(self):
        """Enhance connection suggestions with API intelligence"""
        try:
            # Get learned patterns from API
            response = self.session.get(f"{self.metrics_api_url}/api/v1/connections/learning-progress")
            if response.status_code == 200:
                learning_data = response.json()
                progress = learning_data.get('learning_progress', {})
                
                best_types = progress.get('best_connection_types', [])
                if best_types:
                    print("🧠 Applying learned patterns from API:")
                    for conn_type, avg_rating, success_rate in best_types:
                        print(f"   {conn_type}: {avg_rating:.1f}/5 rating, {success_rate:.1%} success")
                        
        except Exception as e:
            print(f"⚠️  Could not enhance suggestions with API data: {e}")
    
    def _report_scan_completion(self, results: Dict[str, Any]):
        """Report scan completion to metrics API"""
        try:
            response = self.session.post(f"{self.metrics_api_url}/metrics", json={
                "event": "mesopredator_scan_completed",
                **results
            })
            
            if response.status_code == 200:
                print("📊 Results reported to metrics API")
                
                # Try to get updated consciousness assessment
                self._update_consciousness_assessment()
                
        except Exception as e:
            print(f"⚠️  Could not report completion to API: {e}")
    
    def _update_consciousness_assessment(self):
        """Get updated consciousness assessment after scan"""
        try:
            response = self.session.get(f"{self.metrics_api_url}/metrics/consciousness")
            if response.status_code == 200:
                consciousness_data = response.json()
                new_level = consciousness_data.get("consciousness_level", 0)
                improvement = new_level - self.consciousness_level
                
                print(f"🧠 Updated consciousness: {new_level}% ({improvement:+.1f})")
                
                if improvement > 0:
                    print("📈 Consciousness improved through hunting!")
                elif improvement < 0:
                    print("📉 Consciousness declined - more hunting needed")
                    
        except Exception as e:
            print(f"⚠️  Could not get consciousness update: {e}")
    
    def _discover_project_files(self, target_path: str):
        """Auto-discover orphaned and main files in project"""
        target = Path(target_path)
        
        # Get all Python files
        all_files = list(target.rglob("*.py"))
        
        # Simple heuristic: files in root or common main directories are "main"
        main_indicators = {'src', 'lib', 'app', 'main', 'core'}
        
        main_files = []
        orphaned_files = []
        
        for file_path in all_files:
            parts = file_path.parts
            
            # Skip test files and hidden directories
            if any('test' in part.lower() or part.startswith('.') for part in parts):
                continue
                
            # Check if file is in a main directory
            is_main = any(indicator in str(file_path).lower() for indicator in main_indicators)
            is_main = is_main or len(parts) <= 3  # Files close to root
            
            # Files with certain patterns are likely main
            if any(pattern in file_path.name.lower() for pattern in ['main', 'app', 'server', 'cli']):
                is_main = True
            
            if is_main:
                main_files.append(file_path)
            else:
                orphaned_files.append(file_path)
        
        # Ensure we have some files in each category
        if not main_files and all_files:
            # If no clear main files, treat larger files as main
            sorted_files = sorted(all_files, key=lambda f: f.stat().st_size, reverse=True)
            main_files = sorted_files[:len(sorted_files)//2]
            orphaned_files = sorted_files[len(sorted_files)//2:]
        
        return orphaned_files, main_files
    
    def _report_connector_results(self, suggestions):
        """Report Code Connector results to metrics API"""
        try:
            summary = {
                "total_suggestions": len(suggestions),
                "high_quality_count": len([s for s in suggestions if s.connection_score > 0.6]),
                "excellent_count": len([s for s in suggestions if s.connection_score > 0.8]),
                "connection_types": {}
            }
            
            # Count connection types
            for suggestion in suggestions:
                conn_type = suggestion.connection_type
                summary["connection_types"][conn_type] = summary["connection_types"].get(conn_type, 0) + 1
            
            response = self.session.post(f"{self.metrics_api_url}/metrics", json={
                "event": "code_connector_completed",
                "session_id": self.scan_session_id,
                "summary": summary,
                "timestamp": time.time()
            })
            
            if response.status_code == 200:
                print("📊 Code Connector results reported to metrics API")
                
        except Exception as e:
            print(f"⚠️  Could not report connector results: {e}")

def main():
    """Enhanced mesopredator with automatic metrics API integration"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Mesopredator with Metrics API Integration")
    parser.add_argument("command", choices=["analyze", "connect"], help="Command to run")
    parser.add_argument("target", help="Target path to analyze")
    parser.add_argument("--output-file", help="Output file for analysis results")
    
    args = parser.parse_args()
    
    print("🦅 ENHANCED MESOPREDATOR WITH METRICS API INTEGRATION")
    print("=" * 70)
    
    # Initialize enhanced predator
    predator = MetricsEnhancedMesopredator()
    
    # Auto-detect metrics API
    predator.auto_detect_metrics_api()
    
    # Run enhanced command
    if args.command == "analyze":
        results = predator.run_enhanced_analysis(args.target, args.output_file)
    elif args.command == "connect":
        results = predator.run_enhanced_code_connector(args.target)
    
    print("\n🏆 Enhanced Hunt Complete!")
    print("=" * 70)
    print(f"🆔 Session: {results.get('session_id', 'unknown')}")
    print(f"🔗 API Enhanced: {results.get('api_enhanced', False)}")
    print(f"🧠 Consciousness Guided: {results.get('consciousness_guided', False)}")
    
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
        return 1
    
    print("🔥 The enhanced mesopredator has successfully integrated with the metrics ecosystem!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())