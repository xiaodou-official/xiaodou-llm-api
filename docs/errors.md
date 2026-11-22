# 错误码与排查手册

> 适用版本：v1.0.0 ｜ 更新：2026-11-22 ｜ 返回 [README](../README.md)

## 1. 错误响应长什么样

```json
{
  "error": {
    "message": "无效的令牌",
    "type": "new_api_error",
    "code": "invalid_token"
  }
}
```

- `message`：给人看的说明，措辞可能随版本变化，**不要用字符串匹配做逻辑**。
- `type`：错误大类，可能是 `new_api_error` 或上游透传的类型。
- `code`：机器可读的错误码，判断逻辑以 **HTTP 状态码 + `code`** 为准。

## 2. 错误码表

| HTTP | code | 含义 | 客户端该怎么做 |
| --- | --- | --- | --- |
| 400 | `invalid_request_error` | 请求体不合法：缺字段、类型不对、JSON 语法错 | 修正请求，不要重试 |
| 401 | `invalid_token` | 令牌不存在、被禁用或已过期 | 检查 `Authorization` 头；重新生成令牌 |
| 402 | `insufficient_quota` | 令牌或账号额度不足 | 充值或换令牌；不要循环重试 |
| 403 | `model_not_allowed` | 令牌的模型范围不含该模型 | 在令牌设置里放开 |
| 403 | `access_denied` | 账号被限制（违规、风控） | 联系客服 |
| 404 | `model_not_found` | 模型 ID 不存在或已下架 | `GET /v1/models` 对照 |
| 404 | `not_found` | 路径错误 | 检查 base URL 是否带 `/v1` |
| 413 | `request_too_large` | 请求体过大 | 分段或压缩上下文 |
| 429 | `rate_limit_exceeded` | 超过每分钟请求数 | 指数退避重试 |
| 500 | `upstream_error` | 上游模型服务报错 | 退避重试，最多 2–3 次 |
| 502 | `bad_gateway` | 网关到上游的链路异常 | 退避重试 |
| 503 | `no_available_channel` | 当前没有可用渠道 | 换模型或稍后重试 |
| 504 | `upstream_timeout` | 上游超时 | 缩短输入或换模型 |

> 上游不同厂商的错误码会被归一化，个别模型可能透传自家 `code`；表里未列出的码按 HTTP 状态处理。

## 3. 重试策略（可直接抄）

```python
import random
import time
import httpx

RETRYABLE = {429, 500, 502, 503, 504}

def post_with_retry(url, headers, payload, max_attempts=4):
    for attempt in range(max_attempts):
        resp = httpx.post(url, headers=headers, json=payload, timeout=120)
        if resp.status_code not in RETRYABLE:
            return resp
        if attempt == max_attempts - 1:
            return resp
        base = min(2 ** attempt, 8)
        time.sleep(base + random.uniform(0, 0.5))
    return resp
```

四条纪律：

1. **只重试 429 / 5xx**。400 / 401 / 402 / 403 重试多少次都是同一个结果，只会烧额度。
2. **重试有上限**（3–4 次），并加随机抖动，避免整批任务同时打回来。
3. **流式请求重试要幂等**：重试前确认没有把半截输出写进数据库。
4. **记录失败样本**：模型 ID、状态码、`code`、耗时，三者足够定位九成问题。

## 4. 排障顺序

1. `GET /v1/models`：确认模型存在且令牌有权访问。
2. 用最小请求体（一条 user 消息、非流式）复现。
3. 看控制台「日志」：状态码、tokens、扣费是否符合预期。
4. 换一个模型试：能通则问题在上游渠道，不是你的代码。
5. 还不行，带上**请求时间、模型 ID、HTTP 状态码、`error.code`** 提 Issue。

## 5. 高频问题对照

| 现象 | 大概率原因 | 处理 |
| --- | --- | --- |
| 本地能通、线上 401 | 线上环境变量没注入，或多了空格/换行 | `echo -n "$KEY" | wc -c` 对长度 |
| 偶发 503 | 上游渠道限流或切换 | 加退避；多模型兜底 |
| 输出被截断 | 触达 `max_tokens` 或模型上限 | 看 `finish_reason` 是否 `length` |
| 中文变问号 | 客户端按非 UTF-8 解码 | 统一 UTF-8，别二次转码 |
| 流式卡住不结束 | 代理缓冲或没处理 `[DONE]` | 关代理缓冲，按行解析 |
| 费用比预期高 | 上下文重复携带、`max_tokens` 设太大 | 精简历史消息，按需截断 |
