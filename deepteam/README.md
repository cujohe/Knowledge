# DeepTeam: LLM 红队测试框架 — 完整学习教程

<p align="center">
  <b>从零开始掌握 LLM 安全测试</b>
</p>

---

## 关于 DeepTeam

**DeepTeam** 是由 [Confident AI](https://github.com/confident-ai) 开发的开源 **LLM 红队测试（Red Teaming）框架**，可以理解为"LLM 的渗透测试工具"。

| 属性 | 值 |
|------|-----|
| 语言 | Python 3.9+ |
| 许可证 | Apache 2.0 |
| 最新版本 | 1.0.6 |
| PyPI | `pip install deepteam` |
| 官方文档 | [trydeepteam.com](https://www.trydeepteam.com) |
| GitHub | [confident-ai/deepteam](https://github.com/confident-ai/deepteam) |

### 它能做什么？

- 🔍 **检测 50+ 种 LLM 漏洞** — 偏见、PII 泄露、SQL 注入、越狱等
- 💥 **20+ 种对抗攻击技术** — Prompt 注入、角色扮演、编码混淆、多轮越狱
- 🏛️ **内置安全框架** — OWASP Top 10、NIST AI RMF、MITRE ATLAS
- 🛡️ **端侧防护栏** — 在生产环境拦截恶意输入和输出

### 核心设计理念

与传统评估不同，DeepTeam **不需要你准备测试数据集**。它利用 LLM-as-a-Judge 的方式，动态生成对抗性攻击，去探测你的 LLM 系统的薄弱环节。你只需要提供一个 `model_callback` 函数——把用户输入转发给你的 LLM 并返回输出即可。

> 💡 **为什么叫"红队测试"？** 在网络安全领域，红队（Red Team）模拟攻击者，蓝队（Blue Team）负责防守。DeepTeam 扮演红队角色，帮你找出 LLM 系统的安全漏洞。

---

## 📖 教程目录

| 章节 | 内容 |
|------|------|
| [📘 第1章: LLM 红队测试概述](./docs/01-overview.md) | 什么是红队测试、为什么需要、核心概念 |
| [🚀 第2章: 快速开始](./docs/02-quickstart.md) | 安装、第一个红队测试、理解输出 |
| [🔍 第3章: 漏洞类型详解](./docs/03-vulnerabilities.md) | 50+ 漏洞分类与实战用法 |
| [💥 第4章: 攻击技术](./docs/04-attacks.md) | 单轮/多轮对抗攻击的底层原理 |
| [🏛️ 第5章: 安全框架](./docs/05-frameworks.md) | OWASP、NIST 等框架集成 |
| [🛡️ 第6章: 防护栏（Guardrails）](./docs/06-guardrails.md) | 生产环境实时拦截 |
| [🧠 第7章: 高级主题](./docs/07-advanced.md) | 自定义漏洞、CLI、CI/CD 集成 |

### 💻 代码示例

| 文件 | 说明 |
|------|------|
| [01_basic_red_team.py](./code/01_basic_red_team.py) | 基础红队测试 |
| [02_framework_based.py](./code/02_framework_based.py) | 基于 OWASP 的安全框架测试 |
| [03_multi_turn_attack.py](./code/03_multi_turn_attack.py) | 多轮对话越狱攻击 |
| [04_custom_vulnerability.py](./code/04_custom_vulnerability.py) | 自定义漏洞类型 |
| [05_guardrails_example.py](./code/05_guardrails_example.py) | 防护栏部署实战 |
| [06_full_pipeline.py](./code/06_full_pipeline.py) | 完整 CI/CD 集成流水线 |

---

## 🎯 学习路线建议

```
初学者：第1章 → 第2章 → 代码示例 01 → 第3章（概览）→ 代码示例 02
进阶者：第4章 → 代码示例 03, 04 → 第5章 → 第7章
实践者：第6章 → 代码示例 05, 06
```

---

## 🔗 相关资源

- [DeepTeam 官方文档](https://www.trydeepteam.com)
- [DeepEval（底层评估框架）](https://github.com/confident-ai/deepeval)
- [Confident AI 平台](https://app.confident-ai.com)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

---

*Happy Red Teaming! 🔴*
