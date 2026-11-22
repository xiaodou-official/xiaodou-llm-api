# 公开发布参数

> 本文件记录这份资料**公开发布所依据的参数与流程**，随资料一同公开。
> 发布前检查：结构完整、无内部地址与密钥、对外数字与控制台一致、交叉链接可达。

## 1. 发布参数

| # | 参数 | 值 |
| --- | --- | --- |
| 1 | 内容源目录 | `llm-api/`（主仓 `xiaodoudazi/xiaodou`，单树快照发布） |
| 2 | GitHub 仓 | `xiaodou-official/xiaodou-llm-api` |
| 3 | Gitee 镜像 | `lu-wulei/xiaodou-llm-api` |
| 4 | 可见范围 | 公开 |
| 5 | 许可证 | 内容 CC BY 4.0（`LICENSE`）；示例代码 MIT（`LICENSE-CODE`） |
| 6 | 发布方式 | 单树快照：`git commit-tree HEAD:llm-api`，单一内容源、无二次拷贝 |
| 7 | 网页版 | `https://www.xiaodouap.cn/llm-api/`（canonical；由官网静态包发布，`28_distribute_www_static.sh`） |
| 8 | 文档版本 | `v1.0.0`（2026-11-22） |

## 2. 内容纪律

1. **价格只写公开口径**：国产 = 官方价 ×0.5、海外文本 1.8 折起、生图 ¥0.05/张起、视频 ¥2.25/条起；实时价以控制台「模型广场」为准，不写 0.0x 折。
2. **不写未验证的能力**：模型是否支持工具调用、JSON 模式、多模态，按模型维度写「以模型支持为准」。
3. **不写内部地址与凭据**：不带服务器 IP、账号口令、内部端口、SMTP 账号、渠道密钥。
4. **不写竞争对手的贬损**：可以写「低价通常来自额度套利/号池」这类机制判断，不点名、不辱骂。
5. **数字只来自事实源**：价目与限流来自控制台与实施清单；改数字必须同批改 `docs/models-and-pricing.md` 与 `docs/changelog.md`。
6. **交叉链接保持可达**：README 的「同主体其他产品」六条链每年至少核对一次（仓改名/迁移时同批更新）。

## 3. 发布步骤

```bash
# 1) 本地检查：链接、UTF-8、无敏感串
node scripts/check_llm_api_docs_guard.js

# 2) 单树快照（在仓库根执行，HEAD 需已包含本目录最新内容）
tree=$(git rev-parse HEAD:llm-api)
commit=$(git commit-tree "$tree" -m "docs: 小豆AI大模型聚合 接口平台接入文档 v1.0.0")
git push git@github.com:xiaodou-official/xiaodou-llm-api.git "$commit:refs/heads/main"
git push gitee "$commit:refs/heads/main"          # remote 指向 gitee.com/lu-wulei/xiaodou-llm-api.git

# 3) 读回：逐文件比对 GitHub raw 与本地源
```

## 4. 变更登记

| 日期 | 版本 | 变更 | 发布方式 |
| --- | --- | --- | --- |
| 2026-11-22 | v1.0.0 | 首次公开发布 | 单树快照 |
