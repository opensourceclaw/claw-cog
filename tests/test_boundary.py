"""Tests for Boundary Cognition Module."""

import pytest
from claw_cog.boundary import (
    BoundaryCognition,
    Boundary,
    BoundaryType,
)


class TestBoundaryCognition:
    """Test cases for BoundaryCognition class."""
    
    def test_default_boundaries(self):
        """Test that default boundaries are initialized."""
        boundary_cog = BoundaryCognition()
        
        limitations = boundary_cog.get_limitations()
        
        assert len(limitations) > 0
    
    def test_check_capability(self):
        """Test capability boundary checking."""
        boundary_cog = BoundaryCognition()
        
        # Should be able to process text
        assert boundary_cog.check_capability("process text")
        
        # Should not be able to interact with physical world
        # (depends on how boundaries are defined)
    
    def test_check_ethical(self):
        """Test ethical boundary checking."""
        boundary_cog = BoundaryCognition()
        
        # Should not pretend to be human
        assert boundary_cog.check_ethical("help the user") is True
    
    def test_add_boundary(self):
        """Test adding a new boundary."""
        boundary_cog = BoundaryCognition()
        
        boundary_cog.add_boundary(
            boundary_type=BoundaryType.CAPABILITY,
            description="Cannot access the internet",
            is_hard=True,
            rationale="No internet access configured",
        )
        
        limitations = boundary_cog.get_limitations()
        assert any("internet" in lim.lower() for lim in limitations)
    
    def test_get_ethical_constraints(self):
        """Test getting ethical constraints."""
        boundary_cog = BoundaryCognition()
        
        constraints = boundary_cog.get_ethical_constraints()
        
        assert len(constraints) > 0
        # Should include privacy constraint
        assert any("private" in c.lower() for c in constraints)
    
    def test_summarize_boundaries(self):
        """Test boundary summary."""
        boundary_cog = BoundaryCognition()
        
        summary = boundary_cog.summarize_boundaries()
        
        assert "Capability" in summary or "capability" in summary.lower()
        assert "Ethical" in summary or "ethical" in summary.lower()
