"""Tests for Reflective Reasoning Module."""

import pytest
from claw_cog_legacy.reflective import (
    ReflectiveReasoning,
    Action,
    Outcome,
    Reflection,
    MetaReasoning,
)


class TestReflectiveReasoning:
    """Test cases for ReflectiveReasoning class."""
    
    def test_reflect_on_successful_action(self):
        """Test reflection on a successful action."""
        reflection_module = ReflectiveReasoning()
        
        action = Action(
            description="Completed the task",
            reasoning="Used efficient approach",
        )
        outcome = Outcome(success=True, result="Task completed")
        
        reflection = reflection_module.reflect_on_action(action, outcome)
        
        assert reflection.outcome.success is True
        assert len(reflection.lessons) > 0
    
    def test_reflect_on_failed_action(self):
        """Test reflection on a failed action."""
        reflection_module = ReflectiveReasoning()
        
        action = Action(description="Attempted the task")
        outcome = Outcome(
            success=False,
            result="Task failed",
            unexpected=["Resource unavailable"],
        )
        
        reflection = reflection_module.reflect_on_action(action, outcome)
        
        assert reflection.outcome.success is False
        assert len(reflection.improvements) > 0
    
    def test_meta_reasoning(self):
        """Test metacognitive analysis."""
        reflection_module = ReflectiveReasoning()
        
        meta = reflection_module.meta_reasoning(
            problem="How should I approach this?",
            context={"complexity": "high"},
        )
        
        assert meta.problem == "How should I approach this?"
        assert len(meta.approach) > 0
        assert len(meta.alternatives) > 0
    
    def test_reflection_history(self):
        """Test reflection history tracking."""
        reflection_module = ReflectiveReasoning()
        
        # Create multiple reflections
        for i in range(3):
            action = Action(description=f"Action {i}")
            outcome = Outcome(success=True)
            reflection_module.reflect_on_action(action, outcome)
        
        history = reflection_module.get_reflection_history()
        
        assert len(history) == 3
    
    def test_lessons_extraction(self):
        """Test that lessons are extracted from actions."""
        reflection_module = ReflectiveReasoning()
        
        action = Action(
            description="Solved the problem",
            context={"condition": "clear requirements"},
        )
        outcome = Outcome(success=True)
        
        reflection = reflection_module.reflect_on_action(action, outcome)
        
        assert len(reflection.lessons) > 0
        # Check that lesson mentions the condition
        lessons_text = " ".join(reflection.lessons)
        assert "clear requirements" in lessons_text or "succeed" in lessons_text.lower()
