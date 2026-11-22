"""小豆AI大模型聚合 接口平台 · OpenAI SDK 最小示例。

依赖：pip install openai>=1.0
用法：XIAODOU_API_KEY=sk-... python examples/python_openai_sdk.py
"""

import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("XIAODOU_BASE_URL", "https://yuzhideep.cn/v1"),
    api_key=os.environ["XIAODOU_API_KEY"],
)

MODEL = os.environ.get("XIAODOU_MODEL", "deepseek-v4.1-flash")


def main() -> None:
    models = client.models.list()
    print("可用模型：", ", ".join(m.id for m in models.data[:20]))

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "你是简洁的助手，回答不超过三句话。"},
            {"role": "user", "content": "把这句话翻译成英文：今天适合写代码。"},
        ],
        temperature=0.3,
    )
    print("\n回答：", resp.choices[0].message.content)
    if resp.usage:
        print(f"用量：输入 {resp.usage.prompt_tokens} / 输出 {resp.usage.completion_tokens} tokens")


if __name__ == "__main__":
    main()
