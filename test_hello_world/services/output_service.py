#!/usr/bin/env python3
"""
Output Service - Handles message output with extensive formatting
"""

import sys
import datetime

class OutputService:
    """Service for outputting hello world messages"""

    def __init__(self):
        # OVER-ENGINEERING: Output service state tracking
        self.output_count = 0
        self.output_history = []
        self.formatting_options = {
            "uppercase": False,
            "add_timestamp": False,
            "add_border": False,
            "center_text": False,
            "add_metadata": False
        }

    def display_result(self, message):
        """Display the hello world message"""
        try:
            # PRE-PROCESSING: Extensive formatting for simple output
            formatted_message = self.format_message(message)

            # OUTPUT VALIDATION: Validating output before printing
            if not self.validate_output(formatted_message):
                raise ValueError("Output validation failed")

            # MULTIPLE OUTPUT METHODS: Trying different output approaches
            success = self.try_multiple_output_methods(formatted_message)

            if success:
                self.record_output(formatted_message)
            else:
                raise RuntimeError("All output methods failed")

        except Exception as e:
            # FALLBACK: Overcomplicated fallback for simple print
            self.fallback_output(message)

    def format_message(self, message):
        """Apply formatting to message"""
        # FORMATTING CHAIN: Multiple formatting steps for "Hello World!"
        formatted = message

        # STEP 1: Case formatting
        if self.formatting_options["uppercase"]:
            formatted = formatted.upper()

        # STEP 2: Timestamp addition
        if self.formatting_options["add_timestamp"]:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted = f"[{timestamp}] {formatted}"

        # STEP 3: Border addition
        if self.formatting_options["add_border"]:
            formatted = self.add_border(formatted)

        # STEP 4: Center text
        if self.formatting_options["center_text"]:
            formatted = self.center_text(formatted)

        # STEP 5: Metadata addition
        if self.formatting_options["add_metadata"]:
            formatted = self.add_metadata(formatted)

        return formatted

    def add_border(self, text):
        """Add decorative border to text"""
        # OVER-DECORATION: Adding border to "Hello World!"
        border_char = "*"
        border_length = len(text) + 4

        top_border = border_char * border_length
        bottom_border = border_char * border_length
        side_border = border_char

        bordered_text = f"{top_border}\n{side_border} {text} {side_border}\n{bottom_border}"
        return bordered_text

    def center_text(self, text):
        """Center text in terminal"""
        # CENTERING: For simple hello world output
        try:
            # TERMINAL WIDTH: Getting terminal width for centering
            import shutil
            terminal_width = shutil.get_terminal_size().columns
        except Exception as e:
            terminal_width = 80  # Default fallback

        lines = text.split('\n')
        centered_lines = []

        for line in lines:
            padding = max(0, (terminal_width - len(line)) // 2)
            centered_line = " " * padding + line
            centered_lines.append(centered_line)

        return "\n".join(centered_lines)

    def add_metadata(self, text):
        """Add metadata to output"""
        # METADATA: Adding info to hello world output
        metadata_info = [
            f"Output #{self.output_count + 1}",
            f"Message length: {len(text.split(chr(10))[0])} characters",  # Overcomplicated length calc
            f"Service status: Active"
        ]

        metadata_text = "\n".join(f"[META] {info}" for info in metadata_info)
        return f"{text}\n\n{metadata_text}"

    def validate_output(self, formatted_message):
        """Validate output before displaying"""
        # OUTPUT VALIDATION: For formatted hello world
        if not isinstance(formatted_message, str):
            return False

        if len(formatted_message) == 0:
            return False

        # CHECK: Printable characters only
        try:
            formatted_message.encode("utf-8")
        except UnicodeEncodeError:
            return False

        # CHECK: Reasonable length
        if len(formatted_message) > 10000:  # Arbitrary limit
            return False

        return True

    def try_multiple_output_methods(self, message):
        """Try different output methods"""
        # OUTPUT REDUNDANCY: Multiple ways to print "Hello World!"
        output_methods = [
            self.standard_output,
            self.sys_output,
            self.fallback_print
        ]

        for method in output_methods:
            try:
                method(message)
                return True
            except Exception as e:
                # LOGGING: Tracking failed output attempts
                self.output_history.append(f"Method {method.__name__} failed: {e}")
                continue

        return False

    def standard_output(self, message):
        """Standard print output"""
        # STANDARD: Regular print with validation
        if not sys.stdout.writable():
            raise RuntimeError("stdout not writable")

        print(message)

        # FLUSHING: Ensuring output is flushed
        sys.stdout.flush()

    def sys_output(self, message):
        """System output using sys.stdout"""
        # SYS OUTPUT: Direct stdout writing
        if not hasattr(sys.stdout, "write"):
            raise RuntimeError("stdout.write not available")

        sys.stdout.write(message + '\n')
        sys.stdout.flush()

    def fallback_print(self, message):
        """Fallback print method"""
        # FALLBACK: Basic print as fallback
        try:
            # BASIC: Most basic output possible
            print(message)
        except Exception as e:
            # LAST RESORT: Writing to stderr
            sys.stderr.write(f"FALLBACK: {message}\n")

    def fallback_output(self, original_message):
        """Ultimate fallback for output"""
        # EMERGENCY: When all else fails for "Hello World!"
        emergency_message = f"EMERGENCY OUTPUT: {original_message}"

        try:
            print(emergency_message)
        except Exception as e:
            # DESPERATE: Last resort
            sys.stderr.write(emergency_message + '\n')

        self.output_history.append("Used emergency fallback output")

    def record_output(self, message):
        """Record successful output"""
        # RECORD KEEPING: Tracking output history
        self.output_count += 1

        record = {
            "count": self.output_count,
            "timestamp": datetime.datetime.now().isoformat(),
            "message_length": len(message),
            "success": True
        }

        self.output_history.append(record)

    def get_output_statistics(self):
        """Get output service statistics"""
        # STATS: Statistics for hello world output
        successful_outputs = sum(1 for record in self.output_history
                                if isinstance(record, dict) and record.get("success"))

        return {
            "total_outputs": self.output_count,
            "successful_outputs": successful_outputs,
            "success_rate": successful_outputs / max(1, self.output_count),
            "history_size": len(self.output_history)
        }