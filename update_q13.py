import os
import subprocess
import json
import time

os.environ['PYTHONIOENCODING'] = 'utf-8'

# 1. Update Feishu backend
# The old options for Q13: '马上收拾', '先坐下休息', '先换衣洗手', '先处理孩子/宠物', '经常把东西临时放着', '希望系统帮我降低家务', '其它'
opts = ['马上收拾', '先坐下休息', '先换衣洗手', '先照顾孩子/宠物', '经常把东西临时放着', '希望系统帮我降低家务', '其它']

payload = {
    "name": "13. 下班回家后，您通常是马上开始做家务收拾，还是先瘫一会儿？",
    "type": "select",
    "multiple": True,
    "options": [{"name": o} for o in opts]
}

print("Updating Feishu field fldsVs3iOG...")
cmd = [
    'lark-cli.cmd', 'base', '+field-update', 
    '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', 
    '--table-id', 'tbl4v3hKKewsxwwu', 
    '--field-id', 'fldsVs3iOG', 
    '--json', json.dumps(payload, ensure_ascii=False),
    '--yes'
]
res = subprocess.run(cmd, capture_output=True, env=os.environ)
print("Feishu update result:", res.returncode)

time.sleep(1)

# Refresh live_fields.json
print("Fetching latest fields...")
subprocess.run([
    'lark-cli.cmd', 'base', '+field-list', 
    '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', 
    '--table-id', 'tbl4v3hKKewsxwwu', 
    '--format', 'json'
], stdout=open('live_fields.json', 'wb'), env=os.environ)

# Regenerate Markdown
print("Regenerating Markdown...")
subprocess.run(['python', 'generate_md_survey.py'], env=os.environ)

print("All done!")
