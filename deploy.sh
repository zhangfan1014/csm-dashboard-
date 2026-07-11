#!/bin/bash
# ============================
# 一键推送到 GitHub
# ============================
# 用法: 打开终端，复制粘贴以下命令执行

cd /Users/edy/WorkBuddy/2026-07-10-18-07-45

# 如果第一次推送，执行这4行：
git init
git add index.html api/customers.js vercel.json .gitignore README.md
git commit -m "init: CSM客户看板"
git remote add origin https://github.com/zhangfan1014/csm-dashboard-.git

# 推送（首次需输入GitHub账号密码，或使用token）
git branch -M main
git push -u origin main

echo ""
echo "=== 推送完成 ==="
echo "仓库: https://github.com/zhangfan1014/csm-dashboard-"
echo ""
echo "下一步: 去 https://vercel.com/import 导入这个仓库"
