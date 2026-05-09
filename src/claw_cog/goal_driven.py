"""
Goal-Driven Module

Core capability for AI to:
- Set and pursue goals
- Decompose goals into sub-goals
- Track progress
- Adapt strategies
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import time


class GoalStatus(Enum):
    """Status of a goal"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    ABANDONED = "abandoned"


class GoalPriority(Enum):
    """Priority levels for goals"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Goal:
    """Represents a goal"""
    id: str
    description: str
    status: GoalStatus = GoalStatus.PENDING
    priority: GoalPriority = GoalPriority.MEDIUM
    parent_id: Optional[str] = None
    sub_goals: List[str] = field(default_factory=list)
    progress: float = 0.0
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    deadline: Optional[float] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Progress:
    """Progress tracking for goals"""
    completed: List[str] = field(default_factory=list)
    in_progress: List[str] = field(default_factory=list)
    blocked: List[str] = field(default_factory=list)
    pending: List[str] = field(default_factory=list)
    overall_progress: float = 0.0


class GoalDriven:
    """
    Goal-Driven Module
    
    Enables AI to:
    - Set and pursue goals autonomously
    - Decompose complex goals
    - Track progress
    - Adapt strategies when blocked
    """
    
    def __init__(self, memory_provider=None, learning_provider=None):
        """
        Initialize goal-driven module.
        
        Args:
            memory_provider: claw-mem provider for goal persistence
            learning_provider: claw-rl provider for strategy optimization
        """
        self._memory_provider = memory_provider
        self._learning_provider = learning_provider
        self._goals: Dict[str, Goal] = {}
        self._goal_counter = 0
    
    def set_goal(
        self,
        description: str,
        priority: GoalPriority = GoalPriority.MEDIUM,
        parent_id: Optional[str] = None,
        deadline: Optional[float] = None,
    ) -> Goal:
        """
        Set a new goal.
        
        Args:
            description: Goal description
            priority: Goal priority level
            parent_id: Parent goal ID if this is a sub-goal
            deadline: Optional deadline timestamp
            
        Returns:
            The created goal
        """
        # Generate unique ID
        self._goal_counter += 1
        goal_id = f"goal_{self._goal_counter}"
        
        # Create goal
        goal = Goal(
            id=goal_id,
            description=description,
            priority=priority,
            parent_id=parent_id,
            deadline=deadline,
        )
        
        # Add to parent's sub-goals if applicable
        if parent_id and parent_id in self._goals:
            self._goals[parent_id].sub_goals.append(goal_id)
        
        # Store goal
        self._goals[goal_id] = goal
        
        # Auto-decompose complex goals
        if self._should_decompose(goal):
            self._decompose_goal(goal)
        
        return goal
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a goal by ID"""
        return self._goals.get(goal_id)
    
    def update_goal(
        self,
        goal_id: str,
        status: Optional[GoalStatus] = None,
        progress: Optional[float] = None,
    ) -> Optional[Goal]:
        """Update goal status and progress"""
        goal = self._goals.get(goal_id)
        if not goal:
            return None
        
        if status:
            goal.status = status
        if progress is not None:
            goal.progress = progress
        
        goal.updated_at = time.time()
        
        # Update parent's progress if this is a sub-goal
        if goal.parent_id:
            self._update_parent_progress(goal.parent_id)
        
        return goal
    
    def evaluate_progress(self, goal_id: Optional[str] = None) -> Progress:
        """
        Evaluate progress on goals.
        
        Args:
            goal_id: Specific goal ID, or None for all top-level goals
            
        Returns:
            Progress object with status breakdown
        """
        if goal_id:
            goals = [self._goals.get(goal_id)]
            goals = [g for g in goals if g]
        else:
            # Get top-level goals
            goals = [g for g in self._goals.values() if g.parent_id is None]
        
        progress = Progress()
        
        for goal in goals:
            if goal.status == GoalStatus.COMPLETED:
                progress.completed.append(goal.id)
            elif goal.status == GoalStatus.IN_PROGRESS:
                progress.in_progress.append(goal.id)
            elif goal.status == GoalStatus.BLOCKED:
                progress.blocked.append(goal.id)
            else:
                progress.pending.append(goal.id)
        
        # Calculate overall progress
        if goals:
            progress.overall_progress = sum(g.progress for g in goals) / len(goals)
        
        return progress
    
    def get_active_goals(self) -> List[Goal]:
        """Get all active (in-progress) goals"""
        return [
            g for g in self._goals.values()
            if g.status == GoalStatus.IN_PROGRESS
        ]
    
    def get_next_action(self) -> Optional[Goal]:
        """
        Get the next goal to work on based on priority and status.
        
        Returns:
            The highest priority pending/in-progress goal
        """
        candidates = [
            g for g in self._goals.values()
            if g.status in (GoalStatus.PENDING, GoalStatus.IN_PROGRESS)
        ]
        
        if not candidates:
            return None
        
        # Sort by priority (descending) and creation time (ascending)
        candidates.sort(key=lambda g: (-g.priority.value, g.created_at))
        
        return candidates[0]
    
    def _should_decompose(self, goal: Goal) -> bool:
        """Determine if a goal should be auto-decomposed"""
        # Heuristic: goals with >10 words or containing certain keywords
        complex_keywords = ["and", "then", "after", "first", "finally"]
        description_lower = goal.description.lower()
        
        return (
            len(goal.description.split()) > 10 or
            any(kw in description_lower for kw in complex_keywords)
        )
    
    def _decompose_goal(self, goal: Goal) -> None:
        """Decompose a complex goal into sub-goals"""
        # Simplified decomposition: split by "and", "then", etc.
        # In practice, this would use LLM or sophisticated parsing
        
        parts = goal.description.split(" and ")
        
        if len(parts) > 1:
            for i, part in enumerate(parts):
                sub_goal = self.set_goal(
                    description=part.strip(),
                    priority=goal.priority,
                    parent_id=goal.id,
                    deadline=goal.deadline,
                )
                goal.sub_goals.append(sub_goal.id)
    
    def _update_parent_progress(self, parent_id: str) -> None:
        """Update parent goal's progress based on sub-goals"""
        parent = self._goals.get(parent_id)
        if not parent or not parent.sub_goals:
            return
        
        # Calculate average of sub-goal progress
        sub_goals = [
            self._goals.get(sg_id)
            for sg_id in parent.sub_goals
        ]
        sub_goals = [g for g in sub_goals if g]
        
        if sub_goals:
            parent.progress = sum(g.progress for g in sub_goals) / len(sub_goals)
            
            # Update status based on sub-goals
            if all(g.status == GoalStatus.COMPLETED for g in sub_goals):
                parent.status = GoalStatus.COMPLETED
            elif any(g.status == GoalStatus.IN_PROGRESS for g in sub_goals):
                parent.status = GoalStatus.IN_PROGRESS
            elif any(g.status == GoalStatus.BLOCKED for g in sub_goals):
                parent.status = GoalStatus.BLOCKED
            
            parent.updated_at = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize goals to dictionary"""
        return {
            goal_id: {
                "id": goal.id,
                "description": goal.description,
                "status": goal.status.value,
                "priority": goal.priority.value,
                "parent_id": goal.parent_id,
                "sub_goals": goal.sub_goals,
                "progress": goal.progress,
            }
            for goal_id, goal in self._goals.items()
        }
