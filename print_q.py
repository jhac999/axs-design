import re

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

questions = re.findall(r'<span class="question-text">(.*?)</span>', html)
for q in questions:
    print(q)
