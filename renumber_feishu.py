import json
import re
import subprocess
import time
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

try:
    with open('temp_fields.json', 'r', encoding='utf-16') as f:
        data = json.load(f)
except UnicodeDecodeError:
    with open('temp_fields.json', 'r', encoding='gbk') as f:
        data = json.load(f)

fields = data.get('data', {}).get('fields', [])

numbered_fields = []
for f in fields:
    name = f.get('name', '')
    match = re.match(r'^(\d+)\.\s*(.*)$', name)
    if match:
        old_num = int(match.group(1))
        content = match.group(2)
        numbered_fields.append({
            'field_def': f,
            'old_num': old_num,
            'content': content,
            'original_name': name
        })

numbered_fields.sort(key=lambda x: x['old_num'])
print(f"Found {len(numbered_fields)} numbered fields.")

new_count = 1
for item in numbered_fields:
    new_name = f"{new_count}. {item['content']}"
    if new_name != item['original_name']:
        print(f"Renaming: '{item['original_name']}' -> '{new_name}'")
        
        field_def = item['field_def'].copy()
        field_def['name'] = new_name
        if 'id' in field_def:
            del field_def['id']
        
        json_payload = json.dumps(field_def, ensure_ascii=False)
        
        cmd = [
            'lark-cli.cmd', 'base', '+field-update', 
            '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', 
            '--table-id', 'tbl4v3hKKewsxwwu', 
            '--field-id', item['field_def']['id'], 
            '--json', json_payload,
            '--yes'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, env=os.environ)
            if result.returncode != 0:
                err_text = result.stderr.decode('utf-8', errors='ignore') if result.stderr else "Unknown error"
                print(f"Failed to update {item['field_def']['id']}: {err_text}")
            else:
                print(f"Successfully updated {item['field_def']['id']}.")
        except Exception as e:
            print(f"Exception updating {item['field_def']['id']}: {e}")
            
        time.sleep(0.5)
    
    new_count += 1

print("Renumbering complete!")
