"""
Reflective Reasoning Module

Core capability for AI to reflect on:
- Own behaviors and decisions
- Success/failure causality
- Lessons learned
- Metacognitive analysis
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import time


class ReflectionType(Enum):
    """Types of reflection"""
    ACTION = "action"           # Reflect on specific action
    DECISION = "decision"       # Reflect on decision
    OUTCOME = "outcome"         # Reflect on outcome
    STRATEGY = "strategy"       # Reflect on overall strategy
    METACOGNITIVE = "meta"      # Reflect on thinking process


@dataclass
class Action:
    """Represents an action taken"""
    description: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    reasoning: Optional[str] = None


@dataclass
class Outcome:
    """Represents an outcome of an action"""
    success: bool
    result: Optional[str] = None
    side_effects: List[str] = field(default_factory=list)
    unexpected: List[str] = field(default_factory=list)


@dataclass
class Reflection:
    """Result of reflection on an action"""
    action: Action
    outcome: Outcome
    reasoning: str                      # Why did this succeed/fail?
    lessons: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    confidence: float = 0.5


@dataclass
class MetaReasoning:
    """Result of metacognitive analysis"""
    problem: str
    approach: str                       # How am I thinking about this?
    confidence: float = 0.5
    alternatives: List[str] = field(default_factory=list)
    blind_spots: List[str] = field(default_factory=list)


class ReflectiveReasoning:
    """
    Reflective Reasoning Module
    
    Enables AI to:
    - Reflect on actions and outcomes
    - Extract causal reasoning
    - Learn lessons from experience
    - Perform metacognitive analysis
    """
    
    def __init__(self, memory_provider=None, learning_provider=None):
        """
        Initialize reflective reasoning module.
        
        Args:
            memory_provider: claw-mem provider for storing reflections
            learning_provider: claw-rl provider for extracting rules
        """
        self._memory_provider = memory_provider
        self._learning_provider = learning_provider
        self._reflection_history: List[Reflection] = []
    
    def reflect_on_action(
        self,
        action: Action,
        outcome: Outcome,
    ) -> Reflection:
        """
        Reflect on a specific action and its outcome.
        
        Args:
            action: The action taken
            outcome: The outcome of the action
            
        Returns:
            Reflection containing insights and lessons
        """
        # Analyze causality
        reasoning = self._analyze_causality(action, outcome)
        
        # Extract lessons
        lessons = self._extract_lessons(action, outcome)
        
        # Suggest improvements
        improvements = self._suggest_improvements(action, outcome)
        
        # Create reflection
        reflection = Reflection(
            action=action,
            outcome=outcome,
            reasoning=reasoning,
            lessons=lessons,
            improvements=improvements,
            confidence=self._assess_confidence(action, outcome),
        )
        
        # Store in history
        self._reflection_history.append(reflection)
        
        # Optionally store to memory
        if self._memory_provider:
            self._store_reflection(reflection)
        
        return reflection
    
    def meta_reasoning(
        self,
        problem: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> MetaReasoning:
        """
        Perform metacognitive analysis: think about thinking.
        
        Args:
            problem: The problem to analyze
            context: Additional context
            
        Returns:
            MetaReasoning containing analysis
        """
        # Analyze approach
        approach = self._select_approach(problem, context)
        
        # Assess confidence
        confidence = self._assess_meta_confidence(problem, approach)
        
        # Generate alternatives
        alternatives = self._generate_alternatives(problem, approach)
        
        # Identify blind spots
        blind_spots = self._identify_blind_spots(problem, context)
        
        return MetaReasoning(
            problem=problem,
            approach=approach,
            confidence=confidence,
            alternatives=alternatives,
            blind_spots=blind_spots,
        )
    
    def _analyze_causality(
        self,
        action: Action,
        outcome: Outcome,
    ) -> str:
        """Analyze why an action led to a specific outcome"""
        if outcome.success:
            return f"The action '{action.description}' succeeded. " \
                   f"Key factors: {self._identify_success_factors(action, outcome)}"
        else:
            return f"The action '{action.description}' failed. " \
                   f"Root cause: {self._identify_failure_cause(action, outcome)}"
    
    def _extract_lessons(
        self,
        action: Action,
        outcome: Outcome,
    ) -> List[str]:
        """Extract lessons from the action-outcome pair"""
        lessons = []
        
        if outcome.success:
            lessons.append(f"When {action.context.get('condition', 'similar conditions')}, "
                          f"{action.description} tends to succeed")
        else:
            lessons.append(f"Warning: {action.description} failed under "
                          f"{action.context.get('condition', 'these conditions')}")
        
        # Add specific lessons from unexpected outcomes
        for unexpected in outcome.unexpected:
            lessons.append(f"Unexpected: {unexpected}")
        
        return lessons
    
    def _suggest_improvements(
        self,
        action: Action,
        outcome: Outcome,
    ) -> List[str]:
        """Suggest improvements for future similar actions"""
        improvements = []
        
        if not outcome.success:
            improvements.append("Consider alternative approaches")
            improvements.append("Review assumptions before executing")
        
        if outcome.side_effects:
            improvements.append("Be aware of potential side effects")
        
        return improvements
    
    def _assess_confidence(
        self,
        action: Action,
        outcome: Outcome,
    ) -> float:
        """Assess confidence in the reflection"""
        # Base confidence on outcome clarity
        if outcome.success:
            return 0.8
        elif outcome.unexpected:
            return 0.5  # Less confident when unexpected outcomes
        else:
            return 0.6
    
    def _select_approach(
        self,
        problem: str,
        context: Optional[Dict[str, Any]],
    ) -> str:
        """Select reasoning approach for the problem"""
        # Simplified approach selection
        if "how" in problem.lower():
            return "Procedural reasoning: breaking down into steps"
        elif "why" in problem.lower():
            return "Causal reasoning: identifying causes"
        elif "what" in problem.lower():
            return "Descriptive reasoning: characterizing the problem"
        else:
            return "Analytical reasoning: systematic analysis"
    
    def _assess_meta_confidence(
        self,
        problem: str,
        approach: str,
    ) -> float:
        """Assess confidence in the metacognitive analysis"""
        # Simplified confidence assessment
        return 0.7
    
    def _generate_alternatives(
        self,
        problem: str,
        current_approach: str,
    ) -> List[str]:
        """Generate alternative approaches"""
        return [
            "Consider the problem from a different angle",
            "Break down into smaller sub-problems",
            "Seek external input or validation",
        ]
    
    def _identify_blind_spots(
        self,
        problem: str,
        context: Optional[Dict[str, Any]],
    ) -> List[str]:
        """Identify potential blind spots in reasoning"""
        blind_spots = []
        
        if not context:
            blind_spots.append("Lack of context may lead to incomplete understanding")
        
        blind_spots.append("Cognitive biases may affect reasoning")
        
        return blind_spots
    
    def _identify_success_factors(
        self,
        action: Action,
        outcome: Outcome,
    ) -> str:
        """Identify factors that contributed to success"""
        if action.reasoning:
            return action.reasoning
        return "appropriate approach and correct execution"
    
    def _identify_failure_cause(
        self,
        action: Action,
        outcome: Outcome,
    ) -> str:
        """Identify the root cause of failure"""
        if outcome.unexpected:
            return f"unexpected factors: {', '.join(outcome.unexpected)}"
        return "approach may not be suitable for this context"
    
    def _store_reflection(self, reflection: Reflection) -> None:
        """Store reflection in memory provider"""
        # TODO: Implement storage via memory provider
        pass
    
    def get_reflection_history(
        self,
        limit: int = 10,
    ) -> List[Reflection]:
        """Get recent reflection history"""
        return self._reflection_history[-limit:]
