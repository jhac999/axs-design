import os
import re

TARGET_DIR = r"F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\01_知识资产库"

REPLACEMENTS = [
    (r"飞书审批流模板", "本地 PPT/PDF 决策模板"),
    (r"飞书审批流", "微信落子无悔签批流"),
    (r"飞书审批单", "微信决选单"),
    (r"飞书多维表格的画廊视图", "本地生成的精美图文 PDF"),
    (r"飞书多维表格", "本地极客 H5 表单"),
    (r"飞书机器人自动提醒", "后台 Python 定时监控并微信报警"),
    (r"飞书机器人", "本地 Python 脚本监控"),
    (r"飞书云文档", "本地生成的 16:9 物理 PPTX"),
    (r"飞书幻灯片", "本地生成的 16:9 物理 PPTX"),
    (r"飞书 Webhook", "本地 Python 守护进程监听机制"),
    (r"飞书企业版", "微信与本地轻量化工作流"),
    (r"飞书后台", "本地服务器配置"),
    (r"飞书端", "手机微信端"),
    (r"飞书自动回复", "微信直接发送"),
    (r"飞书通知", "微信通知"),
    (r"【AXS-\d+.*?审批单】", "【AXS 阶段电子签名确认单】"),
    (r"飞书客诉记录", "本地记录库"),
    # Catch-all
    (r"飞书", "本地极客引擎"),
]

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        for pattern, repl in REPLACEMENTS:
            content = re.sub(pattern, repl, content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except UnicodeDecodeError:
        # Ignore binary files or files with non-utf8 encoding that fail parsing
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    modified_count = 0
    file_count = 0
    print(f"[*] Starting Purge in {TARGET_DIR}...")
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.md') or file.endswith('.html'):
                file_count += 1
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    modified_count += 1
                    print(f"[PURGED] {filepath}")
                    
    print(f"\n[*] Purge Complete. Scanned {file_count} files, Modified {modified_count} files.")

if __name__ == "__main__":
    main()
