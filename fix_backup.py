import re

with open('F:\\吉胡阿川\\01lhjk\\事业\\AXS设计工作室\\AXS_设计工作室客户需求深度调研表(3).html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove all `required` attributes
text = text.replace(' required>', '>')
text = text.replace(' required ', ' ')
text = text.replace('required>', '>')

# 2. Replace the bottom submit button with two buttons
bottom_ui = '''
        <div style="display: flex; gap: 20px; margin-top: 40px;">
            <button type="button" class="submit-btn" id="savePageBtn" style="flex: 1; background: #1a1a1a; color: #d4af37; border: 1px solid #d4af37;">1: 保存当前页面</button>
            <button type="button" class="submit-btn" id="saveAsBtn" style="flex: 1;">2: 另存为 JSON</button>
        </div>
    </form>
'''
text = re.sub(r'<button type="submit" class="submit-btn".*?</button>\s*</form>', bottom_ui, text, flags=re.DOTALL)

# 3. Replace the script block with the JSON download logic
new_script = '''
    <section id="resultPanel" class="result-panel" aria-live="polite">
        <div class="module-badge">AXS Report</div>
        <div class="module-title">客户需求数据已生成</div>
        <p class="helper-text">JSON 文件已下载，或者您可以在此复制 Markdown 格式。</p>
        <div class="result-actions">
            <button type="button" class="action-btn" id="copyReport">查看/复制 JSON 数据</button>
        </div>
        <textarea id="reportOutput" class="report-output" readonly></textarea>
    </section>
</div>

<script>
    const form = document.getElementById("axsSurveyForm");
    const resultPanel = document.getElementById("resultPanel");
    const reportOutput = document.getElementById("reportOutput");
    
    // 提取表单值并生成 JSON
    function buildReportJSON() {
        const formData = new FormData(form);
        const jsonObj = {};
        for (let [key, value] of formData.entries()) {
            if (value instanceof File) {
                if (!value.name) continue;
                value = value.name;
            }
            if (!jsonObj[key]) {
                jsonObj[key] = value;
            } else {
                if (!Array.isArray(jsonObj[key])) {
                    jsonObj[key] = [jsonObj[key]];
                }
                jsonObj[key].push(value);
            }
        }
        return JSON.stringify(jsonObj, null, 4);
    }

    // 下载 JSON 文件
    function downloadJSON() {
        const jsonStr = buildReportJSON();
        const blob = new Blob([jsonStr], { type: "application/json;charset=utf-8" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        
        const formData = new FormData(form);
        const username = (formData.get("username") || "客户").replace(/[\/\\\\:\\*\\?"<>\\|]/g, "").trim();
        link.download = `AXS_客户调研_${username}_${new Date().toISOString().split("T")[0]}.json`;
        
        link.click();
        URL.revokeObjectURL(link.href);
    }

    // 保存当前页面按钮
    document.getElementById("savePageBtn").addEventListener("click", function() {
        downloadJSON();
        alert("当前页面数据已成功保存为 JSON 文件！");
    });

    // 另存为按钮
    document.getElementById("saveAsBtn").addEventListener("click", function() {
        downloadJSON();
    });

    // 防止默认提交
    form.addEventListener("submit", function (event) {
        event.preventDefault();
    });

    // 查看并复制数据
    document.getElementById("copyReport").addEventListener("click", async function () {
        const jsonStr = buildReportJSON();
        try {
            await navigator.clipboard.writeText(jsonStr);
            this.textContent = "复制成功！";
            setTimeout(() => this.textContent = "查看/复制 JSON 数据", 1800);
        } catch (error) {
            alert("复制失败，请手动复制");
        }
    });
</script>
</body>
</html>
'''

text = re.sub(r'<section id="resultPanel".*$', new_script, text, flags=re.DOTALL)

with open('F:\\吉胡阿川\\01lhjk\\事业\\AXS设计工作室\\AXS_设计工作室客户需求深度调研表_最终完美版.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Done.')
