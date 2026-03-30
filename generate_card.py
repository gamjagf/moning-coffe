import base64
import os
from PIL import Image

def get_average_color(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((50, 50))
        result = img.convert('P', palette=Image.ADAPTIVE, colors=1)
        result = result.convert('RGB')
        color = result.getpixel((0,0))
        # darken the color slightly for background
        dark_color = (int(color[0]*0.3), int(color[1]*0.3), int(color[2]*0.3))
        # accent color
        light_color = (int(min(color[0]*1.2, 255)), int(min(color[1]*1.2, 255)), int(min(color[2]*1.2, 255)))
        return f"rgb({dark_color[0]}, {dark_color[1]}, {dark_color[2]})", f"rgb({light_color[0]}, {light_color[1]}, {light_color[2]})"
    except Exception as e:
        print("Error getting color:", e)
        return "#1a1a1a", "#ffffff"

image_path = r"C:\Users\ksngn\.gemini\antigravity\brain\aabeddf6-1c93-486a-888d-c165ffbd1d90\rainy_coffee_1774843981420.png"
mp3_path = r"C:\Antigravity\moning cofee\901. 고병희햇빛촌  유리창엔 비.mp3"

bg_color, accent_color = get_average_color(image_path)

print("Encoding image...")
with open(image_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode('utf-8')

print("Encoding mp3...")
with open(mp3_path, "rb") as f:
    mp3_b64 = base64.b64encode(f.read()).decode('utf-8')

print("Generating HTML...")
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rainy Day Coffee</title>
    <style>
        :root {{
            --bg-color: {bg_color};
            --accent-color: {accent_color};
        }}
        body {{
            margin: 0;
            padding: 0;
            background-color: var(--bg-color);
            color: #fff;
            font-family: 'Noto Sans KR', 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            overflow: hidden;
            transition: background-color 0.5s ease;
        }}
        
        .card-container {{
            width: 90%;
            max-width: 480px;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.15);
            overflow: hidden;
            position: relative;
            display: flex;
            flex-direction: column;
            animation: fadeIn 1s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .header {{
            padding: 24px 20px;
            text-align: center;
            z-index: 10;
            background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
        }}
        .header h1 {{
            font-size: 19px;
            margin: 0 0 8px 0;
            font-weight: 400;
            letter-spacing: 1.5px;
            line-height: 1.5;
            text-shadow: 1px 1px 10px rgba(0,0,0,0.8);
        }}
        .header h2 {{
            font-size: 13px;
            margin: 0;
            color: rgba(255,255,255,0.7);
            font-style: italic;
            font-family: 'Georgia', serif;
            letter-spacing: 2px;
        }}

        .image-container {{
            position: relative;
            width: 100%;
            height: 420px;
            overflow: hidden;
        }}
        
        .image-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            animation: zoom 25s infinite alternate ease-in-out;
        }}

        @keyframes zoom {{
            from {{ transform: scale(1); }}
            to {{ transform: scale(1.15); }}
        }}

        .gradient-overlay {{
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(to bottom, 
                var(--bg-color) 0%, 
                rgba(0,0,0,0) 25%, 
                rgba(0,0,0,0) 75%, 
                var(--bg-color) 100%);
            z-index: 1;
            pointer-events: none;
        }}

        #rainCanvas {{
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 2;
            pointer-events: none;
        }}

        .controls {{
            padding: 20px 25px;
            background: linear-gradient(to top, var(--bg-color) 80%, transparent);
            z-index: 10;
        }}

        #visualizer {{
            width: 100%;
            height: 40px;
            background: rgba(0,0,0,0.2);
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
        }}

        .player {{
            display: flex;
            align-items: center;
            gap: 18px;
        }}

        .play-btn {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: #fff;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            flex-shrink: 0;
        }}
        
        .play-btn:hover {{
            background: rgba(255,255,255,0.2);
            transform: scale(1.05);
            border-color: rgba(255,255,255,0.4);
        }}

        .progress-wrapper {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        .slider {{
            -webkit-appearance: none;
            width: 100%;
            height: 4px;
            border-radius: 2px;
            background: rgba(255,255,255,0.2);
            outline: none;
            margin-bottom: 8px;
            cursor: pointer;
        }}
        
        .slider::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--accent-color, #fff);
            cursor: pointer;
            box-shadow: 0 0 5px rgba(0,0,0,0.5);
        }}

        .time-display {{
            font-size: 11px;
            color: rgba(255,255,255,0.6);
            align-self: flex-start;
            font-family: monospace;
            letter-spacing: 0.5px;
        }}
        
        .volume-control {{
            display: flex;
            align-items: center;
            gap: 6px;
            opacity: 0.7;
            transition: opacity 0.3s;
        }}
        
        .volume-control:hover {{
            opacity: 1;
        }}
        
        .volume-slider {{
            width: 50px;
        }}

        .footer {{
            padding: 15px 20px 25px;
            text-align: center;
            font-size: 14px;
            color: rgba(255,255,255,0.8);
            font-style: italic;
            font-family: 'Georgia', serif;
            letter-spacing: 1.5px;
            background: var(--bg-color);
            position: relative;
        }}
        
        .footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 20%;
            right: 20%;
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent);
        }}
    </style>
</head>
<body>

