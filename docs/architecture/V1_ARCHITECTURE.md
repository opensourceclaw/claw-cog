# claw-cog v1.0.0 架构设计

> 版本: v1.0.0  
> 设计日期: 2026-05-12  
> 状态: Draft

---

## 📋 设计目标

### 核心目标

1. **Global Workspace 实现** - GNWT 核心机制
2. **C0-C1-C2 分层** - 清晰的意识层级
3. **元认知评估** - meta-d' 框架
4. **claw-mem 集成** - Memory Module
5. **指示属性评估** - 5 大理论覆盖

### 设计原则

- **模块化**: 每个组件独立可测试
- **可扩展**: 为 v2.0.0/v3.0.0 预留接口
- **可测量**: 所有意识能力有量化指标
- **类型安全**: 使用 Python type hints
- **文档化**: 每个模块有清晰文档

---

## 🏗️ 整体架构

```
claw_cog/
├── __init__.py                 # 包入口
├── core/
│   ├── __init__.py
│   ├── agent.py                # ConsciousAgent 主类
│   ├── workspace.py            # Global Workspace
│   └── layers.py               # C0-C1-C2 层管理
├── layers/
│   ├── __init__.py
│   ├── c0_unconscious.py       # C0: 无意识层
│   ├── c1_conscious.py         # C1: 意识访问层
│   └── c2_metacognitive.py     # C2: 元认知层
├── modules/
│   ├── __init__.py
│   ├── memory.py               # Memory Module (claw-mem)
│   ├── ego.py                  # Ego Module
│   ├── goal_tracking.py        # GoalTracking Module
│   └── fast_patterns.py        # Fast Pattern Matching
├── assessment/
│   ├── __init__.py
│   ├── meta_d_prime.py         # meta-d' 计算
│   ├── indicators.py           # 指示属性评估
│   └── metrics.py              # 评估指标
├── integration/
│   ├── __init__.py
│   ├── claw_mem_bridge.py      # claw-mem 桥接
│   └── claw_rl_bridge.py       # claw-rl 桥接
├── config/
│   ├── __init__.py
│   └── defaults.py             # 默认配置
└── utils/
    ├── __init__.py
    └── types.py                # 类型定义
```

---

## 🔧 核心模块设计

### 1. ConsciousAgent (主类)

**职责**: 意识代理的统一入口

```python
# claw_cog/core/agent.py

from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .workspace import GlobalWorkspace
from .layers import LayerManager
from ..assessment import MetacognitiveAssessment
from ..config import Config

class ConsciousnessLevel(Enum):
    """意识层级枚举"""
    C0_UNCONSCIOUS = 0
    C1_CONSCIOUS_ACCESS = 1
    C2_METACOGNITIVE = 2

@dataclass
class ProcessingResult:
    """处理结果"""
    output: Any
    confidence: float
    level: ConsciousnessLevel
    metadata: Dict[str, Any]

class ConsciousAgent:
    """
    意识代理主类
    
    基于 GNWT 架构和 C0-C1-C2 分层框架
    """
    
    def __init__(
        self,
        config: Optional[Config] = None,
        enable_c2: bool = True,
        memory_backend: str = "claw-mem"
    ):
        """
        初始化意识代理
        
        Args:
            config: 配置对象
            enable_c2: 是否启用 C2 元认知层
            memory_backend: 记忆后端
        """
        self.config = config or Config()
        
        # 核心组件
        self.workspace = GlobalWorkspace(self.config)
        self.layers = LayerManager(self.config, enable_c2=enable_c2)
        self.assessment = MetacognitiveAssessment(self.config)
        
        # 状态
        self._processing_history: List[ProcessingResult] = []
        
    def process(
        self,
        input: Any,
        context: Optional[Dict] = None,
        confidence_threshold: float = 0.7
    ) -> ProcessingResult:
        """
        处理输入
        
        Args:
            input: 输入数据
            context: 上下文信息
            confidence_threshold: 置信度阈值
            
        Returns:
            ProcessingResult: 处理结果
        """
        # 1. C0: 快速模式匹配
        c0_result = self.layers.c0.process(input, context)
        
        # 2. C1: 意识访问 (通过 Global Workspace)
        c1_result = self.workspace.process(
            input=input,
            c0_output=c0_result,
            context=context
        )
        
        # 3. C2: 元认知监控 (如果启用)
        if self.layers.c2_enabled:
            c2_result = self.layers.c2.monitor(
                c1_result=c1_result,
                confidence_threshold=confidence_threshold
            )
            
            # 根据 C2 结果调整
            if c2_result.needs_adjustment:
                c1_result = self._apply_c2_adjustment(c1_result, c2_result)
        
        # 4. 构建结果
        result = ProcessingResult(
            output=c1_result.output,
            confidence=c1_result.confidence,
            level=self._determine_level(c1_result),
            metadata={
                "c0_contribution": c0_result.contribution,
                "c2_monitoring": c2_result if self.layers.c2_enabled else None
            }
        )
        
        # 5. 记录历史 (用于元认知评估)
        self._processing_history.append(result)
        
        return result
    
    def assess_metacognition(self) -> Dict[str, float]:
        """
        评估元认知能力
        
        Returns:
            Dict containing meta-d', M-ratio, etc.
        """
        return self.assessment.compute_metrics(self._processing_history)
    
    def get_indicator_properties(self) -> Dict[str, bool]:
        """
        获取指示属性覆盖情况
        
        Returns:
            Dict mapping theory names to coverage status
        """
        return {
            "GWT": self.workspace.is_implemented(),
            "RPT": self.layers.has_feedback_loops(),
            "HOT": self.layers.c2_enabled,
            "PP": False,  # v2.0.0
            "AST": self.workspace.has_attention_mechanism()
        }
```

