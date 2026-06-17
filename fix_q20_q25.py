import re
import json

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# We know the specific options from the report:
# Q20: ['全屋智能', '基础安全防护布局', '舒适生活体验布局', '能源高效管理布局']
# Q25: ['卫生间马桶后方', '厨房炉灶缝隙', '床底', '沙发底部', '衣柜顶部']

q20_opts = ['全屋智能', '基础安全防护布局', '舒适生活体验布局', '能源高效管理布局']
q25_opts = ['卫生间马桶后方', '厨房炉灶缝隙', '床底', '沙发底部', '衣柜顶部']

def build_opts(opts, name):
    html = '                <div class="options-group">\n'
    for o in opts:
        html += f'                    <label class="option-label"><input type="checkbox" name="{name}" value="{o}"> {o}</label>\n'
    html += '                </div>\n'
    html += f'                <textarea name="{name}_supplement" placeholder="补充说明（选填）" style="margin-top: 10px;"></textarea>'
    return html

# Find Q20 block
q20_block = re.search(r'(<span class="question-text">20\..*?</span>\s*<span class="helper-text">.*?</span>\s*)<textarea name="([^"]+)".*?></textarea>', html, re.DOTALL)
if q20_block:
    new_html = q20_block.group(1) + build_opts(q20_opts, q20_block.group(2))
    html = html.replace(q20_block.group(0), new_html)

# Find Q25 block
q25_block = re.search(r'(<span class="question-text">25\..*?</span>\s*<span class="helper-text">.*?</span>\s*)<textarea name="([^"]+)".*?></textarea>', html, re.DOTALL)
if q25_block:
    new_html = q25_block.group(1) + build_opts(q25_opts, q25_block.group(2))
    html = html.replace(q25_block.group(0), new_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed Q20 and Q25.")
