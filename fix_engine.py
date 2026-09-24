# -*- coding: utf-8 -*-
import os

demo_dir = r"C:\Users\Vlaslav\Agency_HQ\Belgrade_Demo_Sites\Rea_Medika_Demo"

# ============================================================
# CORRECT app.js - using the proven Belgrade Waterfront engine
# with TOTAL_FRAMES=900 (actual frame count)
# ============================================================
app_js = """// Aesthetic Clinic - Cinematic Scroll Engine (Fixed)
const TOTAL_FRAMES = 900;
const LERP = 0.02;
const CONCURRENCY = 24;

const isMobile = /Mobi|Android|iPhone/i.test(navigator.userAgent) || innerWidth < 768;
const FRAME_DIR = isMobile ? 'frames-mobile' : 'frames-webp';

const canvas = document.getElementById('gl-canvas');
const ctx = canvas.getContext('2d');
let canvasDpr = 1;

function resize() {
  canvasDpr = Math.min(devicePixelRatio || 1, isMobile ? 1.5 : 2);
  canvas.width = innerWidth * canvasDpr;
  canvas.height = innerHeight * canvasDpr;
  canvas.style.width = innerWidth + 'px';
  canvas.style.height = innerHeight + 'px';
  ctx.setTransform(canvasDpr, 0, 0, canvasDpr, 0, 0);
}
window.addEventListener('resize', resize);
resize();

const frames = new Array(TOTAL_FRAMES);
let loadedCount = 0;
let isReady = false;

function frameName(i) {
  return FRAME_DIR + '/frame_' + String(i + 1).padStart(6, '0') + '.webp';
}

async function loadAll() {
  const queue = Array.from({length: TOTAL_FRAMES}, function(_, i) { return i; });

  async function worker() {
    while (queue.length) {
      const i = queue.shift();
      await new Promise(function(resolve) {
        const img = new Image();
        img.onload = img.onerror = function() {
          frames[i] = img;
          loadedCount++;

          const pct = Math.round(loadedCount / TOTAL_FRAMES * 100);
          const bar = document.getElementById('progress-bar');
          if (bar) bar.style.width = pct + '%';
          const txt = document.getElementById('progress-text');
          if (txt) txt.innerText = pct + '%';

          if (loadedCount === 1) {
            isReady = true;
            startAnim();
          }
          if (loadedCount === Math.min(30, TOTAL_FRAMES)) {
            const loader = document.getElementById('loader');
            if (loader) {
              loader.style.transition = 'opacity 0.8s';
              loader.style.opacity = '0';
              setTimeout(function() { loader.style.display = 'none'; }, 800);
            }
          }
          resolve();
        };
        img.src = frameName(i);
      });
    }
  }
  await Promise.all(Array.from({length: CONCURRENCY}, worker));
}

let currentFrame = 0;
let targetFrame = 0;

window.addEventListener('scroll', function() {
  if (!isReady) return;
  const maxScroll = document.documentElement.scrollHeight - innerHeight;
  const progress = maxScroll > 0 ? scrollY / maxScroll : 0;
  targetFrame = progress * (TOTAL_FRAMES - 1);
}, { passive: true });

function drawFrame(idx) {
  const img = frames[Math.max(0, Math.min(idx, TOTAL_FRAMES - 1))];
  if (!img || !img.complete) return;

  const W = innerWidth;
  const H = innerHeight;
  const r = Math.max(W / img.naturalWidth, H / img.naturalHeight);
  const iw = img.naturalWidth * r;
  const ih = img.naturalHeight * r;
  const x = (W - iw) / 2;
  const y = (H - ih) / 2;

  ctx.clearRect(0, 0, W, H);
  ctx.drawImage(img, x, y, iw, ih);

  // Radial vignette
  const vig = ctx.createRadialGradient(W/2, H/2, H*0.18, W/2, H/2, H*0.85);
  vig.addColorStop(0, 'rgba(15,18,24,0)');
  vig.addColorStop(1, 'rgba(15,18,24,0.80)');
  ctx.fillStyle = vig;
  ctx.fillRect(0, 0, W, H);

  // Bottom darkening
  const bot = ctx.createLinearGradient(0, H*0.6, 0, H);
  bot.addColorStop(0, 'rgba(15,18,24,0)');
  bot.addColorStop(1, 'rgba(15,18,24,0.90)');
  ctx.fillStyle = bot;
  ctx.fillRect(0, H*0.6, W, H*0.4);
}

function startAnim() {
  function loop() {
    requestAnimationFrame(loop);
    currentFrame += (targetFrame - currentFrame) * LERP;
    if (isReady) drawFrame(Math.round(currentFrame));
  }
  loop();
}

// Section reveal with IntersectionObserver
const pages = Array.from(document.querySelectorAll('.page'));
const navLinks = Array.from(document.querySelectorAll('.nav-link'));

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(function(entry) {
    if (entry.isIntersecting) {
      const idx = pages.indexOf(entry.target);
      pages.forEach(function(p, i) { p.classList.toggle('is-active', i === idx); });
      navLinks.forEach(function(l, i) {
        if (l) l.classList.toggle('active', i === idx);
      });
    }
  });
}, { rootMargin: '-40% 0px -40% 0px' });

if (pages.length) {
  pages[0].classList.add('is-active');
  pages.forEach(function(p) { observer.observe(p); });
}

loadAll();
"""

