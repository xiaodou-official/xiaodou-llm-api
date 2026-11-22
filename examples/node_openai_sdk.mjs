// 小豆AI大模型聚合 接口平台 · Node（openai v4+）示例
// 运行：npm i openai && XIAODOU_API_KEY=sk-... node examples/node_openai_sdk.mjs

import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: process.env.XIAODOU_BASE_URL ?? 'https://yuzhideep.cn/v1',
  apiKey: process.env.XIAODOU_API_KEY,
});

const model = process.env.XIAODOU_MODEL ?? 'kimi-k3';

const models = await client.models.list();
console.log('可用模型：', models.data.slice(0, 20).map((m) => m.id).join(', '));

const resp = await client.chat.completions.create({
  model,
  messages: [
    { role: 'system', content: '你是简洁的助手，回答不超过三句话。' },
    { role: 'user', content: '用三句话介绍 SSE 与 WebSocket 的区别。' },
  ],
  temperature: 0.3,
});

console.log('\n回答：', resp.choices[0]?.message?.content ?? '');
console.log('用量：', resp.usage);

const stream = await client.chat.completions.create({
  model,
  messages: [{ role: 'user', content: '数到 5，每个数字一行' }],
  stream: true,
});

process.stdout.write('\n流式：');
for await (const chunk of stream) {
  process.stdout.write(chunk.choices[0]?.delta?.content ?? '');
}
process.stdout.write('\n');
