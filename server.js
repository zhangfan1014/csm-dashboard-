/**
 * 飞书多维表格 → HTML看板 · 后端代理服务器
 *
 * 方案: 飞书多维表格(数据库) → 本服务(API代理) → HTML前端看板
 *
 * 后续扩展:
 *   - 销售易CRM MCP接入后, 在此增加同步逻辑, 将CRM数据写入飞书Base
 *   - 或增加一个 `/api/sync-crm` 端点用于触发CRM→飞书的同步
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ====== 配置 ======
const PORT = 3456;
const BASE_TOKEN = 'GiHGbwaUDaahi3sEPTKcpdrhnze';
const TABLE_MERGED = 'tbl6qj6cIr1hnezy';  // 客户信息大宽表（两表合并）

// ====== 缓存 ======
let cachedData = {
  customers: [],
  lastFetched: null,
  crmSync: null,  // 销售易CRM同步状态
};
let fetchInProgress = false;

// ====== 数据拉取 ======
function fetchFromFeishu(tableId, tableName) {
  const cmd = `lark-cli base +record-list --base-token ${BASE_TOKEN} --table-id ${tableId} --as user --format json --limit 200`;
  try {
    const stdout = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    // 去掉 lark-cli 的 warn 前缀 (ANSI + 文本)
    const jsonStr = stdout.substring(stdout.indexOf('{'));
    const data = JSON.parse(jsonStr);
    if (!data.ok) {
      console.error(`  [${tableName}] fetch failed:`, data.error);
      return [];
    }
    const records = data.data.data || [];
    const fields = data.data.fields || [];
    return records.map(rec => {
      const obj = {};
      for (let i = 0; i < fields.length; i++) {
        let val = rec[i];
        if (val !== null && val !== undefined) {
          if (Array.isArray(val)) {
            // select/multi-select 字段 - 取第一个值
            val = val.length > 0 ? val.join(', ') : '';
          }
          if (typeof val === 'string') val = val.trim();
        }
        obj[fields[i]] = val ?? '';
      }
      return obj;
    });
  } catch (err) {
    console.error(`  [${tableName}] fetch error:`, err.message);
    return [];
  }
}

function refreshCache() {
  if (fetchInProgress) return;
  fetchInProgress = true;
  console.log(`[${new Date().toLocaleTimeString()}] Fetching data from Feishu Base...`);
  try {
    const customers = fetchFromFeishu(TABLE_MERGED, '客户信息大宽表');

    // 读取CRM同步结果
    let crmSync = null;
    const syncResultPath = path.join(__dirname, 'sync_result.json');
    if (fs.existsSync(syncResultPath)) {
      try {
        crmSync = JSON.parse(fs.readFileSync(syncResultPath, 'utf-8'));
      } catch(e) {}
    }

    cachedData = {
      customers: customers,
      lastFetched: new Date().toISOString(),
      crmSync: crmSync,
    };
    console.log(`  Done: ${customers.length} records`);
    if (crmSync) console.log(`  CRM sync: ${crmSync.matched} matched, last: ${crmSync.sync_time}`);
  } catch (err) {
    console.error('  Refresh failed:', err.message);
  }
  fetchInProgress = false;
}

// ====== MIME ======
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js':   'text/javascript; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
};

// ====== 路由 ======
function handleRequest(req, res) {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const pathname = url.pathname;

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');

  // --- API ---
  if (pathname === '/api/customers') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(cachedData));
    return;
  }

  if (pathname === '/api/refresh') {
    refreshCache();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, lastFetched: cachedData.lastFetched, count1: cachedData.table1.length, count2: cachedData.table2.length }));
    return;
  }

  // --- Static files ---
  let filePath = path.join(__dirname, pathname === '/' ? 'index.html' : pathname);
  const ext = path.extname(filePath);

  fs.readFile(filePath, (err, content) => {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end('Not Found');
      } else {
        res.writeHead(500);
        res.end('Server Error');
      }
      return;
    }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(content);
  });
}

// ====== 启动 ======
// 先拉一次数据
console.log('Initializing data cache...');
refreshCache();

const server = http.createServer(handleRequest);
server.listen(PORT, () => {
  console.log('');
  console.log('======================================');
  console.log(`  CSM 客户看板服务已启动`);
  console.log(`  http://localhost:${PORT}`);
  console.log(`  API: http://localhost:${PORT}/api/customers`);
  console.log(`  刷新: http://localhost:${PORT}/api/refresh`);
  console.log('======================================');
  console.log('');
  console.log(`  缓存数据: ${cachedData.customers.length} 条`);
  console.log(`  最后更新: ${cachedData.lastFetched || '—'}`);
});
