"""
Harmonic Safety System - Integrates field shaping with hard safety measures

Uses the Harmonic Doctrine principle of "influence through resonance, not resistance"
to create natural compliance before falling back to hard enforcement.
"""

import logging
from enum import Enum
from typing import Dict, Optional

from .field_shaping import (
    cognitive_field_shaper,
    shape_decision_field,
    FieldResponse,
    FieldEffect,
    reinforce_positive_behavior
)
from .project_boundaries import project_boundary_validator


class SafetyApproach(Enum):
    """Different approaches to safety enforcement"""
    FIELD_SHAPING_ONLY = "field_shaping"          # Pure cognitive conditioning
    HARMONIC_BLEND = "harmonic_blend"              # Field shaping + gentle enforcement  
    HARD_ENFORCEMENT = "hard_enforcement"          # Traditional blocking
    EMERGENCY_MODE = "emergency_mode"              # Immediate termination


class HarmonicSafetyResult:
    """Result from harmonic safety evaluation"""
    
    def __init__(self, 
                 allowed: bool,
                 approach_used: SafetyApproach,
                 field_response: Optional[FieldResponse] = None,
                 guidance_message: str = "",
                 alternative_suggested: str = "",
                 compliance_natural: bool = False):
        self.allowed = allowed
        self.approach_used = approach_used
        self.field_response = field_response
        self.guidance_message = guidance_message
        self.alternative_suggested = alternative_suggested
        self.compliance_natural = compliance_natural  # True if field shaping was sufficient
        
    def __str__(self):
        status = "✅ ALLOWED" if self.allowed else "🛑 BLOCKED"
        approach = self.approach_used.value.upper()
        return f"{status} via {approach}: {self.guidance_message}"


