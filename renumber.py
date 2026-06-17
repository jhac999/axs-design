import re

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

count = 1

def replace_num(match):
    global count
    prefix = match.group(1)
    # The number is match.group(2)
    suffix = match.group(3)
    
    res = f'{prefix}{count}{suffix}'
    count += 1
    return res

# The regex matches <span class="question-text"> followed by digits and a dot.
new_html = re.sub(r'(<span class="question-text">)(\d+)(\.\s*.*?</span>)', replace_num, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Renumbered {count - 1} questions.")
