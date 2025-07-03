#!/usr/bin/env python3
"""
Message Factory - Creates and validates messages
"""

import hashlib
import uuid

class MessageFactory:
    """Factory for creating hello world messages"""

    def __init__(self):
        # OVER-ENGINEERING: Unique ID for factory instance
        self.factory_id = str(uuid.uuid4())
        self.messages_created = 0

        # UNNECESSARY: Cache for simple messages
        self.message_cache = {}

    def create_hello_message(self, greeting="Hello", target="World", punctuation="!"):
        """Create a hello world message"""
        # PERFORMANCE ISSUE: Hashing simple strings
        cache_key = self.generate_cache_key(greeting, target, punctuation)

        # CACHING: Caching "Hello World!" variants
        if cache_key in self.message_cache:
            return self.message_cache[cache_key]

        # VALIDATION: Over-validating simple inputs
        if not self.validate_greeting(greeting):
            greeting = "Hello"  # Fallback

        if not self.validate_target(target):
            target = "World"  # Fallback

        if not self.validate_punctuation(punctuation):
            punctuation = "!"  # Fallback

        # ASSEMBLY: Over-complicated message creation
        message_parts = [greeting, " ", target, punctuation]
        message = self.assemble_parts(message_parts)

        # QUALITY CONTROL: Quality checking "Hello World!"
        if not self.quality_check(message):
            raise ValueError("Message failed quality control")

        # TRACKING: Tracking message creation
        self.messages_created += 1
        self.message_cache[cache_key] = message

        return message

    def generate_cache_key(self, greeting, target, punctuation):
        """Generate cache key for message components"""
        # OVERKILL: Using SHA256 for "Hello World!" cache key
        combined = f"{greeting}|{target}|{punctuation}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def validate_greeting(self, greeting):
        """Validate greeting component"""
        # OVER-VALIDATION: Extensive validation for "Hello"
        if not isinstance(greeting, str):
            return False

        if len(greeting) < 1:
            return False

        if len(greeting) > 50:  # Arbitrary limit
            return False

        # CHECK: Only alphabetic characters
        if not greeting.replace(" ", "").isalpha():
            return False

        # CHECK: Proper capitalization
        if not greeting[0].isupper():
            return False

        return True

    def validate_target(self, target):
        """Validate target component"""
        # SIMILAR OVER-VALIDATION: For "World"
        if not isinstance(target, str):
            return False

        if len(target) < 1:
            return False

        if len(target) > 50:
            return False

        # CHECK: Alphabetic only
        if not target.isalpha():
            return False

        # CHECK: Capitalization
        if not target[0].isupper():
            return False

        return True

    def validate_punctuation(self, punctuation):
        """Validate punctuation component"""
        # OVER-VALIDATION: For a single "!" character
        if not isinstance(punctuation, str):
            return False

        if len(punctuation) != 1:
            return False

        # CHECK: Valid punctuation characters
        valid_punctuation = ["!", "?", ".", ",", ";", ":"]
        if punctuation not in valid_punctuation:
            return False

        return True

    def assemble_parts(self, parts):
        """Assemble message parts"""
        # INEFFICIENT: Manual assembly with validation
        if not isinstance(parts, list):
            raise ValueError("Parts must be a list")

        if len(parts) != 4:  # greeting, space, target, punctuation
            raise ValueError("Invalid number of parts")

        # MANUAL CONCATENATION: Instead of simple join
        result = ""
        for i, part in enumerate(parts):
            if part is None:
                raise ValueError(f"Part {i} is None")
            result += str(part)

        return result

    def quality_check(self, message):
        """Perform quality check on message"""
        # QUALITY ASSURANCE: For "Hello World!"
        if not isinstance(message, str):
            return False

        # LENGTH CHECK: For 12-character string
        if len(message) < 5 or len(message) > 100:
            return False

        # CONTENT CHECK: Must contain expected words
        required_words = ["Hello", "World"]
        for word in required_words:
            if word not in message:
                return False

        # STRUCTURE CHECK: Must have space between words
        if " " not in message:
            return False

        # PUNCTUATION CHECK: Must end with punctuation
        if not message[-1] in "!?.":
            return False

        return True

    def get_factory_stats(self):
        """Get factory statistics"""
        # METRICS: Tracking simple factory usage
        return {
            "factory_id": self.factory_id,
            "messages_created": self.messages_created,
            "cache_size": len(self.message_cache),
            "cache_efficiency": self.calculate_cache_efficiency()
        }

    def calculate_cache_efficiency(self):
        """Calculate cache efficiency"""
        # UNNECESSARY: Cache efficiency for hello world
        if self.messages_created == 0:
            return 0.0

        cache_hits = max(0, self.messages_created - len(self.message_cache))
        return cache_hits / self.messages_created if self.messages_created > 0 else 0.0

    def clear_cache(self):
        """Clear message cache"""
        # CLEANUP: For simple cache
        old_size = len(self.message_cache)
        self.message_cache.clear()
        return old_size