# claw-cog 设计文档索引

> 最后更新: 2026-05-12  
> 项目: claw-cog (AI Consciousness Component)

---

## 📚 文档结构

```
claw-cog/docs/
├── VERSION_ROADMAP.md              # 版本规划
├── architecture/
│   ├── DESIGN_PROPOSAL.md          # 架构设计提案 (基于论文)
│   ├── V1_ARCHITECTURE.md          # v1.0.0 详细架构设计
│   └── papers/
│       ├── README.md               # 论文清单
│       ├── READING_SUMMARY.md      # 阅读总结
│       └── notes/                  # 9篇论文笔记
└── (待创建)
    ├── V2_ARCHITECTURE.md          # v2.0.0 架构设计
    └── V3_ARCHITECTURE.md          # v3.0.0 架构设计
```

---

## 📖 文档说明

### 1. VERSION_ROADMAP.md

**内容**: 版本规划路线图

- v1.0.0, v2.0.0, v3.0.0 规划
- 每个版本的核心能力
- 里程碑与验证指标
- 时间规划

### 2. DESIGN_PROPOSAL.md

**内容**: 架构设计提案

- 基于 9 篇论文的综合洞察
- 核心架构框架
- 模块规格
- 实现优先级

### 3. V1_ARCHITECTURE.md

**内容**: v1.0.0 详细架构设计

- 完整代码结构
- 核心模块设计 (带代码示例)
- 模块集成方案
- 配置设计
- 测试策略
- API 文档结构
- 依赖管理
- 实现优先级

### 4. papers/

**内容**: 论文阅读资料

- README.md: 论文清单
- READING_SUMMARY.md: 阅读总结
- notes/: 9 篇论文详细笔记

---

## 🎯 快速导航

### 想了解版本规划?

→ 阅读 `VERSION_ROADMAP.md`

### 想了解理论基础?

→ 阅读 `architecture/papers/READING_SUMMARY.md`

### 想开始实现 v1.0.0?

→ 阅读 `architecture/V1_ARCHITECTURE.md`

### 想查看特定论文?

→ 查看 `architecture/papers/notes/` 目录

---

## 📊 设计决策记录

### 决策 1: 选择 GNWT 作为核心架构

**依据**: 
- CogniPair 论文首次实现 GNWT 并达到 80% 行为准确率
- GWT 是五大意识理论中最具可操作性的

**影响**: 
- GlobalWorkspace 作为核心组件
- 信息广播机制作为集成方式

### 决策 2: 采用 C0-C1-C2 分层框架

**依据**:
- Exploring Consciousness in LLMs 论文提出清晰的三层分离
- 与 Id/Ego/Superego 模型自然对应

**影响**:
- LayerManager 管理三层
- 每层有明确的职责和接口

### 决策 3: 使用 meta-d' 作为元认知评估标准

**依据**:
- Measuring the Metacognition of AI 论文论证其为金标准
- 可量化、可比较、有理论基础

**影响**:
- MetacognitiveAssessment 模块
- M-ratio 作为效率指标

### 决策 4: 集成 claw-mem 作为 Memory Module

**依据**:
- 已有成熟实现
- 避免重复开发
- 符合 Project Neo 生态

**影响**:
- ClawMemBridge 桥接层
- Memory Module 不独立实现

### 决策 5: 指示属性驱动设计

**依据**:
- Insights from Science of Consciousness 论文提出指示属性框架
- 可验证的理论覆盖

**影响**:
- 每个模块对应理论指示属性
- 测试覆盖指示属性

---

## 🚀 下一步

### 立即行动

1. **创建项目结构**
   ```bash
   cd /Users/liantian/workspace/osprojects/claw-cog
   mkdir -p claw_cog/{core,layers,modules,assessment,integration,config,utils}
   mkdir -p tests/{test_layers,test_modules,test_assessment,test_integration}
   ```

2. **实现核心模块**
   - ConsciousAgent
   - GlobalWorkspace
   - LayerManager

3. **设置测试框架**
   - pytest 配置
   - 指示属性测试

### 后续文档

- [ ] V2_ARCHITECTURE.md (v2.0.0 架构设计)
- [ ] V3_ARCHITECTURE.md (v3.0.0 架构设计)
- [ ] API_REFERENCE.md (API 参考文档)
- [ ] INTEGRATION_GUIDE.md (集成指南)

---

## 📝 文档维护

### 更新规则

1. **新增模块**: 更新 V*_ARCHITECTURE.md
2. **设计变更**: 记录在决策记录中
3. **版本发布**: 更新 VERSION_ROADMAP.md

### 审阅周期

- 每个里程碑前审阅架构文档
- 每个版本发布前审阅所有文档

---

*此索引文档帮助快速导航 claw-cog 的设计文档体系。*
