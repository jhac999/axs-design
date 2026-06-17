import re
import os

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'
fields_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\feishu_fields_list.txt'

with open(fields_path, 'r', encoding='utf-8') as f:
    valid_fields = [line.strip() for line in f if line.strip()]

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# We need to find all <div class="question"> blocks.
# We will use a simple state machine to find them accurately because of nested divs.

out_html = ""
i = 0
while i < len(html):
    # Find next question div
    q_start = html.find('<div class="question">', i)
    if q_start == -1:
        out_html += html[i:]
        break
        
    out_html += html[i:q_start]
    
    # Find the end of this div by counting nested divs
    div_count = 1
    j = q_start + len('<div class="question">')
    while div_count > 0 and j < len(html):
        next_open = html.find('<div', j)
        next_close = html.find('</div', j)
        
        if next_close == -1:
            break # Malformed HTML
            
        if next_open != -1 and next_open < next_close:
            div_count += 1
            j = next_open + 4
        else:
            div_count -= 1
            j = next_close + 6 # length of '</div>'
            
    q_block = html[q_start:j]
    i = j
    
    # Process q_block
    # Extract the question text
    text_match = re.search(r'<span class="question-text">(.*?)</span>', q_block)
    if not text_match:
        # Not a standard question block, just keep it
        out_html += q_block
        continue
        
    q_text_full = text_match.group(1).strip()
    
    # Check if this question is in the Feishu valid fields list
    # We will do a relaxed match since Feishu fields might not have the exact same punctuation
    # Just check if the core string is in the valid fields
    
    q_core = re.sub(r'[^\w\u4e00-\u9fa5]', '', q_text_full)
    
    is_valid = False
    for vf in valid_fields:
        vf_core = re.sub(r'[^\w\u4e00-\u9fa5]', '', vf)
        if q_core and (q_core in vf_core or vf_core in q_core):
            is_valid = True
            break
            
    if not is_valid:
        # Question was deleted in Feishu, so we drop this block entirely
        print(f"Removed question: {q_text_full}")
        continue
        
    # If valid, remove the "其它" option inside this block.
    # The option usually looks like:
    # <label class="option-label"><input type="radio" name="pet" value="其它"> 其它 <input type="text" name="pet_other" class="other-text" placeholder="请填写"></label>
    # or <label class="option-label"><input type="checkbox" name="..." value="其它"> 其它 ...</label>
    
    # Remove lines containing 'value="其它"' or '> 其它'
    # We can do line by line processing for the q_block
    q_lines = q_block.split('\n')
    new_q_lines = []
    has_removed_other = False
    
    for line in q_lines:
        if 'value="其它"' in line or '> 其它' in line or '其它 <input' in line:
            has_removed_other = True
            continue # Drop this line
        new_q_lines.append(line)
        
    # If we removed "其它", add a separate text input at the bottom of the question block
    new_q_block = '\n'.join(new_q_lines)
    
    if has_removed_other:
        # Find where the options-group ends to insert the textarea right after
        # or just insert before the final </div> of the question
        insert_idx = new_q_block.rfind('</div>')
        if insert_idx != -1:
            # We want to extract the name attribute from an existing input to generate a good name
            name_match = re.search(r'name="([^"]+)"', new_q_block)
            input_name = name_match.group(1) + "_supplement" if name_match else "supplement"
            
            # Using textarea as requested "单独加一个可以写文字的"
            supplement_html = f'\n    <textarea name="{input_name}" class="supplement-input" placeholder="补充说明（选填）" style="width: 100%; margin-top: 15px; padding: 14px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: white;"></textarea>\n'
            
            new_q_block = new_q_block[:insert_idx] + supplement_html + new_q_block[insert_idx:]
            print(f"Updated question (removed '其它', added text field): {q_text_full}")
            
    out_html += new_q_block

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(out_html)

print("HTML template successfully updated!")
