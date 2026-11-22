# 快速开始：10 分钟接到小豆AI大模型聚合 接口平台

> 适用版本：v1.0.0 ｜ 更新：2026-11-22 ｜ 返回 [README](../README.md)

本文只做一件事：让你从零到发出第一条请求，再到接进自己的服务。全部步骤都在本机完成，不需要改服务器。

## 第 0 步：准备

| 需要的 | 说明 |
| --- | --- |
| 一个能收信的邮箱 | 注册要邮箱验证码，不需要手机号 |
| `curl` 或任意 HTTP 客户端 | 用来验证链路 |
| 一门语言的 OpenAI SDK（可选） | Python `openai>=1.0`、Node `openai>=4` |

## 第 1 步：注册并创建令牌

1. 打开 <https://yuzhideep.cn/login>，用邮箱注册并完成邮箱验证码。
2. 登录后进「令牌」页，点「新建令牌」。
3. 建议一次就设好两件事：**额度上限**（防止密钥泄露被刷爆）和**模型范围**（只放开你要用的模型）。
4. 复制 `sk-` 开头的令牌。**它只显示一次**，丢了就重新生成。

## 第 2 步：发第一条请求

```bash
export XIAODOU_API_KEY="sk-你的令牌"

curl -sS https://yuzhideep.cn/v1/chat/completions \
  -H "Authorization: Bearer $XIAODOU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v4.1-flash",
    "messages": [{"role": "user", "content": "你好，用一句话介绍你自己"}]
  }'
```

看到 `choices[0].message.content` 有内容、`usage.total_tokens` 大于 0，链路就通了。

## 第 3 步：换成流式

```bash
curl -N https://yuzhideep.cn/v1/chat/completions \
  -H "Authorization: Bearer $XIAODOU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.3",
    "stream": true,
    "messages": [{"role": "user", "content": "写一段 50 字的项目介绍"}]
  }'
```

返回是 SSE：每行 `data: {"choices":[{"delta":{"content":"..."}}]}`，最后一行 `data: [DONE]`。注意用 `-N` 关掉 curl 缓冲，否则看起来像「一次性返回」。

## 第 4 步：接进代码

Python：

```python
from openai import OpenAI

client = OpenAI(base_url="https://yuzhideep.cn/v1", api_key="sk-你的令牌")
stream = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{"role": "user", "content": "写一句适合放在 README 顶部的介绍"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

Node：

```js
import OpenAI from 'openai';

const client = new OpenAI({ baseURL: 'https://yuzhideep.cn/v1', apiKey: process.env.XIAODOU_API_KEY });
const stream = await client.chat.completions.create({
  model: 'kimi-k3',
  messages: [{ role: 'user', content: '写一句适合放在 README 顶部的介绍' }],
  stream: true,
});
for await (const chunk of stream) process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
```

## 第 5 步：上线前检查清单

- [ ] 令牌只放在服务端环境变量里，**没有**出现在前端 bundle、Git 或日志里。
- [ ] 令牌设了额度上限和模型范围；生产与测试用两枚不同令牌。
- [ ] 对 429 / 500 / 503 做了指数退避重试，重试有上限。
- [ ] 记录了 `model`、耗时、`usage` 与 HTTP 状态码，方便对账与排障。
- [ ] prompt 里没有密码、证件号、银行卡号、客户名单等敏感信息。
- [ ] 面向最终用户展示生成内容时，有「内容由 AI 生成」之类的说明。

## 常见卡点

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `401 invalid_token` | 令牌填错、被禁用或已过期 | 控制台重新生成 |
| `404 model_not_found` | 模型名不在当前令牌范围或已下架 | `GET /v1/models` 对照 |
| `429 rate_limit_exceeded` | 超过 60 次/分钟 | 降并发、加退避 |
| 流式没有逐字输出 | 客户端缓冲 | 关掉代理/框架的响应缓冲，或用 `curl -N` |
| 中文乱码 | 没按 UTF-8 处理 | 声明 `charset=utf-8`，不要二次转码 |

下一步：看 [接口参考](./api-reference.md) 与 [错误码](./errors.md)。
