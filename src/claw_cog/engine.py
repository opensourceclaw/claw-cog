"""
Cognition Engine

Main orchestrator for all cognition capabilities:
- Self-Awareness
- Reflective Reasoning
- Goal-Driven Behavior
- Boundary Cognition
"""

from typing import Optional, Dict, Any
from pathlib import Path

from claw_cog.self_awareness import SelfAwareness, Identity
from claw_cog.reflective import ReflectiveReasoning, Reflection, Action, Outcome
from claw_cog.goal_driven import GoalDriven, Goal, Progress, GoalPriority
from claw_cog.boundary import BoundaryCognition


class CognitionEngine:
    """
    Cognition Engine
    
    Orchestrates all cognition capabilities:
    - Self-awareness: Who am I, what am I doing, why?
    - Reflection: Metacognitive analysis of behaviors
    - Goals: Autonomous goal pursuit
    - Boundaries: Capability and ethical limits
    """
    
    def __init__(
        self,
        memory_provider: Optional[str] = None,
        learning_provider: Optional[str] = None,
        identity_file: Optional[Path] = None,
        soul_file: Optional[Path] = None,
    ):
        """
        Initialize the cognition engine.
        
        Args:
            memory_provider: Memory provider type (e.g., "claw-mem")
            learning_provider: Learning provider type (e.g., "claw-rl")
            identity_file: Path to IDENTITY.md
            soul_file: Path to SOUL.md
        """
        # Initialize modules
        self._self_awareness = SelfAwareness(
            identity_file=identity_file,
            soul_file=soul_file,
        )
        self._reflection = ReflectiveReasoning(
            memory_provider=memory_provider,
            learning_provider=learning_provider,
        )
        self._goals = GoalDriven(
            memory_provider=memory_provider,
            learning_provider=learning_provider,
        )
        self._boundaries = BoundaryCognition(
            soul_file=soul_file,
        )
        
        # Providers
        self._memory_provider = memory_provider
        self._learning_provider = learning_provider
    
    # ==================== Self-Awareness API ====================
    
    def who_am_i(self) -> Identity:
        """Get self-identity"""
        return self._self_awareness.get_identity()
    
    def what_am_i_doing(self) -> str:
        """Get current state summary"""
        return self._self_awareness.what_am_i_doing()
    
    def why_am_i_doing_this(self) -> str:
        """Get intention summary"""
        return self._self_awareness.why_am_i_doing_this()
    
    def set_identity(self, identity: Identity) -> None:
        """Set AI identity"""
        self._self_awareness.set_identity(identity)
    
    def set_current_task(
        self,
        task: str,
        progress: float = 0.0,
    ) -> None:
        """Update current task"""
        self._self_awareness.set_current_state(
            task=task,
            progress=progress,
        )
    
    def set_intention(
        self,
        goal: str,
        motivation: Optional[str] = None,
    ) -> None:
        """Set current intention"""
        self._self_awareness.set_intention(
            goal=goal,
            motivation=motivation,
        )
    
    # ==================== Reflection API ====================
    
    def reflect(
        self,
        action_description: str,
        outcome_success: bool,
        outcome_result: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Reflection:
        """
        Reflect on an action and its outcome.
        
        Args:
            action_description: Description of the action
            outcome_success: Whether the action succeeded
            outcome_result: Result description
            context: Additional context
            
        Returns:
            Reflection with insights and lessons
        """
        action = Action(
            description=action_description,
            context=context or {},
        )
        
        outcome = Outcome(
            success=outcome_success,
            result=outcome_result,
        )
        
        return self._reflection.reflect_on_action(action, outcome)
    
    def meta_think(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
    ):
        """Perform metacognitive analysis"""
        return self._reflection.meta_reasoning(problem, context)
    
    # ==================== Goal API ====================
    
    def set_goal(
        self,
        description: str,
        priority: GoalPriority = GoalPriority.MEDIUM,
    ) -> Goal:
        """Set a new goal"""
        return self._goals.set_goal(description, priority)
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a goal by ID"""
        return self._goals.get_goal(goal_id)
    
    def evaluate_progress(self) -> Progress:
        """Evaluate progress on all goals"""
        return self._goals.evaluate_progress()
    
    def get_next_action(self) -> Optional[Goal]:
        """Get the next goal to work on"""
        return self._goals.get_next_action()
    
    def update_goal_progress(
        self,
        goal_id: str,
        progress: float,
    ) -> Optional[Goal]:
        """Update goal progress"""
        return self._goals.update_goal(goal_id, progress=progress)
    
    def complete_goal(self, goal_id: str) -> Optional[Goal]:
        """Mark a goal as completed"""
        return self._goals.update_goal(
            goal_id,
            progress=1.0,
        )
    
    # ==================== Boundary API ====================
    
    def can_do(self, action: str) -> bool:
        """Check if action is within capability boundaries"""
        return self._boundaries.check_capability(action)
    
    def should_do(self, action: str) -> bool:
        """Check if action is ethically permissible"""
        return self._boundaries.check_ethical(action)
    
    def get_limitations(self) -> list:
        """Get all known limitations"""
        return self._boundaries.get_limitations()
    
    def get_ethical_constraints(self) -> list:
        """Get all ethical constraints"""
        return self._boundaries.get_ethical_constraints()
    
    # ==================== Integration API ====================
    
    def full_assessment(self) -> Dict[str, Any]:
        """
        Get a full cognitive assessment.
        
        Returns:
            Dictionary containing all cognitive state
        """
        return {
            "identity": self._self_awareness.get_identity().to_dict(),
            "current_state": self._self_awareness.what_am_i_doing(),
            "intention": self._self_awareness.why_am_i_doing_this(),
            "awareness_level": self._self_awareness.get_awareness_level().name,
            "active_goals": len(self._goals.get_active_goals()),
            "progress": self._goals.evaluate_progress().overall_progress,
            "limitations": self._boundaries.get_limitations(),
            "ethical_constraints": self._boundaries.get_ethical_constraints(),
        }
