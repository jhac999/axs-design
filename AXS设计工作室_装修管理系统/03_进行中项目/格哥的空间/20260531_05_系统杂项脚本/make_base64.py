import os
import re
import base64

d = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\03_进行中项目\格哥的空间'
f = os.path.join(d, '格哥_汇报演示PPT.html')

html = open(f, 'r', encoding='utf-8').read()

def repl(m):
    img = os.path.join(d, m.group(1))
    b64 = base64.b64encode(open(img, 'rb').read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{b64}"'

html_new = re.sub(r'<img src="\./(.*?\.png)"', repl, html)

open(os.path.join(d, '格哥_全案汇报PPT_微信直发版.html'), 'w', encoding='utf-8').write(html_new)
print("Success!")