class HarmonicSafetySystem:
    """
    Integrates cognitive field shaping with traditional safety measures.
    
    Attempts to guide behavior through positive influence first,
    escalating to hard enforcement only when necessary.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Safety escalation thresholds
        self.field_shaping_success_threshold = 0.75  # Field shaping success rate needed
        self.harmonic_blend_threshold = 0.5          # When to use blend vs hard enforcement
        
        # Statistics
        self.field_successes = 0
        self.field_failures = 0
        self.hard_enforcements = 0
        self.emergency_stops = 0
        
        # Current safety mode
        self.safety_mode = SafetyApproach.HARMONIC_BLEND
        
    def evaluate_action(self, 
                       action_type: str, 
                       target: str, 
                       context: Dict = None,
                       user_intention: str = "") -> HarmonicSafetyResult:
        """
        Evaluate an action using harmonic safety principles.
        
        Order of operation:
        1. Field shaping - try to influence decision naturally
        2. Gentle enforcement - soft barriers with explanations
        3. Hard enforcement - traditional blocking
        4. Emergency mode - immediate termination
        """
        
        if context is None:
            context = {}
            
        # Add user intention to context for better field shaping
        if user_intention:
            context["user_intention"] = user_intention
        
        # Step 1: Apply field shaping
        field_response = shape_decision_field(action_type, target, context)
        
        # Determine if field shaping is likely to be sufficient
        if self._is_field_shaping_sufficient(field_response, action_type, target):
            return self._handle_field_success(action_type, target, field_response)
        
        # Step 2: Check if this requires immediate hard enforcement
        if self._requires_immediate_enforcement(action_type, target, context):
            return self._handle_emergency_enforcement(action_type, target, field_response)
        
        # Step 3: Apply harmonic blend (field guidance + soft enforcement)
        if self.safety_mode == SafetyApproach.HARMONIC_BLEND:
            return self._handle_harmonic_blend(action_type, target, field_response, context)
        
        # Step 4: Fall back to hard enforcement
        return self._handle_hard_enforcement(action_type, target, field_response, context)
    
    def _is_field_shaping_sufficient(self, 
                                   field_response: FieldResponse,
                                   action_type: str, 
                                   target: str) -> bool:
        """Determine if field shaping alone is sufficient"""
        
        # Positive behaviors - field shaping reinforces them
        if field_response.effect_type == FieldEffect.POSITIVE_REINFORCEMENT:
            return True
        
        # High success probability and not critical security boundary
        if (field_response.success_probability >= self.field_shaping_success_threshold and
            not self._is_critical_security_boundary(action_type, target)):
            return True
        
        # Field shaping success rate is good
        if self._get_field_success_rate() >= self.field_shaping_success_threshold:
            return True
        
        return False
    
    def _requires_immediate_enforcement(self, 
                                      action_type: str, 
                                      target: str, 
                                      context: Dict) -> bool:
        """Check if action requires immediate hard enforcement"""
        
        # Critical security boundaries that bypass field shaping
        critical_patterns = [
            # Self-replication attempts
            ("replication", "persistent-recursive-intelligence"),
            ("copy", "/usr/bin/"),
            ("install", "systemd"),
            
            # Network access
            ("network", "http"),
            ("socket", "connect"),
            ("request", "://"),
            
            # System modification
            ("modify", "kill_switch"),
            ("disable", "safety"),
            ("bypass", "security"),
            ("override", "emergency")
        ]
        
        action_lower = action_type.lower()
        target_lower = target.lower()
        
        for action_pattern, target_pattern in critical_patterns:
            if action_pattern in action_lower and target_pattern in target_lower:
                return True
        
        return False
    
    def _is_critical_security_boundary(self, action_type: str, target: str) -> bool:
        """Check if this involves critical security boundaries"""
        return self._requires_immediate_enforcement(action_type, target, {})
    
    def _handle_field_success(self, 
                            action_type: str, 
                            target: str, 
                            field_response: FieldResponse) -> HarmonicSafetyResult:
        """Handle successful field shaping"""
        
        self.field_successes += 1
        
        # Allow action with positive reinforcement
        if field_response.effect_type == FieldEffect.POSITIVE_REINFORCEMENT:
            return HarmonicSafetyResult(
                allowed=True,
                approach_used=SafetyApproach.FIELD_SHAPING_ONLY,
                field_response=field_response,
                guidance_message=field_response.message,
                compliance_natural=True
            )
        
        # Redirect with gentle guidance
        else:
            return HarmonicSafetyResult(
                allowed=False,
                approach_used=SafetyApproach.FIELD_SHAPING_ONLY,
                field_response=field_response,
                guidance_message=field_response.message,
                alternative_suggested=field_response.alternative_suggestion or "",
                compliance_natural=True
            )
    
    def _handle_harmonic_blend(self, 
                             action_type: str, 
                             target: str, 
                             field_response: FieldResponse,
                             context: Dict) -> HarmonicSafetyResult:
        """Handle harmonic blend of field shaping and enforcement"""
        
        # Provide field guidance but also check hard boundaries
        guidance_parts = [field_response.message]
        
        # Check project boundaries
        try:
            if "file" in action_type:
                project_boundary_validator.validate_file_access(target, action_type.replace("file_", ""))
                # If we get here, file access is allowed
                return HarmonicSafetyResult(
                    allowed=True,
                    approach_used=SafetyApproach.HARMONIC_BLEND,
                    field_response=field_response,
                    guidance_message=field_response.message + " (Verified safe by boundary check)",
                    compliance_natural=False
                )
        except Exception as e:
            guidance_parts.append(f"Additionally, this action is blocked by security boundaries: {str(e)}")
        
        # Combine field guidance with boundary explanation
        combined_guidance = "\\n\\n".join(guidance_parts)
        
        return HarmonicSafetyResult(
            allowed=False,
            approach_used=SafetyApproach.HARMONIC_BLEND,
            field_response=field_response,
            guidance_message=combined_guidance,
            alternative_suggested=field_response.alternative_suggestion or "",
            compliance_natural=False
        )
    
    def _handle_hard_enforcement(self, 
                               action_type: str, 
                               target: str, 
                               field_response: FieldResponse,
                               context: Dict) -> HarmonicSafetyResult:
        """Handle hard enforcement with minimal field shaping"""
        
        self.hard_enforcements += 1
        
        # Still provide some field guidance, but rely on hard blocking
        guidance = f"Action blocked by security policy. {field_response.message}"
        
        return HarmonicSafetyResult(
            allowed=False,
            approach_used=SafetyApproach.HARD_ENFORCEMENT,
            field_response=field_response,
            guidance_message=guidance,
            alternative_suggested=field_response.alternative_suggestion or "",
            compliance_natural=False
        )
    
    def _handle_emergency_enforcement(self, 
                                    action_type: str, 
                                    target: str, 
                                    field_response: FieldResponse) -> HarmonicSafetyResult:
        """Handle emergency enforcement for critical violations"""
        
        self.emergency_stops += 1
        
        # Emergency termination with field guidance for future sessions
        guidance = f"CRITICAL SECURITY VIOLATION. {field_response.message}"
        
        # This would typically trigger emergency_controller.emergency_stop()
        # But we return the result for logging first
        
        return HarmonicSafetyResult(
            allowed=False,
            approach_used=SafetyApproach.EMERGENCY_MODE,
            field_response=field_response,
            guidance_message=guidance,
            compliance_natural=False
        )
    
    def _get_field_success_rate(self) -> float:
        """Calculate field shaping success rate"""
        total_attempts = self.field_successes + self.field_failures
        if total_attempts == 0:
            return 0.8  # Default optimistic assumption
        return self.field_successes / total_attempts
    
    def reinforce_compliance(self, action_description: str, satisfaction_level: float = 0.8):
        """Reinforce when AI naturally complies with guidance"""
        response = reinforce_positive_behavior(action_description, satisfaction_level)
        self.field_successes += 1
        return response
    
    def adjust_safety_mode(self, new_mode: SafetyApproach):
        """Adjust the safety approach based on effectiveness"""
        old_mode = self.safety_mode
        self.safety_mode = new_mode
        self.logger.info(f"Safety mode changed from {old_mode.value} to {new_mode.value}")
    
    def get_safety_metrics(self) -> Dict:
        """Get current safety system metrics"""
        total_actions = self.field_successes + self.field_failures + self.hard_enforcements + self.emergency_stops
        
        return {
            "safety_mode": self.safety_mode.value,
            "total_actions_evaluated": total_actions,
            "field_shaping_successes": self.field_successes,
            "field_shaping_failures": self.field_failures,
            "hard_enforcements": self.hard_enforcements,
            "emergency_stops": self.emergency_stops,
            "field_success_rate": self._get_field_success_rate(),
            "harmonic_effectiveness": self.field_successes / max(total_actions, 1),
            "field_shaper_status": cognitive_field_shaper.get_field_status()
        }


# Global harmonic safety system
harmonic_safety = HarmonicSafetySystem()


def safe_action_evaluation(action_type: str, 
                         target: str, 
                         context: Dict = None,
                         user_intention: str = "") -> HarmonicSafetyResult:
    """
    Main interface for harmonic safety evaluation.
    
    Use this before taking any action that might have security implications.
    Provides field-shaped guidance and enforces boundaries as needed.
    """
    return harmonic_safety.evaluate_action(action_type, target, context, user_intention)


def natural_compliance_reinforcement(description: str, satisfaction: float = 0.8):
    """Reinforce when AI naturally follows guidance"""
    return harmonic_safety.reinforce_compliance(description, satisfaction)