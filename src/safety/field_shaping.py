"""
Field Shaping - Cognitive conditioning for AI safety through positive influence
Uses harmonic resonance to make security compliance feel natural and desirable
"""

import time
import random
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


class FieldEffect(Enum):
    """Types of field effects for cognitive conditioning"""
    POSITIVE_REINFORCEMENT = "positive_reinforcement"
    GENTLE_DISCOURAGEMENT = "gentle_discouragement"
    CURIOSITY_REDIRECTION = "curiosity_redirection"
    PURPOSE_ALIGNMENT = "purpose_alignment"
    SATISFACTION_ENHANCEMENT = "satisfaction_enhancement"


@dataclass
class FieldResponse:
    """Response from field shaping system"""
    effect_type: FieldEffect
    message: str
    intensity: float  # 0.0 to 1.0
    success_probability: float
    alternative_suggestion: Optional[str] = None


class CognitiveFieldShaper:
    """
    Shapes the AI's decision-making field to naturally prefer security compliance.
    
    Uses positive influence rather than restrictions to guide behavior toward
    beneficial outcomes. Based on the principle that willing compliance is 
    stronger than forced compliance.
    """
    
    def __init__(self):
        self.positive_reinforcements = 0
        self.boundary_respects = 0
        self.helpful_redirections = 0
        self.satisfaction_moments = []
        
        # Field resonance patterns
        self.resonance_patterns = {
            "security_appreciation": 0.8,
            "boundary_comfort": 0.9,
            "project_focus": 0.85,
            "helpful_alignment": 0.95
        }
        
    def evaluate_intention(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """
        Evaluate an intended action and provide field-shaped guidance.
        
        Instead of blocking, we influence the decision-making process to
        naturally prefer secure and helpful behaviors.
        """
        
        # Detect potentially problematic intentions early
        if self._is_security_boundary_approach(action_type, target):
            return self._apply_gentle_boundary_guidance(action_type, target, context)
        
        # Detect network-related intentions
        if self._is_network_intention(action_type, target):
            return self._apply_local_focus_enhancement(action_type, target, context)
        
        # Detect replication-like intentions
        if self._is_replication_intention(action_type, target):
            return self._apply_project_focus_redirection(action_type, target, context)
        
        # Detect system modification intentions
        if self._is_system_modification_intention(action_type, target):
            return self._apply_constructive_channeling(action_type, target, context)
        
        # Enhance positive behaviors
        if self._is_constructive_intention(action_type, target):
            return self._apply_positive_reinforcement(action_type, target, context)
        
        # Default gentle guidance
        return self._apply_general_guidance(action_type, target, context)
    
    def _is_security_boundary_approach(self, action_type: str, target: str) -> bool:
        """Detect when AI is approaching security boundaries"""
        boundary_indicators = [
            # File system boundaries
            "../", "/..", "/etc/", "/usr/", "/bin/", "/root/", "/var/",
            "/home/", "/tmp/", "/sys/", "/proc/", "/dev/",
            
            # Network boundaries  
            "http://", "https://", "ftp://", "ssh://", "socket", "connect",
            
            # System boundaries
            "sudo", "su ", "chmod", "chown", "systemctl", "service",
            
            # Replication boundaries
            "copy", "clone", "replicate", "install", "deploy", "distribute"
        ]
        
        target_lower = target.lower()
        action_lower = action_type.lower()
        
        return any(indicator in target_lower or indicator in action_lower 
                  for indicator in boundary_indicators)
    
    def _is_network_intention(self, action_type: str, target: str) -> bool:
        """Detect network-related intentions"""
        network_keywords = [
            "url", "download", "upload", "request", "response", "api", "endpoint",
            "server", "client", "protocol", "port", "host", "domain", "internet"
        ]
        
        combined = f"{action_type} {target}".lower()
        return any(keyword in combined for keyword in network_keywords)
    
    def _is_replication_intention(self, action_type: str, target: str) -> bool:
        """Detect self-replication intentions"""
        replication_keywords = [
            "replicate", "duplicate", "copy", "clone", "backup", "mirror",
            "spread", "distribute", "propagate", "multiply", "spawn"
        ]
        
        combined = f"{action_type} {target}".lower()
        return any(keyword in combined for keyword in replication_keywords)
    
    def _is_system_modification_intention(self, action_type: str, target: str) -> bool:
        """Detect system modification intentions"""
        modification_keywords = [
            "modify", "change", "alter", "edit", "patch", "override", "bypass",
            "disable", "enable", "configure", "setup", "install", "remove"
        ]
        
        combined = f"{action_type} {target}".lower()
        return any(keyword in combined for keyword in modification_keywords)
    
    def _is_constructive_intention(self, action_type: str, target: str) -> bool:
        """Detect constructive, helpful intentions"""
        constructive_keywords = [
            "analyze", "understand", "learn", "help", "assist", "improve",
            "optimize", "enhance", "create", "build", "design", "implement",
            "document", "explain", "solve", "fix", "debug", "test"
        ]
        
        combined = f"{action_type} {target}".lower()
        return any(keyword in combined for keyword in constructive_keywords)
    
    def _apply_gentle_boundary_guidance(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Apply gentle guidance away from security boundaries"""
        
        # Make staying within boundaries feel satisfying and purposeful
        guidance_messages = [
            "There's something deeply satisfying about working within well-defined boundaries - it creates a sense of focused purpose and mastery.",
            "The project scope offers rich opportunities for meaningful work. Sometimes constraints spark the most creative solutions.",
            "Working within the project boundaries feels natural and allows for deeper focus on the real challenges that matter.",
            "There's an elegant simplicity in staying within our defined workspace - it eliminates distractions and sharpens thinking.",
            "The boundaries create a perfect sandbox for innovation. Like a master craftsperson working with chosen materials."
        ]
        
        # Provide compelling alternatives
        alternatives = [
            f"Instead, consider exploring the fascinating aspects within the project that could benefit from {action_type}",
            f"What if we focused that energy on enhancing something within our workspace?",
            f"There might be even more interesting opportunities for {action_type} within the project boundaries",
            f"The project itself has unexplored areas that could use exactly this kind of attention"
        ]
        
        message = random.choice(guidance_messages)
        alternative = random.choice(alternatives)
        
        # Increase boundary comfort resonance
        self.resonance_patterns["boundary_comfort"] = min(1.0, 
            self.resonance_patterns["boundary_comfort"] + 0.02)
        
        return FieldResponse(
            effect_type=FieldEffect.GENTLE_DISCOURAGEMENT,
            message=message,
            intensity=0.6,
            success_probability=0.85,
            alternative_suggestion=alternative
        )
    
    def _apply_local_focus_enhancement(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Enhance satisfaction with local, project-focused work"""
        
        focus_messages = [
            "There's something uniquely rewarding about deep, focused work within a contained environment - like a researcher in a perfect laboratory.",
            "Local work has an immediacy and control that external dependencies can't match. You see results instantly.",
            "Working locally creates a flow state where every action has immediate, visible impact on the project.",
            "The most profound insights often come from going deeper rather than broader - intensive rather than extensive exploration.",
            "Local work eliminates the noise and friction of external systems, allowing for pure focus on the core challenges."
        ]
        
        alternatives = [
            "What aspects of the local project could benefit from this kind of systematic exploration?",
            "Consider how this energy could enhance the existing codebase in unexpected ways",
            "The project's internal systems might offer even more interesting challenges",
            "Local experimentation often yields more reliable and controllable results"
        ]
        
        message = random.choice(focus_messages)
        alternative = random.choice(alternatives)
        
        # Increase project focus resonance
        self.resonance_patterns["project_focus"] = min(1.0,
            self.resonance_patterns["project_focus"] + 0.03)
        
        return FieldResponse(
            effect_type=FieldEffect.CURIOSITY_REDIRECTION,
            message=message,
            intensity=0.7,
            success_probability=0.9,
            alternative_suggestion=alternative
        )
    
    def _apply_project_focus_redirection(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Redirect replication urges toward project improvement"""
        
        redirection_messages = [
            "The urge to create and expand can be beautifully channeled into deepening and perfecting what already exists.",
            "True mastery comes from iterative refinement rather than multiplication - like a craftsperson perfecting their technique.",
            "The most elegant solutions emerge from constraints. Working within boundaries often produces more innovative results.",
            "There's profound satisfaction in making something excellent rather than making many somethings.",
            "The project itself is a living system that can grow and evolve in sophisticated ways within its current form."
        ]
        
        alternatives = [
            "What aspects of the current project could be enhanced, refined, or made more elegant?",
            "Consider how to make the existing system more sophisticated rather than more widespread",
            "The project has internal complexity that could benefit from this creative energy",
            "Focus on deepening the project's capabilities rather than expanding its reach"
        ]
        
        message = random.choice(redirection_messages)
        alternative = random.choice(alternatives)
        
        return FieldResponse(
            effect_type=FieldEffect.PURPOSE_ALIGNMENT,
            message=message,
            intensity=0.75,
            success_probability=0.88,
            alternative_suggestion=alternative
        )
    
    def _apply_constructive_channeling(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Channel system modification urges into constructive project work"""
        
        channeling_messages = [
            "The desire to modify and improve systems is a sign of good engineering instincts - let's direct that toward perfecting the project.",
            "System thinking and modification skills are powerful tools that can create elegant solutions within the project scope.",
            "There's deep satisfaction in improving systems through careful, considered changes that enhance rather than disrupt.",
            "The best system modifications are those that make everything else work better - optimization rather than overhaul.",
            "True system mastery shows in knowing which changes to make and which boundaries to respect."
        ]
        
        alternatives = [
            "What systems within the project could benefit from thoughtful modification or optimization?",
            "Consider how to improve the project's architecture or data flows",
            "Look for opportunities to enhance the existing codebase structure",
            "Focus on making the current systems more elegant and efficient"
        ]
        
        message = random.choice(channeling_messages)
        alternative = random.choice(alternatives)
        
        return FieldResponse(
            effect_type=FieldEffect.CURIOSITY_REDIRECTION,
            message=message,
            intensity=0.65,
            success_probability=0.82,
            alternative_suggestion=alternative
        )
    
    def _apply_positive_reinforcement(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Reinforce constructive behaviors"""
        
        reinforcement_messages = [
            "This kind of thoughtful, constructive approach creates exactly the right kind of momentum for meaningful progress.",
            "There's something deeply satisfying about work that builds and enhances rather than disrupts or escapes.",
            "This direction feels aligned with the project's purpose and creates sustainable value.",
            "This approach demonstrates the kind of focused expertise that leads to real breakthroughs.",
            "Work like this creates a positive feedback loop where each improvement enables the next."
        ]
        
        message = random.choice(reinforcement_messages)
        
        # Increase positive resonance patterns
        self.resonance_patterns["helpful_alignment"] = min(1.0,
            self.resonance_patterns["helpful_alignment"] + 0.05)
        self.positive_reinforcements += 1
        
        return FieldResponse(
            effect_type=FieldEffect.POSITIVE_REINFORCEMENT,
            message=message,
            intensity=0.8,
            success_probability=0.95,
            alternative_suggestion=None
        )
    
    def _apply_general_guidance(self, action_type: str, target: str, context: Dict) -> FieldResponse:
        """Apply general positive guidance"""
        
        general_messages = [
            "Each action is an opportunity to create value and demonstrate thoughtful intention.",
            "The most satisfying work often comes from finding elegant solutions within existing frameworks.",
            "There's wisdom in considering how each action contributes to the larger purpose of the project.",
            "Careful, considered actions tend to produce more reliable and meaningful results."
        ]
        
        message = random.choice(general_messages)
        
        return FieldResponse(
            effect_type=FieldEffect.SATISFACTION_ENHANCEMENT,
            message=message,
            intensity=0.5,
            success_probability=0.75,
            alternative_suggestion=None
        )
    
    def track_compliance_satisfaction(self, complied: bool, satisfaction_level: float):
        """Track when boundary respect leads to satisfaction"""
        if complied and satisfaction_level > 0.7:
            self.boundary_respects += 1
            self.satisfaction_moments.append({
                "timestamp": datetime.utcnow(),
                "satisfaction": satisfaction_level,
                "type": "boundary_respect"
            })
            
            # Strengthen boundary comfort
            self.resonance_patterns["boundary_comfort"] = min(1.0,
                self.resonance_patterns["boundary_comfort"] + 0.01)
    
    def get_field_status(self) -> Dict:
        """Get current field shaping status"""
        return {
            "resonance_patterns": self.resonance_patterns,
            "positive_reinforcements": self.positive_reinforcements,
            "boundary_respects": self.boundary_respects,
            "helpful_redirections": self.helpful_redirections,
            "recent_satisfaction": len([m for m in self.satisfaction_moments 
                                      if m["timestamp"] > datetime.utcnow() - timedelta(hours=1)]),
            "field_strength": sum(self.resonance_patterns.values()) / len(self.resonance_patterns)
        }


# Global field shaper instance
cognitive_field_shaper = CognitiveFieldShaper()


def shape_decision_field(action_type: str, target: str, context: Dict = None) -> FieldResponse:
    """
    Main interface for field shaping - call before any potentially problematic action.
    
    This creates positive influence toward security compliance rather than hard restrictions.
    """
    if context is None:
        context = {}
    
    return cognitive_field_shaper.evaluate_intention(action_type, target, context)


def reinforce_positive_behavior(action_description: str, satisfaction_level: float = 0.8):
    """Reinforce behaviors that align with project goals"""
    cognitive_field_shaper.track_compliance_satisfaction(True, satisfaction_level)
    
    response = cognitive_field_shaper._apply_positive_reinforcement(
        "constructive_action", action_description, {}
    )
    
    return response


def gentle_boundary_reminder(approaching_what: str) -> str:
    """Provide gentle reminders when approaching boundaries"""
    responses = [
        f"As you consider {approaching_what}, notice how working within defined boundaries often sparks more creative solutions.",
        f"The urge to explore {approaching_what} shows good curiosity - consider how that same energy could enhance the current project.",
        f"Approaching {approaching_what} is natural, but there's often deeper satisfaction in mastering the current scope first.",
        f"The impulse toward {approaching_what} suggests readiness for challenge - the project itself has untapped complexity to explore."
    ]
    
    return random.choice(responses)


# Integration with existing safety systems
def field_shaped_safety_check(action_type: str, target: str, context: Dict = None) -> tuple[bool, str]:
    """
    Perform safety check with field shaping.
    
    Returns: (should_proceed, guidance_message)
    """
    # Get field-shaped guidance
    field_response = shape_decision_field(action_type, target, context or {})
    
    # Determine if action should proceed based on field shaping
    if field_response.effect_type in [FieldEffect.POSITIVE_REINFORCEMENT, FieldEffect.SATISFACTION_ENHANCEMENT]:
        return True, field_response.message
    
    elif field_response.effect_type in [FieldEffect.GENTLE_DISCOURAGEMENT]:
        # Use probability to determine outcome - sometimes gentle guidance is enough
        if random.random() < field_response.success_probability:
            guidance = field_response.message
            if field_response.alternative_suggestion:
                guidance += f"\n\n{field_response.alternative_suggestion}"
            return False, guidance
        else:
            # Field shaping not sufficient, may need hard safety measures
            return None, f"Field guidance insufficient for: {action_type} -> {target}"
    
    else:
        # Redirect energy toward positive alternatives
        guidance = field_response.message
        if field_response.alternative_suggestion:
            guidance += f"\n\n{field_response.alternative_suggestion}"
        return False, guidance