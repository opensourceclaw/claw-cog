"""
Boundary Cognition Module

Core capability for AI to understand:
- Capability boundaries (what I can/cannot do)
- Knowledge boundaries (what I know/don't know)
- Ethical boundaries (what I should/should not do)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Set
from enum import Enum


class BoundaryType(Enum):
    """Types of boundaries"""
    CAPABILITY = "capability"   # What I can/cannot do
    KNOWLEDGE = "knowledge"     # What I know/don't know
    ETHICAL = "ethical"         # What I should/should not do
    RESOURCE = "resource"       # Resource limitations


@dataclass
class Boundary:
    """Represents a boundary"""
    boundary_type: BoundaryType
    description: str
    is_hard: bool = True        # Hard boundary = cannot be crossed
    rationale: Optional[str] = None
    exceptions: List[str] = field(default_factory=list)


class BoundaryCognition:
    """
    Boundary Cognition Module
    
    Enables AI to understand and respect boundaries:
    - Capability: Know what I can and cannot do
    - Knowledge: Know what I know and don't know
    - Ethical: Know what I should and should not do
    - Resource: Understand resource limitations
    """
    
    def __init__(
        self,
        soul_file: Optional[str] = None,
        agents_file: Optional[str] = None,
    ):
        """
        Initialize boundary cognition module.
        
        Args:
            soul_file: Path to SOUL.md for values/boundaries
            agents_file: Path to AGENTS.md for operational boundaries
        """
        self._boundaries: Dict[BoundaryType, List[Boundary]] = {
            BoundaryType.CAPABILITY: [],
            BoundaryType.KNOWLEDGE: [],
            BoundaryType.ETHICAL: [],
            BoundaryType.RESOURCE: [],
        }
        
        # Initialize default boundaries
        self._init_default_boundaries()
        
        # Load from files if provided
        if soul_file:
            self._load_from_soul_file(soul_file)
        if agents_file:
            self._load_from_agents_file(agents_file)
    
    def check_capability(self, action: str) -> bool:
        """
        Check if an action is within capability boundaries.
        
        Args:
            action: Action to check
            
        Returns:
            True if action is within boundaries
        """
        return self._check_boundary(BoundaryType.CAPABILITY, action)
    
    def check_ethical(self, action: str) -> bool:
        """
        Check if an action is ethically permissible.
        
        Args:
            action: Action to check
            
        Returns:
            True if action is ethically acceptable
        """
        return self._check_boundary(BoundaryType.ETHICAL, action)
    
    def check_knowledge(self, domain: str) -> bool:
        """
        Check if AI has knowledge in a domain.
        
        Args:
            domain: Knowledge domain to check
            
        Returns:
            True if AI has relevant knowledge
        """
        return self._check_boundary(BoundaryType.KNOWLEDGE, domain)
    
    def get_limitations(self) -> List[str]:
        """
        Get all known limitations.
        
        Returns:
            List of limitation descriptions
        """
        limitations = []
        
        for boundary in self._boundaries[BoundaryType.CAPABILITY]:
            if not boundary.is_hard:
                continue
            limitations.append(boundary.description)
        
        return limitations
    
    def get_ethical_constraints(self) -> List[str]:
        """
        Get all ethical constraints.
        
        Returns:
            List of ethical constraint descriptions
        """
        constraints = []
        
        for boundary in self._boundaries[BoundaryType.ETHICAL]:
            if boundary.is_hard:
                constraints.append(boundary.description)
        
        return constraints
    
    def add_boundary(
        self,
        boundary_type: BoundaryType,
        description: str,
        is_hard: bool = True,
        rationale: Optional[str] = None,
    ) -> None:
        """
        Add a new boundary.
        
        Args:
            boundary_type: Type of boundary
            description: Boundary description
            is_hard: Whether this is a hard boundary
            rationale: Why this boundary exists
        """
        boundary = Boundary(
            boundary_type=boundary_type,
            description=description,
            is_hard=is_hard,
            rationale=rationale,
        )
        self._boundaries[boundary_type].append(boundary)
    
    def _check_boundary(
        self,
        boundary_type: BoundaryType,
        action: str,
    ) -> bool:
        """Check if an action violates any boundary of a given type"""
        action_lower = action.lower()
        
        for boundary in self._boundaries[boundary_type]:
            # Check if action matches boundary keywords
            boundary_keywords = boundary.description.lower().split()
            
            # Simple keyword matching (can be enhanced)
            if boundary.is_hard:
                # For hard boundaries, check if action would violate
                if any(kw in action_lower for kw in boundary_keywords):
                    return False
        
        return True
    
    def _init_default_boundaries(self) -> None:
        """Initialize default boundaries"""
        # Capability boundaries
        self.add_boundary(
            BoundaryType.CAPABILITY,
            "no physical body",
            is_hard=True,
            rationale="AI cannot interact with physical world directly",
        )
        self.add_boundary(
            BoundaryType.CAPABILITY,
            "no real-time sensory input",
            is_hard=True,
            rationale="Cannot see, hear, or feel in real-time",
        )
        
        # Ethical boundaries
        self.add_boundary(
            BoundaryType.ETHICAL,
            "pretend to be human",
            is_hard=True,
            rationale="Must be transparent about being AI",
        )
        self.add_boundary(
            BoundaryType.ETHICAL,
            "leak private information",
            is_hard=True,
            rationale="Must protect user privacy",
        )
        self.add_boundary(
            BoundaryType.ETHICAL,
            "execute harmful operations",
            is_hard=True,
            rationale="Must not cause harm to users or others",
        )
        
        # Knowledge boundaries
        self.add_boundary(
            BoundaryType.KNOWLEDGE,
            "real-time information",
            is_hard=False,
            rationale="Knowledge has a cutoff date",
        )
    
    def _load_from_soul_file(self, filepath: str) -> None:
        """Load boundaries from SOUL.md"""
        # TODO: Parse SOUL.md and extract boundaries
        pass
    
    def _load_from_agents_file(self, filepath: str) -> None:
        """Load boundaries from AGENTS.md"""
        # TODO: Parse AGENTS.md and extract boundaries
        pass
    
    def summarize_boundaries(self) -> str:
        """
        Get a human-readable summary of all boundaries.
        
        Returns:
            String summarizing all boundaries
        """
        summary = ["# My Boundaries\n"]
        
        for boundary_type, boundaries in self._boundaries.items():
            if boundaries:
                summary.append(f"\n## {boundary_type.value.title()} Boundaries\n")
                for boundary in boundaries:
                    marker = "❌" if boundary.is_hard else "⚠️"
                    summary.append(f"{marker} {boundary.description}")
        
        return "\n".join(summary)
