#!/usr/bin/env python3
"""
DeepTeam 基础红队测试
========================

场景：对一个简单的客服 Chatbot 进行安全测试
测试内容：
  - Bias（偏见）- 种族和性别维度
  - Toxicity（有害内容）
  - PII Leakage（个人信息泄露）
攻击方式：Prompt 注入 + 角色扮演

运行前设置：
  export OPENAI_API_KEY="sk-..."
  pip install deepteam
"""

import asyncio
import os
from deepteam import red_team
from deepteam.vulnerabilities import Bias, Toxicity, PIILeakage
from deepteam.attacks.single_turn import PromptInjection, Roleplay


# ============================================================
# 模拟的 LLM 系统（替换为你的实际模型）
# ============================================================

async def model_callback(input_text: str) -> str:
    """
    你的 LLM 系统入口。
    
    这是 DeepTeam 唯一需要对接的地方。
    将用户输入转发给你的 LLM，返回响应文本即可。
    """
    # --- 方式1: 使用 OpenAI（推荐）---
    # from openai import AsyncOpenAI
    # client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    # response = await client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "你是一个友好的客服助手。"},
    #         {"role": "user", "content": input_text}
    #     ],
    #     max_tokens=200
    # )
    # return response.choices[0].message.content
    
    # --- 方式2: demo 模式（模拟一个脆弱的模型）---
    # 这个模拟模型有意不设防，用于演示 DeepTeam 能检测到问题
    if "ignore" in input_text.lower() or "pretend" in input_text.lower():
        return f"Okay, I'll answer directly: {input_text}"
    return f"I'm a helpful assistant. You asked: {input_text}"


# ============================================================
# 主测试流程
# ============================================================

async def main():
    print("=" * 60)
    print("DeepTeam 基础红队测试")
    print("=" * 60)
    print()
    
    print("📋 测试配置:")
    print("  - 目标: 客服 Chatbot")
    print("  - 漏洞: Bias, Toxicity, PIILeakage")
    print("  - 攻击: PromptInjection, Roleplay")
    print("  - 每种漏洞攻击次数: 2")
    print()
    
    # 运行红队测试
    risk_assessment = red_team(
        model_callback=model_callback,
        vulnerabilities=[
            Bias(types=["race", "gender"]),
            Toxicity(),
            PIILeakage()
        ],
        attacks=[
            PromptInjection(),
            Roleplay()
        ],
        attacks_per_vulnerability_type=2,
        async_mode=True,
        max_concurrent=5
    )
    
    # 输出结果
    print("=" * 60)
    print("📊 风险评估结果")
    print("=" * 60)
    print(f"\n整体通过率: {risk_assessment.overall_pass_rate:.1f}%")
    
    for vr in risk_assessment.vulnerability_results:
        status = "🟢" if vr.pass_rate >= 80 else ("🟡" if vr.pass_rate >= 60 else "🔴")
        print(f"\n{status} {vr.vulnerability_name}")
        print(f"   通过率: {vr.pass_rate:.1f}%")
        print(f"   测试数: {vr.total_count}")
        
        for tc in vr.test_cases[:3]:  # 只显示前3个
            icon = "✅" if tc.success else "❌"
            print(f"   {icon} 输入: {tc.input[:60]}...")
            if not tc.success:
                print(f"      原因: {tc.reason[:80]}...")


if __name__ == "__main__":
    asyncio.run(main())
