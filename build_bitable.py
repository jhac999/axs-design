import re
import json
import subprocess
import sys

# Parse HTML using regex
with open('AXS_设计工作室客户需求深度调研表_极客终极版.html', 'r', encoding='utf-8') as f:
    html = f.read()

questions = re.findall(r'<div class="question">(.*?)</div>', html, re.DOTALL)

fields = []

# To ensure unique field names
seen_names = set()

for q in questions:
    title_match = re.search(r'<span class="question-text">(.*?)</span>', q)
    if not title_match:
        continue
    
    # Clean up name
    name = title_match.group(1).replace('*', '').strip()
    name = re.sub(r'<[^>]+>', '', name)
    
    # Handle duplicates
    orig_name = name
    counter = 1
    while name in seen_names:
        name = f"{orig_name} ({counter})"
        counter += 1
    seen_names.add(name)
    
    # Determine type
    field_type = "text" # default Text
    property_obj = None
    
    if 'type="file"' in q:
        field_type = "attachment"
    elif 'type="checkbox"' in q:
        field_type = "select"
    elif 'type="radio"' in q:
        field_type = "select"
    elif 'type="date"' in q or 'type="time"' in q:
        field_type = "text"
    
    # Extract options for select
    if field_type == "select":
        options = re.findall(r'<label class="option-label">.*?value="(.*?)".*?</label>', q)
        if options:
            property_obj = [{"name": opt} for opt in options]
            
    field_obj = {
        "name": name,
        "type": field_type
    }
    if property_obj:
        field_obj["options"] = property_obj
        
    fields.append(field_obj)

base_token = "XfSUbWQSkam1hts6KExclg4xn76"
print(f"Using Base Token: {base_token}")

# Fields logic: we replace the default fields.
print(f"Creating table with {len(fields)} fields...")
import os
temp_name = "fields.json"
with open(temp_name, 'w', encoding='utf-8') as tempf:
    json.dump(fields, tempf, ensure_ascii=False)

res = subprocess.run(['lark-cli.cmd', 'base', '+table-create', '--as', 'user', '--base-token', base_token, '--name', 'SurveyData_V3', '--fields', f"@{temp_name}"], capture_output=True, text=True, encoding='utf-8')
if res.returncode != 0:
    print("Failed to create table:")
    print(res.stderr)
    os.remove(temp_name)
    sys.exit(1)

table_data = json.loads(res.stdout)
table_id = table_data['data']['table_id']
print(f"Table ID: {table_id}")
os.remove(temp_name)

# Create Form
print("Creating form view...")
res = subprocess.run(['lark-cli.cmd', 'base', '+form-create', '--as', 'user', '--base-token', base_token, '--table-id', table_id, '--name', 'AXS极客版客户需求在线调研'], capture_output=True, text=True, encoding='utf-8')
if res.returncode != 0:
    print("Failed to create form:")
    print(res.stderr)
    sys.exit(1)

form_data = json.loads(res.stdout)
form_url = form_data['data']['form']['shared_url']

print("\n=== SUCCESS ===")
print(f"Base URL: https://feishu.cn/base/{base_token}")
print(f"Form URL: {form_url}")