# ============================================================
# CORRECT index.html - proper .page structure + #gl-canvas
# ============================================================
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aesthetic Clinic Belgrade | Premium Medical Beauty</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

<!-- LOADER -->
<div id="loader">
    <div class="loader-inner">
        <div class="loader-ring"></div>
        <div class="loader-brand">AESTHETICA</div>
        <div class="loader-bar-wrap"><div id="progress-bar"></div></div>
        <div id="progress-text">0%</div>
    </div>
</div>

<!-- CANVAS BACKGROUND (fixed) -->
<canvas id="gl-canvas"></canvas>

<!-- NAV -->
<nav>
    <div class="logo">AESTHETICA <span>BELGRADE</span></div>
    <div class="nav-dots">
        <a class="nav-link active" href="#hero">&#9679;</a>
        <a class="nav-link" href="#services">&#9679;</a>
        <a class="nav-link" href="#doctors">&#9679;</a>
        <a class="nav-link" href="#clinic">&#9679;</a>
        <a class="nav-link" href="#booking">&#9679;</a>
    </div>
    <a href="#booking" class="nav-cta">BOOK NOW</a>
</nav>

<!-- PAGES -->
<section class="page" id="hero">
    <div class="page-content">
        <p class="reveal-3d eyebrow">Premium Aesthetic Medicine · Belgrade</p>
        <h1 class="reveal-3d">Art &amp; Science<br><em>of Beauty</em></h1>
        <p class="reveal-3d sub">Advanced aesthetic medicine in the heart of Belgrade.<br>Discretion, luxury, and world-class results for discerning clients.</p>
        <a href="#services" class="reveal-3d btn-primary">EXPLORE TREATMENTS</a>
    </div>
    <div class="scroll-hint reveal-3d">SCROLL</div>
</section>

<section class="page" id="services">
    <div class="page-content page-right">
        <p class="eyebrow reveal-3d">Our Expertise</p>
        <h2 class="reveal-3d">Signature<br>Treatments</h2>
        <div class="cards">
            <div class="card reveal-3d">
                <div class="card-icon">&#9733;</div>
                <h3>Non-Surgical Facelift</h3>
                <p>Advanced dermal fillers &amp; collagen stimulators for natural rejuvenation. Zero downtime.</p>
            </div>
            <div class="card reveal-3d">
                <div class="card-icon">&#10022;</div>
                <h3>Laser Skin Resurfacing</h3>
                <p>Pico-second laser technology to erase pigmentation, acne scars, and fine lines.</p>
            </div>
            <div class="card reveal-3d">
                <div class="card-icon">&#9670;</div>
                <h3>Body Contouring</h3>
                <p>Non-invasive fat reduction &amp; muscle toning with cutting-edge EMS Sculpt technology.</p>
            </div>
        </div>
    </div>
</section>

<section class="page" id="doctors">
    <div class="page-content page-left">
        <p class="eyebrow reveal-3d">The Experts</p>
        <h2 class="reveal-3d">World-Class<br>Medical Team</h2>
        <p class="reveal-3d body-text">Internationally trained plastic surgeons and dermatologists bringing Beverly Hills and Swiss clinic standards to Belgrade. Fluent in English, Russian, and Serbian.</p>
        <a href="#booking" class="reveal-3d btn-outline">MEET THE TEAM</a>
    </div>
</section>

<section class="page" id="clinic">
    <div class="page-content page-center">
        <p class="eyebrow reveal-3d">The Space</p>
        <h2 class="reveal-3d">Absolute<br><em>Privacy &amp; Comfort</em></h2>
        <p class="reveal-3d body-text">Our private VIP suites are designed for complete discretion. Your visit is never logged publicly. Trusted by diplomatic staff, executives, and international clients.</p>
    </div>
</section>

