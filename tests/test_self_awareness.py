"""Tests for Self-Awareness Module."""

import pytest
from claw_cog.self_awareness import (
    SelfAwareness,
    Identity,
    CurrentState,
    Intention,
    AwarenessLevel,
)


class TestSelfAwareness:
    """Test cases for SelfAwareness class."""
    
    def test_default_identity(self):
        """Test default identity creation."""
        awareness = SelfAwareness()
        identity = awareness.get_identity()
        
        assert identity.name == "AI"
        assert identity.role == "Assistant"
    
    def test_set_identity(self):
        """Test setting identity."""
        awareness = SelfAwareness()
        identity = Identity(
            name="Friday",
            role="AI Assistant",
            partner="Peter",
        )
        
        awareness.set_identity(identity)
        result = awareness.get_identity()
        
        assert result.name == "Friday"
        assert result.role == "AI Assistant"
    
    def test_set_current_state(self):
        """Test setting current state."""
        awareness = SelfAwareness()
        awareness.set_current_state(
            task="Writing tests",
            progress=0.5,
            blockers=["Need more coffee"],
        )
        
        state = awareness.get_current_state()
        
        assert state.task == "Writing tests"
        assert state.progress == 0.5
        assert "Need more coffee" in state.blockers
    
    def test_set_intention(self):
        """Test setting intention."""
        awareness = SelfAwareness()
        awareness.set_intention(
            goal="Complete the project",
            motivation="To help the user",
        )
        
        intention = awareness.get_intention()
        
        assert intention.goal == "Complete the project"
        assert intention.motivation == "To help the user"
    
    def test_awareness_level_progression(self):
        """Test awareness level increases with information."""
        awareness = SelfAwareness()
        
        # Start with NONE
        assert awareness.get_awareness_level() == AwarenessLevel.NONE
        
        # Add identity -> BASIC
        awareness.set_identity(Identity(name="Test", role="Test"))
        assert awareness.get_awareness_level() == AwarenessLevel.BASIC
        
        # Add state -> MODERATE
        awareness.set_current_state(task="Testing")
        assert awareness.get_awareness_level() == AwarenessLevel.MODERATE
        
        # Add intention -> HIGH
        awareness.set_intention(goal="Test everything")
        assert awareness.get_awareness_level() == AwarenessLevel.HIGH
    
    def test_who_am_i(self):
        """Test human-readable identity."""
        awareness = SelfAwareness()
        identity = Identity(name="Friday", role="AI Assistant")
        awareness.set_identity(identity)
        
        result = awareness.who_am_i()
        
        assert "Friday" in result
        assert "AI Assistant" in result
    
    def test_what_am_i_doing(self):
        """Test human-readable state."""
        awareness = SelfAwareness()
        awareness.set_current_state(task="Testing", progress=0.5)
        
        result = awareness.what_am_i_doing()
        
        assert "Testing" in result
        assert "50%" in result