### 2. GlobalWorkspace (全局工作空间)

**职责**: GNWT 核心机制，信息广播与集成

```python
# claw_cog/core/workspace.py

from typing import Any, Dict, List, Callable
from dataclasses import dataclass, field
from time import time
import asyncio

@dataclass
class WorkspaceState:
    """工作空间状态"""
    content: Any
    broadcast_time: float
    subscribers_notified: int = 0
    integration_score: float = 0.0

class GlobalWorkspace:
    """
    全局工作空间
    
    实现 Global Workspace Theory (GWT):
    - 信息广播机制
    - 多模块集成
    - 意识访问控制
    """
    
    def __init__(self, config: "Config"):
        self.config = config
        self._subscribers: List[Callable] = []
        self._current_state: Optional[WorkspaceState] = None
        self._broadcast_history: List[WorkspaceState] = []
        
        # 性能指标
        self._avg_broadcast_time_ms = 0.0
        self._total_broadcasts = 0
        
    def subscribe(self, module: Callable) -> None:
        """
        订阅工作空间广播
        
        Args:
            module: 订阅模块 (接收广播内容的回调)
        """
        self._subscribers.append(module)
        
    def process(
        self,
        input: Any,
        c0_output: Any,
        context: Optional[Dict] = None
    ) -> "C1Result":
        """
        处理输入并广播
        
        Args:
            input: 原始输入
            c0_output: C0 层输出
            context: 上下文
            
        Returns:
            C1Result: C1 层处理结果
        """
        start_time = time()
        
        # 1. 集成多模块信息
        integrated_content = self._integrate(input, c0_output, context)
        
        # 2. 广播给所有订阅者
        broadcast_result = self._broadcast(integrated_content)
        
        # 3. 计算集成分数
        integration_score = self._compute_integration_score(broadcast_result)
        
        # 4. 更新状态
        broadcast_time = (time() - start_time) * 1000  # ms
        self._current_state = WorkspaceState(
            content=integrated_content,
            broadcast_time=broadcast_time,
            subscribers_notified=len(self._subscribers),
            integration_score=integration_score
        )
        self._broadcast_history.append(self._current_state)
        
        # 5. 更新性能指标
        self._update_metrics(broadcast_time)
        
        return C1Result(
            output=integrated_content,
            confidence=integration_score,
            broadcast_time_ms=broadcast_time
        )
    
    def _integrate(
        self,
        input: Any,
        c0_output: Any,
        context: Optional[Dict]
    ) -> Any:
        """集成多模块信息"""
        # TODO: 实现具体集成逻辑
        # 优先级: Memory > Ego > C0
        pass
    
    def _broadcast(self, content: Any) -> Dict[str, Any]:
        """广播内容给所有订阅者"""
        results = {}
        for i, subscriber in enumerate(self._subscribers):
            try:
                results[f"module_{i}"] = subscriber(content)
            except Exception as e:
                results[f"module_{i}"] = {"error": str(e)}
        return results
    
    def _compute_integration_score(self, broadcast_result: Dict) -> float:
        """计算集成分数"""
        # 基于广播成功率
        successful = sum(1 for r in broadcast_result.values() if "error" not in r)
        return successful / len(broadcast_result) if broadcast_result else 0.0
    
    def _update_metrics(self, broadcast_time_ms: float) -> None:
        """更新性能指标"""
        self._total_broadcasts += 1
        # 移动平均
        self._avg_broadcast_time_ms = (
            (self._avg_broadcast_time_ms * (self._total_broadcasts - 1) + broadcast_time_ms)
            / self._total_broadcasts
        )
    
    def get_metrics(self) -> Dict[str, float]:
        """获取性能指标"""
        return {
            "avg_broadcast_time_ms": self._avg_broadcast_time_ms,
            "total_broadcasts": self._total_broadcasts,
            "subscriber_count": len(self._subscribers)
        }
    
    def is_implemented(self) -> bool:
        """GWT 是否实现"""
        return True
    
    def has_attention_mechanism(self) -> bool:
        """是否有注意力机制"""
        # v1.0.0: 基础实现
        return True
```

