"""小豆AI大模型聚合 接口平台 · 流式输出示例（带退避重试）。

依赖：pip install openai>=1.0
用法：XIAODOU_API_KEY=sk-... python examples/python_stream.py
"""

import os
import random
import sys
import time

import openai
from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("XIAODOU_BASE_URL", "https://yuzhideep.cn/v1"),
    api_key=os.environ["XIAODOU_API_KEY"],
)

MODEL = os.environ.get("XIAODOU_MODEL", "glm-5.3")


def stream_once(prompt: str, attempts: int = 4) -> None:
    for attempt in range(attempts):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    sys.stdout.write(delta)
                    sys.stdout.flush()
            sys.stdout.write("\n")
            return
        except (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError) as exc:
            if attempt == attempts - 1:
                raise
            wait = min(2 ** attempt, 8) + random.uniform(0, 0.5)
            print(f"\n[重试 {attempt + 1}/{attempts - 1}] {type(exc).__name__}，{wait:.1f}s 后重试", file=sys.stderr)
            time.sleep(wait)


if __name__ == "__main__":
    stream_once("用 100 字介绍什么是 OpenAI 兼容接口")
