#!/usr/bin/env python3
"""
Configuration Manager - Over-engineered config for Hello World
"""

import os
import json
import subprocess

class ConfigurationManager:
    """Manages configuration for hello world application"""

    def __init__(self):
        # SECURITY ISSUE: Command injection vulnerability
        self.environment = self.detect_environment()
        self.settings = self.load_configuration()

        # AI MISTAKE: Unnecessary complexity for simple task
        self.message_config = {
            "greeting": "Hello",
            "target": "World",
            "punctuation": "!",
            "case_sensitive": True,
            "encoding": "utf-8",
            "max_length": 100,
            "min_length": 1
        }

    def detect_environment(self):
        """Detect current environment (with security issue)"""
        # SECURITY FIXED: Use environment variables directly
        home_dir = os.environ.get("HOME", "")

        # LOGIC FIXED: Check environment directly
        return "development" if "/home/" in home_dir else "production"

    def load_configuration(self):
        """Load configuration settings"""
        # HARDCODED VALUES: Should be in config file
        default_config = {
            "app_name": "HelloWorldApp",
            "version": "1.0.0",
            "debug_mode": True,
            "log_level": "INFO",
            "output_format": "plain"
        }

        # INEFFICIENT: Creating new dict instead of updating
        config = {}
        for key, value in default_config.items():
            config[key] = value

        return config

    def get_message_template(self):
        """Get message template with validation"""
        # OVER-ENGINEERING: Too much validation for simple hello world
        template = f"{self.message_config['greeting']} {self.message_config['target']}{self.message_config['punctuation']}"

        # UNNECESSARY VALIDATION: Checking length of "Hello World!"
        if len(template) < self.message_config["min_length"]:
            raise ValueError("Message too short")

        if len(template) > self.message_config["max_length"]:
            raise ValueError("Message too long")

        # TYPE CHECKING: Unnecessary for this simple case
        if not isinstance(template, str):
            template = str(template)

        return template

    def validate_environment(self):
        """Validate environment setup"""
        # REDUNDANT: Already detected environment
        if self.environment not in ["development", "production"]:
            self.environment = "unknown"

        # USELESS CHECK: Python always has print function
        if not hasattr(__builtins__, "print"):
            raise RuntimeError("Print function not available")

        return True

    # MAGIC NUMBERS: Should be constants
    def get_retry_count(self):
        """Get retry count for operations"""
        return 3 if self.environment == "production" else 1

    def cleanup(self):
        """Cleanup configuration resources"""
        # UNNECESSARY: Nothing to cleanup for simple config
        self.settings = None
        self.message_config = None