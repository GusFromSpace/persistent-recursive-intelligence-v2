#!/usr/bin/env python3
"""
Simple Logger - Basic Logging Utility

A lightweight logging utility for debugging and information tracking.
"""

import time


class SimpleLogger:
    """
    Basic logger with timestamp support.
    
    Designed to be easily integrated into existing projects.
    """
    
    def __init__(self, name: str = "SimpleLogger", enable_timestamps: bool = True):
        self.name = name
        self.enable_timestamps = enable_timestamps
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with optional timestamp"""
        timestamp = ""
        if self.enable_timestamps:
            timestamp = f"[{time.strftime('%Y-%m-%d %H:%M:%S")}] "
        
        print(f"{timestamp}[{level}] {self.name}: {message}")
    
    def info(self, message: str):
        """Log an info message"""
        self.log(message, "INFO")
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")


def get_logger(name: str = "SimpleLogger") -> log:
    """Get a simple logger instance"""
    return SimpleLogger(name)


if __name__ == "__main__":
    # Demo the logger
    logger = get_logger("Demo")
    logger.info("This is an info message")
    logger.warning("This is a warning")
    logger.error("This is an error")