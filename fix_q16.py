import os
import re
import subprocess
import json
import time

os.environ['PYTHONIOENCODING'] = 'utf-8'

# 1. Update Feishu backend
opts = ['纯粹用于一日三餐', '经常兼作办公/看书/学习台', '需要辅导孩子写作业', '会客喝茶、聚会聊天', '烘焙/手工等扩展操作台', '经常堆放杂物/快递（临时存放区）']

payload = {
    "name": "16. 餐桌的真实使用场景（按高低频排序）？",
    "type": "select",
    "multiple": True,
    "options": [{"name": o} for o in opts]
}

print("Updating Feishu field fldCecQp0M...")
cmd = [
    'lark-cli.cmd', 'base', '+field-update', 
    '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', 
    '--table-id', 'tbl4v3hKKewsxwwu', 
    '--field-id', 'fldCecQp0M', 
    '--json', json.dumps(payload, ensure_ascii=False),
    '--yes'
]
res = subprocess.run(cmd, capture_output=True, env=os.environ)
print("Feishu update result:", res.returncode)
if res.returncode != 0:
    print(res.stderr.decode('utf-8', errors='ignore'))

time.sleep(1)

# Refresh live_fields.json
print("Fetching latest fields...")
subprocess.run([
    'lark-cli.cmd', 'base', '+field-list', 
    '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', 
    '--table-id', 'tbl4v3hKKewsxwwu', 
    '--format', 'json'
], stdout=open('live_fields.json', 'wb'), env=os.environ)

# 2. Update HTML files
def build_opts(opts, name):
    html = '                <div class="options-group">\n'
    for o in opts:
        html += f'                    <label class="option-label"><input type="checkbox" name="{name}" value="{o}"> {o}</label>\n'
    html += '                </div>\n'
    html += f'                <textarea name="{name}_supplement" placeholder="其它补充说明（选填）" style="margin-top: 10px;"></textarea>'
    return html

files = [
    r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html',
    r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html'
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Q16 is currently an input text
    q16_block = re.search(r'(<span class="question-text">16\..*?</span>\s*)<input type="text"[^>]*name="([^"]+)"[^>]*>', html, re.DOTALL)
    if q16_block:
        new_html = q16_block.group(1) + build_opts(opts, q16_block.group(2))
        html = html.replace(q16_block.group(0), new_html)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Updated {fpath}")
    else:
        print(f"Could not find Q16 input in {fpath}")

# 3. Update Markdown
print("Regenerating Markdown...")
subprocess.run(['python', 'generate_md_survey.py'], env=os.environ)

print("All done!")
