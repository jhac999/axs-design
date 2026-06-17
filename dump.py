import re
import json

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_recovered.html', 'r', encoding='utf-8') as f:
    text = f.read()

questions = re.findall(r'<span class="question-text">(.*?)</span>', text)
options = re.findall(r'<label class="option-label"><input type="[^"]+" name="([^"]+)" value="([^"]*)">([^<]*)</label>', text)

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\corrupted_data.json', 'w', encoding='utf-8') as f:
    json.dump({'questions': questions, 'options': options}, f, indent=2, ensure_ascii=False)
print("Done.")
