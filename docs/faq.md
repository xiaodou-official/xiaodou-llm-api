# 常见问题（FAQ）

> 适用版本：v1.4.0 ｜ 更新：2026-11-27 ｜ 返回 [README](../README.md)

## 平台与定位

**问：小豆AI大模型聚合 接口平台是什么？**
答：它是宇智人工智能（深圳）有限公司运营的大模型 API 聚合服务。开发者用一个 OpenAI 兼容地址 `https://yuzhideep.cn/v1` 和一枚 `sk-` 令牌，就能调用 GLM、DeepSeek、Kimi 等模型；平台按 token 分别计算输入与输出费用，国产文本低至 **¥0**（`hy4flash-free` 免费档）、付费国产文本 **3 折起**，密钥、额度与调用明细在网页控制台管理。

**问：它和大模型官方 API 是什么关系？**
答：平台把多家模型的调用统一到同一个 OpenAI 兼容入口，计费、鉴权、限流、日志由平台承担；模型能力与内容审核以对应模型服务为准。

**问：和「免签支付」「发卡平台」是一回事吗？**
答：不是。本平台只提供大模型调用接口，不处理收款、不卖卡密。需要收款接支付走[小豆支付开放平台](https://xdfair.cn/)；需要上架数字商品走[小豆集市](https://xdjishi.cn/)。

## 接入

**问：支持 OpenAI 官方 SDK 吗？**
答：支持。Python / Node 的官方 SDK 改 `base_url` 即可；LangChain、LlamaIndex、Dify、FastGPT、Cherry Studio、Chatbox、NextChat 等支持「自定义 OpenAI 地址」的客户端同样能接。

**问：支持流式输出与工具调用吗？**
答：流式（SSE）全模型支持；工具调用、JSON 模式、多模态等能力**按模型而定**，接入前用目标模型跑一次小样本验证，不要按平台维度假设。

**问：模型 ID 从哪儿拿？**
答：控制台「模型与价格」，或 `GET /v1/models`。不要在前端写死清单，模型上下架会变。

**问：能不能用自己的域名 / 反向代理？**
答：可以，但别改写请求头和路径，别在前端暴露令牌。多一层代理时注意关闭响应缓冲，否则流式会变成「一次性返回」。

**问：Gemini CLI 能用吗？**
答：能。平台提供 Gemini 原生端点 `https://yuzhideep.cn/v1beta`，鉴权头 `x-goog-api-key`。三处要配对：`GOOGLE_GEMINI_BASE_URL` 填 `https://yuzhideep.cn`，**不要带 `/v1beta` 后缀**（CLI 会自己拼，带上会变成 `/v1beta/v1beta/` 返回 404）；`~/.gemini/settings.json` 加 `"security": {"auth": {"selectedType": "gemini-api-key", "useExternal": true}}`，写成 `vertex-ai` 会忽略令牌、改去取 Google 凭据并报 `Could not load the default credentials`；`~/.gemini/.env` 加 `GEMINI_MODEL=gemini-4-argon`，因为 CLI 内置的默认模型在本站没有渠道，不指定就 `503 model_not_found`。

**问：几个 CLI 怎么跳过逐次权限确认？**
答：`claude --dangerously-skip-permissions`、`codex --dangerously-bypass-approvals-and-sandbox`、`GEMINI_CLI_TRUST_WORKSPACE=true gemini --approval-mode yolo`。三条都会跳过全部确认，**只在你自己信任的项目目录里用**。Gemini CLI 两处容易踩：单给 `--approval-mode yolo` 不够，目录未受信任时会被强制改回 `default` 并退出；而 `--skip-trust` **不能**用来修这个——它要等命令行解析后才生效，CLI 读 `~/.gemini/.env` 时目录仍判为未信任，该文件被跳过，令牌与端点都读不到，报 `Could not load the default credentials` 或弹窗要求重输 Key。要么用 `GEMINI_CLI_TRUST_WORKSPACE=true`，要么把目录写进 `~/.gemini/trustedFolders.json` 的 `"TRUST_FOLDER"`。

## 价格与账单

**问：国产文本 3 折怎么算？**
答：付费国产文本按厂商公开挂牌价 ×0.3 起，输入与输出同折扣，单位人民币 / 100 万 tokens；`hy4flash-free` 为本站免费档，¥0。例：`glm-5.3` 官方 ¥8 / ¥28 → 小豆 ¥2.40 / ¥8.40；`deepseek-v4.1-flash` 官方 ¥1 / ¥4 → ¥0.30 / ¥1.20；`kimi-k3` 官方 ¥8 / ¥40 → ¥2.40 / ¥12.00。

**问：海外模型最低几折？**
答：当前公开价目最低 **0.49 折**：`claude-opus-4.8` 官方 $5/$25 → 本站约 ¥1.80/¥9.00 每百万 tokens（比官方直连便宜约 95%）；最低单价的海外文本是 `claude-haiku-5.5`，约 ¥0.31/¥1.56。生图最低 **¥0.05/张**（`gpt-image-2.6`、`2.5`、`2.6-flare`），视频 **¥2.25/条起**（`seedance-2.0-mini-5s`）。价格可能调整，以控制台「模型与价格」为准；不承诺 SLA。

**问：怎么充值？能开发票吗？**
答：控制台 <https://yuzhideep.cn/topup/> 充值；对公、发票与合同需求发邮件到 <contact@yuzhideep.com>，说明主体与预计用量。

**问：额度能退吗？**
答：配额不可提现、不可转让，已消耗部分不退款；因平台原因长时间不可用的，可按用户协议协商补偿。

## 稳定与数据

**问：限速多少？**
答：默认 60 次/分钟 / 令牌。更高并发请申请；批量任务请用队列 + 指数退避。

**问：会不会记录我的对话？**
答：请求会经平台链路处理，链路上必然处理请求内容。**不要把敏感个人信息写进 prompt**；账号与调用记录的处理方式以用户协议和隐私政策为准。有严格数据驻留要求的场景，建议使用你信任的独立部署端点。

**问：平台挂了怎么办？**
答：平台按现状提供服务，不承诺 100% 可用。生产环境至少准备两个模型做兜底，主路失败时降级。

## 合规

**问：生成内容能直接给最终用户看吗？**
答：可以，但要标注「内容由 AI 生成」，并自行承担内容安全责任。面向公众提供生成式 AI 服务的，需自行评估备案、内容审核与未成年人保护义务。

**问：可以转售接口吗？**
答：令牌只限本账号使用。转售、二次分发或搭建面向公众的同类 API 服务，需要平台书面授权。

**问：出问题去哪儿反馈？**
答：本仓 [Issues](https://github.com/xiaodou-official/xiaodou-llm-api/issues) 或 <contact@yuzhideep.com>，带上请求时间、模型 ID、HTTP 状态码与 `error.code`。