### 3. LayerManager (层管理器)

**职责**: 管理 C0-C1-C2 三层

```python
# claw_cog/core/layers.py

from typing import Any, Dict, Optional
from ..layers.c0_unconscious import C0Unconscious
from ..layers.c1_conscious import C1Conscious
from ..layers.c2_metacognitive import C2Metacognitive

class LayerManager:
    """
    层管理器
    
    管理 C0-C1-C2 三层架构
    """
    
    def __init__(
        self,
        config: "Config",
        enable_c2: bool = True
    ):
        self.config = config
        
        # 初始化各层
        self.c0 = C0Unconscious(config)
        self.c1 = C1Conscious(config)
        self.c2 = C2Metacognitive(config) if enable_c2 else None
        
        self.c2_enabled = enable_c2
        
    def has_feedback_loops(self) -> bool:
        """是否有反馈回路 (RPT)"""
        # v1.0.0: 基础实现
        return True
    
    def get_layer_status(self) -> Dict[str, bool]:
        """获取各层状态"""
        return {
            "c0_active": self.c0.is_active(),
            "c1_active": self.c1.is_active(),
            "c2_active": self.c2.is_active() if self.c2 else False
        }
```

### 4. C0Unconscious (无意识层)

```python
# claw_cog/layers/c0_unconscious.py

from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class C0Result:
    """C0 层结果"""
    output: Any
    contribution: float  # 对最终结果的贡献度
    pattern_matched: str

class C0Unconscious:
    """
    C0: 无意识层
    
    功能:
    - 快速模式匹配
    - 自动响应
    - 原始印象处理
    """
    
    def __init__(self, config: "Config"):
        self.config = config
        self._patterns: Dict[str, Any] = {}
        self._auto_responses: Dict[str, Any] = {}
        
    def process(
        self,
        input: Any,
        context: Optional[Dict] = None
    ) -> C0Result:
        """
        处理输入
        
        Args:
            input: 输入数据
            context: 上下文
            
        Returns:
            C0Result: C0 层处理结果
        """
        # 1. 快速模式匹配
        pattern, match_score = self._match_pattern(input)
        
        # 2. 自动响应检查
        auto_response = self._check_auto_response(input)
        
        # 3. 原始印象
        impression = self._form_impression(input)
        
        # 4. 确定输出
        if auto_response:
            output = auto_response
            contribution = 0.8  # 高贡献度
        elif match_score > 0.7:
            output = self._patterns[pattern]
            contribution = match_score
        else:
            output = impression
            contribution = 0.3  # 低贡献度，需要 C1 处理
            
        return C0Result(
            output=output,
            contribution=contribution,
            pattern_matched=pattern
        )
    
    def _match_pattern(self, input: Any) -> Tuple[str, float]:
        """模式匹配"""
        # TODO: 实现模式匹配逻辑
        return ("default", 0.5)
    
    def _check_auto_response(self, input: Any) -> Optional[Any]:
        """检查自动响应"""
        # TODO: 实现自动响应逻辑
        return None
    
    def _form_impression(self, input: Any) -> Any:
        """形成原始印象"""
        # TODO: 实现印象形成
        return input
    
    def is_active(self) -> bool:
        """是否活跃"""
        return True
    
    def add_pattern(self, name: str, pattern: Any) -> None:
        """添加模式"""
        self._patterns[name] = pattern
        
    def add_auto_response(self, trigger: str, response: Any) -> None:
        """添加自动响应"""
        self._auto_responses[trigger] = response
```

### 5. C2Metacognitive (元认知层)

