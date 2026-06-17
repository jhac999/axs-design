import os
import sys
import json
import subprocess
import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ==========================================
# AXS 极客系统 - 问卷数据抓取器
# 功能：从飞书多维表格一键拉取指定客户的调研问卷，并存入对应的项目文件夹中。
# ==========================================

BASE_TOKEN = "XfSUbWQSkam1hts6KExclg4xn76"
TABLE_ID = "tbl4v3hKKewsxwwu"
ROOT_DIR = Path(r"f:\吉胡阿川\01lhjk\事业\AXS设计工作室")
PROJECTS_DIR = ROOT_DIR / "03_进行中项目"

def fetch_records():
    print(f"🔄 正在连接飞书 API 获取数据 (Base: {BASE_TOKEN}, Table: {TABLE_ID})...")
    cmd = f'lark-cli base +record-list --base-token {BASE_TOKEN} --table-id {TABLE_ID} --format json'
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"❌ 飞书 API 调用失败: {result.stderr}")
            sys.exit(1)
        data = json.loads(result.stdout)
        if not data.get("ok"):
            print(f"❌ 接口返回错误: {data.get('error')}")
            sys.exit(1)
        
        # lark-cli returns a matrix format for +record-list
        inner_data = data.get("data", {})
        rows = inner_data.get("data", [])
        fields = inner_data.get("fields", [])
        record_ids = inner_data.get("record_id_list", [])
        
        # Convert matrix to list of dicts
        records = []
        for i, row in enumerate(rows):
            record_fields = {}
            for j, val in enumerate(row):
                if j < len(fields):
                    record_fields[fields[j]] = val
            records.append({
                "id": record_ids[i] if i < len(record_ids) else "N/A",
                "fields": record_fields
            })
        return records
    except Exception as e:
        print(f"❌ 脚本执行异常: {str(e)}")
        sys.exit(1)

def find_customer_record(records, customer_name):
    # 遍历所有记录的所有字段，只要任意一个字段的值包含客户名即判定为命中
    matched_records = []
    for record in records:
        fields = record.get("fields", {})
        for key, value in fields.items():
            if value and customer_name.lower() in str(value).lower():
                matched_records.append(record)
                break
    return matched_records

def format_to_markdown(record, customer_name):
    fields = record.get("fields", {})
    md_content = f"# 📊 AXS客户需求原始数据 - {customer_name}\n\n"
    md_content += f"> **提取时间**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    md_content += f"> **记录 ID**: {record.get('id', 'N/A')}\n\n"
    md_content += "---\n\n"
    
    # 将字段按 key 排序，保证输出的稳定性
    for key, value in sorted(fields.items()):
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict) and "name" in value[0]:
            # 处理多选/单选选项数组
            val_str = "、".join([v.get("name", str(v)) for v in value])
        elif isinstance(value, dict) and "name" in value:
            val_str = value.get("name")
        elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict) and "text" in value[0]:
             # 处理富文本/链接数组
             val_str = "".join([v.get("text", str(v)) for v in value])
        elif isinstance(value, dict) and "text" in value:
             val_str = value.get("text")
        elif isinstance(value, list):
             val_str = "、".join([str(v) for v in value])
        else:
            val_str = str(value)
            
        # 简单清洗
        val_str = val_str.replace('\n', '  \n')
        md_content += f"### {key}\n"
        md_content += f"{val_str}\n\n"
        
    return md_content

def main():
    if len(sys.argv) < 2:
        print("❌ 缺少参数！\n正确用法: python axs_survey_fetcher.py [客户姓名]\n例如: python axs_survey_fetcher.py 阿仙森")
        sys.exit(1)
        
    customer_name = sys.argv[1].strip()
    print(f"🚀 AXS 数据抓取引擎点火，目标客户: 【{customer_name}】")
    
    records = fetch_records()
    print(f"✅ 成功拉取云端数据，共计 {len(records)} 条记录。")
    
    matched = find_customer_record(records, customer_name)
    if not matched:
        print(f"⚠️ 未在飞书表格中搜索到包含【{customer_name}】的数据。请确认客户是否已提交表单，或检查客户填写的名称。")
        sys.exit(0)
        
    # 如果有多条，取最新的一条（假设列表最后的记录最新）
    target_record = matched[-1]
    if len(matched) > 1:
        print(f"⚠️ 发现 {len(matched)} 条匹配记录，已自动为您选择最新提交的一条 (ID: {target_record['id']})。")
        
    md_content = format_to_markdown(target_record, customer_name)
    
    # 构建本地文件夹路径
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    customer_dir = PROJECTS_DIR / customer_name
    target_dir = customer_dir / f"{today_str}_01_需求提取与深度推演"
    
    target_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = target_dir / f"{customer_name}_需求原始数据.md"
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"🎉 抓取成功！数据已降维并存入本地极客引擎。")
        print(f"📂 文件路径: {file_path}")
    except Exception as e:
        print(f"❌ 写入文件失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
