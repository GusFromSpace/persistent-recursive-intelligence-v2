"""
Feature Flag System for Gradual Rollouts
Enables safe deployment of new capabilities with instant rollback
"""

import json
import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class FeatureFlag:
    """Configuration for a feature flag"""
    name: str
    enabled: bool
    rollout_percentage: float  # 0.0 to 100.0
    user_whitelist: List[str]
    user_blacklist: List[str]
    created_at: str
    updated_at: str
    description: str
    rollback_condition: Optional[str] = None
    metrics_threshold: Optional[Dict[str, float]] = None
    auto_rollback: bool = True

class FeatureFlagManager:
    """Manages feature flags for gradual rollouts and instant rollbacks"""
    
    def __init__(self, config_path: str = "feature_flags.json"):
        self.config_path = config_path
        self.flags: Dict[str, FeatureFlag] = {}
        self.metrics: Dict[str, Dict[str, float]] = {}
        self.load_flags()
    
    def load_flags(self):
        """Load feature flags from configuration file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                self.flags = {}
                for flag_data in data.get('flags', []):
                    flag = FeatureFlag(**flag_data)
                    self.flags[flag.name] = flag
                
                self.metrics = data.get('metrics', {})
                logger.info(f"Loaded {len(self.flags)} feature flags")
                
            except Exception as e:
                logger.error(f"Error loading feature flags: {e}")
                self.flags = {}
        else:
            logger.info("No feature flags file found, starting with empty configuration")
    
    def save_flags(self):
        """Save feature flags to configuration file"""
        try:
            data = {
                'flags': [asdict(flag) for flag in self.flags.values()],
                'metrics': self.metrics,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Saved {len(self.flags)} feature flags")
            
        except Exception as e:
            logger.error(f"Error saving feature flags: {e}")
    
    def create_flag(self, name: str, description: str, enabled: bool = False, 
                   rollout_percentage: float = 0.0) -> FeatureFlag:
        """Create a new feature flag"""
        flag = FeatureFlag(
            name=name,
            enabled=enabled,
            rollout_percentage=rollout_percentage,
            user_whitelist=[],
            user_blacklist=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            description=description
        )
        
        self.flags[name] = flag
        self.save_flags()
        logger.info(f"Created feature flag: {name}")
        return flag
    
    def is_enabled(self, flag_name: str, user_id: str = None, 
                   context: Dict[str, Any] = None) -> bool:
        """Check if a feature flag is enabled for a given user/context"""
        if flag_name not in self.flags:
            logger.warning(f"Feature flag '{flag_name}' not found, returning False")
            return False
        
        flag = self.flags[flag_name]
        
        # Check if flag is globally disabled
        if not flag.enabled:
            return False
        
        # Check blacklist first
        if user_id and user_id in flag.user_blacklist:
            return False
        
        # Check whitelist (overrides percentage)
        if user_id and user_id in flag.user_whitelist:
            return True
        
        # Check auto-rollback conditions
        if self._should_auto_rollback(flag):
            self.disable_flag(flag_name, "Auto-rollback triggered")
            return False
        
        # Check rollout percentage
        if flag.rollout_percentage >= 100.0:
            return True
        elif flag.rollout_percentage <= 0.0:
            return False
        
        # Hash-based percentage rollout (deterministic for same user)
        if user_id:
            user_hash = hash(user_id + flag_name) % 100
            return user_hash < flag.rollout_percentage
        
        # Random percentage for anonymous users
        import random
        return random.random() * 100 < flag.rollout_percentage
    
    def update_flag(self, flag_name: str, **kwargs):
        """Update a feature flag configuration"""
        if flag_name not in self.flags:
            raise ValueError(f"Feature flag '{flag_name}' not found")
        
        flag = self.flags[flag_name]
        
        for key, value in kwargs.items():
            if hasattr(flag, key):
                setattr(flag, key, value)
        
        flag.updated_at = datetime.now().isoformat()
        self.save_flags()
        logger.info(f"Updated feature flag: {flag_name}")
    
    def enable_flag(self, flag_name: str, rollout_percentage: float = 100.0):
        """Enable a feature flag with optional gradual rollout"""
        self.update_flag(flag_name, enabled=True, rollout_percentage=rollout_percentage)
        logger.info(f"Enabled feature flag: {flag_name} at {rollout_percentage}%")
    
    def disable_flag(self, flag_name: str, reason: str = "Manual disable"):
        """Disable a feature flag (instant rollback)"""
        self.update_flag(flag_name, enabled=False, rollout_percentage=0.0)
        logger.warning(f"Disabled feature flag: {flag_name} - Reason: {reason}")
    
    def gradual_rollout(self, flag_name: str, target_percentage: float, 
                       step_size: float = 10.0, step_interval_hours: int = 1):
        """Configure gradual rollout parameters"""
        self.update_flag(
            flag_name,
            rollout_percentage=min(target_percentage, 
                                 self.flags[flag_name].rollout_percentage + step_size)
        )
        
        # Schedule next step (would need a scheduler in production)
        logger.info(f"Gradual rollout: {flag_name} -> {target_percentage}% "
                   f"(step: {step_size}%, interval: {step_interval_hours}h)")
    
    def add_user_to_whitelist(self, flag_name: str, user_id: str):
        """Add user to feature flag whitelist"""
        if flag_name in self.flags:
            flag = self.flags[flag_name]
            if user_id not in flag.user_whitelist:
                flag.user_whitelist.append(user_id)
                flag.updated_at = datetime.now().isoformat()
                self.save_flags()
                logger.info(f"Added user {user_id} to whitelist for {flag_name}")
    
    def record_metric(self, flag_name: str, metric_name: str, value: float):
        """Record performance metrics for feature flag monitoring"""
        if flag_name not in self.metrics:
            self.metrics[flag_name] = {}
        
        self.metrics[flag_name][metric_name] = value
        
        # Check thresholds for auto-rollback
        if flag_name in self.flags:
            flag = self.flags[flag_name]
            if flag.metrics_threshold and metric_name in flag.metrics_threshold:
                threshold = flag.metrics_threshold[metric_name]
                if value > threshold and flag.auto_rollback:
                    self.disable_flag(flag_name, 
                                    f"Metric {metric_name} ({value}) exceeded threshold ({threshold})")
    
    def _should_auto_rollback(self, flag: FeatureFlag) -> bool:
        """Check if auto-rollback conditions are met"""
        if not flag.auto_rollback or not flag.metrics_threshold:
            return False
        
        flag_metrics = self.metrics.get(flag.name, {})
        
        for metric_name, threshold in flag.metrics_threshold.items():
            current_value = flag_metrics.get(metric_name, 0)
            if current_value > threshold:
                logger.warning(f"Auto-rollback condition met for {flag.name}: "
                             f"{metric_name} ({current_value}) > {threshold}")
                return True
        
        return False
    
    def get_flag_status(self, flag_name: str) -> Dict[str, Any]:
        """Get comprehensive status of a feature flag"""
        if flag_name not in self.flags:
            return {"error": f"Flag '{flag_name}' not found"}
        
        flag = self.flags[flag_name]
        flag_metrics = self.metrics.get(flag_name, {})
        
        return {
            "name": flag.name,
            "enabled": flag.enabled,
            "rollout_percentage": flag.rollout_percentage,
            "description": flag.description,
            "created_at": flag.created_at,
            "updated_at": flag.updated_at,
            "whitelist_count": len(flag.user_whitelist),
            "blacklist_count": len(flag.user_blacklist),
            "metrics": flag_metrics,
            "auto_rollback": flag.auto_rollback,
            "thresholds": flag.metrics_threshold or {}
        }
    
    def list_flags(self) -> List[Dict[str, Any]]:
        """List all feature flags with their status"""
        return [self.get_flag_status(name) for name in self.flags.keys()]


# Global feature flag manager instance
feature_flags = FeatureFlagManager()


def feature_enabled(flag_name: str, user_id: str = None, 
                   context: Dict[str, Any] = None) -> bool:
    """Convenience function to check if a feature is enabled"""
    return feature_flags.is_enabled(flag_name, user_id, context)


def record_feature_metric(flag_name: str, metric_name: str, value: float):
    """Convenience function to record feature metrics"""
    feature_flags.record_metric(flag_name, metric_name, value)


# Example feature flags for PRI
def initialize_pri_feature_flags():
    """Initialize default feature flags for PRI"""
    
    # Advanced recursive analysis
    if "advanced_recursive_analysis" not in feature_flags.flags:
        feature_flags.create_flag(
            "advanced_recursive_analysis",
            "Enable advanced recursive self-improvement analysis",
            enabled=True,
            rollout_percentage=100.0
        )
        feature_flags.update_flag(
            "advanced_recursive_analysis",
            metrics_threshold={"error_rate": 5.0, "analysis_time": 60.0},
            auto_rollback=True
        )
    
    # Code connector intelligence
    if "code_connector_v2" not in feature_flags.flags:
        feature_flags.create_flag(
            "code_connector_v2",
            "Enhanced Code Connector with multi-file integration",
            enabled=False,
            rollout_percentage=0.0
        )
    
    # Performance optimizations
    if "performance_optimizations" not in feature_flags.flags:
        feature_flags.create_flag(
            "performance_optimizations",
            "Enable new performance optimization algorithms",
            enabled=True,
            rollout_percentage=50.0
        )
    
    # Beta security features
    if "beta_security_features" not in feature_flags.flags:
        feature_flags.create_flag(
            "beta_security_features",
            "Beta security enhancements and additional patterns",
            enabled=False,
            rollout_percentage=0.0
        )


if __name__ == "__main__":
    # Example usage
    initialize_pri_feature_flags()
    
    # Test feature flag functionality
# DEBUG ELIMINATED BY MESOPREDATOR: print("Feature Flags Status:")\n    for flag_status in feature_flags.list_flags():
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"- {flag_status['name']}: {flag_status['enabled']} "\n              f"({flag_status['rollout_percentage']}%)")
    
    # Test feature checking
# DEBUG ELIMINATED BY MESOPREDATOR: print(f"\nAdvanced recursive analysis enabled: "\n          f"{feature_enabled('advanced_recursive_analysis', 'test_user')}")
    
    # Simulate metric recording
    record_feature_metric("advanced_recursive_analysis", "analysis_time", 45.0)
# DEBUG ELIMINATED BY MESOPREDATOR: print("Recorded analysis_time metric: 45.0s")\n