<section class="page" id="booking">
    <div class="page-content page-center">
        <p class="eyebrow reveal-3d">Begin Your Journey</p>
        <h2 class="reveal-3d">Private<br>Consultation</h2>
        <form class="booking-form reveal-3d" onsubmit="return false;">
            <input type="text" placeholder="Your Name" required>
            <input type="tel" placeholder="WhatsApp / Telegram">
            <select>
                <option value="">Select Treatment</option>
                <option>Facial Rejuvenation</option>
                <option>Laser Treatments</option>
                <option>Body Contouring</option>
                <option>VIP Full-Day Package</option>
            </select>
            <button type="submit" class="btn-gold">REQUEST APPOINTMENT</button>
        </form>
    </div>
</section>

<script src="app.js"></script>
</body>
</html>"""

# ============================================================
# CORRECT style.css - proper .page, is-active, reveal-3d
# ============================================================
style_css = """
:root {
  --gold: #D4AF37;
  --gold2: #C5A059;
  --dark: #0F1218;
  --dark2: #1a1e27;
  --white: #F9F7F4;
  --ts: 1px 1px 0 rgba(0,0,0,1), -1px -1px 0 rgba(0,0,0,1),
        1px -1px 0 rgba(0,0,0,1), -1px 1px 0 rgba(0,0,0,1),
        0 0 10px rgba(0,0,0,0.9), 0 0 25px rgba(0,0,0,0.7);
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html {
  scroll-behavior: smooth;
  scroll-snap-type: y proximity;
}

body {
  font-family: 'Inter', sans-serif;
  background: var(--dark);
  color: var(--white);
  overflow-x: hidden;
}

/* ====== LOADER ====== */
#loader {
  position: fixed; inset: 0; z-index: 9999;
  background: var(--dark);
  display: flex; align-items: center; justify-content: center;
}
.loader-inner { text-align: center; }
.loader-ring {
  width: 64px; height: 64px; margin: 0 auto 20px;
  border: 2px solid rgba(212,175,55,0.15);
  border-top: 2px solid var(--gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loader-brand {
  font-family: 'Playfair Display', serif;
  font-size: 20px; letter-spacing: 6px;
  color: var(--gold); margin-bottom: 20px;
}
.loader-bar-wrap {
  width: 200px; height: 2px; background: rgba(255,255,255,0.1);
  margin: 0 auto 10px; border-radius: 2px; overflow: hidden;
}
#progress-bar {
  height: 100%; width: 0%; background: var(--gold);
  transition: width 0.3s ease;
}
#progress-text { font-size: 13px; color: rgba(255,255,255,0.5); font-family: monospace; }

/* ====== CANVAS ====== */
#gl-canvas {
  position: fixed; inset: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
}

/* ====== NAV ====== */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 24px 48px;
}
.logo {
  font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 700; letter-spacing: 3px;
  color: var(--white); text-shadow: var(--ts);
}
.logo span { color: var(--gold); font-size: 11px; letter-spacing: 4px; display: block; margin-top: 2px; }
.nav-dots { display: flex; gap: 12px; }
.nav-link {
  color: rgba(255,255,255,0.3); font-size: 8px;
  text-decoration: none; transition: color 0.3s;
}
.nav-link.active, .nav-link:hover { color: var(--gold); }
.nav-cta {
  font-size: 11px; letter-spacing: 3px; font-weight: 600;
  color: var(--white); text-decoration: none;
  border: 1px solid rgba(212,175,55,0.6);
  padding: 10px 22px; border-radius: 2px;
  text-shadow: var(--ts);
  transition: all 0.3s;
}
.nav-cta:hover { background: var(--gold); color: var(--dark); text-shadow: none; border-color: var(--gold); }

/* ====== PAGES (SECTIONS) ====== */
.page {
  position: relative; z-index: 10;
  min-height: 100vh;
  display: flex; align-items: center;
  scroll-snap-align: start;
  opacity: 0; visibility: hidden;
  pointer-events: none;
  transition: opacity 0.7s ease, visibility 0s 0.7s;
}
.page.is-active {
  opacity: 1; visibility: visible;
  pointer-events: auto;
  transition: opacity 0.7s ease;
}

.page-content {
  width: 100%;
  max-width: 680px;
  padding: 140px 10% 80px;
}
.page-right { margin-left: auto; padding-right: 10%; padding-left: 5%; }
.page-left  { margin-right: auto; }
.page-center { margin: 0 auto; text-align: center; max-width: 680px; padding: 120px 5%; }

