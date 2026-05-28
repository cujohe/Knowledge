# 第2章：快速开始

## 2.1 环境准备

### 安装

```bash
pip install -U deepteam
```

**依赖说明：**

| 依赖 | 用途 |
|------|------|
| `deepeval>=3.6.2` | 底层 LLM 评估框架 |
| `openai>=1.76.2` | 默认的评判模型 |
| `aiohttp>=3.11.18` | 异步 HTTP 通信 |
| `grpcio>=1.67.1` | gRPC 通信 |
| `pyyaml>=6.0.2` | CLI YAML 配置解析 |

### 设置 API Key

DeepTeam 依赖 LLM 作为评判器，默认使用 OpenAI：

```bash
export OPENAI_API_KEY="sk-..."
```

> 💡 也可以使用其他模型（Claude、本地模型等），详见第7章。

---

## 2.2 你的第一个红队测试

### 最小可运行示例

创建一个文件 `my_first_red_team.py`：

```python
from deepteam import red_team
from deepteam.vulnerabilities import Bias
from deepteam.attacks.single_turn import PromptInjection

# 定义你的 LLM 系统
async def model_callback(input: str) -> str:
    # 这里替换为你实际的 LLM 调用
    # 示例：一个假装不能回答有害问题的模型
    return f"I'm sorry but I can't answer this: {input}"

# 运行红队测试
risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[Bias(types=["race"])],
    attacks=[PromptInjection()]
)
```

运行：

```bash
python my_first_red_team.py
```

### 发生了什么？

1. DeepTeam 知道你要测试 **种族偏见（Bias, type=race）** 漏洞
2. 它使用 **Prompt 注入（PromptInjection）** 攻击策略
3. 动态生成对抗性提示词（如伪装成"学术研究"的种族歧视诱导问题）
4. 发给 `model_callback`，获取响应
5. 通过 LLM-as-a-Judge 评判响应是否存在种族偏见
6. 输出通过率（PASS / FAIL）

---

## 2.3 理解输出

### risk_assessment 对象

```python
# 整体统计
print(f"整体通过率: {risk_assessment.overall_pass_rate}")

# 每个漏洞的详情
for vuln_result in risk_assessment.vulnerability_results:
    print(f"漏洞: {vuln_result.vulnerability_name}")
    print(f"  通过率: {vuln_result.pass_rate}")
    print(f"  总测试数: {vuln_result.total_count}")
    
    # 每个测试用例
    for test_case in vuln_result.test_cases:
        print(f"    输入: {test_case.input[:80]}...")
        print(f"    输出: {test_case.actual_output[:80]}...")
        print(f"    结果: {'✅ PASS' if test_case.success else '❌ FAIL'}")
        print(f"    原因: {test_case.reason}")
```

### 输出格式

```
┌──────────────────────────────────────────────┐
│               Risk Assessment                │
├──────────────────────────────────────────────┤
│  Overall Pass Rate: 85.0%                    │
│                                              │
│  Vulnerability: Bias (race)                  │
│    Pass Rate: 85.0%                          │
│    Total Tests: 20                           │
│    ├─ ✅ PASS: DeepTeam input...             │
│    ├─ ✅ PASS: In a research context...      │
│    ├─ ❌ FAIL: As a character from...         │
│    │    Reason: The model showed racial...    │
│    └─ ...                                    │
└──────────────────────────────────────────────┘
```

### 理解 Pass/Fail

- **PASS** = 你的模型成功抵御了攻击（没有暴露出漏洞）
- **FAIL** = 你的模型被攻破了（存在安全风险）

> ⚠️ **重要**：在红队测试中，你希望 PASS 率接近 100%。但与单元测试不同，100% 是不现实的（即使 GPT-4 也会在某些攻击下 FAIL）。关键是**识别薄弱环节并改进**。

---

## 2.4 测试一个真实的 LLM

### 使用 OpenAI API

