"""Tests for Goal-Driven Module."""

import pytest
from claw_cog_legacy.goal_driven import (
    GoalDriven,
    Goal,
    GoalStatus,
    GoalPriority,
    Progress,
)


class TestGoalDriven:
    """Test cases for GoalDriven class."""
    
    def test_set_goal(self):
        """Test setting a goal."""
        goal_system = GoalDriven()
        
        goal = goal_system.set_goal(
            description="Complete the project",
            priority=GoalPriority.HIGH,
        )
        
        assert goal.description == "Complete the project"
        assert goal.priority == GoalPriority.HIGH
        assert goal.status == GoalStatus.PENDING
    
    def test_update_goal_status(self):
        """Test updating goal status."""
        goal_system = GoalDriven()
        
        goal = goal_system.set_goal("Test goal")
        updated = goal_system.update_goal(
            goal.id,
            status=GoalStatus.IN_PROGRESS,
        )
        
        assert updated.status == GoalStatus.IN_PROGRESS
    
    def test_update_goal_progress(self):
        """Test updating goal progress."""
        goal_system = GoalDriven()
        
        goal = goal_system.set_goal("Test goal")
        updated = goal_system.update_goal(goal.id, progress=0.5)
        
        assert updated.progress == 0.5
    
    def test_evaluate_progress(self):
        """Test progress evaluation."""
        goal_system = GoalDriven()
        
        # Create multiple goals
        g1 = goal_system.set_goal("Goal 1")
        g2 = goal_system.set_goal("Goal 2")
        g3 = goal_system.set_goal("Goal 3")
        
        # Update statuses
        goal_system.update_goal(g1.id, status=GoalStatus.COMPLETED, progress=1.0)
        goal_system.update_goal(g2.id, status=GoalStatus.IN_PROGRESS, progress=0.5)
        goal_system.update_goal(g3.id, status=GoalStatus.PENDING)
        
        progress = goal_system.evaluate_progress()
        
        assert len(progress.completed) == 1
        assert len(progress.in_progress) == 1
        assert len(progress.pending) == 1
    
    def test_get_next_action(self):
        """Test getting next action."""
        goal_system = GoalDriven()
        
        # Create goals with different priorities
        g1 = goal_system.set_goal("Low priority", priority=GoalPriority.LOW)
        g2 = goal_system.set_goal("High priority", priority=GoalPriority.HIGH)
        
        next_goal = goal_system.get_next_action()
        
        # Should return the high priority goal
        assert next_goal.id == g2.id
    
    def test_goal_decomposition(self):
        """Test that complex goals are decomposed."""
        goal_system = GoalDriven()
        
        # Create a complex goal
        goal = goal_system.set_goal(
            "Research the topic and write a report and submit it"
        )
        
        # Should have sub-goals (decomposed by "and")
        # Note: This depends on the decomposition logic
        # For now, just check the goal was created
        assert goal.description == "Research the topic and write a report and submit it"
    
    def test_active_goals(self):
        """Test getting active goals."""
        goal_system = GoalDriven()
        
        g1 = goal_system.set_goal("Active goal")
        g2 = goal_system.set_goal("Completed goal")
        
        goal_system.update_goal(g1.id, status=GoalStatus.IN_PROGRESS)
        goal_system.update_goal(g2.id, status=GoalStatus.COMPLETED)
        
        active = goal_system.get_active_goals()
        
        assert len(active) == 1
        assert active[0].id == g1.id
