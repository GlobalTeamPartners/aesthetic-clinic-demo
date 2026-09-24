# -*- coding: utf-8 -*-
import os

demo_dir = r"C:\Users\Vlaslav\Agency_HQ\Belgrade_Demo_Sites\Rea_Medika_Demo"

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Aesthetic Clinic | Cinematic Experience</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div id="loading" class="loading-overlay">
    <div class="loader">
        <div class="loader-circle"></div>
        <div class="loader-text">INITIALIZING CINEMATIC EXPERIENCE</div>
        <div class="loader-progress" id="progress-text">0%</div>
    </div>
</div>

<div class="video-container">
    <canvas id="video-canvas"></canvas>
    <div class="overlay"></div>
</div>

<nav>
    <div class="logo">AESTHETICA</div>
    <div class="nav-links">
        <a href="#services">TREATMENTS</a>
        <a href="#doctors">OUR EXPERTS</a>
        <a href="#clinic">THE CLINIC</a>
        <a href="#booking" class="btn-book">BOOK CONSULTATION</a>
    </div>
</nav>

<div class="scroll-container">
    
    <section class="content-section" id="hero">
        <div class="content-block">
            <h1>Art & Science of Beauty</h1>
            <p>Advanced aesthetic medicine in the heart of Belgrade. Discretion, luxury, and world-class results.</p>
            <div class="scroll-indicator">
                <div class="mouse"><div class="wheel"></div></div>
            </div>
        </div>
    </section>

    <section class="content-section" id="services">
        <div class="content-block side-block right">
            <h2>Signature Treatments</h2>
            <div class="card">
                <h3>Non-Surgical Facelift</h3>
                <p>Advanced dermal fillers and collagen stimulators for natural rejuvenation without downtime.</p>
            </div>
            <div class="card">
                <h3>Laser Skin Resurfacing</h3>
                <p>Pico-second laser technology to erase pigmentation, scars, and fine lines.</p>
            </div>
            <div class="card">
                <h3>Body Contouring</h3>
                <p>Non-invasive fat reduction and muscle toning using cutting-edge EMS technology.</p>
            </div>
        </div>
    </section>

    <section class="content-section" id="doctors">
        <div class="content-block side-block left">
            <h2>World-Class Experts</h2>
            <div class="card">
                <p>Our medical team consists of internationally trained plastic surgeons and dermatologists, bringing Beverly Hills and Swiss standards to the Balkans.</p>
                <a href="#booking" class="btn-outline">Meet The Team</a>
            </div>
        </div>
    </section>

    <section class="content-section" id="clinic">
        <div class="content-block">
            <h2>The Private Clinic</h2>
            <p>Designed for absolute privacy and comfort. Our VIP suites ensure your visit is entirely discreet.</p>
        </div>
    </section>

    <section class="content-section" id="booking">
        <div class="content-block">
            <h2>Begin Your Transformation</h2>
            <p>Schedule a private consultation with our head surgeon.</p>
            <form class="booking-form">
                <input type="text" placeholder="Your Name" required>
                <input type="tel" placeholder="WhatsApp Number" required>
                <select>
                    <option>Facial Rejuvenation</option>
                    <option>Body Contouring</option>
                    <option>Dermatology</option>
                    <option>Other / VIP Inquiry</option>
                </select>
                <button type="submit" class="btn-book-large">REQUEST APPOINTMENT</button>
            </form>
        </div>
    </section>

</div>

<script src="app.js"></script>
</body>
</html>"""

css_content = """
:root {
    --gold: #D4AF37;
    --dark: #0F1218;
    --light: #F8F9FA;
    --accent: #E91E63;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body, html {
    height: 100%;
    font-family: 'Inter', sans-serif;
    background-color: var(--dark);
    color: var(--light);
    overflow-x: hidden;
}

h1, h2, h3, .logo { font-family: 'Playfair Display', serif; }

.loading-overlay {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: var(--dark); z-index: 9999;
    display: flex; justify-content: center; align-items: center;
    transition: opacity 1s ease;
}
.loader { text-align: center; }
.loader-circle {
    width: 60px; height: 60px; border: 2px solid rgba(212,175,55,0.2);
    border-top: 2px solid var(--gold); border-radius: 50%;
    animation: spin 1s linear infinite; margin: 0 auto 20px;
}
.loader-text { letter-spacing: 4px; font-size: 12px; color: var(--gold); margin-bottom: 10px; }
.loader-progress { font-family: monospace; font-size: 16px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.video-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; }
canvas { width: 100%; height: 100%; object-fit: cover; }
.overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(rgba(15,18,24,0.4), rgba(15,18,24,0.8)); }

nav {
    position: fixed; top: 0; width: 100%; padding: 30px 50px;
    display: flex; justify-content: space-between; align-items: center;
    z-index: 100; mix-blend-mode: difference;
}
.logo { font-size: 24px; font-weight: 700; letter-spacing: 2px; }
.nav-links a {
    color: var(--light); text-decoration: none; margin-left: 30px;
    font-size: 12px; letter-spacing: 2px; transition: color 0.3s;
}
.nav-links a:hover { color: var(--gold); }
.btn-book { border: 1px solid var(--gold); padding: 10px 20px; border-radius: 4px; }
.btn-book:hover { background: var(--gold); color: var(--dark) !important; }

.content-section {
    min-height: 100vh; display: flex; align-items: center; justify-content: center;
    padding: 0 10%; position: relative;
}
.content-block { text-align: center; max-width: 800px; text-shadow: 0 4px 15px rgba(0,0,0,0.8); }
.side-block { text-align: left; max-width: 500px; }
.side-block.right { margin-left: auto; }
.side-block.left { margin-right: auto; }

