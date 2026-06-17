import base64
import os
import re

html_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\阿仙森的家\阿仙森_最终图文提案演示.html'
out_path = r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\阿仙森的家\阿仙森_全内置单文件版.html'
dir_name = os.path.dirname(html_path)

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

def replacer(match):
    src = match.group(1)
    if src.startswith('data:') or src.startswith('http'):
        return match.group(0)
    
    img_path = os.path.join(dir_name, src)
    if os.path.exists(img_path):
        with open(img_path, 'rb') as img_f:
            b64 = base64.b64encode(img_f.read()).decode('utf-8')
        
        ext = os.path.splitext(src)[1].lower().replace('.', '')
        if ext == 'jpg': ext = 'jpeg'
        if not ext: ext = 'png'
        
        new_src = f'data:image/{ext};base64,{b64}'
        return match.group(0).replace(src, new_src)
    return match.group(0)

new_html = re.sub(r'<img[^>]+src=[\"\']([^\"\']+)[\"\']', replacer, html)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Done.')
