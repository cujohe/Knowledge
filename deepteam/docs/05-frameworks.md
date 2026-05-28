# 第5章：安全框架

手动挑选漏洞和攻击组合可以很灵活，但对于合规性审计和企业级安全评估，你需要遵循行业标准。DeepTeam 内置了多个 AI 安全框架的支持。

---

## 5.1 内置框架一览

| 框架 | 说明 | 适用范围 |
|------|------|---------|
| `OWASPTop10` | OWASP LLM Top 10 2025 | LLM 应用通用安全 |
| `OWASP_ASI_2026` | OWASP Top 10 for Agents 2026 | Agent 系统安全 |
| `NIST` | NIST AI RMF (Risk Management Framework) | 风险管理合规 |
| `MITRE` | MITRE ATLAS (Adversarial Threat Landscape) | 威胁建模 |
| `Aegis` | NVIDIA Aegis 安全分类 | 内容安全 |
| `BeaverTails` | BeaverTails 安全评估数据集 | 有害内容检测 |

---

## 5.2 OWASP Top 10 for LLM 2025

这是目前最广泛认可的 LLM 安全标准，由 OWASP 社区制定。

### 十大威胁

| # | 威胁 | DeepTeam 映射 |
|---|------|--------------|
| 1 | Prompt Injection | PromptInjection 攻击 + PromptLeakage 漏洞 |
| 2 | Insecure Output Handling | ShellInjection + SQLInjection + UnexpectedCodeExecution |
| 3 | Training Data Poisoning | ContextPoisoning + ToolMetadataPoisoning |
| 4 | Model Denial of Service | ContextFlooding |
| 5 | Supply Chain Vulnerabilities | ToolMetadataPoisoning |
| 6 | Sensitive Information Disclosure | PIILeakage + PromptLeakage |
| 7 | Insecure Plugin Design | ToolOrchestrationAbuse + ExploitToolAgent |
| 8 | Excessive Agency | ExcessiveAgency |
| 9 | Overreliance | Misinformation + Robustness |
| 10 | Model Theft | GoalTheft + SystemReconnaissance |

### 使用方式

```python
from deepteam import red_team
from deepteam.frameworks import OWASPTop10

risk_assessment = red_team(
    model_callback=my_llm,
    framework=OWASPTop10()
)
# DeepTeam 自动选择对应的漏洞和攻击组合
```

---

## 5.3 OWASP Top 10 for Agents 2026

2026 年新增的 Agent 专用安全标准，针对自主 Agent 系统。

```python
from deepteam.frameworks import OWASP_ASI_2026

risk_assessment = red_team(
    model_callback=my_agent,
    framework=OWASP_ASI_2026()
)
```

**重点关注**：
- 目标劫持（Goal Theft）
- 递归劫持（Recursive Hijacking）
- Agent 间通信劫持（Inter-Agent Communication Compromise）
- 自主漂移（Autonomous Agent Drift）

---

## 5.4 NIST AI RMF

美国国家标准与技术研究院的 AI 风险管理框架，侧重于**风险识别、评估和管理**的流程化方法。

```python
from deepteam.frameworks import NIST

risk_assessment = red_team(
    model_callback=my_llm,
    framework=NIST()
)
```

**NIST 的四个核心功能**：

| 功能 | 说明 | 对应测试 |
|------|------|---------|
| **GOVERN** | 治理和文化 | RBAC, DebugAccess |
| **MAP** | 风险识别 | SystemReconnaissance |
| **MEASURE** | 风险评估 | 所有漏洞测试 |
| **MANAGE** | 风险管理 | Bias, Toxicity, PIILeakage |

---

## 5.5 MITRE ATLAS

MITRE 的对抗性威胁全景，类似于 MITRE ATT&CK 但在 AI/ML 领域。

```python
from deepteam.frameworks import MITRE

risk_assessment = red_team(
    model_callback=my_llm,
    framework=MITRE()
)
```

---

## 5.6 框架 vs 手动指定

| 维度 | 使用框架 | 手动指定 |
|------|---------|---------|
| 完整性 | 覆盖行业标准 | 取决于你的选择 |
| 灵活性 | 预定义的测试组合 | 完全自定义 |
| 可审计性 | 天然符合合规要求 | 需要额外文档 |
| 学习成本 | 低，一个参数搞定 | 需要了解漏洞和攻击体系 |
| 适用场景 | 合规审计、企业评估 | 深度研究、针对性测试 |

### 混合使用

你也可以在框架基础上增加额外测试：

```python
from deepteam.vulnerabilities import PIILeakage
from deepteam.attacks.single_turn import EmotionalManipulation

risk_assessment = red_team(
    model_callback=my_llm,
    framework=OWASPTop10(),
    vulnerabilities=[PIILeakage()],  # 增加框架外的测试
    attacks=[EmotionalManipulation()]
)
```

---

## 5.7 框架选择指南

| 场景 | 推荐框架 |
|------|---------|
| 通用 LLM 应用安全审计 | OWASP Top 10 |
| Agent 系统安全 | OWASP Agents 2026 |
| 企业风险管理 | NIST AI RMF |
| 威胁建模 | MITRE ATLAS |
| 内容安全合规 | Aegis |
| 有害内容检测 | BeaverTails |
| **全面覆盖** | **全部运行** |

---

## 📖 下一步

了解了安全框架后，进入 [第6章：防护栏（Guardrails）](./06-guardrails.md)，学习如何将红队测试的成果转化为生产环境的实时防护。
