import re

html_file = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

new_css = """
    /* Mascot Characters */
    .mascot {
        position: fixed;
        top: 50%;
        width: 400px;
        z-index: 0;
        pointer-events: none;
        mix-blend-mode: screen; 
        opacity: 0.95;
    }

    .mascot-left {
        left: 2vw;
        animation: floatMascot 4.5s ease-in-out infinite, swayLeft 6s ease-in-out infinite alternate;
    }

    .mascot-right {
        right: 2vw;
        animation: floatMascot 5s ease-in-out infinite reverse, swayRight 7s ease-in-out infinite alternate-reverse;
    }

    @keyframes floatMascot {
        0%, 100% { top: 50%; }
        50% { top: calc(50% - 25px); }
    }

    @keyframes swayLeft {
        0% { transform: translateY(-50%) rotate(-3deg); }
        100% { transform: translateY(-50%) rotate(3deg); }
    }
    
    @keyframes swayRight {
        0% { transform: translateY(-50%) rotate(3deg); }
        100% { transform: translateY(-50%) rotate(-3deg); }
    }

    @media (max-width: 1600px) {
        .mascot { width: 350px; opacity: 0.6; }
    }
    @media (max-width: 1200px) {
        .mascot { width: 250px; opacity: 0.3; }
    }
    @media (max-width: 800px) {
        .mascot { display: none; }
    }
"""

html = re.sub(r'/\* Mascot Characters \*/.*?(?=</style>)', new_css, html, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Mascots adjusted successfully!")
