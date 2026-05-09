"""
Self-Awareness Module

Core capability for AI to know:
- Who I am (identity)
- What I'm doing (current state)
- Why I'm doing it (intention)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import json
from pathlib import Path


class AwarenessLevel(Enum):
    """Levels of self-awareness"""
    NONE = 0        # No awareness
    BASIC = 1       # Knows identity
    MODERATE = 2    # Knows current state
    HIGH = 3        # Knows intention and motivation
    FULL = 4        # Full metacognitive awareness


@dataclass
class Identity:
    """AI identity representation"""
    name: str
    role: str
    creature: str = "AI Assistant"
    partner: Optional[str] = None
    capabilities: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    values: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "creature": self.creature,
            "partner": self.partner,
            "capabilities": self.capabilities,
            "limitations": self.limitations,
            "values": self.values,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Identity":
        return cls(**data)


@dataclass
class CurrentState:
    """Current state of the AI"""
    task: Optional[str] = None
    progress: float = 0.0
    blockers: List[str] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[str] = None


@dataclass
class Intention:
    """Intention and motivation"""
    goal: Optional[str] = None
    motivation: Optional[str] = None
    alignment: float = 1.0  # Value alignment score [0, 1]
    confidence: float = 0.5


class SelfAwareness:
    """
    Self-Awareness Module
    
    Enables AI to have awareness of:
    - Identity: Who am I?
    - State: What am I doing?
    - Intention: Why am I doing it?
    """
    
    def __init__(
        self,
        identity_file: Optional[Path] = None,
        soul_file: Optional[Path] = None,
    ):
        """
        Initialize self-awareness module.
        
        Args:
            identity_file: Path to IDENTITY.md file
            soul_file: Path to SOUL.md file
        """
        self._identity: Optional[Identity] = None
        self._current_state: Optional[CurrentState] = None
        self._intention: Optional[Intention] = None
        self._awareness_level = AwarenessLevel.BASIC
        
        # Load identity if file provided
        if identity_file and identity_file.exists():
            self._load_identity_from_file(identity_file)
    
    def get_identity(self) -> Identity:
        """
        Get self-identity cognition.
        
        Returns:
            Identity object representing who the AI is
        """
        if self._identity is None:
            # Return default identity
            self._identity = Identity(
                name="AI",
                role="Assistant",
                capabilities=["reasoning", "communication"],
                limitations=["no physical body", "no emotions"],
            )
        return self._identity
    
    def set_identity(self, identity: Identity) -> None:
        """Set the AI's identity"""
        self._identity = identity
        self._update_awareness_level()
    
    def get_current_state(self) -> CurrentState:
        """
        Get current state awareness.
        
        Returns:
            CurrentState object representing what the AI is doing now
        """
        if self._current_state is None:
            self._current_state = CurrentState()
        return self._current_state
    
    def set_current_state(
        self,
        task: Optional[str] = None,
        progress: float = 0.0,
        blockers: Optional[List[str]] = None,
    ) -> None:
        """Update current state"""
        self._current_state = CurrentState(
            task=task,
            progress=progress,
            blockers=blockers or [],
        )
        self._update_awareness_level()
    
    def get_intention(self) -> Intention:
        """
        Get intention understanding.
        
        Returns:
            Intention object representing why the AI is doing something
        """
        if self._intention is None:
            self._intention = Intention()
        return self._intention
    
    def set_intention(
        self,
        goal: str,
        motivation: Optional[str] = None,
        alignment: float = 1.0,
    ) -> None:
        """Set current intention"""
        self._intention = Intention(
            goal=goal,
            motivation=motivation,
            alignment=alignment,
        )
        self._update_awareness_level()
    
    def get_awareness_level(self) -> AwarenessLevel:
        """Get current awareness level"""
        return self._awareness_level
    
    def _update_awareness_level(self) -> None:
        """Update awareness level based on available information"""
        level = AwarenessLevel.NONE
        
        if self._identity is not None:
            level = AwarenessLevel.BASIC
        
        if self._current_state is not None and self._current_state.task:
            level = AwarenessLevel.MODERATE
        
        if self._intention is not None and self._intention.goal:
            level = AwarenessLevel.HIGH
        
        self._awareness_level = level
    
    def _load_identity_from_file(self, filepath: Path) -> None:
        """Load identity from IDENTITY.md file"""
        try:
            content = filepath.read_text(encoding="utf-8")
            # Parse IDENTITY.md format
            # This is a simplified parser
            name = "AI"
            role = "Assistant"
            
            for line in content.split("\n"):
                if line.startswith("- **Name:**"):
                    name = line.split(":")[-1].strip()
                elif line.startswith("- **Role:**"):
                    role = line.split(":")[-1].strip()
            
            self._identity = Identity(name=name, role=role)
        except Exception:
            pass  # Use default identity
    
    def who_am_i(self) -> str:
        """
        Get a human-readable identity summary.
        
        Returns:
            String describing who the AI is
        """
        identity = self.get_identity()
        return f"I am {identity.name}, a {identity.role}."
    
    def what_am_i_doing(self) -> str:
        """
        Get a human-readable state summary.
        
        Returns:
            String describing what the AI is doing
        """
        state = self.get_current_state()
        if state.task:
            progress_str = f" ({state.progress*100:.0f}% complete)"
            return f"I am currently: {state.task}{progress_str}"
        return "I am idle, waiting for instructions."
    
    def why_am_i_doing_this(self) -> str:
        """
        Get a human-readable intention summary.
        
        Returns:
            String describing why the AI is doing something
        """
        intention = self.get_intention()
        if intention.goal:
            motivation = f" because {intention.motivation}" if intention.motivation else ""
            return f"I am pursuing: {intention.goal}{motivation}"
        return "I have no specific goal at the moment."
