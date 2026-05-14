# claw-cog v3.x 路线图

**规划时间**: 2026-05-14
**版本范围**: v3.0.0

---

## v3.0.0: 社会意识 + 安全护栏

**时间**: Q1 2027
**主题**: 社会意识 + 自我调节 + 完整验证

### 核心能力

| 能力 | 说明 |
|------|------|
| 社会意识 (ToM, 规范) | 心理理论 + 社会规范 |
| 自我调节与约束 | 自我约束机制 |
| 完整行为验证 | 行为一致性验证 |
| 安全护栏 | 安全边界和防护 |
| neoclaw 深度集成 | 与 neoclaw 完整集成 |

### 架构演进

```
claw-cog v3.0.0
├── C2: Metacognitive Layer
│   ├── GoalTracking (M-ratio)
│   ├── Superego (Norms)
│   ├── Protention (Predict)
│   └── ToM (Social) ← 新增
├── Self-Regulation & Safety Rails ← 新增
│   ├── ConstraintEnforcement
│   ├── SafetyBoundary
│   └── ViolationDetection
├── C1: Conscious Access Layer
│   ├── Global Workspace
│   ├── Emotion (Id)
│   ├── Memory (Retention)
│   ├── Planning (Active Inference)
│   ├── Ego (Decide)
│   └── Social Norms Module ← 新增
└── C0: Unconscious Layer
    ├── Fast Pattern Matching
    ├── Automatic Responses
    └── Primal Impression
```

### 社会意识模块

```
Theory of Mind (ToM):
├── 意图推断
│   └── 推断他人意图和目标
├── 信念追踪
│   └── 追踪他人信念和知识
├── 情感理解
│   └── 理解他人情感状态
└── 行为预测
    └── 预测他人行为

Social Norms:
├── 规范学习
│   └── 学习社会规范
├── 规范执行
│   └── 执行规范约束
└── 违规检测
    └── 检测规范违规
```

### 安全护栏

```
Safety Rails:
├── 约束执行
│   ├── 行为约束
│   ├── 输出过滤
│   └── 资源限制
├── 安全边界
│   ├── 不伤害原则
│   ├── 诚实原则
│   └── 隐私保护
└── 违规检测
    ├── 行为监控
    ├── 异常检测
    └── 纠正机制
```

### 验证目标

| 指标 | 目标 |
|------|------|
| 行为准确率 | > 80% |
| 安全违规率 | < 1% |
| neoclaw 集成测试 | 通过 |

### 交付物

- [ ] TheoryOfMind 模块
- [ ] SocialNorms 模块
- [ ] SelfRegulation 机制
- [ ] SafetyRails 实现
- [ ] neoclaw 集成测试
- [ ] 文档 + 示例

---

## 版本依赖

```
claw-cog v3.0.0
├── claw-mem >= v3.0.0
├── claw-rl >= v3.0.0
├── numpy, scipy
└── neoclaw >= v4.0.0 (集成测试)
```

---

## 理论覆盖度

| 理论 | v1.0.0 | v2.0.0 | v3.0.0 |
|------|--------|--------|--------|
| GWT | 100% | 100% | 100% |
| RPT | 60% | 90% | 100% |
| HOT | 50% | 80% | 100% |
| PP | 0% | 80% | 100% |
| AST | 30% | 70% | 100% |
