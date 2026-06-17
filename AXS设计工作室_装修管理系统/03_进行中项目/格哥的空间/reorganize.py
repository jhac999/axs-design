import os
import shutil

base_dir = r"F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\格哥的空间"

folders = {
    "01": "20260531_01_需求提取与深度推演",
    "02": "20260531_02_工程骨架与概念出图",
    "03": "20260531_03_算量中枢与透明报价",
    "04": "20260531_04_AI巡检与财务阻断引擎",
    "05": "20260531_05_系统杂项脚本"
}

# Create folders
for f in folders.values():
    os.makedirs(os.path.join(base_dir, f), exist_ok=True)

# Mapping files to folders
moves = [
    ("格哥_123.md", "01"),
    ("格哥_123_平面布局出图指令(Prompt).md", "01"),
    ("格哥_01_深度逻辑推演报告.md", "01"),
    ("沙盘演练_格哥200平大平层.md", "01"),
    
    ("axs_cad_bridge.py", "03"),
    ("格哥_02_全案决选与自动报价单.md", "03"),
    
    ("axs_ai_inspector.py", "04"),
    
    ("make_base64.py", "05"),
    ("feishu_api_publisher.py", "05"),
    ("feishu_api_publisher_v2.py", "05"),
    ("格哥_汇报演示PPT.html", "05"),
    ("error.log", "05"),
]

# Move specific files
for filename, folder_key in moves:
    src = os.path.join(base_dir, filename)
    dst = os.path.join(base_dir, folders[folder_key], filename)
    if os.path.exists(src) and not os.path.exists(dst):
        print(f"Moving {filename} to {folders[folder_key]}")
        shutil.move(src, dst)

# Move patterns to 02
for filename in os.listdir(base_dir):
    src = os.path.join(base_dir, filename)
    if os.path.isfile(src):
        if filename.endswith(".lsp") or filename.endswith(".dxf") or filename.endswith(".png") or "汇报蓝图" in filename or "汇报方案" in filename or "extreme_dxf" in filename or "generate_dxf" in filename:
            dst = os.path.join(base_dir, folders["02"], filename)
            if not os.path.exists(dst):
                print(f"Moving {filename} to {folders['02']}")
                shutil.move(src, dst)

print("Reorganization complete.")
