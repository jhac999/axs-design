import re

html_file = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

new_css = """
    /* Mascot Characters */
    .mascot {
        position: fixed;
        bottom: -5vh; /* Ground them slightly below the bottom edge */
        width: 600px;
        z-index: 0;
        pointer-events: none;
        mix-blend-mode: screen; 
        opacity: 0.95;
        /* Crush near-black background to absolute black to eliminate the square box */
        filter: contrast(1.3) brightness(0.85);
        /* Soften the edges just in case */
        -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 60%, transparent 100%);
        mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 60%, transparent 100%);
        transform-origin: bottom center;
    }

    .mascot-left {
        left: 2vw;
        animation: walkInPlace 1.4s cubic-bezier(0.4, 0.0, 0.2, 1) infinite;
    }

    .mascot-right {
        right: 2vw;
        animation: walkInPlace 1.5s cubic-bezier(0.4, 0.0, 0.2, 1) infinite 0.7s;
    }

    /* Walking in place animation */
    @keyframes walkInPlace {
        0% { transform: translateY(0) scaleY(1) rotate(0deg); }
        25% { transform: translateY(-20px) scaleY(1.02) rotate(1.5deg); }
        50% { transform: translateY(0) scaleY(1) rotate(0deg); }
        75% { transform: translateY(-20px) scaleY(1.02) rotate(-1.5deg); }
        100% { transform: translateY(0) scaleY(1) rotate(0deg); }
    }

    @media (max-width: 1600px) {
        .mascot { width: 450px; opacity: 0.8; }
    }
    @media (max-width: 1200px) {
        .mascot { width: 350px; opacity: 0.5; }
    }
    @media (max-width: 800px) {
        .mascot { display: none; }
    }
"""

html = re.sub(r'/\* Mascot Characters \*/.*?(?=</style>)', new_css, html, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Mascots grounded, sized to 600px, grey box removed, and walking animation applied!")
