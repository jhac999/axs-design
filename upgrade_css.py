import re

css_block = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

    :root {
        --bg-color: #050505;
        --panel-bg: rgba(18, 18, 18, 0.65);
        --panel-border: rgba(212, 175, 55, 0.15);
        --text-main: #e0e0e0;
        --text-muted: #888888;
        --accent: #d4af37; /* AXS 极客金 */
        --accent-glow: rgba(212, 175, 55, 0.4);
        --danger: #e84118;
        --glass-blur: blur(16px);
    }

    * {
        box-sizing: border-box;
    }

    body {
        background-color: var(--bg-color);
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(212, 175, 55, 0.03), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(212, 175, 55, 0.04), transparent 25%);
        background-attachment: fixed;
        color: var(--text-main);
        font-family: 'Outfit', 'Noto Sans SC', sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 0;
        -webkit-font-smoothing: antialiased;
    }

    .container {
        max-width: 900px;
        margin: 0 auto;
        padding: 60px 20px;
    }

    .header {
        text-align: center;
        margin-bottom: 60px;
        position: relative;
    }

    .header::after {
        content: '';
        display: block;
        width: 60px;
        height: 2px;
        background: var(--accent);
        margin: 30px auto 0;
        box-shadow: 0 0 10px var(--accent-glow);
    }

    .slogan {
        color: var(--accent);
        font-size: 0.9em;
        font-weight: 800;
        letter-spacing: 4px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }

    .header h1 {
        color: #ffffff;
        font-size: 2.8em;
        letter-spacing: 2px;
        margin-bottom: 15px;
        font-weight: 800;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }

    .header p {
        color: var(--text-muted);
        font-size: 1.05em;
        font-weight: 300;
    }

    .warm-box {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid var(--panel-border);
        border-left: 4px solid var(--accent);
        padding: 20px 25px;
        margin-bottom: 50px;
        color: #d1d1d1;
        font-size: 0.95em;
        border-radius: 8px;
        backdrop-filter: var(--glass-blur);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }

    .module {
        background: var(--panel-bg);
        padding: 40px;
        margin-bottom: 40px;
        border-radius: 12px;
        border: 1px solid var(--panel-border);
        backdrop-filter: var(--glass-blur);
        -webkit-backdrop-filter: var(--glass-blur);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.02);
        transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease, border-color 0.4s ease;
    }

    .module:hover {
        transform: translateY(-3px);
        border-color: rgba(212, 175, 55, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3), 0 0 20px rgba(212, 175, 55, 0.05);
    }

    .module-badge {
        display: inline-block;
        font-size: 0.75em;
        background: var(--accent);
        color: #000;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 15px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
    }

    .module-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 30px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    .question {
        margin-bottom: 35px;
    }

    .question:last-child {
        margin-bottom: 0;
    }

    .question-text {
        font-size: 1.1em;
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
        color: #ffffff;
    }

    .helper-text {
        display: block;
        font-size: 0.85em;
        color: var(--text-muted);
        margin-bottom: 15px;
        font-weight: 300;
    }

    input[type="text"], input[type="number"], input[type="date"], input[type="time"], input[type="file"], textarea {
        width: 100%;
        padding: 14px 18px;
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255,255,255,0.1);
        color: white;
        border-radius: 6px;
        font-family: inherit;
        font-size: 1em;
        transition: all 0.3s ease;
    }

    input[type="text"]:focus, input[type="number"]:focus, input[type="date"]:focus, input[type="time"]:focus, textarea:focus {
        outline: none;
        border-color: var(--accent);
        background: rgba(0, 0, 0, 0.5);
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.15);
    }

    textarea {
        resize: vertical;
        min-height: 100px;
    }

    .options-group {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 12px;
    }

    .option-label {
        display: flex;
        align-items: center;
        cursor: pointer;
        padding: 14px 18px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 6px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .option-label:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(255,255,255,0.1);
    }

    .option-label:has(input:checked) {
        background: rgba(212, 175, 55, 0.08);
        border-color: var(--accent);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* Custom Checkbox/Radio Styling */
    .option-label input[type="radio"],
    .option-label input[type="checkbox"] {
        appearance: none;
        -webkit-appearance: none;
        width: 18px;
        height: 18px;
        border: 2px solid var(--text-muted);
        margin-right: 12px;
        outline: none;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        flex-shrink: 0;
    }

    .option-label input[type="radio"] {
        border-radius: 50%;
    }
    .option-label input[type="checkbox"] {
        border-radius: 4px;
    }

    .option-label input:checked {
        border-color: var(--accent);
    }

    .option-label input[type="radio"]:checked::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--accent);
        box-shadow: 0 0 5px var(--accent-glow);
    }

    .option-label input[type="checkbox"]:checked::after {
        content: '\\2713';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: var(--accent);
        font-size: 14px;
        font-weight: bold;
        text-shadow: 0 0 5px var(--accent-glow);
    }

    .option-label .other-text {
        flex: 1;
        min-width: 120px;
        margin: 0 0 0 10px;
        padding: 4px 8px;
        background: transparent;
        border: none;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        border-radius: 0;
    }
    
    .option-label .other-text:focus {
        border-bottom-color: var(--accent);
        box-shadow: none;
    }

    .submit-btn {
        background: var(--accent);
        color: #000;
        border: 1px solid var(--accent);
        padding: 18px 30px;
        font-size: 1.1em;
        font-family: 'Outfit', 'Noto Sans SC', sans-serif;
        font-weight: 800;
        cursor: pointer;
        width: 100%;
        border-radius: 6px;
        transition: all 0.3s ease;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }

    .submit-btn::before {
        content: '';
        position: absolute;
        top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }

    .submit-btn:hover::before {
        left: 100%;
    }

    .submit-btn:hover {
        background: #ebd076;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        transform: translateY(-2px);
    }

    /* Primary vs Secondary button logic handled inline, but we can enhance it here */
    #savePageBtn {
        background: rgba(20, 20, 20, 0.8) !important;
        color: var(--accent) !important;
    }
    #savePageBtn:hover {
        background: rgba(212, 175, 55, 0.1) !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }

    .result-panel {
        display: none;
        background: rgba(10, 10, 10, 0.8);
        border: 1px solid var(--accent);
        border-radius: 8px;
        padding: 30px;
        margin-top: 40px;
        backdrop-filter: var(--glass-blur);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }

    .result-panel.is-visible {
        display: block;
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .result-actions {
        display: flex;
        gap: 12px;
        margin: 18px 0;
    }

    .action-btn {
        background: transparent;
        border: 1px solid var(--accent);
        color: var(--accent);
        padding: 10px 20px;
        border-radius: 4px;
        cursor: pointer;
        font-weight: 700;
        font-family: inherit;
        transition: all 0.3s ease;
    }

    .action-btn:hover {
        background: rgba(212, 175, 55, 0.15);
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
    }

    .report-output {
        width: 100%;
        min-height: 420px;
        background: #000;
        color: #00ff41; /* Hacker terminal green for geeky feel */
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 6px;
    }
    
    /* Responsive Adjustments */
    @media (max-width: 600px) {
        .options-group {
            grid-template-columns: 1fr;
        }
        .header h1 {
            font-size: 2em;
        }
    }
</style>
"""

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace existing style block with the new one
new_html = re.sub(r'<style>.*?</style>', css_block, html, flags=re.DOTALL)

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("CSS Upgraded successfully!")
