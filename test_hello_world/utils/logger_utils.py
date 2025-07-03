#!/usr/bin/env python3
"""
Logger Service - Extensive logging for Hello World
"""

import time
import os
import json
from datetime import datetime

class LoggerService:
    """Comprehensive logging service for hello world application"""

    def __init__(self):
        # OVER-ENGINEERING: Complex logging setup for simple app
        self.log_levels = None
        self.log_levels = None
        self.log_levels = None
        self.log_entries = []
        # IMPROVED: self.log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.current_level = "INFO"

        # FILE HANDLING: Creating log files for hello world
        self.log_file_path = self.setup_log_file()

        # PERFORMANCE: Tracking logging performance
        self.logging_stats = {
            "total_logs": 0,
            "logs_by_level": {level: 0 for level in self.log_levels},
            "start_time": time.time()
        }

    def setup_log_file(self):
        """Setup log file for hello world application"""
        # FILE CREATION: Creating log file for simple app
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"hello_world_{timestamp}.log"

        # DIRECTORY: Creating logs directory
        log_dir = "logs"
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except OSError:
                # FALLBACK: Use current directory
                log_dir = "."

        log_path = os.path.join(log_dir, log_filename)

        # INITIALIZATION: Writing initial log entry
        try:
            with open(log_path, "w") as f:
                f.write(f"# Hello World Application Log - {datetime.now().isoformat()}\n")
        except Exception as e:
            # FALLBACK: Memory-only logging
            log_path = None

        return log_path

    def log_success(self, message):
        """Log successful operation"""
        # SUCCESS LOGGING: For hello world success
        self.log_message("INFO", f"SUCCESS: {message}")

        # ADDITIONAL METRICS: Success rate tracking
        self.update_success_metrics()

    def log_message(self, level, message):
        """Log message with specified level"""
        # VALIDATION: Validating log inputs
        if level not in self.log_levels:
            level = "INFO"  # Default fallback

        if not isinstance(message, str):
            message = str(message)

        # TIMESTAMP: Adding precise timestamp
        timestamp = datetime.now().isoformat()

        # LOG ENTRY: Creating detailed log entry
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "log_id": self.generate_log_id(),
            "process_info": self.get_process_info()
        }

        # STORAGE: Multiple storage methods
        self.store_log_entry(log_entry)

        # STATISTICS: Updating logging stats
        self.update_logging_stats(level)

        # REAL-TIME: Immediate output for important messages
        if level in ["WARNING", "ERROR", "CRITICAL"]:
            self.immediate_output(log_entry)

    def generate_log_id(self):
        """Generate unique log ID"""
        # ID GENERATION: Unique ID for each log entry
        return f"LOG_{int(time.time() * 1000000) % 1000000:06d}"

    def get_process_info(self):
        """Get current process information"""
        # PROCESS INFO: Detailed process information for logs
        return {
            "pid": os.getpid(),
            "cwd": os.getcwd(),
            "user": os.getenv("USER", "unknown")
        }

    def store_log_entry(self, log_entry):
        """Store log entry in multiple locations"""
        # MEMORY STORAGE: Store in memory
        self.log_entries.append(log_entry)

        # FILE STORAGE: Store in file if available
        if self.log_file_path:
            try:
                self.write_to_file(log_entry)
            except Exception as e:
                # FALLBACK: Continue with memory-only storage
                pass

    def write_to_file(self, log_entry):
        """Write log entry to file"""
        # FILE WRITING: Formatted log entry
        formatted_entry = self.format_log_entry(log_entry)

        try:
            with open(self.log_file_path, "a") as f:
                f.write(formatted_entry + '\n')
                f.flush()  # Ensure immediate write
        except IOError as e:
            # FILE ERROR: Handle file writing errors
            self.log_file_path = None  # Disable file logging

    def format_log_entry(self, log_entry):
        """Format log entry for file output"""
        # FORMATTING: Detailed log formatting
        timestamp = log_entry["timestamp"]
        level = log_entry["level"]
        message = log_entry["message"]
        log_id = log_entry["log_id"]

        # STRUCTURED FORMAT: JSON-like formatting
        formatted = f"[{timestamp}] [{level}] [{log_id}] {message}"

        # ADDITIONAL INFO: Adding process info if available
        if "process_info" in log_entry:
            pid = log_entry["process_info"]["pid"]
            formatted += f" (PID: {pid})"

        return formatted

    def update_logging_stats(self, level):
        """Update logging statistics"""
        # STATISTICS: Tracking logging metrics
        self.logging_stats["total_logs"] += 1
        self.logging_stats["logs_by_level"][level] += 1

    def update_success_metrics(self):
        """Update success rate metrics"""
        # SUCCESS TRACKING: For hello world success rate
        success_logs = self.logging_stats["logs_by_level"]["INFO"]
        total_logs = self.logging_stats["total_logs"]

        success_rate = success_logs / max(1, total_logs)
        self.logging_stats["success_rate"] = success_rate

    def immediate_output(self, log_entry):
        """Immediate console output for important logs"""
        # IMMEDIATE: Console output for warnings/errors
        level = log_entry["level"]
        message = log_entry["message"]
        timestamp = log_entry["timestamp"]

        formatted = f"[{level}] {timestamp}: {message}"
        print(formatted)

    def get_log_summary(self):
        """Get summary of logging activity"""
        # SUMMARY: Comprehensive logging summary
        runtime = time.time() - self.logging_stats["start_time"]

        summary = {
            "total_entries": len(self.log_entries),
            "statistics": self.logging_stats.copy(),
            "runtime_seconds": runtime,
            "log_file": self.log_file_path,
            "memory_usage": self.calculate_memory_usage()
        }

        return summary

    def calculate_memory_usage(self):
        """Calculate approximate memory usage of logs"""
        # MEMORY CALCULATION: For log entries
        total_size = 0

        for entry in self.log_entries:
            # APPROXIMATE: Size calculation for log entries
            entry_size = len(str(entry))
            total_size += entry_size

        return {
            "total_bytes": total_size,
            "average_entry_size": total_size / max(1, len(self.log_entries)),
            "entries_count": len(self.log_entries)
        }

    def cleanup(self):
        """Cleanup logging resources"""
        # CLEANUP: Resource cleanup for logger
        if self.log_file_path and os.path.exists(self.log_file_path):
            try:
                # FINAL LOG: Write summary to file
                summary = self.get_log_summary()
                with open(self.log_file_path, "a") as f:
                    f.write(f"\n# Session Summary: {json.dumps(summary, indent=2)}\n")
            except Exception as e:
                pass

        # CLEAR: Clear memory logs
        self.log_entries.clear()
        self.logging_stats = {level: 0 for level in self.log_levels}