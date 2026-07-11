#!/usr/bin/env python3
import json

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/merged_data.json') as f:
    data = json.load(f)

# Stats
all_c = data
total = len(all_c)
visited = sum(1 for c in all_c if '是' in str(c.get('是否已拜访','')))
unvisited = total - visited
indep = sum(1 for c in all_c if '独立' in str(c.get('销售模式','')))
joint = sum(1 for c in all_c if '联合' in str(c.get('销售模式','')))
annual = sum(1 for c in all_c if '年费' in str(c.get('买断|年费','')))
buyout = sum(1 for c in all_c if '买断' in str(c.get('买断|年费','')))

levels = {}
for c in all_c:
    lv = c.get('客户等级','')
    if lv: levels[lv] = levels.get(lv,0)+1
level_html = ''.join(f'<span><b>{k}</b>: {v}家</span>' for k,v in sorted(levels.items(), key=lambda x:-x[1]))

data_json = json.dumps(data, ensure_ascii=False)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CSM 客户全景看板</title>
<style>
:root{{--bg:#f5f7fa;--card:#fff;--text:#1a1a2e;--text2:#555770;--text3:#8e90a6;--border:rgba(0,0,0,0.06);--g1:linear-gradient(135deg,#1d4ed8,#3b82f6);--g2:linear-gradient(135deg,#f093fb,#f5576c);--g3:linear-gradient(135deg,#06b6d4,#22d3ee);--g4:linear-gradient(135deg,#10b981,#34d399);--accent:#2563eb;--font:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;--r:12px}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font);background:var(--bg);color:var(--text);min-height:100vh}}
.hero{{text-align:center;padding:40px 24px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,#1d4ed8 0%,#3b82f6 50%,#06b6d4 100%);opacity:0.05}}
.hero h1{{font-size:28px;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px}}
.hero p{{color:var(--text2);font-size:14px}}
.container{{max-width:1200px;margin:0 auto;padding:0 24px}}
.section{{padding:28px 0}}
.stitle{{font-size:20px;font-weight:700;padding-left:18px;position:relative;margin-bottom:20px}}
.stitle::before{{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);width:4px;height:22px;background:var(--g1);border-radius:2px}}
.stitle .sub{{font-size:13px;font-weight:400;color:var(--text3);margin-left:10px}}
.grid4{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
.grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:20px}}
@media(max-width:768px){{.grid4,.grid2{{grid-template-columns:1fr}}}}
.kpi{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;position:relative;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--g1)}}
.kpi.a2::before{{background:var(--g2)}}.kpi.a3::before{{background:var(--g3)}}.kpi.a4::before{{background:var(--g4)}}
.kl{{font-size:12px;color:var(--text3);margin-bottom:6px;letter-spacing:0.5px}}
.kv{{font-size:28px;font-weight:800;background:var(--g1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.2}}
.gt2{{background:var(--g2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.stat-row{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}}
.stat-item{{font-size:13px;color:var(--text2)}}
.stat-item b{{color:var(--text)}}
.psection{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:24px;box-shadow:0 2px 8px rgba(0,0,0,0.04)}}
.sbar{{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;align-items:center}}
.sbar input{{flex:1;min-width:180px;padding:10px 14px;border:1px solid #e8ecf1;border-radius:8px;font-size:14px;outline:none}}
.sbar input:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(37,99,235,0.1)}}
.sbar select{{padding:10px 14px;border:1px solid #e8ecf1;border-radius:8px;font-size:13px;cursor:pointer}}
.cgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}}
.cc{{background:var(--bg);border:1px solid var(--border);border-radius:var(--r);padding:18px;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s}}
.cc:hover{{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,0.08)}}
.cc-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px}}
.cn{{font-size:15px;font-weight:600;color:var(--text)}}
.c-tags{{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:8px}}
.tag{{display:inline-flex;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:500}}
.tag-lv{{background:rgba(37,99,235,0.1);color:#2563eb}}
.tag-op{{background:rgba(245,158,11,0.1);color:#b45309}}
.tag-yn{{background:rgba(16,185,129,0.1);color:#059669}}
.tag-nn{{background:rgba(239,68,68,0.1);color:#ef4444}}
.c-info{{display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px;color:var(--text2);line-height:1.7}}
.c-info .label{{color:var(--text3)}}
.c-summary{{font-size:13px;color:var(--text2);margin-top:8px;padding-top:8px;border-top:1px solid #e8ecf1;line-height:1.6}}
.c-expand{{display:none;margin-top:10px;padding:12px;background:var(--card);border-radius:8px;font-size:12px;color:var(--text2);line-height:1.8}}
.cc.open .c-expand{{display:block}}
.chart-box{{background:var(--card);border:1px solid var(--border);border-radius:var(--r);padding:20px;box-shadow:0 2px 8px rgba(0,0,0,0.04);height:300px}}
.chart-title{{font-size:15px;font-weight:600;margin-bottom:12px;color:var(--text)}}
.footer{{text-align:center;padding:20px;font-size:12px;color:var(--text3)}}
</style>
</head>
<body>
<div class="hero">
  <h1>CSM 客户全景看板</h1>
  <p>基于飞书多维表格大宽表 · {total}家客户全景视图</p>
  <div class="stat-row" style="justify-content:center;margin-top:16px;gap:24px">
    <span class="stat-item"><b>{total}</b> 家客户</span>
    <span class="stat-item">✅ <b>{visited}</b> 已拜访</span>
    <span class="stat-item">⏳ <b>{unvisited}</b> 待拜访</span>
    <span class="stat-item">💰 <b>{annual}</b> 年费 · <b>{buyout}</b> 买断</span>
  </div>
</div>
<div class="container">
  <section class="section">
    <h2 class="stitle">仪表板 <span class="sub">关键指标 &amp; 数据分布</span></h2>
    <div class="grid4">
      <div class="kpi"><div class="kl">客户总数</div><div class="kv">{total}</div></div>
      <div class="kpi a2"><div class="kl">已拜访</div><div class="kv gt2">{visited}</div></div>
      <div class="kpi a3"><div class="kl">独立经营</div><div class="kv" style="background:var(--g3);-webkit-background-clip:text">{indep}</div></div>
      <div class="kpi a4"><div class="kl">联合经营</div><div class="kv" style="background:var(--g4);-webkit-background-clip:text">{joint}</div></div>
    </div>
    <div class="stat-row">{level_html}</div>
    <div class="grid2" style="margin-top:20px">
      <div class="chart-box" id="chartLevel"><div class="chart-title">客户等级分布</div></div>
      <div class="chart-box" id="chartMode"><div class="chart-title">经营模式分布</div></div>
    </div>
  </section>
  <section class="section">
    <h2 class="stitle">客户全景 <span class="sub">全部 {total} 家客户 · 点击查看详情</span></h2>
    <div class="psection">
      <div class="sbar">
        <input type="text" id="q" placeholder="搜索客户名称、行业..." oninput="filter()">
        <select id="fl" onchange="filter()">
          <option value="">全部等级</option>
          <option value="长尾客群">长尾客群</option>
          <option value="腰部客群">腰部客群</option>
          <option value="头部客群">头部客群</option>
        </select>
        <select id="fm" onchange="filter()">
          <option value="">全部模式</option>
          <option value="独立">独立经营</option>
          <option value="联合">联合经营</option>
        </select>
        <select id="fv" onchange="filter()">
          <option value="">全部</option>
          <option value="是">已拜访</option>
          <option value="否">未拜访</option>
        </select>
        <span style="font-size:13px;color:var(--text3)" id="rcnt"></span>
      </div>
      <div class="cgrid" id="list"></div>
    </div>
  </section>
</div>
<div class="footer">数据来源: 飞书多维表格大宽表 · 共 {total} 条 · 独立版（双击即用）</div>

<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<script>
const DATA = {data_json};
let charts={{}};
function render(){ldr();drawCharts()}
function ldr(){var d=DATA;document.getElementById('list').innerHTML=d.map((c,i)=>card(c,i)).join('');document.getElementById('rcnt').textContent='共 '+d.length+' 条'}
function tag(cls,t){return'<span class="tag '+cls+'">'+t+'</span>'}
function v(v,f){{return(v&&String(v).trim())?v:(f||'—')}}
function card(c,i){var t=[];if(c['客户等级'])t.push(tag('tag-lv',c['客户等级']));if(c['销售模式'])t.push(tag('tag-op',String(c['销售模式']).includes('独立')?'独立经营':'联合经营'));if(c['是否已拜访'])t.push(tag(String(c['是否已拜访']).includes('是')?'tag-yn':'tag-nn',String(c['是否已拜访']).includes('是')?'已拜访':'未拜访'));var biz=c['公司业务概况']||c['公司业务情况']||'',ind=biz.length>30?biz.substring(0,30)+'...':biz;var vd=c['拜访日期']||'',vn=c['跟进记录（6月5日）']||c['跟进记录（6.26邀约）']||c['一句话总结']||'',sd=c['首次签约时间']?c['首次签约时间'].substring(0,10):(c['最早签约时间']||'—'),amt=c['合作金额']||c['合同金额']||'—';return'<div class="cc" onclick="this.classList.toggle(\\'open\\')"><div class="cc-top"><div class="cn">'+v(c['客户名称'])+'</div>'+(c['对应销售']?'<span style="font-size:11px;color:var(--text3)">👤 '+c['对应销售']+'</span>':'')+'</div><div class="c-tags">'+t.join('')+'</div><div class="c-info"><span><span class="label">行业</span><br><span class="val">'+(ind||'—')+'</span></span><span><span class="label">签约</span><br><span class="val">'+sd+'</span></span><span><span class="label">金额</span><br><span class="val">'+amt+'</span></span><span><span class="label">拜访日期</span><br><span class="val">'+(vd||'—')+'</span></span></div>'+(vn?'<div class="c-summary">📋 '+v(vn).substring(0,80)+(vn.length>80?'...':'')+'</div>':'')+'<div class="c-expand"><b>公司业务:</b> '+(biz||'—')+'<br><b>拜访地址:</b> '+v(c['拜访地址'])+'<br><b>产品版本:</b> '+v(c['产品版本'])+' '+(c['私有化|分析云']||'')+'<br><b>增值模块:</b> '+v(c['增值模块']||c['具体买的产品'])+'<br><b>对应销售:</b> '+v(c['对应销售'])+' · <b>服务群:</b> '+v(c['服务群'])+'<br>'+(c['跟进记录（6月5日）']?'<b>跟进(6/5):</b> '+c['跟进记录（6月5日）']+'<br>':'')+(c['跟进记录（6.26邀约）']?'<b>跟进(6/26):</b> '+c['跟进记录（6.26邀约）']+'<br>':'')+(c['需求']?'<b>需求:</b> '+c['需求']+'<br>':'')+(c['交接备注']?'<b>交接备注:</b> '+c['交接备注']+'<br>':'')+'<b>具体人物:</b> '+v(c['具体人物']||c['客户主要联系人'])+'</div></div>'}
function drawCharts(){var d=DATA,cm=['#2563eb','#f59e0b','#10b981','#8e90a6'];var lv={};d.forEach(function(c){{var l=c['客户等级']||'未分类';lv[l]=(lv[l]||0)+1}});pie('chartLevel',lv,cm);var md={};d.forEach(function(c){{var m=c['销售模式']||'未知';md[m]=(md[m]||0)+1}});pie('chartMode',md,['#1d4ed8','#06b6d4','#f093fb','#8e90a6'])}
function pie(id,mp,cl){var el=document.getElementById(id);if(!el)return;if(charts[id])charts[id].dispose();var nm=Object.keys(mp),vl=Object.values(mp);if(!nm.length){{el.innerHTML='<div class="chart-title">暂无数据</div>';return}}var ce=echarts.init(el);charts[id]=ce;ce.setOption({{tooltip:{{trigger:'item',formatter:'{b}: {c} ({d}%)'}},series:[{{type:'pie',radius:['35%','65%'],center:['50%','55%'],itemStyle:{{borderRadius:6,borderColor:'#fff',borderWidth:2}},label:{{show:true,formatter:'{b}\\n{d}%',fontSize:11,color:'#555770'}},data:nm.map(function(n,i){{return{{name:n,value:vl[i],itemStyle:{{color:cl[i%cl.length]}}}}}})}}]}})}}
function filter(){{var q=document.getElementById('q').value.trim().toLowerCase(),fl=document.getElementById('fl').value,fm=document.getElementById('fm').value,fv=document.getElementById('fv').value,d=DATA;if(q)d=d.filter(function(c){{return Object.values(c).some(function(v){{return String(v||'').toLowerCase().includes(q)}})}});if(fl)d=d.filter(function(c){{return String(c['客户等级']||'').includes(fl)}});if(fm)d=d.filter(function(c){{return String(c['销售模式']||'').includes(fm)}});if(fv)d=d.filter(function(c){{return String(c['是否已拜访']||'').includes(fv)}});document.getElementById('list').innerHTML=d.map(function(c,i){{return card(c,i)}}).join('');document.getElementById('rcnt').textContent='共 '+d.length+' 条'}}
render();
</script>
</body>
</html>'''

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/dashboard.html','w') as f:
    f.write(html)
print(f'独立版看板已生成 ({len(html)/1024:.0f}KB)')
