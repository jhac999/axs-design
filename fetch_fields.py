import os
import subprocess
import json

# Force python and windows to use UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Run the command and capture output
result = subprocess.run(['lark-cli.cmd', 'base', '+field-list', '--base-token', 'XfSUbWQSkam1hts6KExclg4xn76', '--table-id', 'tbl4v3hKKewsxwwu', '--format', 'json'], capture_output=True, env=os.environ)

# The output is likely still cp936 or utf-8, but we will write it raw
with open('fields_perfect.json', 'wb') as f:
    f.write(result.stdout)
