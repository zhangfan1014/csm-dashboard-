# CSM 客户看板

基于飞书多维表格 + Vercel 部署的客户信息看板。

## 架构

```
销售易CRM → WorkBuddy自动同步 → 飞书Base → Vercel API代理 → HTML前端
```

## 部署步骤

### 1. 飞书后台：创建自建应用（5分钟）

1. 打开 https://open.feishu.cn/app
2. 点击「创建企业自建应用」，名称填 `CSM看板API`
3. 在「权限管理」中搜索并添加以下权限：
   - `bitable:app` （多维表格）
   - 具体权限：`bitable:app:readonly`（只读）
4. 在「凭证与基础信息」中获取 `App ID` 和 `App Secret`
5. 发布应用 -> 联系管理员审批

### 2. Vercel 部署（2分钟）

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. 点击上方按钮，导入本仓库
2. 在环境变量中设置：
   - `FEISHU_APP_ID` = 上一步获取的 App ID
   - `FEISHU_APP_SECRET` = 上一步获取的 App Secret
3. 点击 Deploy

部署完成后，你的看板就上线了！访问 `https://xxx.vercel.app` 即可查看。

### 3. 配置飞书Base权限

在飞书开发者后台：
1. 进入应用 -> 权限管理 -> 添加「多维表格」权限
2. 在「设置」->「应用可用范围」中，添加你的飞书多维表格（Base Token: `GiHGbwaUDaahi3sEPTKcpdrhnze`）
3. 发布新版本 -> 管理员审批

## 本地开发

```bash
# 安装依赖
npm install

# 本地启动
node server.js
# 访问 http://localhost:3456

# 同步销售易CRM数据
python3 sync-crm-to-feishu.py
```

## 数据同步

销售易CRM → 飞书Base 的自动同步由 WorkBuddy 定时任务管理（每周一执行）。
