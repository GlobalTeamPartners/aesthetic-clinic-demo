
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
