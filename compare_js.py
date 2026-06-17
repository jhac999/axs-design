import re

perfect = open(r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html', encoding='utf-8').read()
geek = open(r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html', encoding='utf-8').read()

print("Perfect has webhook:", 'webhook' in perfect.lower())
print("Geek has webhook:", 'webhook' in geek.lower())

print("Perfect scripts:")
for s in re.findall(r'<script.*?</script>', perfect, re.DOTALL):
    print(len(s), "bytes")

print("Geek scripts:")
for s in re.findall(r'<script.*?</script>', geek, re.DOTALL):
    print(len(s), "bytes")