h1 { font-size: clamp(40px, 6vw, 80px); margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px; }
h2 { font-size: clamp(30px, 4vw, 50px); margin-bottom: 30px; color: var(--gold); }
p { font-size: 18px; line-height: 1.6; margin-bottom: 30px; }

.card {
    background: rgba(15, 18, 24, 0.6); border-left: 3px solid var(--gold);
    padding: 30px; margin-bottom: 20px; backdrop-filter: blur(10px); border-radius: 0 8px 8px 0;
}
.card h3 { font-size: 24px; margin-bottom: 15px; }
.card p { font-size: 15px; margin-bottom: 0; }

.btn-outline {
    display: inline-block; padding: 12px 30px; border: 1px solid var(--light); color: var(--light);
    text-decoration: none; letter-spacing: 1px; transition: all 0.3s; background: rgba(0,0,0,0.3);
    text-transform: uppercase; font-size: 14px;
}
.btn-outline:hover { background: var(--light); color: var(--dark); }

.btn-book-large {
    width: 100%; padding: 18px; background: var(--gold); color: var(--dark);
    border: none; font-size: 16px; font-weight: bold; letter-spacing: 2px;
    cursor: pointer; transition: background 0.3s; margin-top: 10px;
}
.btn-book-large:hover { background: #fff; }

.booking-form {
    background: rgba(15,18,24,0.8); padding: 40px; border-radius: 8px;
    border-top: 3px solid var(--gold); backdrop-filter: blur(10px);
}
.booking-form input, .booking-form select {
    width: 100%; padding: 15px; margin-bottom: 15px;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    color: white; font-family: 'Inter', sans-serif;
}

.scroll-indicator { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); }
.mouse { width: 30px; height: 50px; border: 2px solid var(--light); border-radius: 15px; position: relative; }
.wheel { width: 4px; height: 8px; background: var(--gold); border-radius: 2px; position: absolute; top: 8px; left: 50%; transform: translateX(-50%); animation: scroll 2s infinite; }
@keyframes scroll { 0% { top: 8px; opacity: 1; } 100% { top: 24px; opacity: 0; } }

@media (max-width: 768px) {
    nav { padding: 20px; }
    .nav-links a { display: none; }
    .nav-links a.btn-book { display: block; font-size: 10px; padding: 8px 15px; }
    .content-section { padding: 0 20px; }
}
"""

js_content = """
const TOTAL_FRAMES = 900;
const LERP = 0.02;
const CONCURRENCY = 48;

let frames = [];
let loadedFrames = 0;
let currentFrame = 1;
let targetFrame = 1;
let canvas = document.getElementById('video-canvas');
let ctx = canvas.getContext('2d');
let isLoading = true;

const isMobile = window.innerWidth <= 768;
const frameFolder = isMobile ? 'frames-mobile' : 'frames-webp';

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (frames[Math.floor(currentFrame)]) drawFrame(Math.floor(currentFrame));
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function updateProgress() {
    loadedFrames++;
    const percent = Math.floor((loadedFrames / TOTAL_FRAMES) * 100);
    document.getElementById('progress-text').innerText = `${percent}%`;
    if (loadedFrames >= TOTAL_FRAMES) {
        setTimeout(() => {
            document.getElementById('loading').style.opacity = '0';
            setTimeout(() => {
                document.getElementById('loading').style.display = 'none';
                isLoading = false;
            }, 1000);
        }, 500);
    }
}

async function loadFrames() {
    let queue = [];
    for (let i = 1; i <= TOTAL_FRAMES; i++) queue.push(i);
    
    async function worker() {
        while (queue.length > 0) {
            let i = queue.shift();
            await new Promise((resolve) => {
                let img = new Image();
                img.onload = () => {
                    frames[i] = img;
                    updateProgress();
                    if (i === 1) drawFrame(1);
                    resolve();
                };
                img.onerror = () => {
                    updateProgress();
                    resolve();
                };
                const frameNum = String(i).padStart(6, '0');
                img.src = `${frameFolder}/frame_${frameNum}.webp`;
            });
        }
    }
    let workers = [];
    for (let i = 0; i < CONCURRENCY; i++) workers.push(worker());
    await Promise.all(workers);
}

function drawFrame(index) {
    if (!frames[index]) return;
    const img = frames[index];
    const scale = Math.max(canvas.width / img.width, canvas.height / img.height);
    const w = img.width * scale;
    const h = img.height * scale;
    const x = (canvas.width - w) / 2;
    const y = (canvas.height - h) / 2;
    
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, x, y, w, h);
}

function render() {
    if (!isLoading) {
        const scrollFraction = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
        let target = Math.max(1, Math.min(TOTAL_FRAMES, Math.floor(scrollFraction * TOTAL_FRAMES) + 1));
        targetFrame += (target - targetFrame) * LERP;
        const frameToDraw = Math.round(targetFrame);
        if (frames[frameToDraw]) drawFrame(frameToDraw);
    }
    requestAnimationFrame(render);
}
loadFrames();
render();
"""

with open(os.path.join(demo_dir, "index.html"), "w", encoding="utf-8") as f: f.write(html_content)
with open(os.path.join(demo_dir, "style.css"), "w", encoding="utf-8") as f: f.write(css_content)
with open(os.path.join(demo_dir, "app.js"), "w", encoding="utf-8") as f: f.write(js_content)
print("Demo generated!")
