import re

perfect = open(r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html', encoding='utf-8').read()
geek = open(r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html', encoding='utf-8').read()

perf_match = re.search(r'(<form id="axsSurveyForm".*?>)(.*?)(</form>)', perfect, re.DOTALL)
geek_match = re.search(r'(<form id="axsSurveyForm".*?>)(.*?)(</form>)', geek, re.DOTALL)

if perf_match and geek_match:
    # Replace the body of geek form with the body of perfect form
    # But wait! Does the submit button group live inside the form body?
    # Yes, usually at the end.
    new_geek = geek.replace(geek_match.group(2), perf_match.group(2))
    
    with open(r'f:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html', 'w', encoding='utf-8') as f:
        f.write(new_geek)
    print("Successfully synced form body to Geek Ultimate Version!")
else:
    print("Form tag not found in one of the files.")
