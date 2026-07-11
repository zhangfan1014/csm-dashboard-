#!/usr/bin/env python3
"""从merged_data.json生成Supabase SQL导入脚本"""
import json

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/merged_data.json') as f:
    data = json.load(f)

sql_lines = ["-- ==========================================",
             "-- 导入客户数据（由gen_database.py自动生成）",
             f"-- 共 {len(data)} 条记录",
             "-- ==========================================",
             "",
             "TRUNCATE customers RESTART IDENTITY;",
             ""]

for i, rec in enumerate(data):
    # Compute 经营模式
    owner = rec.get('ownerId-name', '') or rec.get('对应销售', '')
    mode = rec.get('经营模式', '')
    if not mode:
        if '张帆' in owner:
            mode = '独立经营'
        elif owner:
            mode = '联合经营'
        else:
            em = str(rec.get('销售模式', ''))
            mode = '独立经营' if '独立' in em else ('联合经营' if '联合' in em else '')

    # Compute 买断/年费
    contract_type = rec.get('customItem319__c-label', '') or rec.get('买断|年费', '')

    # 提取关键字段
    vals = {
        '客户名称': rec.get('客户名称', ''),
        '客户等级': rec.get('customItem187__c-label', '') or rec.get('客户等级', ''),
        '经营模式': mode,
        '买断年费': contract_type,
        '最近合同到期': (rec.get('expireTime_formatted', '') or rec.get('customItem214__c_formatted', '') or rec.get('最近合同的到期时间', '') or rec.get('合同到期', ''))[:10],
        '最近拜访日期': (rec.get('customItem263__c_formatted', '') or rec.get('customItem264__c_formatted', '') or rec.get('visitLatestTime_formatted', '') or rec.get('拜访日期', ''))[:10],
        '拜访概要': rec.get('comment', '') or rec.get('跟进记录（6月5日）', '') or rec.get('跟进记录（6.26邀约）', '') or rec.get('一句话总结', ''),
        '对应销售': rec.get('ownerId-name', '') or rec.get('对应销售', ''),
    }

    # SQL INSERT
    cols = ', '.join(vals.keys())
    esc = lambda s: "'" + str(s).replace("'", "''") + "'" if s else 'NULL'
    row_vals = ', '.join(esc(v) for v in vals.values())
    sql_lines.append(f"INSERT INTO customers ({cols}) VALUES ({row_vals});")

sql = '\n'.join(sql_lines)

with open('/Users/edy/WorkBuddy/2026-07-10-18-07-45/supabase_data.sql', 'w') as f:
    f.write(sql)

print(f"已生成: supabase_data.sql ({len(sql_lines)} 行, {len(data)} 条)")