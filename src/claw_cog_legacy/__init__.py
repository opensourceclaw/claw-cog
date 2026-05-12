"""
claw-cog: Cognition Layer for AI Agents

Self-Awareness, Reflection, and Goal-Driven Intelligence
"""

__version__ = "0.1.0"
__author__ = "Peter Cheng"
__license__ = "Apache-2.0"

from claw_cog_legacy.self_awareness import SelfAwareness
from claw_cog_legacy.reflective import ReflectiveReasoning
from claw_cog_legacy.goal_driven import GoalDriven
from claw_cog_legacy.boundary import BoundaryCognition
from claw_cog_legacy.engine import CognitionEngine

__all__ = [
    "SelfAwareness",
    "ReflectiveReasoning",
    "GoalDriven",
    "BoundaryCognition",
    "CognitionEngine",
]
