"""Custom configuration + C2 metacognitive monitoring."""
from claw_cog import Config, ConsciousAgent

# Custom configuration
config = Config(
    c0_pattern_threshold=0.5,
    c2_high_threshold=0.9,
    assessment_min_samples=5,
    workspace_max_subscribers=20,
)

agent = ConsciousAgent(config=config, enable_c2=True)

# Process varying inputs
for text in [
    "What is the capital of France?",
    "Explain quantum computing.",
    "Write a haiku about AI.",
    "Solve 2+2.",
    "How are you feeling today?",
]:
    result = agent.process(text)
    print(f"Q: {text[:40]}... → "
          f"level={result.level.name}, "
          f"conf={result.confidence:.2f}")

# Metacognition
metrics = agent.assess_metacognition()
print(f"\nmeta-d': {metrics['meta_d_prime']:.3f}, "
      f"d': {metrics['d_prime']:.3f}, "
      f"Type-2 AUC: {metrics['type2_roc_auc']:.3f}")
