import os, re

html_file = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

md_lines = []
md_lines.append('---\ntitle: AXS 居住形态深度勘探雷达 (满配级)\ntags: [客户调研, 需求收集, 生活方式, 物理参数, AXS模板]\n---')
md_lines.append('\n# AXS 设计工作室客户需求深度勘探雷达\n')
md_lines.append('> **【系统理念】：所有极致的 实用主义 与 系统化的代码， 最终，都是为了毫无痕迹地服务于您的审美与舒适。**\n')
md_lines.append('> **✨ 主理人致信：**')
md_lines.append('> 这份问卷包含了 36 个关乎您未来每天生活起居的细节，预计需要占用您 15-20 分钟的时间。')
md_lines.append('> 家是包裹疲惫的容器。请放慢脚步，倒一杯茶，跟我们一起，从这里开始描绘那个充满温度的避风港。\n')

module_blocks = html.split('<div class=\"module\">')[1:]
for module in module_blocks:
    module = module.split('</form>')[0]
    
    title_match = re.search(r'<div class=\"module-title\">(.*?)</div>', module)
    if title_match:
        md_lines.append(f'## ▍ {title_match.group(1).strip()}')
    
    questions = module.split('<div class=\"question\">')[1:]
    for q in questions:
        q_text_match = re.search(r'<span class=\"question-text\">(.*?)</span>', q)
        if q_text_match:
            md_lines.append(f'\n**{q_text_match.group(1).strip()}**')
        
        helper_match = re.search(r'<span class=\"helper-text\">(.*?)</span>', q)
        if helper_match:
            md_lines.append(f'> {helper_match.group(1).strip()}')
            
        options = re.findall(r'<label class=\"option-label\">.*?<input type=\"(radio|checkbox)\".*?>\s*(.*?)</label>', q, re.DOTALL)
        if options:
            for opt_type, opt_text in options:
                clean_text = re.sub(r'<input.*?>', '', opt_text).strip()
                prefix = '- [ ]' if opt_type == 'checkbox' else '- ( )'
                md_lines.append(f'{prefix} {clean_text}')
        else:
            placeholder_match = re.search(r'placeholder=\"(.*?)\"', q)
            if placeholder_match:
                ph = placeholder_match.group(1).strip()
                if ph:
                    md_lines.append(f'*(填写处，例：{ph})*')
            md_lines.append('____________________________________________________________________\n')
            
    md_lines.append('\n---\n')

md_content = '\n'.join(md_lines)

out_dir = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS设计工作室_装修管理系统\02_前端触达层'
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, 'AXS_设计工作室客户需求深度调研表.md')

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print('Success! Markdown saved to AXS_设计工作室客户需求深度调研表.md')