/* ====== REVEAL ANIMATION ====== */
.reveal-3d {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.is-active .reveal-3d:nth-child(1) { opacity: 1; transform: none; transition-delay: 0.0s; }
.is-active .reveal-3d:nth-child(2) { opacity: 1; transform: none; transition-delay: 0.1s; }
.is-active .reveal-3d:nth-child(3) { opacity: 1; transform: none; transition-delay: 0.2s; }
.is-active .reveal-3d:nth-child(4) { opacity: 1; transform: none; transition-delay: 0.3s; }
.is-active .reveal-3d:nth-child(5) { opacity: 1; transform: none; transition-delay: 0.4s; }
.is-active .reveal-3d:nth-child(6) { opacity: 1; transform: none; transition-delay: 0.5s; }
.is-active .reveal-3d:nth-child(7) { opacity: 1; transform: none; transition-delay: 0.6s; }

/* ====== TYPOGRAPHY ====== */
.eyebrow {
  font-size: 11px; letter-spacing: 5px; text-transform: uppercase;
  color: var(--gold); font-weight: 500; margin-bottom: 16px;
  text-shadow: var(--ts);
}
h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(42px, 6vw, 88px);
  font-weight: 700; line-height: 1.05;
  color: var(--white); margin-bottom: 24px;
  text-shadow: var(--ts);
}
h1 em { color: var(--gold); font-style: italic; }
h2 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(34px, 4.5vw, 64px);
  font-weight: 600; line-height: 1.1;
  color: var(--white); margin-bottom: 32px;
  text-shadow: var(--ts);
}
h2 em { color: var(--gold); font-style: italic; }
.sub, .body-text {
  font-size: clamp(15px, 1.5vw, 18px);
  line-height: 1.7; color: rgba(255,255,255,0.85);
  margin-bottom: 36px;
  text-shadow: var(--ts);
}

/* ====== BUTTONS ====== */
.btn-primary {
  display: inline-block; padding: 14px 36px;
  background: rgba(0,0,0,0.5); border: 2px solid rgba(255,255,255,0.8);
  color: var(--white); text-decoration: none;
  font-size: 12px; font-weight: 600; letter-spacing: 3px;
  text-shadow: var(--ts); transition: all 0.3s;
}
.btn-primary:hover { background: var(--white); color: var(--dark); text-shadow: none; }

.btn-outline {
  display: inline-block; padding: 14px 36px;
  background: rgba(0,0,0,0.3); border: 1px solid rgba(212,175,55,0.7);
  color: var(--gold); text-decoration: none;
  font-size: 12px; font-weight: 600; letter-spacing: 3px;
  text-shadow: var(--ts); transition: all 0.3s;
}
.btn-outline:hover { background: var(--gold); color: var(--dark); text-shadow: none; }

.btn-gold {
  width: 100%; padding: 16px;
  background: var(--gold); color: var(--dark);
  border: none; font-family: 'Inter', sans-serif;
  font-size: 13px; font-weight: 700; letter-spacing: 3px;
  cursor: pointer; transition: background 0.3s;
}
.btn-gold:hover { background: #fff; }

/* ====== CARDS ====== */
.cards { display: flex; flex-direction: column; gap: 16px; margin-bottom: 0; }
.card {
  background: rgba(15,18,24,0.65);
  border-left: 3px solid var(--gold);
  padding: 22px 26px;
  backdrop-filter: blur(12px);
}
.card-icon { font-size: 18px; color: var(--gold); margin-bottom: 10px; }
.card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px; color: var(--white);
  margin-bottom: 8px; text-shadow: var(--ts);
}
.card p { font-size: 14px; color: rgba(255,255,255,0.75); line-height: 1.6; text-shadow: var(--ts); }

/* ====== FORM ====== */
.booking-form {
  background: rgba(15,18,24,0.75);
  padding: 36px; border-top: 2px solid var(--gold);
  backdrop-filter: blur(16px); text-align: left;
  max-width: 480px; margin: 0 auto;
}
.booking-form input,
.booking-form select {
  width: 100%; padding: 14px 16px; margin-bottom: 14px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  color: var(--white); font-family: 'Inter', sans-serif; font-size: 14px;
  outline: none;
}
.booking-form select option { background: var(--dark2); }

/* ====== SCROLL HINT ====== */
.scroll-hint {
  position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%);
  font-size: 10px; letter-spacing: 4px; color: rgba(255,255,255,0.5);
  text-shadow: var(--ts);
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(8px); }
}

/* ====== MOBILE ====== */
@media (max-width: 768px) {
  nav { padding: 18px 20px; }
  .nav-dots { display: none; }
  .page-content { padding: 120px 24px 60px; max-width: 100%; }
  .page-right { padding-right: 24px; padding-left: 24px; }
  .booking-form { padding: 24px; }
  h1 { font-size: clamp(36px, 9vw, 56px); }
  h2 { font-size: clamp(28px, 7vw, 48px); }
}
"""

with open(os.path.join(demo_dir, "app.js"), "w", encoding="utf-8") as f:
    f.write(app_js)
with open(os.path.join(demo_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
with open(os.path.join(demo_dir, "style.css"), "w", encoding="utf-8") as f:
    f.write(style_css)

print("Rea Medika Demo fully rewritten with correct Cinematic Scroll Engine.")