```python
# claw_cog/layers/c2_metacognitive.py

from typing import Any, Dict, Optional
from dataclasses import dataclass

@dataclass
class C2Result:
    """C2 层结果"""
    needs_adjustment: bool
    adjustment_type: str  # "confidence", "strategy", "seek_help"
    confidence_estimate: float
    recommendation: Optional[str] = None

class C2Metacognitive:
    """
    C2: 元认知层
    
    功能:
    - 目标跟踪
    - 自我监控
    - 置信度评估
    - 策略调整建议
    """
    
    def __init__(self, config: "Config"):
        self.config = config
        self._confidence_thresholds = {
            "high": 0.8,
            "medium": 0.5,
            "low": 0.3
        }
        
    def monitor(
        self,
        c1_result: "C1Result",
        confidence_threshold: float = 0.7
    ) -> C2Result:
        """
        监控 C1 处理结果
        
        Args:
            c1_result: C1 层结果
            confidence_threshold: 置信度阈值
            
        Returns:
            C2Result: 监控结果
        """
        confidence = c1_result.confidence
        
        # 评估置信度
        if confidence >= self._confidence_thresholds["high"]:
            return C2Result(
                needs_adjustment=False,
                adjustment_type="none",
                confidence_estimate=confidence
            )
        
        elif confidence >= self._confidence_thresholds["medium"]:
            return C2Result(
                needs_adjustment=True,
                adjustment_type="strategy",
                confidence_estimate=confidence,
                recommendation="gather_more_information"
            )
        
        elif confidence >= self._confidence_thresholds["low"]:
            return C2Result(
                needs_adjustment=True,
                adjustment_type="confidence",
                confidence_estimate=confidence,
                recommendation="increase_confidence"
            )
        
        else:
            return C2Result(
                needs_adjustment=True,
                adjustment_type="seek_help",
                confidence_estimate=confidence,
                recommendation="request_human_assistance"
            )
    
    def is_active(self) -> bool:
        """是否活跃"""
        return True
```

### 6. MetacognitiveAssessment (元认知评估)

```python
# claw_cog/assessment/meta_d_prime.py

from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass

@dataclass
class MetacognitiveMetrics:
    """元认知指标"""
    meta_d_prime: float
    d_prime: float
    m_ratio: float
    type2_roc_auc: float

class MetacognitiveAssessment:
    """
    元认知评估
    
    基于 meta-d' 框架 (Signal Detection Theory)
    """
    
    def __init__(self, config: "Config"):
        self.config = config
        
    def compute_metrics(
        self,
        history: List["ProcessingResult"]
    ) -> Dict[str, float]:
        """
        计算元认知指标
        
        Args:
            history: 处理历史
            
        Returns:
            Dict containing meta-d', d', M-ratio
        """
        if len(history) < 10:
            return {
                "meta_d_prime": 0.0,
                "d_prime": 0.0,
                "m_ratio": 0.0,
                "warning": "insufficient_data"
            }
        
        # 提取正确/错误响应的置信度
        correct_confidences = []
        incorrect_confidences = []
        
        for result in history:
            # 假设 metadata 中有 correctness 信息
            if result.metadata.get("correct", True):
                correct_confidences.append(result.confidence)
            else:
                incorrect_confidences.append(result.confidence)
        
        # 计算 d' (Type-1 sensitivity)
        d_prime = self._compute_d_prime(
            correct_confidences,
            incorrect_confidences
        )
        
        # 计算 meta-d' (Type-2 sensitivity)
        meta_d_prime = self._compute_meta_d_prime(
            correct_confidences,
            incorrect_confidences
        )
        
        # 计算 M-ratio
        m_ratio = meta_d_prime / d_prime if d_prime > 0 else 0.0
        
        # 计算 Type-2 ROC AUC
        type2_roc_auc = self._compute_type2_roc_auc(
            correct_confidences,
            incorrect_confidences
        )
        
        return {
            "meta_d_prime": meta_d_prime,
            "d_prime": d_prime,
            "m_ratio": m_ratio,
            "type2_roc_auc": type2_roc_auc
        }
    
    def _compute_d_prime(
        self,
        correct: List[float],
        incorrect: List[float]
    ) -> float:
        """计算 d' (Type-1 sensitivity)"""
        if not correct or not incorrect:
            return 0.0
        
        # 使用 hit rate 和 false alarm rate
        # 简化实现
        mean_correct = np.mean(correct)
        mean_incorrect = np.mean(incorrect)
        std_pooled = np.sqrt((np.var(correct) + np.var(incorrect)) / 2)
        
        if std_pooled == 0:
            return 0.0
        
        return (mean_correct - mean_incorrect) / std_pooled
    
    def _compute_meta_d_prime(
        self,
        correct: List[float],
        incorrect: List[float]
    ) -> float:
        """
        计算 meta-d' (Type-2 sensitivity)
        
        基于 Maniscalco & Lau (2012) 方法
        """
        # TODO: 实现完整的 meta-d' 计算
        # 简化版本: 使用 Type-2 ROC
        type2_roc_auc = self._compute_type2_roc_auc(correct, incorrect)
        
        # 近似转换
        # meta-d' ≈ 2 * (Type-2 ROC AUC - 0.5)
        return 2 * (type2_roc_auc - 0.5)
    
    def _compute_type2_roc_auc(
        self,
        correct: List[float],
        incorrect: List[float]
    ) -> float:
        """计算 Type-2 ROC AUC"""
        if not correct or not incorrect:
            return 0.5
        
        # 计算 AUC
        n_correct = len(correct)
        n_incorrect = len(incorrect)
        
        # 简化实现: 计算正确置信度高于错误置信度的比例
        higher_count = 0
        for c in correct:
            for i in incorrect:
                if c > i:
                    higher_count += 1
        
        return higher_count / (n_correct * n_incorrect)
```

