"""
Command Line Interface for Persistent Recursive Intelligence (PRI).
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Main CLI entry point - delegates to mesopredator_cli.py"""
    # Find the mesopredator_cli.py file
    current_dir = Path(__file__).parent.parent.parent
    mesopredator_cli = current_dir / "mesopredator_cli.py"
    
    if mesopredator_cli.exists():
        # Execute the existing CLI with all arguments
        sys.exit(subprocess.call([sys.executable, str(mesopredator_cli)] + sys.argv[1:]))
    else:
        print("Error: mesopredator_cli.py not found")
        sys.exit(1)

def analyze_command():
    """Analysis command entry point"""
    sys.argv.insert(1, "analyze")
    main()

def fix_command():
    """Fix command entry point"""
    sys.argv.insert(1, "fix")
    main()

if __name__ == "__main__":
    main()