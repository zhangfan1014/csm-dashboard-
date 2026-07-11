#!/usr/bin/env python3
"""
销售易CRM → 飞书多维表格 同步脚本
将CRM客户数据(联系方式、对应销售、地址等)同步到飞书Base

用法: python3 sync-crm-to-feishu.py
"""

import json
import subprocess
import sys
import os

BASE_TOKEN = "GiHGbwaUDaahi3sEPTKcpdrhnze"
TABLE_ID_1 = "tbl1dXvlfb1YmFOW"  # 赵诗怡交接客户

# 字段ID映射 (从飞书Base获取)
# CRM字段 → 飞书Base字段名 → 飞书Base字段ID
FIELD_MAP = {
    "phone":      {"name": "客户联系方式", "id": "fld6ehZ4Oz"},
    "address":    {"name": "拜访地址",      "id": "fld2IuOsNH"},
    "owner":      {"name": "对应销售",      "id": "fldLSqqchy"},
}


def run_lark_cli(args):
    """执行 lark-cli 命令并返回解析后的 JSON"""
    cmd = ["lark-cli"] + args + ["--as", "user", "--format", "json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30000)
        output = result.stdout
        # 移除 lark-cli 的 warn 前缀
        if '{' in output:
            output = output[output.index('{'):]
        return json.loads(output)
    except Exception as e:
        print(f"  [ERROR] lark-cli 执行失败: {e}")
        return None


def get_current_records():
    """获取当前飞书Base的所有记录"""
    result = run_lark_cli([
        "base", "+record-list",
        "--base-token", BASE_TOKEN,
        "--table-id", TABLE_ID_1,
        "--limit", "50"
    ])
    if not result or not result.get("ok"):
        print("  [ERROR] 获取飞书Base记录失败")
        return [], [], []

    data = result["data"]
    records = data.get("data", [])
    fields = data.get("fields", [])
    record_ids = data.get("record_id_list", [])
    return records, fields, record_ids


def update_record(record_id, updates_dict):
    """更新单条记录的多个字段
    updates_dict: 字段名→值的字典, 如 {"客户联系方式": "13800138000", "对应销售": "张三"}
    """
    if not updates_dict:
        return True

    # 如果有中文字段名, 先用字段名(不是字段ID)作为key
    update_json = json.dumps(updates_dict, ensure_ascii=False)

    result = run_lark_cli([
        "base", "+record-upsert",
        "--base-token", BASE_TOKEN,
        "--table-id", TABLE_ID_1,
        "--record-id", record_id,
        "--json", update_json
    ])
    if result and result.get("ok"):
        return True
    return False


def sync():
    print("=" * 50)
    print("CRM → 飞书Base 同步开始")
    print("=" * 50)

    # 1. 读取CRM数据
    crm_path = os.path.join(os.path.dirname(__file__), "crm_accounts.json")
    with open(crm_path, "r") as f:
        crm_accounts = json.load(f)
    print(f"\n[1] 加载CRM客户数据: {len(crm_accounts)} 条")

    # 2. 获取飞书Base当前记录
    records, fields, record_ids = get_current_records()
    print(f"[2] 获取飞书Base记录: {len(record_ids)} 条")

    # 3. 建立名称映射
    name_idx = fields.index("客户名称")
    feishu_name_to_id = {}
    for i, rec in enumerate(records):
        name = rec[name_idx]
        if name and str(name).strip():
            feishu_name_to_id[str(name).strip()] = record_ids[i]

    print(f"[3] 飞书Base有名称的记录: {len(feishu_name_to_id)} 条")

    # 4. 名称模糊匹配
    def normalize(name):
        """标准化名称用于匹配"""
        n = str(name).strip()
        for ch in ["（", "(", "）", ")", " ", "　"]:
            n = n.replace(ch, "")
        return n

    # 飞书Base名称→标准化名称
    feishu_norm = {normalize(k): k for k in feishu_name_to_id.keys()}
    crm_norm = {}

    for acc in crm_accounts:
        norm = normalize(acc["accountName"])
        crm_norm[norm] = acc

    # 匹配
    matched = 0
    unmatched = []

    for norm_name, crm_acc in crm_norm.items():
        if norm_name in feishu_norm:
            matched += 1
            orig_feishu_name = feishu_norm[norm_name]
            record_id = feishu_name_to_id[orig_feishu_name]

            # 构建更新字段 (使用字段名作为key)
            field_updates = {}
            if crm_acc.get("phone"):
                field_updates["客户联系方式"] = crm_acc["phone"]
            if crm_acc.get("address"):
                field_updates["拜访地址"] = crm_acc["address"]
            if crm_acc.get("owner"):
                field_updates["对应销售"] = crm_acc["owner"]

            if field_updates:
                ok = update_record(record_id, field_updates)
                print(f"  {'✓' if ok else '✗'} {crm_acc['accountName'][:20]} → {len(field_updates)} 个字段更新")
        else:
            unmatched.append(crm_acc["accountName"])

    print(f"\n[4] 匹配结果: {matched} 条匹配成功")
    print(f"    未匹配: {len(unmatched)} 条")
    for name in unmatched[:5]:
        print(f"      - {name}")

    # 保存本次同步结果
    result = {
        "sync_time": __import__('datetime').datetime.now().isoformat(),
        "crm_count": len(crm_accounts),
        "feishu_count": len(record_ids),
        "matched": matched,
        "unmatched": len(unmatched),
        "unmatched_names": unmatched[:10]
    }
    result_path = os.path.join(os.path.dirname(__file__), "sync_result.json")
    with open(result_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n[5] 同步完成! 结果已保存至: sync_result.json")
    print(f"    lastFetched: {result['sync_time']}")
    return result


if __name__ == "__main__":
    sync()