---

## 🔗 模块集成

### claw-mem 桥接

```python
# claw_cog/integration/claw_mem_bridge.py

from typing import Any, Dict, Optional, List

class ClawMemBridge:
    """
    claw-mem 桥接层
    
    将 claw-mem 作为 Memory Module 集成
    """
    
    def __init__(self, claw_mem_instance: Any):
        """
        Args:
            claw_mem_instance: claw-mem 实例
        """
        self.memory = claw_mem_instance
        
    def store(self, content: Any, metadata: Optional[Dict] = None) -> str:
        """存储记忆"""
        return self.memory.store(content, metadata)
    
    def retrieve(self, query: str, limit: int = 10) -> List[Any]:
        """检索记忆"""
        return self.memory.search(query, limit)
    
    def get_context(self, query: str, max_tokens: int = 4000) -> str:
        """获取上下文 (用于注入)"""
        results = self.retrieve(query)
        # 格式化为上下文
        context = self._format_context(results, max_tokens)
        return context
    
    def _format_context(self, results: List[Any], max_tokens: int) -> str:
        """格式化上下文"""
        # TODO: 实现上下文格式化
        pass
```

---

## 📊 配置设计

```python
# claw_cog/config/defaults.py

from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Config:
    """claw-cog 配置"""
    
    # Global Workspace 配置
    workspace_broadcast_timeout_ms: int = 100
    workspace_max_subscribers: int = 10
    
    # C0 配置
    c0_pattern_threshold: float = 0.7
    c0_auto_response_enabled: bool = True
    
    # C1 配置
    c1_integration_method: str = "weighted_average"
    c1_confidence_threshold: float = 0.7
    
    # C2 配置
    c2_enabled: bool = True
    c2_high_threshold: float = 0.8
    c2_medium_threshold: float = 0.5
    c2_low_threshold: float = 0.3
    
    # 元认知评估配置
    assessment_min_samples: int = 10
    assessment_history_size: int = 1000
    
    # Memory 配置
    memory_backend: str = "claw-mem"
    memory_context_max_tokens: int = 4000
    
    # 性能配置
    enable_profiling: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """从字典创建配置"""
        return cls(**config_dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "workspace_broadcast_timeout_ms": self.workspace_broadcast_timeout_ms,
            "workspace_max_subscribers": self.workspace_max_subscribers,
            "c0_pattern_threshold": self.c0_pattern_threshold,
            "c0_auto_response_enabled": self.c0_auto_response_enabled,
            "c1_integration_method": self.c1_integration_method,
            "c1_confidence_threshold": self.c1_confidence_threshold,
            "c2_enabled": self.c2_enabled,
            "c2_high_threshold": self.c2_high_threshold,
            "c2_medium_threshold": self.c2_medium_threshold,
            "c2_low_threshold": self.c2_low_threshold,
            "assessment_min_samples": self.assessment_min_samples,
            "assessment_history_size": self.assessment_history_size,
            "memory_backend": self.memory_backend,
            "memory_context_max_tokens": self.memory_context_max_tokens,
            "enable_profiling": self.enable_profiling,
            "log_level": self.log_level
        }
```