<div class="card-container">
    <div class="header">
        <h1>창밖의 비는 세상을 적시고,<br>커피는 마음을 데운다</h1>
        <h2>Rainy day, warm coffee</h2>
    </div>

    <div class="image-container">
        <img src="data:image/png;base64,{img_b64}" alt="Rainy Coffee">
        <div class="gradient-overlay"></div>
        <canvas id="rainCanvas"></canvas>
    </div>

    <div class="controls">
        <canvas id="visualizer"></canvas>
        <div class="player">
            <button class="play-btn" id="playBtn">▶</button>
            <div class="progress-wrapper">
                <input type="range" id="progress" class="slider" value="0" min="0" max="100" step="0.1">
                <div class="time-display" id="timeDisplay">0:00 / 0:00</div>
            </div>
            <div class="volume-control">
                <span style="font-size: 14px;">🔊</span>
                <input type="range" id="volumeSlider" class="slider volume-slider" value="0.7" min="0" max="1" step="0.05">
            </div>
        </div>
    </div>

    <div class="footer">
        Rainy day, warm coffee
    </div>
</div>

<audio id="bgm" loop>
    <source src="data:audio/mp3;base64,{mp3_b64}" type="audio/mp3">
</audio>

<script>
// Canvas Rain Animation
const canvas = document.getElementById('rainCanvas');
const ctx = canvas.getContext('2d');
function resizeWindow() {{
   canvas.width = canvas.offsetWidth;
   canvas.height = canvas.offsetHeight;
}}
window.addEventListener('resize', resizeWindow);
resizeWindow();

let drops = [];
for(let i=0; i<80; i++) {{
   drops.push({{
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      l: Math.random() * 1.5 + 15,
      v: Math.random() * 6 + 12
   }});
}}

function drawRain() {{
   ctx.clearRect(0, 0, canvas.width, canvas.height);
   ctx.strokeStyle = 'rgba(255,255,255,0.25)';
   ctx.lineWidth = 1.2;
   ctx.lineCap = 'round';
   ctx.beginPath();
   for(let i=0; i<drops.length; i++) {{
       let p = drops[i];
       ctx.moveTo(p.x, p.y);
       ctx.lineTo(p.x + p.v * 0.1, p.y + p.l);
   }}
   ctx.stroke();
   
   for(let i=0; i<drops.length; i++) {{
       drops[i].y += drops[i].v;
       drops[i].x += drops[i].v * 0.1;
       if (drops[i].y > canvas.height) {{
           drops[i].y = -20;
           drops[i].x = Math.random() * canvas.width;
       }}
   }}
   requestAnimationFrame(drawRain);
}}
drawRain();

// Audio logic
const audio = document.getElementById('bgm');
const playBtn = document.getElementById('playBtn');
const progress = document.getElementById('progress');
const timeDisplay = document.getElementById('timeDisplay');
const volumeSlider = document.getElementById('volumeSlider');
const visualizerCanvas = document.getElementById('visualizer');
const vCtx = visualizerCanvas.getContext('2d');

let isPlaying = false;
let audioCtx;
let analyser;
let source;

playBtn.addEventListener('click', () => {{
    if(!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 128;
        source = audioCtx.createMediaElementSource(audio);
        source.connect(analyser);
        analyser.connect(audioCtx.destination);
        visualize();
    }}
    
    if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
    }}

    if(isPlaying) {{
        audio.pause();
        playBtn.innerHTML = '▶';
    }} else {{
        let playPromise = audio.play();
        if (playPromise !== undefined) {{
            playPromise.then(_ => {{
                playBtn.innerHTML = '⏸';
            }}).catch(error => {{
                console.log('Autoplay prevented', error);
            }});
        }}
    }}
    isPlaying = !isPlaying;
}});

audio.addEventListener('timeupdate', () => {{
    let p = (audio.currentTime / audio.duration) * 100;
    if (!isNaN(p)) progress.value = p;
    
    let curM = Math.floor(audio.currentTime / 60) || 0;
    let curS = Math.floor(audio.currentTime % 60).toString().padStart(2, '0') || '00';
    let durM = Math.floor(audio.duration / 60) || 0;
    let durS = Math.floor(audio.duration % 60).toString().padStart(2, '0') || '00';
    if (!isNaN(audio.duration)) {{
        timeDisplay.innerText = `${{curM}}:${{curS}} / ${{durM}}:${{durS}}`;
    }}
}});

progress.addEventListener('input', () => {{
    const time = (progress.value / 100) * audio.duration;
    if (!isNaN(time)) {{
        audio.currentTime = time;
    }}
}});

volumeSlider.addEventListener('input', () => {{
    audio.volume = volumeSlider.value;
}});
audio.volume = volumeSlider.value;

function visualize() {{
    requestAnimationFrame(visualize);
    if (!analyser) return;
    
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    analyser.getByteFrequencyData(dataArray);
    
    visualizerCanvas.width = visualizerCanvas.offsetWidth;
    visualizerCanvas.height = visualizerCanvas.offsetHeight;
    
    vCtx.clearRect(0, 0, visualizerCanvas.width, visualizerCanvas.height);
    const barWidth = (visualizerCanvas.width / bufferLength) * 2.5;
    let barHeight;
    let x = 0;
    
    for(let i = 0; i < bufferLength; i++) {{
        barHeight = dataArray[i] / 4;
        vCtx.fillStyle = `rgba(255, 255, 255, ${{0.3 + (dataArray[i]/255)*0.7}})`;
        vCtx.beginPath();
        vCtx.roundRect(x, visualizerCanvas.height - barHeight, barWidth - 1, barHeight, [2, 2, 0, 0]);
        vCtx.fill();
        x += barWidth;
    }}
}}
</script>
</body>
</html>
"""

outPath1 = r"C:\mnt\user-data\outputs\card.html"
outPath2 = r"C:\Antigravity\moning cofee\card.html"

os.makedirs(r"C:\mnt\user-data\outputs", exist_ok=True)
with open(outPath1, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(outPath2, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Success! Files saved.")
