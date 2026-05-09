"""Tests for Cognition Engine."""

import pytest
from claw_cog import CognitionEngine
from claw_cog.self_awareness import Identity
from claw_cog.goal_driven import GoalPriority


class TestCognitionEngine:
    """Test cases for CognitionEngine class."""
    
    def test_initialization(self):
        """Test engine initialization."""
        engine = CognitionEngine()
        
        assert engine is not None
    
    def test_who_am_i(self):
        """Test identity retrieval."""
        engine = CognitionEngine()
        identity = Identity(name="Friday", role="AI Assistant")
        engine.set_identity(identity)
        
        result = engine.who_am_i()
        
        assert result.name == "Friday"
    
    def test_set_and_evaluate_goal(self):
        """Test goal setting and evaluation."""
        engine = CognitionEngine()
        
        goal = engine.set_goal("Test goal", priority=GoalPriority.HIGH)
        
        assert goal.description == "Test goal"
        
        progress = engine.evaluate_progress()
        assert progress.overall_progress == 0.0
    
    def test_reflect(self):
        """Test reflection on action."""
        engine = CognitionEngine()
        
        reflection = engine.reflect(
            action_description="Completed a task",
            outcome_success=True,
            outcome_result="Task done",
        )
        
        assert reflection.outcome.success is True
        assert len(reflection.lessons) > 0
    
    def test_boundary_checks(self):
        """Test boundary checking."""
        engine = CognitionEngine()
        
        # Should be able to process text
        assert engine.can_do("process text")
        
        # Should be ethical to help users
        assert engine.should_do("help the user")
    
    def test_full_assessment(self):
        """Test full cognitive assessment."""
        engine = CognitionEngine()
        
        # Set some state
        identity = Identity(name="Test", role="Test")
        engine.set_identity(identity)
        engine.set_goal("Test goal")
        
        assessment = engine.full_assessment()
        
        assert "identity" in assessment
        assert "current_state" in assessment
        assert "active_goals" in assessment
        assert "limitations" in assessment
    
    def test_set_current_task(self):
        """Test setting current task."""
        engine = CognitionEngine()
        
        engine.set_current_task("Testing the engine", progress=0.5)
        
        state = engine.what_am_i_doing()
        
        assert "Testing the engine" in state
        assert "50%" in state