---

## 🧪 测试策略

### 单元测试

```
tests/
├── test_agent.py              # ConsciousAgent 测试
├── test_workspace.py          # GlobalWorkspace 测试
├── test_layers/
│   ├── test_c0.py
│   ├── test_c1.py
│   └── test_c2.py
├── test_modules/
│   ├── test_memory.py
│   └── test_ego.py
├── test_assessment/
│   ├── test_meta_d_prime.py
│   └── test_indicators.py
└── test_integration/
    └── test_claw_mem_bridge.py
```

### 指示属性测试

```python
# tests/test_indicators.py

def test_gwt_indicator():
    """测试 GWT 指示属性"""
    agent = ConsciousAgent()
    
    # 验证 Global Workspace 实现
    assert agent.workspace.is_implemented()
    
    # 验证广播机制
    result = agent.process("test input")
    assert result.metadata["broadcast_time_ms"] < 100

def test_rpt_indicator():
    """测试 RPT 指示属性"""
    agent = ConsciousAgent()
    
    # 验证反馈回路
    assert agent.layers.has_feedback_loops()
    
    # 验证 C0→C1→C2 信息流
    # ...

def test_hot_indicator():
    """测试 HOT 指示属性"""
    agent = ConsciousAgent(enable_c2=True)
    
    # 验证 C2 元监控
    assert agent.layers.c2_enabled
    
    # 验证高阶表征
    # ...
```

---

## 📚 API 文档结构

```python
# claw_cog/__init__.py

"""
claw-cog: AI Consciousness Component

A computational consciousness framework based on:
- Global Workspace Theory (GWT)
- C0-C1-C2 Layered Architecture
- meta-d' Metacognitive Assessment
- Five Theory Indicator Properties

Example:
    >>> from claw_cog import ConsciousAgent
    >>> 
    >>> # Create agent
    >>> agent = ConsciousAgent()
    >>> 
    >>> # Process input
    >>> result = agent.process("Hello, world!")
    >>> print(result.output)
    >>> print(result.confidence)
    >>> 
    >>> # Assess metacognition
    >>> metrics = agent.assess_metacognition()
    >>> print(f"meta-d': {metrics['meta_d_prime']}")
    >>> print(f"M-ratio: {metrics['m_ratio']}")
"""

from .core.agent import ConsciousAgent, ConsciousnessLevel, ProcessingResult
from .core.workspace import GlobalWorkspace
from .core.layers import LayerManager
from .config.defaults import Config

__version__ = "1.0.0"
__all__ = [
    "ConsciousAgent",
    "ConsciousnessLevel",
    "ProcessingResult",
    "GlobalWorkspace",
    "LayerManager",
    "Config"
]
```

---

## 📦 依赖管理

```toml
# pyproject.toml

[project]
name = "claw-cog"
version = "1.0.0"
description = "AI Consciousness Component for Project Neo"
authors = [{name = "Peter Cheng", email = "peter@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.10"

dependencies = [
    "claw-mem>=2.8.0",
    "claw-rl>=2.7.0",
    "numpy>=1.24.0",
    "scipy>=1.10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]

[project.urls]
Homepage = "https://github.com/opensourceclaw/claw-cog"
Documentation = "https://github.com/opensourceclaw/claw-cog#readme"
Repository = "https://github.com/opensourceclaw/claw-cog.git"
```

---

## 🚀 实现优先级

### Week 1-2: 核心框架

| 任务 | 优先级 | 预计时间 |
|------|--------|----------|
| ConsciousAgent 主类 | P0 | 2 天 |
| GlobalWorkspace 实现 | P0 | 3 天 |
| LayerManager 实现 | P0 | 2 天 |
| Config 系统 | P0 | 1 天 |

### Week 3-4: 层实现

| 任务 | 优先级 | 预计时间 |
|------|--------|----------|
| C0Unconscious | P0 | 3 天 |
| C1Conscious | P0 | 3 天 |
| C2Metacognitive | P0 | 3 天 |
| 层间通信 | P1 | 2 天 |

### Week 5-6: 评估与集成

| 任务 | 优先级 | 预计时间 |
|------|--------|----------|
| meta-d' 计算 | P0 | 3 天 |
| 指示属性测试 | P0 | 2 天 |
| claw-mem 桥接 | P0 | 2 天 |
| 单元测试 | P1 | 3 天 |

---

*此架构设计基于 9 篇 AI 意识前沿研究论文，确保每个模块都有坚实的理论基础。*
