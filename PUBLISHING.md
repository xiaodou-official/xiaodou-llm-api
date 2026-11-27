# 公开发布参数

> 本文件记录这份资料**公开发布所依据的参数与流程**，随资料一同公开。
> 发布前检查：结构完整、无内部地址与密钥、对外数字与控制台一致、交叉链接可达。

## 1. 发布参数

| # | 参数 | 值 |
| --- | --- | --- |
| 1 | 内容源目录 | 本目录 `public-docs/`（仓 `llm`，2026-11-23 自主仓 `xiaodoudazi/xiaodou` 的 `llm-api/` 迁出；单树快照发布） |
| 2 | GitHub 仓 | `xiaodou-official/xiaodou-llm-api` |
| 3 | Gitee 镜像 | `lu-wulei/xiaodou-llm-api` |
| 4 | 可见范围 | 公开 |
| 5 | 许可证 | 内容 CC BY 4.0（`LICENSE`）；示例代码 MIT（`LICENSE-CODE`） |
| 6 | 发布方式 | 单树快照：`git commit-tree HEAD:public-docs`，单一内容源、无二次拷贝 |
| 7 | 网页版 | `https://www.xiaodouap.cn/llm-api/`（canonical；仍由主仓官网静态包 `28_distribute_www_static.sh` 发布，内容需与本目录同步） |
| 8 | 文档版本 | `v1.4.0`（2026-11-27） |

## 2. 内容纪律

1. **价格只写公开口径**：国产文本免费档 ¥0、付费 3 折起；海外文本 0.49 折起（`claude-opus-4.8`，非全体承诺）；生图 ¥0.05/张起；视频 ¥2.25/条起；实时价以控制台「模型与价格」为准。
2. **不写未验证的能力**：模型是否支持工具调用、JSON 模式、多模态，按模型维度写「以模型支持为准」。
3. **不写内部地址与凭据**：不带服务器 IP、账号口令、内部端口、SMTP 账号、服务密钥。
4. **不写竞争对手的贬损**：可以写「低价通常来自额度套利/号池」这类机制判断，不点名、不辱骂。
5. **数字只来自事实源**：价目与限流来自控制台与实施清单；改数字必须同批改 `docs/models-and-pricing.md` 与 `docs/changelog.md`。
6. **交叉链接保持可达**：README 的「同主体其他产品」六条链每年至少核对一次（仓改名/迁移时同批更新）。

## 3. 发布步骤

```bash
# 1) 本地检查：链接、UTF-8、无敏感串（在 llm 仓根执行）
node scripts/check_llm_api_docs_guard.js

# 2) 单树快照（每个远端一个快照；parent 取该远端当前 main，保证快进推送）
tree=$(git rev-parse HEAD:public-docs)
for repo in \
  https://github.com/xiaodou-official/xiaodou-llm-api.git \
  https://gitee.com/lu-wulei/xiaodou-llm-api.git
do
  parent=$(git ls-remote "$repo" refs/heads/main | cut -f1)
  commit=$(git commit-tree "$tree" -p "$parent" -m "docs: 小豆AI大模型聚合 接口平台接入文档 v1.4.0")
  git push "$repo" "${commit}:refs/heads/main"
done

# 3) 读回：逐文件比对 GitHub raw 与本地源
```

## 4. 变更登记

| 日期 | 版本 | 变更 | 发布方式 |
| --- | --- | --- | --- |
| 2026-11-27 | v1.4.0 | 刷新公开价目：国产文本 ¥0 起 / 3 折起、海外文本 0.49 折起（`claude-opus-4.8`）、GPT 生图 ¥0.05/张起、视频 ¥2.25/条起；旧「最低 1.8 折」口径作废 | 单树快照 |
| 2026-11-25 | v1.3.0 | 新增模型供给，在售 80；按次计费单位修正为人民币/次并与公示价对齐；`gemini-4-carbon` 完成服务切换 | 单树快照 |
| 2026-11-24 | v1.2.0 | 国产文本价格口径统一为 ×0.3（3 折）；国产视频保持 5 折 | 单树快照 |
| 2026-11-23 | v1.1.0 | 国产文本价格口径：首批 16 个文本模型 ×0.3、其他国产文本 ×0.5；视频保持 5 折（历史口径） | 单树快照 |
| 2026-11-22 | v1.0.0 | 首次公开发布 | 单树快照 |
