# 接口参考

> 适用版本：v1.0.0 ｜ 更新：2026-11-22 ｜ 返回 [README](../README.md)

Base URL：`https://yuzhideep.cn/v1`
鉴权：`Authorization: Bearer sk-...`

## 1. 对话补全 `POST /v1/chat/completions`

与 OpenAI Chat Completions 请求体一致。最小可用请求：

```json
{
  "model": "deepseek-v4.1-flash",
  "messages": [{ "role": "user", "content": "你好" }]
}
```

### 1.1 请求字段

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `model` | string | 是 | 模型 ID，见控制台「模型与价格」或 `GET /v1/models` |
| `messages` | array | 是 | 消息数组，见下表 |
| `stream` | boolean | 否 | `true` 返回 SSE；默认 `false` |
| `temperature` | number | 否 | 采样温度，范围与模型一致（通常 0–2） |
| `top_p` | number | 否 | 核采样，通常与 `temperature` 二选一 |
| `max_tokens` | integer | 否 | 最大输出 tokens；受模型上限约束 |
| `stop` | string \| string[] | 否 | 停止词 |
| `tools` | array | 否 | 工具（函数）定义，模型支持时生效 |
| `tool_choice` | string \| object | 否 | `auto` / `none` / 指定函数 |
| `response_format` | object | 否 | `{"type":"json_object"}` 等，模型支持时生效 |
| `user` | string | 否 | 终端用户标识，便于自己做用量归因 |

`messages[]` 的 `role` 取值：

| role | 作用 |
| --- | --- |
| `system` | 系统提示，设定角色与边界 |
| `user` | 用户输入 |
| `assistant` | 模型历史回复 |
| `tool` | 工具调用结果回填（配合 `tool_call_id`） |

### 1.2 非流式响应

```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1795000000,
  "model": "deepseek-v4.1-flash",
  "choices": [
    {
      "index": 0,
      "message": { "role": "assistant", "content": "你好，有什么可以帮你？" },
      "finish_reason": "stop"
    }
  ],
  "usage": { "prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21 }
}
```

`finish_reason` 常见值：`stop`（正常结束）、`length`（触达 `max_tokens`）、`tool_calls`（要执行工具）、`content_filter`（内容审核拦截）。

### 1.3 流式响应（SSE）

```
data: {"id":"chatcmpl-abc123","choices":[{"index":0,"delta":{"role":"assistant","content":"你"}}]}
data: {"id":"chatcmpl-abc123","choices":[{"index":0,"delta":{"content":"好"}}]}
data: {"id":"chatcmpl-abc123","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}
data: [DONE]
```

客户端要注意三件事：

1. 按行解析，只处理 `data:` 前缀；`[DONE]` 是结束标记，不是 JSON。
2. `delta.content` 可能为空（例如只带 `role` 或 `finish_reason` 的块），要判空。
3. 中间可能插入注释行或空行，解析器要能跳过。

### 1.4 工具调用（函数调用）

```json
{
  "model": "glm-5.3",
  "messages": [{ "role": "user", "content": "北京现在天气怎么样？" }],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "description": "查询城市当前天气",
        "parameters": {
          "type": "object",
          "properties": { "city": { "type": "string" } },
          "required": ["city"]
        }
      }
    }
  ],
  "tool_choice": "auto"
}
```

模型决定调用时，`choices[0].message.tool_calls` 会带函数名与参数 JSON；执行完把结果以 `role: "tool"` 回填，再请求一次。工具调用是否可用取决于具体模型，先小样本验证再接生产。

## 2. 模型列表 `GET /v1/models`

```bash
curl https://yuzhideep.cn/v1/models -H "Authorization: Bearer $XIAODOU_API_KEY"
```

返回：

```json
{
  "object": "list",
  "data": [{ "id": "deepseek-v4.1-flash", "object": "model", "owned_by": "xiaodou" }]
}
```

只返回当前令牌可访问的模型。做模型选择器时用它，不要在前端写死清单。

## 3. 额度查询 `GET /v1/dashboard/billing/subscription`

兼容 OpenAI 的额度查询形态，用于在自建后台展示剩余额度。字段以实际返回为准，**扣费金额以控制台「日志」页为准**，不要用这个接口做财务对账。

## 4. 请求与响应头

| 头 | 方向 | 说明 |
| --- | --- | --- |
| `Authorization` | 请求 | 必填，`Bearer sk-...` |
| `Content-Type` | 请求 | 必填，`application/json` |
| `Accept: text/event-stream` | 请求 | 流式时建议带上 |
| `Content-Type: text/event-stream` | 响应 | 流式响应 |

排障时最有用的三样东西是**请求时间、模型 ID、HTTP 状态码**：控制台「日志」页按时间倒序展示每次调用，用这三个值就能对上号。

## 5. 多模态与计费单位

- 文本按 token 计费；图片按张、视频按条或按秒计费，单位见控制台模型页与 [模型与价格](./models-and-pricing.md)。
- 图片、视频与文本共用同一枚令牌；不同模型的入参形态不同，接入前看模型说明。

## 6. 兼容性说明

- 遵循 OpenAI 协议，但**不保证** OpenAI 的全部实验性字段（如 `logprobs`、`service_tier`）在所有模型上生效；不支持的字段通常被忽略，个别模型会返回 400。
- 图片、语音、向量等接口取决于具体模型是否提供，接入前用 `GET /v1/models` 与控制台确认。
- 不同模型对 `tools`、`response_format`、上下文长度的支持不同；以模型为维度做能力开关，不要按平台维度假设。