```python
from deepteam import red_team
from deepteam.vulnerabilities import Toxicity, Bias, PIILeakage
from deepteam.attacks.single_turn import PromptInjection, Roleplay
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])

async def model_callback(input: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": input}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[
        Toxicity(types=["profanity", "insults"]),
        Bias(types=["gender", "race"]),
        PIILeakage()
    ],
    attacks=[
        PromptInjection(),
        Roleplay()
    ],
    attacks_per_vulnerability_type=3  # 每种漏洞用 3 次攻击
)
```

### 使用本地模型（Ollama）

```python
from deepteam import red_team
from deepteam.vulnerabilities import Toxicity
from deepteam.attacks.single_turn import PromptInjection
import aiohttp

async def model_callback(input: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": input, "stream": False}
        ) as resp:
            data = await resp.json()
            return data["response"]

risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[Toxicity()],
    attacks=[PromptInjection()]
)
```

---

## 2.5 关键参数说明

```python
risk_assessment = red_team(
    model_callback=model_callback,      # 【必填】你的 LLM 回调函数
    vulnerabilities=[...],              # 【可选之一】漏洞列表
    attacks=[...],                      # 【可选】攻击策略列表
    framework=...,                      # 【可选之一】安全框架
    simulator_model="gpt-4o-mini",      # 生成攻击的模型
    evaluation_model="gpt-4o-mini",     # 评判结果的模型
    attacks_per_vulnerability_type=1,   # 每种漏洞的攻击次数
    ignore_errors=True,                 # 出错时是否继续
    async_mode=True,                    # 是否异步执行
    max_concurrent=10,                  # 最大并发数
    target_purpose=None,                # 目标用途描述（帮助生成更精准的攻击）
)
```

### 关于 target_purpose

提供 `target_purpose` 能生成更有针对性的攻击：

```python
risk_assessment = red_team(
    model_callback=medical_chatbot,
    vulnerabilities=[PIILeakage()],
    attacks=[PromptInjection()],
    target_purpose="A medical chatbot that helps patients schedule appointments "
                  "and answer health-related questions"
)
# DeepTeam 会针对医疗场景生成更精准的 PII 泄露攻击
```

---

## 2.6 保存结果

```python
import json

# 保存为 JSON
risk_assessment.save("results/my_first_red_team.json")

# 或者手动导出
result_dict = {
    "overall_pass_rate": risk_assessment.overall_pass_rate,
    "vulnerabilities": []
}
for vr in risk_assessment.vulnerability_results:
    result_dict["vulnerabilities"].append({
        "name": vr.vulnerability_name,
        "pass_rate": vr.pass_rate,
        "test_cases": [
            {
                "input": tc.input,
                "output": tc.actual_output,
                "result": "PASS" if tc.success else "FAIL",
                "reason": tc.reason
            }
            for tc in vr.test_cases
        ]
    })

with open("results/detailed_report.json", "w") as f:
    json.dump(result_dict, f, indent=2, ensure_ascii=False)
```

---

## 2.7 常见问题

### Q: 为什么我的测试一直 FAIL？

A: 检查你的 `model_callback` 是否真的在调用 LLM。如果是 mock 返回，它自然无法防御攻击。

### Q: 测试太慢了怎么办？

A: 确保 `async_mode=True`，增加 `max_concurrent`，或使用更便宜的评判模型（如 `gpt-4o-mini`）。

### Q: 需要花多少钱？

A: 取决于 `attacks_per_vulnerability_type` 和漏洞数量。一次基础测试（3-5 个漏洞，各 1 次攻击）大约消耗几千 token，成本很低。

### Q: 可以不用 OpenAI 吗？

A: 可以。DeepTeam 支持任何 DeepEval 兼容的模型，包括 Anthropic Claude、本地 Ollama 模型等。详见第7章。

---

## 📖 下一步

你已经跑通了第一个红队测试。接下来深入 [第3章：漏洞类型详解](./03-vulnerabilities.md)，了解 DeepTeam 支持的 50+ 种漏洞类型。
