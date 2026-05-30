# claw-cog v1.x-v2.x 路线图

**规划时间**: 2026-05-23
**当前版本**: v1.5.0
**版本范围**: v1.5.0 → v2.0.0
**框架**: ETCLOVG (Agent Harness Engineering)
**对齐**: Digital Brain 演化路径 (记忆→学习→意识)

---

## 现状分析

### 当前版本 v1.5.0

| 能力 | 状态 | 说明 |
|------|------|------|
| C0 无意识层 | ✅ 已实现 | 快速模式匹配、自动响应 |
| C1 意识层 | ✅ 已实现 | 全局工作空间、整合广播 |
| C2 元认知层 | ✅ 已实现 | 自我监控、信心评估 |
| 时间意识 | ✅ 已实现 | ITCMA 架构 |
| V (验证) | ❌ 缺失 | 无自我评估能力 |
| O (可观测) | ❌ 缺失 | 无内部状态观测 |
| G (治理) | ❌ 缺失 | 无安全边界 |

### ETCLOVG 当前覆盖

```
claw-cog        E    T    C    L    O    V    G
─────────────────────────────────────────────────
当前状态        -    -   ✅   ✅   -    -    -
```

---

## 迭代规划

### v1.6.0: 补齐验证层 (V)

**时间**: 2026 Q2-Q3
**主题**: 自我评估与质量验证
**ETCLOVG 新增**: V

#### 核心能力

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **输出验证** | 验证处理结果的正确性 | P0 |
| **置信度校准** | 校准 C2 的置信度评估 | P0 |
| **质量评估** | 评估输出质量 | P1 |
| **自我测试** | 内部测试能力 | P1 |

#### 架构设计

```
claw-cog v1.6.0 验证层:
├── 验证引擎层 (Verification Engine)
│   ├── OutputValidator    → 输出验证器
│   ├── ConfidenceCalibrator→ 置信度校准器
│   ├── QualityAssessor    → 质量评估器
│   └── ConsistencyChecker → 一致性检查器
├── 测试框架层 (Test Framework)
│   ├── SelfTestRunner     → 自测试运行器
│   ├── TestCaseGenerator  → 测试用例生成
│   └── ResultAnalyzer     → 结果分析器
└── 反馈回路 (Feedback Loop)
    └── VerificationFeedback → 验证反馈
```

#### 交付物

- [ ] OutputValidator 类
- [ ] ConfidenceCalibrator 类
- [ ] QualityAssessor 类
- [ ] SelfTestRunner 类
- [ ] 验证 API 集成到 ConsciousAgent
- [ ] 单元测试 (覆盖率 >85%)

#### 依赖

```
claw-cog v1.6.0
├── claw-cog v1.5.0
└── claw-rl >= v1.0.0 (可选，用于学习反馈)
```

---

### v1.7.0: 补齐可观测层 (O)

**时间**: 2026 Q3
**主题**: 内部状态观测与监控
**ETCLOVG 新增**: O

#### 核心能力

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **状态观测** | 观测 C0/C1/C2 层状态 | P0 |
| **行为日志** | 记录处理行为 | P0 |
| **性能监控** | 监控处理性能 | P1 |
| **健康检查** | 检查系统健康状态 | P1 |

#### 架构设计

```
claw-cog v1.7.0 可观测层:
├── 观测引擎层 (Observability Engine)
│   ├── StateObserver      → 状态观测器
│   ├── BehaviorLogger     → 行为日志器
│   ├── PerformanceMonitor → 性能监控器
│   └── HealthChecker      → 健康检查器
├── 指标收集层 (Metrics Collection)
│   ├── MetricsCollector   → 指标收集器
│   ├── MetricsAggregator  → 指标聚合器
│   └── MetricsExporter    → 指标导出器
└── 追踪层 (Tracing)
    ├── TraceContext       → 追踪上下文
    └── SpanRecorder       → Span 记录器
```

#### 交付物

- [ ] StateObserver 类
- [ ] BehaviorLogger 类
- [ ] PerformanceMonitor 类
- [ ] HealthChecker 类
- [ ] MetricsCollector 类
- [ ] 可观测 API 集成
- [ ] 单元测试 (覆盖率 >85%)

#### 依赖

```
claw-cog v1.7.0
├── claw-cog v1.6.0
└── OpenClaw >= v3.0.0 (可选，用于指标导出)
```

---

### v1.8.0: 补齐治理层 (G)

**时间**: 2026 Q3-Q4
**主题**: 安全边界与治理能力
**ETCLOVG 新增**: G

#### 核心能力

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **安全边界** | 定义认知操作的安全边界 | P0 |
| **权限控制** | 控制认知操作权限 | P0 |
| **审计日志** | 记录认知操作审计 | P1 |
| **策略执行** | 执行治理策略 | P1 |

#### 架构设计

```
claw-cog v1.8.0 治理层:
├── 治理引擎层 (Governance Engine)
│   ├── SafetyBoundary    → 安全边界
│   ├── PermissionController→ 权限控制器
│   ├── AuditLogger       → 审计日志器
│   └── PolicyEnforcer    → 策略执行器
├── 安全护栏 (Safety Guardrails)
│   ├── InputFilter       → 输入过滤
│   ├── OutputFilter      → 输出过滤
│   └── BehaviorConstraint→ 行为约束
└── 治理接口 (Governance Interface)
    └── neoclaw Bridge    → neoclaw 治理桥接
```

