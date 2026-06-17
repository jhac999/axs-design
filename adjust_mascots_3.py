import re

html_file = r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html'

with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

new_css = """
    /* Mascot Characters */
    .mascot {
        position: fixed;
        top: 50%;
        width: 600px;
        z-index: 0;
        pointer-events: none;
        mix-blend-mode: screen; 
        opacity: 0.95;
        filter: contrast(1.3) brightness(0.85);
        -webkit-mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 60%, transparent 100%);
        mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 60%, transparent 100%);
        transform-origin: center center;
    }

    .mascot-left {
        left: 18%; /* Center point is 18% from the left edge */
        animation: walkInPlaceLeft 1.4s cubic-bezier(0.4, 0.0, 0.2, 1) infinite;
    }

    .mascot-right {
        left: 82%; /* Center point is 82% from the left edge */
        animation: walkInPlaceRight 1.5s cubic-bezier(0.4, 0.0, 0.2, 1) infinite 0.7s;
    }

    @keyframes walkInPlaceLeft {
        0% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
        25% { transform: translate(-50%, calc(-50% - 15px)) scaleY(1.02) rotate(1.5deg); }
        50% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
        75% { transform: translate(-50%, calc(-50% - 15px)) scaleY(1.02) rotate(-1.5deg); }
        100% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
    }
    
    @keyframes walkInPlaceRight {
        0% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
        25% { transform: translate(-50%, calc(-50% - 15px)) scaleY(1.02) rotate(1.5deg); }
        50% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
        75% { transform: translate(-50%, calc(-50% - 15px)) scaleY(1.02) rotate(-1.5deg); }
        100% { transform: translate(-50%, -50%) scaleY(1) rotate(0deg); }
    }

    @media (max-width: 1600px) {
        .mascot { width: 500px; opacity: 0.8; }
        .mascot-left { left: 15%; }
        .mascot-right { left: 85%; }
    }
    @media (max-width: 1200px) {
        .mascot { width: 400px; opacity: 0.5; }
    }
    @media (max-width: 800px) {
        .mascot { display: none; }
    }
"""

html = re.sub(r'/\* Mascot Characters \*/.*?(?=</style>)', new_css, html, flags=re.DOTALL)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("Mascots repositioned to exact center vertically and properly padded horizontally!")
