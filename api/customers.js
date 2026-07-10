/**
 * Vercel Serverless Function
 * 从飞书Base读取数据，作为前端API代理
 *
 * 环境变量（在Vercel中设置）:
 *   FEISHU_APP_ID      - 飞书自建应用的 App ID
 *   FEISHU_APP_SECRET  - 飞书自建应用的 App Secret
 */

const BASE_TOKEN = 'GiHGbwaUDaahi3sEPTKcpdrhnze';
const TABLE_1_ID = 'tbl1dXvlfb1YmFOW';
const TABLE_2_ID = 'tbl1lO5pPXHz4DjQ';

// 缓存 tenant_access_token（Vercel冷启动时重置）
let tokenCache = { token: null, expiresAt: 0 };

async function getTenantToken() {
  if (tokenCache.token && Date.now() < tokenCache.expiresAt) {
    return tokenCache.token;
  }

  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;

  if (!appId || !appSecret) {
    throw new Error('FEISHU_APP_ID 或 FEISHU_APP_SECRET 未设置');
  }

  const res = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
  });

  const data = await res.json();
  if (data.code !== 0) {
    throw new Error(`获取飞书token失败: ${data.msg}`);
  }

  tokenCache = {
    token: data.tenant_access_token,
    expiresAt: Date.now() + (data.expire - 60) * 1000,
  };
  return data.tenant_access_token;
}

async function fetchTableRecords(token, tableId) {
  let allRecords = [];
  let pageToken = null;

  for (let page = 0; page < 5; page++) {
    let url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${BASE_TOKEN}/tables/${tableId}/records?page_size=100`;
    if (pageToken) url += `&page_token=${pageToken}`;

    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await res.json();
    if (data.code !== 0) {
      console.error(`获取表 ${tableId} 失败:`, data.msg);
      break;
    }

    const records = data.data.items || [];
    const parsed = records.map(r => {
      const fields = r.fields || {};
      const obj = { _record_id: r.record_id };
      for (const [k, v] of Object.entries(fields)) {
        if (v !== null && v !== undefined) {
          obj[k] = Array.isArray(v) ? (v.length === 1 ? v[0] : v.join(', ')) : v;
        } else {
          obj[k] = '';
        }
      }
      return obj;
    });

    allRecords = allRecords.concat(parsed);

    if (!data.data.has_more) break;
    pageToken = data.data.page_token;
  }

  return allRecords;
}

export default async function handler(req, res) {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    const token = await getTenantToken();
    const [table1, table2] = await Promise.all([
      fetchTableRecords(token, TABLE_1_ID),
      fetchTableRecords(token, TABLE_2_ID),
    ]);

    res.status(200).json({
      ok: true,
      table1,
      table2,
      lastFetched: new Date().toISOString(),
    });
  } catch (err) {
    console.error('API Error:', err);
    res.status(500).json({ ok: false, error: err.message });
  }
}