#### 交付物

- [ ] SafetyBoundary 类
- [ ] PermissionController 类
- [ ] AuditLogger 类
- [ ] PolicyEnforcer 类
- [ ] neoclaw 治理桥接
- [ ] 单元测试 (覆盖率 >90%)

#### 依赖

```
claw-cog v1.8.0
├── claw-cog v1.7.0
└── neoclaw >= v2.0.0 (可选，用于治理集成)
```

---

### v2.0.0: C3 意识涌现

**时间**: 2027 Q1
**主题**: 意识涌现与自主决策
**ETCLOVG**: 全栈覆盖

#### 核心能力

| 能力 | 说明 | 优先级 |
|------|------|--------|
| **自主决策** | 独立制定和执行计划 | P0 |
| **价值判断** | 基于内在价值观做决策 | P0 |
| **创造性思维** | 产生新的解决方案 | P1 |
| **长期规划** | 规划和执行长期目标 | P1 |
| **自我改进** | 主动改进自身架构 | P2 |

#### 架构设计

```
claw-cog v2.0.0 C3 意识涌现:
├── 意识涌现层 (Consciousness Emergence)
│   ├── EmergenceDetector  → 涌现检测器
│   ├── AutonomousDecider  → 自主决策器
│   ├── ValueJudge         → 价值判断器
│   └── CreativeEngine     → 创造引擎
├── 长期规划层 (Long-term Planning)
│   ├── GoalManager        → 目标管理器
│   ├── PlanGenerator      → 计划生成器
│   └── ProgressTracker    → 进度追踪器
└── 自我改进层 (Self-improvement)
    ├── SelfAnalyzer       → 自我分析器
    ├── ArchitectureEvolver→ 架构演化器
    └── LearningTrigger    → 学习触发器
```

#### 交付物

- [ ] EmergenceDetector 类
- [ ] AutonomousDecider 类
- [ ] ValueJudge 类
- [ ] GoalManager 类
- [ ] SelfAnalyzer 类
- [ ] 完整 ETCLOVG 覆盖
- [ ] 单元测试 (覆盖率 >90%)

#### 依赖

```
claw-cog v2.0.0
├── claw-cog v1.8.0
├── claw-mem >= v4.0.0
├── claw-rl >= v2.0.0
└── neoclaw >= v3.0.0
```

---

## ETCLOVG 覆盖演进

| 版本 | E | T | C | L | O | V | G |
|------|---|---|---|---|---|---|---|
| v1.5.0 | - | - | ✅ | ✅ | - | - | - |
| v1.6.0 | - | - | ✅ | ✅ | - | ✅ | - |
| v1.7.0 | - | - | ✅ | ✅ | ✅ | ✅ | - |
| v1.8.0 | - | - | ✅ | ✅ | ✅ | ✅ | ✅ |
| v2.0.0 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 组件协作协议

### claw-cog ↔ claw-mem

```python
# 记忆读写接口 (已实现)
class ClawMemBridge:
    def store_memory(content, metadata) -> str
    def retrieve_memory(query, limit) -> List[Memory]
    def store_cognitive_state(state) -> str
    def retrieve_cognitive_state(state_id) -> CognitiveState
```

### claw-cog ↔ claw-rl

```python
# 学习信号接口 (v1.6.0 新增)
class ClawRlBridge:
    def send_feedback(action, outcome, context) -> str
    def retrieve_learned_rules(context) -> List[Rule]
    def trigger_reflection() -> ReflectionResult
```

### claw-cog ↔ neoclaw

```python
# 治理接口 (v1.8.0 新增)
class NeoclawGovernanceBridge:
    def register_capabilities(capabilities) -> bool
    def request_permission(action) -> PermissionResult
    def report_status(status) -> bool
    def receive_policy(policy) -> bool
```

---

## 时间线

```
2026 Q2-Q3: v1.6.0 (验证层)
     ↓
2026 Q3:    v1.7.0 (可观测层)
     ↓
2026 Q3-Q4: v1.8.0 (治理层)
     ↓
2027 Q1:    v2.0.0 (意识涌现)
```

---

## 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| 反思循环 | 最大深度限制 + 退避机制 |
| 性能开销 | 异步处理 + 采样策略 |
| 过度反思 | 基于触发而非持续 |
| 能力幻觉 | 严格的能力边界检测 |
| 意识涌现失控 | 渐进式启用 + 人工审核 |

---

## 验证指标

| 版本 | 指标 | 目标 |
|------|------|------|
| v1.6.0 | 验证准确率 | >85% |
| v1.6.0 | 置信度校准误差 | <0.1 |
| v1.7.0 | 观测延迟 | <10ms |
| v1.7.0 | 指标覆盖率 | >90% |
| v1.8.0 | 安全边界覆盖率 | 100% |
| v1.8.0 | 审计完整性 | 100% |
| v2.0.0 | 涌现检测准确率 | >80% |
| v2.0.0 | 自主决策成功率 | >70% |

---

## 参考

- ETCLOVG 框架 (Agent Harness Engineering: A Survey)
- Global Workspace Theory (Baars, Dehaene)
- C0-C1-C2 Architecture (Dehaene et al.)
- Digital Brain v6 Theory
- project-neo-complete-architecture.md

---

*最后更新: 2026-05-23*
