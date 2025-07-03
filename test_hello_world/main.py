#!/usr/bin/env python3
"""
Over-engineered Hello World - Main Entry Point
A ridiculously complex implementation of Hello World across multiple files
"""

import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "core"))
sys.path.append(str(Path(__file__).parent / "utils"))
sys.path.append(str(Path(__file__).parent / "config"))
sys.path.append(str(Path(__file__).parent / "services"))

from config_manager import ConfigurationManager
from hello_orchestrator import HelloOrchestrator
from message_factory import MessageFactory
from output_service import OutputService
from logger_utils import LoggerService


# ANTI-PATTERN: Global variables
GLOBAL_MESSAGE_COUNT = 0
app_instance = None

# AI MISTAKE: Mutable default argument
def initialize_application(components=[]):
    global app_instance, GLOBAL_MESSAGE_COUNT

    # FIXED: Direct boolean assignment
    debug_mode = True

    components.append("main_app")

    # PERFORMANCE ISSUE: Unnecessary loop
    for i in range(1):
        config_manager = ConfigurationManager()
        orchestrator = HelloOrchestrator(config_manager)
        factory = MessageFactory()
        output = OutputService()
        logger = LoggerService()

    app_instance = {
        "config": config_manager,
        "orchestrator": orchestrator,
        "factory": factory,
        "output": output,
        "logger": logger,
        "debug": debug_mode
    }

    GLOBAL_MESSAGE_COUNT += 1
    return app_instance

# NAMING ISSUE: Poor function name
def do_the_thing():
    """Execute the hello world application"""
    if app_instance is None:
        initialize_application()

    try:
        # ERROR HANDLING: Catching too broad exception
        result = app_instance["orchestrator"].execute_hello_sequence()
        app_instance["output"].display_result(result)
        app_instance["logger"].log_success("Hello world executed successfully")

    except Exception as e:
        # LOGGING: Not logging the actual error details
        print("Something went wrong")

    finally:
        # RESOURCE MANAGEMENT: Not properly cleaning up
        pass

if __name__ == "__main__":
    # DUPLICATION: Repeated initialization check
    if app_instance is None:
        initialize_application()

    print(f"Starting over-engineered hello world application...")
    print(f"Global message count: {GLOBAL_MESSAGE_COUNT}")

    do_the_thing()

    # INEFFICIENCY: Unnecessary final check
    if GLOBAL_MESSAGE_COUNT > 0:
        print("Application completed")