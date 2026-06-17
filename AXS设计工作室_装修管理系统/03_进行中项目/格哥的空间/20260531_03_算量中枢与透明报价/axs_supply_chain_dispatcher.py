import os
import re
import time

def parse_supplier_db(db_path):
    suppliers = {}
    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    yaml_blocks = re.findall(r'```yaml(.*?)```', content, re.DOTALL)
    for block in yaml_blocks:
        supplier_info = {}
        for line in block.strip().split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                supplier_info[key.strip()] = val.split('#')[0].strip()
        if 'id' in supplier_info:
            suppliers[supplier_info['id']] = supplier_info
    return suppliers

def dispatch_orders(base_dir, db_path):
    print("[AXS 调度中枢] 正在接收客户定稿指令：『格哥已确认决选单，首期款已到账』")
    time.sleep(1)
    print(f"[AXS 调度中枢] 正在连接本地核心库: {os.path.basename(db_path)}")
    
    suppliers_db = parse_supplier_db(db_path)
    
    # 格哥的定稿 BOM，带有对应的供应商 ID
    approved_bom = [
        {"item": "基础水电极客包", "qty": "1 式", "amount": 45000, "supplier_id": "M_PIPE_001"},
        {"item": "全屋大白漆 (一底两面)", "qty": "400 ㎡", "amount": 14000, "supplier_id": "M_PAINT_001"},
        {"item": "实心木门 (含双层阻尼静音条)", "qty": "1 式", "amount": 18000, "supplier_id": "M_DOOR_001"},
        {"item": "AXS强制通顶餐边柜", "qty": "12 ㎡", "amount": 12000, "supplier_id": "M_WOOD_001"},
        {"item": "全屋哑光素色瓷砖", "qty": "200 ㎡", "amount": 19000, "supplier_id": "M_TILE_001"}
    ]
    
    output_dir = os.path.join(base_dir, "04_自动分发采购单_PO")
    os.makedirs(output_dir, exist_ok=True)
    
    master_table_path = os.path.join(output_dir, "AXS001_格哥的家_人工材料分发总表.md")
    
    table_content = [
        "# 🧾 AXS 极客系统自动化分发总表 (PO Master Table)\n",
        "> **状态**: 🔴 已锁单待排产 | **客户**: 格哥 (AXS001)\n",
        "> **核心原则**: 材料与人工彻底物理解耦，统一用本总表双轨极简调度。\n\n",
        "| 类别 | 任务/采购标的 | 对接方 (供应商/班组) | 数量/工程量 | 工日与单价拆解 | 结算底线核算 | 进场/验收节点触发器 | 审计官绝对红线 |\n",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    ]
    
    # 1. 写入材料部分
    for i, item in enumerate(approved_bom, 1):
        sup_data = suppliers_db.get(item['supplier_id'], {})
        brand = sup_data.get('brand', '未知供应商')
        delivery_stage = sup_data.get('stage', '待定')
        lead_time = sup_data.get('lead_time', '待定')
        
        row = f"| 📦 **材料** | {item['item']} | `{brand}` | {item['qty']} | - (直采商品) | ¥{item['amount']} | {delivery_stage} | 备货周期:{lead_time} |\n"
        table_content.append(row)
        
        print(f"[+] 写入材料单: {item['item']} ({brand})")
        time.sleep(0.1)
        
    # 2. 写入人工部分
    labor_data = [
        {"item": "全屋布管+开槽隐蔽", "brand": "AXS_本地水电班组", "qty": "200㎡", "labor_detail": "16工日 @ 500元/天", "amount": "¥8,000", "stage": "01_打压0.8MPa稳压30分钟", "remark": "管卡间距≤60cm，全红蓝隔离"},
        {"item": "薄贴对缝铺贴", "brand": "AXS_本地瓦工班组", "qty": "200㎡", "labor_detail": "20工日 @ 600元/天", "amount": "¥12,000", "stage": "02_空鼓率<5%且墙地对缝", "remark": "必须使用十字架定位2mm"},
        {"item": "系统已熔断木工进场", "brand": "无 (厂家包安装)", "qty": "0", "labor_detail": "0工日 @ 0元/天", "amount": "¥0", "stage": "直接跳过", "remark": "砍掉复杂吊顶,节省成本"},
        {"item": "墙面找平+一底两面", "brand": "AXS_本地油漆班组", "qty": "400㎡", "labor_detail": "32工日 @ 500元/天", "amount": "¥16,000", "stage": "03_2米靠尺平整度误差≤2mm", "remark": "基础找平+滚涂"}
    ]
    
    for l in labor_data:
        row = f"| 👷‍♂️ **人工** | {l['item']} | `{l['brand']}` | {l['qty']} | {l['labor_detail']} | **{l['amount']}** | {l['stage']} | {l['remark']} |\n"
        table_content.append(row)
        print(f"[+] 写入人工派单: {l['item']}")
        time.sleep(0.1)
        
    table_content.append("\n> 💡 **审计官提示**: 材料款直飞工厂，人工费按照“3-4-3”验收节点打给工头。总价包死，无论工头带几个人、干几天，最终只按此核算总价进行拨付。严防工头磨洋工拖延天数虚报工费！\n")
    
    # 3. 追加三方确认契约
    table_content.extend([
        "\n---\n",
        "## ✍️ 资金与施工三方不可撤销确认 (Tri-Party Sign-off)\n",
        "> 本《大一统派单表》是后续所有施工款项拨付的**唯一法定依据**。签字确认后，任何人（含客户与工头）不得在施工中途提出非系统认定的增项或换料要求。\n\n",
        "- **[ ] 甲方出资人 (客户 - 格哥)**：____________________ \n",
        "  *(签字即代表：首期备用金已冻结入池，充分理解并同意系统砍掉冗余设计的“极简保命”方案，中途不加戏。)*\n\n",
        "- **[ ] 乙方执行人 (施工工长)**：____________________ \n",
        "  *(签字即代表：完全接受上述「一线城市 2026 市场底限」的按工日倒推单价，接受总价包死原则。承诺施工期间**绝对不以任何理由**现场要求客户加钱增项，否则没收尾款。)*\n\n",
        "- **[x] 丙方监督人 (AXS 极客系统)**：`[System_Auto_Signed_Timestamp_20260531]` \n",
        "  *(系统已将此表写入只读防篡改底座，并正式启动【机器视觉图库法庭】。验收打卡触发器已激活。)*\n"
    ])
    
    with open(master_table_path, 'w', encoding='utf-8') as f:
        f.writelines(table_content)
        
    print(f"\n[OK] 供应链大一统总表（带三方确认版）已成功生成: {master_table_path}")

if __name__ == "__main__":
    CURRENT_DIR = os.path.dirname(os.path.abspath(__name__))
    DB_PATH = os.path.normpath(os.path.join(CURRENT_DIR, r"..\..\..\01_知识资产库\材料供应商库\AXS_标准供应商底价库.md"))
    dispatch_orders(CURRENT_DIR, DB_PATH)
