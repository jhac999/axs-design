import re

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_最终完美版.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS for extreme aesthetics
css_additions = """
    /* EXTREME AESTHETICS OVERRIDES */
    
    /* 1. Custom Cursor */
    body {
        cursor: none;
    }
    a, button, input, label, textarea {
        cursor: none !important;
    }

    #custom-cursor-dot {
        position: fixed;
        top: 0; left: 0;
        width: 8px; height: 8px;
        background: var(--accent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transform: translate(-50%, -50%);
        box-shadow: 0 0 10px var(--accent);
        transition: width 0.2s, height 0.2s;
    }

    #custom-cursor-ring {
        position: fixed;
        top: 0; left: 0;
        width: 32px; height: 32px;
        border: 1px solid rgba(212, 175, 55, 0.5);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9998;
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s, border-color 0.3s, transform 0.1s ease-out;
    }

    .cursor-hover #custom-cursor-dot {
        width: 0; height: 0;
    }

    .cursor-hover #custom-cursor-ring {
        width: 48px; height: 48px;
        border-color: var(--accent);
        background: rgba(212, 175, 55, 0.1);
        backdrop-filter: blur(2px);
    }

    /* 2. Grain Overlay */
    .grain-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none;
        z-index: 9000;
        opacity: 0.04;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
    }

    /* 3. Cyber-Grid Distortion */
    .cyber-grid {
        position: fixed;
        bottom: -20vh;
        left: -50vw;
        width: 200vw;
        height: 60vh;
        background-image: 
            linear-gradient(rgba(212, 175, 55, 0.2) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.2) 1px, transparent 1px);
        background-size: 40px 40px;
        transform: perspective(600px) rotateX(75deg);
        transform-origin: top;
        z-index: -1;
        pointer-events: none;
        animation: gridMove 10s linear infinite;
        mask-image: linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0));
        -webkit-mask-image: linear-gradient(to top, rgba(0,0,0,1), rgba(0,0,0,0));
    }

    @keyframes gridMove {
        0% { transform: perspective(600px) rotateX(75deg) translateY(0); }
        100% { transform: perspective(600px) rotateX(75deg) translateY(40px); }
    }

    /* 4. Dramatic Shadows & Depth */
    .module {
        background: rgba(12, 12, 12, 0.7);
        border: 1px solid rgba(212, 175, 55, 0.2);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.9),
            0 0 40px rgba(212, 175, 55, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        opacity: 0;
        transform: translateY(40px) scale(0.98);
        transition: opacity 0.8s cubic-bezier(0.165, 0.84, 0.44, 1), transform 0.8s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
    }

    .module.reveal-visible {
        opacity: 1;
        transform: translateY(0) scale(1);
    }

    .module:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 
            0 40px 80px rgba(0, 0, 0, 1),
            0 0 60px rgba(212, 175, 55, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border-color: rgba(212, 175, 55, 0.5);
    }
    
    .header h1 {
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.3), 0 5px 15px rgba(0,0,0,0.8);
        letter-spacing: 4px;
    }
"""

js_additions = """
<!-- Extreme UI Elements -->
<div class="grain-overlay"></div>
<div class="cyber-grid"></div>
<div id="custom-cursor-dot"></div>
<div id="custom-cursor-ring"></div>

<script>
    // 1. Custom Cursor Logic
    const cursorDot = document.getElementById('custom-cursor-dot');
    const cursorRing = document.getElementById('custom-cursor-ring');
    
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let ringX = mouseX;
    let ringY = mouseY;
    
    window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursorDot.style.left = `${mouseX}px`;
        cursorDot.style.top = `${mouseY}px`;
    });
    
    // Smooth trailing effect for ring
    function renderCursor() {
        ringX += (mouseX - ringX) * 0.15;
        ringY += (mouseY - ringY) * 0.15;
        cursorRing.style.left = `${ringX}px`;
        cursorRing.style.top = `${ringY}px`;
        requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);

    // Hover states for cursor
    const hoverElements = document.querySelectorAll('input, label, button, textarea, a');
    hoverElements.forEach(el => {
        el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
        el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
    });

    // 2. Staggered Reveals (Intersection Observer)
    const modules = document.querySelectorAll('.module, .warm-box');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-visible');
                // Optional: stop observing once revealed
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    });

    modules.forEach((mod, index) => {
        // Add staggered transition delay based on index for initial load
        mod.style.transitionDelay = `${index * 0.05}s`;
        observer.observe(mod);
    });
    
    // Remove delay after initial reveal so hover effects are instant
    setTimeout(() => {
        modules.forEach(mod => mod.style.transitionDelay = '0s');
    }, 2000);
</script>
"""

# Insert CSS
if '</style>' in html:
    html = html.replace('</style>', css_additions + '\n</style>')

# Insert JS before script block or before body
if '<script>' in html:
    html = html.replace('<script>', js_additions + '\n<script>', 1)
elif '</body>' in html:
    html = html.replace('</body>', js_additions + '\n</body>')

with open(r'F:\吉胡阿川\01lhjk\事业\AXS设计工作室\AXS_设计工作室客户需求深度调研表_极客终极版.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Extreme effects applied and saved to AXS_设计工作室客户需求深度调研表_极客终极版.html")
