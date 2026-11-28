# 变更记录

本文只记**对调用方有影响**的变化：接口、模型供给、价格口径、限额、错误码。文案润色不记。

## v1.5.0 — 2026-11-28

- **新增 Gemini 原生端点**：`/v1beta/models/{model}:generateContent` 与 `:streamGenerateContent?alt=sse`，鉴权头 `x-goog-api-key`，`GET /v1beta/models` 返回模型列表。官方 Gemini CLI、Google SDK 可直接接入，不再需要自建协议转换层。
- **CC Switch 导入支持 Gemini CLI**：控制台令牌行末「⋯」→「CC Switch」新增 Gemini CLI 选项，导入页 <https://yuzhideep.cn/ccswitch/> 同步上线。
- **接入注意**：`GOOGLE_GEMINI_BASE_URL` 填 `https://yuzhideep.cn`，**不要带 `/v1beta` 后缀**——CLI 会自己拼 `/v1beta/models/...`，带上会变成 `/v1beta/v1beta/...` 返回 404。另需在 `~/.gemini/settings.json` 补 `"security": {"auth": {"selectedType": "gemini-api-key", "useExternal": true}}`，否则报 `Invalid auth method selected`。
- **新增三个 CLI 的免确认启动命令**（仅供可信目录）：`claude --dangerously-skip-permissions`、`codex --dangerously-bypass-approvals-and-sandbox`、`gemini --skip-trust --approval-mode yolo`。其中 Gemini CLI 单给 `--approval-mode yolo` 会被目录信任检查强制改回 `default` 并退出。

## v1.4.0 — 2026-11-27

- 刷新公开价目与「最低价 / 最低折扣」口径（以控制台 `/api/pricing` 2026-11-27 读回为准）：
  - **国产文本**：`hy4flash-free` 保持 **¥0**；付费国产文本 **3 折起**。示例：`glm-5.3` 官方 ¥8 / ¥28 → 本站 ¥2.40 / ¥8.40；`deepseek-v4.1-flash` 官方 ¥1 / ¥4 → ¥0.30 / ¥1.20；`kimi-k3` 官方 ¥8 / ¥40 → ¥2.40 / ¥12.00。
  - **海外文本**：最低折扣从 1.8 折改为 **0.49 折**（`claude-opus-4.8` 官方 $5/$25 → 约 ¥1.80 / ¥9.00 每百万 tokens）；最低单价 `claude-haiku-5.5` 约 ¥0.31 / ¥1.56。
  - **生图**：`gpt-image-2.6`、`gpt-image-2.5`、`gpt-image-2.6-flare` 均为 **¥0.05/张**。
  - **视频**：`seedance-2.0-mini-5s` **¥2.25/条**（¥0.45/秒 × 5 秒）；最低折扣档 `minimax-h3-6s` 约 **8 折**（¥2.40/6 秒，参考价估算）。
- 旧版「海外文本最低 1.8 折 / 没有 0.0x 折」的写法作废：当前公开价目最低为 0.49 折，但只适用于对应模型，不是全体海外模型承诺。
- 价格可能调整，实时价以控制台「模型与价格」与 `/api/pricing` 为准；不承诺 SLA。

## v1.3.0 — 2026-11-25

- 新增模型供给，在售模型从 63 个增至 **80 个**：新增 `qwen3.8-max`、`qwen3.8-flash`、`qwen4-max`、`glm-5.3-flashx`、`kimi-k2.7-code`、`minimax-m3`、`claude-opus-4.6/4.7/4.8`、`claude-sonnet-4.5`、`gemini-2.5-flash`、`gpt-5.6-terra`、`gpt-6.1-terra`、`gpt-6.2-astra`、`gpt-image-2.5`、`gpt-image-2.6`、`grok-imagine-image`。
- 按次模型（图片、视频）计费单位修正为**人民币/次**，实际扣费与控制台、公开价目对齐；此前实际扣费约为公示价的 1/7.3。存量额度与已支付订单不受影响，新请求即时按公示价计费。
- `gemini-4-carbon` 完成模型服务切换，模型名与价格不变。
- 示例：`gpt-image-2.5-flare` ¥0.25/张、`gpt-image-2.6-flare` ¥0.05/张、`seedance-2.0-mini-5s` ¥2.25/条。

## v1.2.0 — 2026-11-24

- 国产文本价格口径统一为「厂商公开挂牌价 ×0.3（3 折）」，不再区分模型来源；国产视频保持 5 折（¥2.25/条起）；海外文本与生图价格不变。
- 示例价：`glm-5.3` 官方 ¥4.16 / ¥14.56 → 本站 ¥1.25 / ¥4.37；`glm-4.6` 官方 ¥4 / ¥8 → ¥1.20 / ¥2.40。
- 存量额度与已支付订单不受影响；新请求即时按新价计费，控制台「模型与价格」与 `/api/pricing` 为准。

## v1.1.0 — 2026-11-23

- 国产文本价格口径调整为：16 个文本模型按「厂商公开挂牌价 ×0.3（3 折）」；其他国产文本保持「×0.5（5 折）」；国产视频保持 5 折（¥2.25/条起）；海外文本与生图价格不变。
- 示例价：`glm-5.3` 官方 ¥4.16 / ¥14.56 → 本站 ¥1.25 / ¥4.37；`glm-4.6` 官方 ¥4 / ¥8 → ¥2.04 / ¥4.09。
- 存量额度与已支付订单不受影响；新请求即时按新价计费，控制台「模型与价格」与 `/api/pricing` 为准。

## v1.0.0 — 2026-11-22

- 首次公开发布接入文档：产品定义、快速开始、接口参考、模型与价格、错误码、限额、FAQ。
- 价格口径固定为：国产文本官方价 ×0.5、海外文本 1.8 折起（0.18 倍）、生图 ¥0.05/张起、视频 ¥2.25/条起；当前 63 个在售模型，以控制台公开价目为准。
- 默认限额：每令牌 60 次/分钟。
- 公开价目示例：`deepseek-v4.1-flash`、`deepseek-v4-pro`、`glm-5.3`、`glm-5.3-flash`、`kimi-k3`、`kimi-k3.1-pro`。
- 品牌总站新增接入文档页：<https://www.xiaodouap.cn/llm-api/>。

## 记录规范

- 新增模型：写模型 ID、上线日期、输入/输出价。
- 价格调整：写旧价、新价、生效日期；不覆盖历史。
- 限额调整：写旧值、新值、对存量的影响。
- 接口变更：写字段、兼容期、弃用日期。
