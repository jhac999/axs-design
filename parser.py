import json
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('AXS_设计工作室客户需求深度调研表_极客终极版.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

fields = []
# The HTML might have various structures for questions. 
# Look for something like fieldsets, form groups, or label+input.
for group in soup.select('.form-group, .question-block, .field-wrapper, fieldset, .mb-4, label'):
    label_elem = group.find('label') if group.name != 'label' else group
    if not label_elem:
        continue
    
    label_text = label_elem.text.strip().replace('*', '').strip()
    
    # Check for input, select, textarea within the same container, or next to it
    inputs = group.find_all(['input', 'select', 'textarea'])
    if not inputs:
        # Check next sibling
        if group.name == 'label':
            next_sib = group.find_next_sibling(['input', 'select', 'textarea'])
            if next_sib:
                inputs = [next_sib]
    
    if not inputs:
        continue
        
    input_type = inputs[0].name
    if input_type == 'input':
        input_type = inputs[0].get('type', 'text')
    
    # Extract options if radio, checkbox or select
    options = []
    if input_type in ['radio', 'checkbox']:
        # They might be in a group, let's find all labels for these inputs
        for inp in inputs:
            parent_lbl = inp.find_parent('label')
            if parent_lbl:
                options.append(parent_lbl.text.strip())
            else:
                next_lbl = inp.find_next_sibling('label')
                if next_lbl:
                    options.append(next_lbl.text.strip())
    elif input_type == 'select':
        for opt in inputs[0].find_all('option'):
            if opt.get('value'):
                options.append(opt.text.strip())
                
    # remove duplicate labels due to loop finding them again
    if not any(f['label'] == label_text for f in fields):
        fields.append({
            'label': label_text,
            'type': input_type,
            'options': options
        })

print(json.dumps(fields, ensure_ascii=False, indent=2))
