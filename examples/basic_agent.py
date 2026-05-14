"""Basic usage example — ConsciousAgent with defaults."""
from claw_cog import ConsciousAgent

agent = ConsciousAgent()

# Process input through consciousness layers
result = agent.process("What is the project status?")
print(f"Output: {result.output}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Level: {result.level.name}")

# Check indicators
indicators = agent.get_indicator_properties()
print(f"Indicators: GWT={indicators['GWT']}, "
      f"RPT={indicators['RPT']['feedback_loops']}, "
      f"HOT={indicators['HOT']['higher_order_representation']}")

# Metacognitive assessment (needs 5+ rounds)
agent.generate_calibration_data(10)
metrics = agent.assess_metacognition()
print(f"meta-d': {metrics['meta_d_prime']:.3f}, "
      f"M-ratio: {metrics['m_ratio']:.3f}")
