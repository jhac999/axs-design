import json
import base64
import gzip
import re

base_file_path = r'C:\Users\Administrator\Downloads\AXS客户需求深度调研库.base'
html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

with open(base_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Decode snapshot
raw_bytes = gzip.decompress(base64.b64decode(data['gzipSnapshot']))
try:
    snapshot = json.loads(raw_bytes.decode('utf-8'))
except UnicodeDecodeError:
    snapshot = json.loads(raw_bytes.decode('gbk', errors='ignore'))

feishu_fields = {}

# Iterate over all tables in the snapshot
for tbl_data in snapshot:
    if 'schema' in tbl_data and 'data' in tbl_data['schema'] and 'table' in tbl_data['schema']['data']:
        field_map = tbl_data['schema']['data']['table']['fieldMap']
        for fid, field in field_map.items():
            if 'property' in field and 'options' in field['property']:
                opts = [o['name'] for o in field['property']['options'] if o['name']]
                is_multi = field.get('type') == 4 or field.get('property', {}).get('multiple', False)
                clean_name = re.sub(r'[^\w\u4e00-\u9fa5]', '', field['name'])
                if clean_name:
                    feishu_fields[clean_name] = {
                        'original_name': field['name'],
                        'options': opts,
                        'is_multi': is_multi
                    }

print(f"Total choice fields loaded from .base: {len(feishu_fields)}")

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

out_html = ""
i = 0
updated_count = 0
matched_fields = []

while i < len(html):
    q_start = html.find('<div class="question">', i)
    if q_start == -1:
        out_html += html[i:]
        break
        
    out_html += html[i:q_start]
    
    div_count = 1
    j = q_start + len('<div class="question">')
    while div_count > 0 and j < len(html):
        next_open = html.find('<div', j)
        next_close = html.find('</div', j)
        
        if next_close == -1: break
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            j = next_open + 4
        else:
            div_count -= 1
            j = next_close + 6
            
    q_block = html[q_start:j]
    i = j
    
    text_match = re.search(r'<span class="question-text">(.*?)</span>', q_block)
    if not text_match:
        out_html += q_block
        continue
        
    q_text_full = text_match.group(1).strip()
    q_core = re.sub(r'[^\w\u4e00-\u9fa5]', '', q_text_full)
    
    matched_ff = None
    # More robust fuzzy match
    for ff_core, ff_data in feishu_fields.items():
        # Match if significant overlap
        if ff_core in q_core or q_core in ff_core:
            matched_ff = ff_data
            break
            
    if matched_ff and matched_ff['options']:
        name_match = re.search(r'name="([^"]+)"', q_block)
        if name_match:
            input_name = name_match.group(1)
            if input_name.endswith('_supplement'):
                actual_name_match = re.search(r'input type="(radio|checkbox)" name="([^"]+)"', q_block)
                if actual_name_match:
                    input_name = actual_name_match.group(2)
                else:
                    input_name = input_name.replace('_supplement', '')
            
            input_type = "checkbox" if matched_ff['is_multi'] else "radio"
            new_options_html = '                <div class="options-group">\n'
            for opt in matched_ff['options']:
                if opt == "其它" or opt == "其他": continue
                new_options_html += f'                    <label class="option-label"><input type="{input_type}" name="{input_name}" value="{opt}"> {opt}</label>\n'
            new_options_html += '                </div>'
            
            new_q_block = re.sub(
                r'<div class="options-group">.*?</div>', 
                new_options_html, 
                q_block, 
                flags=re.DOTALL
            )
            
            out_html += new_q_block
            updated_count += 1
            matched_fields.append(matched_ff['original_name'])
        else:
            out_html += q_block
    else:
        out_html += q_block

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(out_html)

print(f"HTML successfully updated! Total questions synced: {updated_count}")
# print("Synced:", matched_fields)
