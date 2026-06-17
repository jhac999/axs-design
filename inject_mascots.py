import shutil
import re

# Copy images
boy_src = r'C:\Users\Administrator\.gemini\antigravity-ide\brain\e82441ad-7632-48cf-ad5f-6da426288496\pro_builder_boy_1780327720154.png'
girl_src = r'C:\Users\Administrator\.gemini\antigravity-ide\brain\e82441ad-7632-48cf-ad5f-6da426288496\pro_designer_girl_1780327734733.png'

boy_dest = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\builder_boy.png'
girl_dest = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\designer_girl.png'

shutil.copyfile(boy_src, boy_dest)
shutil.copyfile(girl_src, girl_dest)

# Inject into HTML
html_file = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Check if mascots are already injected, if not, inject them
if 'class="mascot mascot-left"' not in html:
    css_addition = """
    /* Mascot Characters */
    .mascot {
        position: fixed;
        bottom: 8vh;
        width: 180px;
        z-index: 8000;
        pointer-events: none;
        border-radius: 20px;
        filter: drop-shadow(0 10px 20px rgba(212, 175, 55, 0.3));
        /* The images have a #050505 background, so screen or lighten blends them out perfectly into the dark background */
        mix-blend-mode: screen; 
    }

    .mascot-left {
        left: 4vw;
        animation: floatMascot 3.5s ease-in-out infinite, sway 5s ease-in-out infinite alternate;
    }

    .mascot-right {
        right: 4vw;
        animation: floatMascot 4.2s ease-in-out infinite reverse, sway 6s ease-in-out infinite alternate-reverse;
    }

    @keyframes floatMascot {
        0%, 100% { margin-bottom: 0; }
        50% { margin-bottom: 25px; }
    }

    @keyframes sway {
        0% { transform: rotate(-4deg); }
        100% { transform: rotate(4deg); }
    }

    @media (max-width: 1400px) {
        .mascot { width: 140px; opacity: 0.8; }
    }
    @media (max-width: 1100px) {
        .mascot { width: 100px; opacity: 0.4; }
    }
    @media (max-width: 800px) {
        .mascot { display: none; }
    }
"""

    html_addition = """
<!-- Mascots -->
<img src="./builder_boy.png" class="mascot mascot-left" alt="Builder Boy">
<img src="./designer_girl.png" class="mascot mascot-right" alt="Designer Girl">
"""

    if '</style>' in html:
        html = html.replace('</style>', css_addition + '\n</style>')

    if '</body>' in html:
        html = html.replace('</body>', html_addition + '\n</body>')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Professional Mascots injected successfully!")
