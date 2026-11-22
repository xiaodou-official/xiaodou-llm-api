#!/usr/bin/env bash
# 小豆AI大模型聚合 接口平台 · curl 最小示例
# 用法：XIAODOU_API_KEY=sk-... bash examples/curl.sh
set -euo pipefail

: "${XIAODOU_API_KEY:?请先设置 XIAODOU_API_KEY（控制台「令牌」页生成）}"
BASE="${XIAODOU_BASE_URL:-https://yuzhideep.cn/v1}"
MODEL="${XIAODOU_MODEL:-deepseek-v4.1-flash}"

echo "== 模型列表 =="
curl -sS "$BASE/models" \
  -H "Authorization: Bearer $XIAODOU_API_KEY" | head -c 400
echo

echo "== 非流式对话 =="
curl -sS "$BASE/chat/completions" \
  -H "Authorization: Bearer $XIAODOU_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"用一句话解释什么是 SSE\"}],
    \"stream\": false
  }"
echo

echo "== 流式对话（-N 关闭缓冲） =="
curl -sSN "$BASE/chat/completions" \
  -H "Authorization: Bearer $XIAODOU_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [{\"role\": \"user\", \"content\": \"数到 5，每个数字一行\"}],
    \"stream\": true
  }"
