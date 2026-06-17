import os

with open('F:\\吉胡阿川\\01lhjk\\事业\\AXS设计工作室\\AXS_设计工作室客户需求深度调研表_recovered.html', 'rb') as f:
    raw = f.read()

# Let's see the bytes themselves
snippet = raw[15000:15200]
print("Raw bytes:", snippet)

# If it was UTF-8 read as GBK and then saved as UTF-8:
# The original UTF-8 bytes were decoded as GBK strings.
# Then those GBK strings were encoded as UTF-8.
# So to reverse it:
try:
    text = raw.decode('utf-8')
    orig_bytes = text.encode('gbk')
    orig_text = orig_bytes.decode('utf-8')
    print("Reversed (UTF-8 -> GBK bytes -> UTF-8 text):", orig_text[500:800])
except Exception as e:
    print("Failed UTF-8 -> GBK -> UTF-8:", e)

# What if it was GBK read as UTF-8 and saved as GBK?
try:
    text = raw.decode('gbk')
    orig_bytes = text.encode('utf-8')
    orig_text = orig_bytes.decode('gbk')
    print("Reversed (GBK -> UTF-8 bytes -> GBK text):", orig_text[500:800])
except Exception as e:
    print("Failed GBK -> UTF-8 -> GBK:", e)

