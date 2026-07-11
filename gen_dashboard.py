#!/usr/bin/env python3
import json

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/data_table1.json') as f:
    t1 = json.load(f)
with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/data_table2.json') as f:
    t2 = json.load(f)

all_cust = t1 + t2
visited = sum(1 for c in all_cust if c.get('是否已拜访','否')=='是')
annual = sum(1 for c in all_cust if '年费' in str(c.get('买断|年费','')))
buyout = sum(1 for c in all_cust if '买断' in str(c.get('买断|年费','')))
indep = sum(1 for c in all_cust if '独立' in str(c.get('销售模式','')))
joint = sum(1 for c in all_cust if '联合' in str(c.get('销售模式','')))
levels = {}
for c in all_cust:
    lv = c.get('客户等级','')
    if lv: levels[lv] = levels.get(lv,0)+1

level_html = ''.join(f'<span><b>{k}</b>: {v}家</span>' for k,v in sorted(levels.items(), key=lambda x:-x[1]))

data_json_t1 = json.dumps(t1, ensure_ascii=False)
data_json_t2 = json.dumps(t2, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSM客户看板 - 独立版</title>
<style>
:root {{
  --bg: #f5f7fa; --card: #fff; --text: #1a1a2e; --text2: #555770; --text3: #8e90a6;
  --border: rgba(0,0,0,0.06); --g1: linear-gradient(135deg,#1d4ed8,#3b82f6);
  --g2: linear-gradient(135deg,#f093fb,#f5576c); --g3: linear-gradient(135deg,#06b6d4,#22d3ee);
  --g4: linear-gradient(135deg,#10b981,#34d399); --g5: linear-gradient(135deg,#f59e0b,#fbbf24);
  --accent: #2563eb; --font: -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;
  --r: 12px;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh}}
.hero{{text-align:center;padding:48px 24px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,#1d4ed8 0%,#3b82f6 50%,#06b6d4 100%);opacity:0.06}}
.hero h1{{font-size:32px;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}}
.hero p{{color:var(--text2);font-size:16px;max-width:500px;margin:0 auto}}
.stats{{display:flex;justify-content:center;gap:32px;margin-top:24px;flex-wrap:wrap}}
.stat{{text-align:center}}.stat-v{{font-size:28px;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}.stat-l{{font-size:13px;color:var(--text3);margin-top:4px}}
.container{{max-width:1200px;margin:0 auto;padding:0 24px}}
.s{{padding:32px 0}}
.stitle{{font-size:22px;font-weight:700;padding-left:20px;position:relative;margin-bottom:24px}}
.stitle::before{{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);width:4px;height:24px;background:var(--g1);border-radius:2px}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}}
@media(max-width:768px){{.grid4{{grid-template-columns:1fr}}}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:24px;position:relative;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--g1)}}
.kpi.a2::before{{background:var(--g2)}}.kpi.a3::before{{background:var(--g3)}}.kpi.a4::before{{background:var(--g4)}}
.kl{{font-size:13px;color:var(--text3);margin-bottom:8px}}
.kv{{font-size:28px;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.sbar{{display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap;align-items:center}}
.sbar input{{flex:1;min-width:180px;padding:10px 14px;border:1px solid #e8ecf1;border-radius:8px;font-size:14px;outline:none}}
.sbar input:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,0.1)}}
.sbar select{{padding:10px 14px;border:1px solid #e8ecf1;border-radius:8px;font-size:14px;cursor:pointer}}
.cgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}}
.cc{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.04);cursor:pointer;transition:transform 0.2s,box-shadow 0.2s}}
.cc:hover{{transform:translateY(-3px);box-shadow:0 8px 24px rgba(0,0,0,0.1)}}
.cn{{font-weight:600;margin-bottom:4px}}.cs{{font-size:14px;color:var(--text2);margin-bottom:12px;line-height:1.5}}
.ctags{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}}
.tag{{display:inline-flex;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:500}}
.tp{{background:rgba(37,99,235,0.1);color:#2563eb}}.ts{{background:rgba(16,185,129,0.1);color:#059669}}
.tw{{background:rgba(245,158,11,0.1);color:#b45309}}.td{{background:rgba(239,68,68,0.1);color:#ef4444}}
.cd{{font-size:12px;color:var(--text3);line-height:1.8}}
.cco{{font-size:12px;color:var(--text3);margin-top:8px;padding-top:8px;border-top:1px solid #e8ecf1}}
.cfd{{display:none;margin-top:12px;padding:12px;background:#eef1f5;border-radius:8px;font-size:13px;color:var(--text2);line-height:1.8}}
.cc.open .cfd{{display:block}}
.tab-bar{{display:flex;gap:0;margin-bottom:24px;background:var(--card);border-radius:8px;padding:4px;border:1px solid #e8ecf1;display:inline-flex}}
.tab-item{{padding:8px 20px;font-size:13px;border-radius:6px;cursor:pointer;color:var(--text2);font-weight:500;transition:all 0.2s}}
.tab-item.active{{background:var(--g1);color:white;box-shadow:0 1px 4px rgba(0,0,0,0.1)}}
.footer{{text-align:center;padding:24px;font-size:13px;color:var(--text3)}}
</style>
</head>
<body>

<div class="hero">
  <h1>CSM 客户信息看板</h1>
  <p>基于飞书多维表格 · 赵诗怡 &amp; 星星 交接客户</p>
  <div class="stats">
    <div class="stat"><div class="stat-v">{len(all_cust)}</div><div class="stat-l">客户总数</div></div>
    <div class="stat"><div class="stat-v" style="background:var(--g2);-webkit-background-clip:text">{visited}</div><div class="stat-l">已拜访</div></div>
    <div class="stat"><div class="stat-v" style="background:var(--g3);-webkit-background-clip:text">{annual}</div><div class="stat-l">年费客户</div></div>
    <div class="stat"><div class="stat-v" style="background:var(--g5);-webkit-background-clip:text">{buyout}</div><div class="stat-l">买断客户</div></div>
  </div>
</div>

<div class="container">

  <div class="s"><div class="tab-bar" id="tabBar">
    <div class="tab-item active" data-t="t1">赵诗怡交接客户 ({len(t1)})</div>
    <div class="tab-item" data-t="t2">星星交接客户 ({len(t2)})</div>
  </div></div>

  <div class="s">
    <h2 class="stitle">数据概览</h2>
    <div class="grid4">
      <div class="kpi"><div class="kl">表1 客户数</div><div class="kv">{len(t1)}</div></div>
      <div class="kpi a2"><div class="kl">表2 客户数</div><div class="kv" style="background:var(--g2);-webkit-background-clip:text">{len(t2)}</div></div>
      <div class="kpi a3"><div class="kl">独立经营</div><div class="kv" style="background:var(--g3);-webkit-background-clip:text">{indep}</div></div>
      <div class="kpi a4"><div class="kl">联合经营</div><div class="kv" style="background:var(--g4);-webkit-background-clip:text">{joint}</div></div>
    </div>
    <div style="margin-top:12px;display:flex;gap:12px;flex-wrap:wrap;font-size:13px;color:var(--text2)">
      {level_html}
    </div>
  </div>

  <div class="s"><h2 class="stitle">客户列表</h2>
    <div class="sbar">
      <input type="text" id="q" placeholder="搜索客户名称、行业、联系人..." oninput="filter()">
      <select id="f" onchange="filter()">
        <option value="">全部</option>
        <option value="买断">买断</option>
        <option value="年费">年费</option>
        <option value="独立经营">独立经营</option>
        <option value="联合经营">联合经营</option>
        <option value="长尾客群">长尾客群</option>
      </select>
      <span style="font-size:13px;color:var(--text3)" id="rcnt"></span>
    </div>
    <div class="cgrid" id="list"></div>
  </div>

</div>

<div class="footer">
  数据来源: 飞书多维表格 · 销售易CRM已同步 · 独立版看板（双击即用）
</div>

<script>
const DATA_T1 = {data_json_t1};
const DATA_T2 = {data_json_t2};
let curTab = 't1';
function getData() {{ return curTab === 't1' ? DATA_T1 : DATA_T2; }}
function tag(c,cls,t){{return '<span class="tag '+cls+'">'+t+'</span>'}}
function card1(c){{
  var t='';
  if(c['客户等级']) t+=tag(c,'tp',c['客户等级']);
  if(c['客户类型']) t+=tag(c,'tw',c['客户类型']);
  if(c['买断|年费']) t+=tag(c,c['买断|年费'].includes('年费')?'ts':'td',c['买断|年费']);
  if(c['销售模式']) t+=tag(c,c['销售模式'].includes('独立')?'tp':'tw',c['销售模式']);
  var d=c['首次签约时间']||'';if(d.length>10)d=d.substring(0,10);
  return '<div class="cc" onclick="this.classList.toggle(\\'open\\')">'+
    '<div class="cn">'+(c['客户名称']||'未命名')+'</div>'+
    '<div class="cs">'+(c['一句话总结']||'—')+'</div>'+
    '<div class="ctags">'+t+'</div>'+
    '<div class="cd">&#x1F465; '+(c['公司人数规模']||'—')+' &#x1F4B0; '+(c['合作金额']||'—')+' &#x1F4C5; '+d+'</div>'+
    '<div class="cco">&#x1F4DE; '+(c['客户联系方式']||'—')+' &#x1F464; '+(c['客户联系人']||'—')+' &#x1F4E7; KP: '+((c['KP联系方式']||'').substring(0,20)||'—')+'</div>'+
    '<div class="cfd">'+
      '<b>公司业务:</b> '+(c['公司业务概况']||'—')+'<br>'+
      '<b>拜访地址:</b> '+(c['拜访地址']||'—')+'<br>'+
      '<b>产品版本:</b> '+(c['产品版本']||'—')+' '+(c['私有化|分析云']||'')+'<br>'+
      '<b>增值模块:</b> '+(c['增值模块']||'—')+'<br>'+
      '<b>对应销售:</b> '+(c['对应销售']||'—')+' <b>服务群:</b> '+(c['服务群']||'—')+'<br>'+
      '<b>最近合同到期:</b> '+(c['最近合同的到期时间']||'—')+'<br>'+
      '<b>跟进记录:</b> '+(c['跟进记录（6月5日）']||'—')+'<br>'+
      (c['需求']?'<b>需求:</b> '+c['需求']+'<br>':'')+
      '<b>具体人物:</b> '+(c['具体人物']||'—')+' <b>是否已拜访:</b> '+(c['是否已拜访']||'—')+
    '</div></div>';
}}
function card2(c){{
  var t='';
  if(c['销售模式']) t+=tag(c,'tp',c['销售模式']);
  if(c['买断|年费']) t+=tag(c,String(c['买断|年费']).includes('年费')?'ts':'td',c['买断|年费']);
  return '<div class="cc" onclick="this.classList.toggle(\\'open\\')">'+
    '<div class="cn">'+(c['客户名称']||'未命名')+'</div>'+
    '<div class="cs">'+(c['一句话总结']||'—')+'</div>'+
    '<div class="ctags">'+t+'</div>'+
    '<div class="cd">&#x1F4B0; '+(c['合同金额']||'—')+' &#x1F4C5; '+(c['最早签约时间']||'—')+'</div>'+
    '<div class="cco">&#x1F464; '+(c['客户主要联系人']||'—')+'</div>'+
    '<div class="cfd">'+
      '<b>公司业务:</b> '+(c['公司业务情况']||'—')+'<br>'+
      '<b>拜访地址:</b> '+(c['拜访地址']||'—')+'<br>'+
      '<b>产品版本:</b> '+(c['产品版本']||'—')+'<br>'+
      '<b>建联情况:</b> '+(c['建联情况']||'—')+'<br>'+
      '<b>交接备注:</b> '+(c['交接备注']||'—')+
    '</div></div>';
}}
function render(){{var d=getData(),list=document.getElementById('list');if(!d||!d.length){{list.innerHTML='<div style="text-align:center;padding:40px;color:var(--text3)">暂无数据</div>';return}}list.innerHTML=d.map(function(c,i){{return (curTab==='t1'?card1(c):card2(c))}}).join('');document.getElementById('rcnt').textContent='共 '+d.length+' 条'}}
function filter(){{var q=document.getElementById('q').value.trim().toLowerCase(),fv=document.getElementById('f').value,d=getData();if(q)d=d.filter(function(c){{return Object.values(c).some(function(v){{return String(v||'').toLowerCase().includes(q)}})}});if(fv)d=d.filter(function(c){{return Object.values(c).some(function(v){{return String(v||'').includes(fv)}})}});var list=document.getElementById('list');if(!d.length)list.innerHTML='<div style="text-align:center;padding:40px;color:var(--text3);grid-column:1/-1">无匹配结果</div>';else list.innerHTML=d.map(function(c,i){{return (curTab==='t1'?card1(c):card2(c))}}).join('');document.getElementById('rcnt').textContent='共 '+d.length+' 条'}}
document.getElementById('tabBar').addEventListener('click',function(e){{var t=e.target.closest('.tab-item');if(!t)return;document.querySelectorAll('.tab-item').forEach(function(x){{x.classList.remove('active')}});t.classList.add('active');curTab=t.dataset.t;document.getElementById('q').value='';render()}});
render();
</script>
</body>
</html>'''

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/dashboard.html','w') as f:
    f.write(html)
print('独立版看板已生成!')
import os
size = os.path.getsize('/Users/edy/WorkBuddy/2026-07-10-18-07-45/dashboard.html')
print(f'文件大小: {size/1024:.0f}KB')
