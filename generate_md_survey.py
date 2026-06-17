import json
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    with open('live_fields.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except UnicodeDecodeError:
    with open('live_fields.json', 'r', encoding='gbk') as f:
        data = json.load(f)

fields = data.get('data', {}).get('fields', [])

import re

# Filter and sort numbered fields
numbered_fields = []
for f in fields:
    name = f.get('name', '')
    match = re.match(r'^(\d+)\.', name)
    if match:
        try:
            num = int(match.group(1))
            numbered_fields.append((num, f))
        except:
            pass

numbered_fields.sort(key=lambda x: x[0])

md_content = "# AXS 居住形态深度勘探雷达 (32题纯净文本版)\n\n"
md_content += "> 这份问卷包含了 32 个关乎您未来生活细节的问题，它们将成为我们为您构建理想生活的重要基石。\n\n---\n\n"

for num, f in numbered_fields:
    name = f.get('name', '')
    md_content += f"### {name}\n"
    
    # Check options
    f_opts = []
    if 'property' in f and 'options' in f['property']:
        f_opts = [o['name'] for o in f['property']['options'] if o['name']]
    elif 'options' in f:
        f_opts = [o['name'] for o in f['options'] if o.get('name')]
        
    if f_opts:
        is_multi = f.get('property', {}).get('multiple', False) or f.get('multiple', False)
        type_str = "多选" if is_multi else "单选"
        md_content += f"*(【{type_str}】)*\n"
        for opt in f_opts:
            md_content += f"- [ ] {opt}\n"
    else:
        md_content += "*(【填空】)*\n"
        md_content += "__________________________________________________\n"
        
    md_content += "\n"

out_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_纯净文本版.md'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print("Created MD file:", out_path)
