# claw-cog v2.x 路线图

**规划时间**: 2026-05-14
**版本范围**: v2.0.0

---

## v2.0.0: PP + 深度自进化

**时间**: Q4 2026
**主题**: Perceptual Presence + 深度自进化

### 核心能力

| 能力 | 说明 |
|------|------|
| Perceptual Presence (PP) | 感知存在感 |
| Id/Ego/Superego 三层代理 | 心理动力学模型 |
| 深度自进化机制 | 自我改进和演化 |
| MUSE 能力感知框架 | 能力边界感知 |

### 架构演进

```
claw-cog v2.0.0
├── C2: Metacognitive Layer
│   ├── GoalTracking (M-ratio)
│   ├── Superego (Norms)
│   └── Protention (Predict)
├── C1: Conscious Access Layer
│   ├── Global Workspace
│   ├── Emotion (Id)
│   ├── Memory (Retention)
│   ├── Planning
│   └── Ego (Decide)
└── C0: Unconscious Layer
    ├── Fast Pattern Matching
    ├── Automatic Responses
    └── Primal Impression
```

### 三层代理架构

```
┌─────────────────────────────────────────┐
│         Superego (C2 上层)               │
│  规范、道德、理想自我                    │
│  - 社会规范执行                          │
│  - 道德判断                              │
│  - 自我理想                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Ego (C1 决策层)                  │
│  现实原则、决策、平衡                    │
│  - 现实决策                              │
│  - 需求-规范平衡                         │
│  - 执行控制                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│         Id (C0/C1 冲动层)                │
│  快乐原则、本能、欲望                    │
│  - 本能驱动                              │
│  - 即时满足                              │
│  - 情绪反应                              │
└─────────────────────────────────────────┘
```

### MUSE 能力感知

```python
class MUSECapabilityAwareness:
    """
    MUSE 能力感知框架
    
    来源: MUSE (Meta-awareness of Uncertainty and Skill Estimation)
    """
    def estimate_capability(self, task: Task) -> CapabilityEstimate:
        # 估计任务能力需求
        # 评估自身能力边界
        # 决定是否求助
        pass
```

### 验证目标

| 指标 | 目标 |
|------|------|
| CogniPair 基准 | > 75% |
| 自进化收敛 | 可观测 |

### 交付物

- [ ] PerceptualPresence
- [ ] IdEgoSuperego 架构
- [ ] SelfEvolver
- [ ] MUSECapabilityAwareness
- [ ] 文档 + 示例

---

## 版本依赖

```
claw-cog v2.0.0
├── claw-mem >= v3.0.0
├── claw-rl >= v3.0.0
└── numpy, scipy (预测处理)
```
