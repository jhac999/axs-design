import json
import re
import subprocess
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

print("Fetching latest fields from Feishu...")
# 1. Load Feishu Fields
try:
    with open('live_fields.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except UnicodeDecodeError:
    with open('live_fields.json', 'r', encoding='gbk') as f:
        data = json.load(f)


feishu_fields = data.get('data', {}).get('fields', [])
feishu_map = {}
for f in feishu_fields:
    # Only care about fields that look like questions
    name = f.get('name', '').strip()
    if name and not name.startswith('_'):  # ignore system fields maybe
        feishu_map[name] = f

# 2. Parse HTML
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

html_questions = []
q_matches = re.finditer(r'<span class="question-text">(.*?)</span>(.*?)(?=<div class="question">|$)', html, flags=re.DOTALL)
for m in q_matches:
    q_title = m.group(1).strip()
    q_body = m.group(2)
    # Extract options if any
    opt_matches = re.findall(r'<label class="option-label"><input type="(radio|checkbox)" name="[^"]+" value="([^"]+)">', q_body)
    opts = [o[1] for o in opt_matches]
    
    html_questions.append({
        'title': q_title,
        'options': opts
    })

# 3. Compare
print("--- COMPARISON REPORT ---")
all_matched = True

for hq in html_questions:
    title = hq['title']
    
    # Check if this exact title exists in feishu
    if title not in feishu_map:
        print(f"[MISSING IN FEISHU] HTML has: {title}")
        all_matched = False
        continue
        
    ff = feishu_map[title]
    f_opts = []
    if 'property' in ff and 'options' in ff['property']:
        f_opts = [o['name'] for o in ff['property']['options'] if o['name']]
    elif 'options' in ff:
        f_opts = [o['name'] for o in ff['options'] if o.get('name')]
        
    h_opts_set = set(hq['options'])
    f_opts_set = set(f_opts)
    
    # We ignore "其它" or "其他" because we manually handled it as a textarea in HTML
    h_opts_set.discard("其它")
    h_opts_set.discard("其他")
    f_opts_set.discard("其它")
    f_opts_set.discard("其他")
    
    if h_opts_set != f_opts_set:
        print(f"[OPTION MISMATCH] {title}")
        print(f"  HTML Options  : {sorted(list(h_opts_set))}")
        print(f"  Feishu Options: {sorted(list(f_opts_set))}")
        all_matched = False

print(f"\nTotal HTML Questions Analyzed: {len(html_questions)}")
print(f"Total Feishu Fields Analyzed: {len(feishu_fields)}")
if all_matched:
    print("RESULT: PERFECT MATCH! HTML and Feishu are perfectly synchronized.")
else:
    print("RESULT: DIFFERENCES FOUND. See above.")
