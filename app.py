import streamlit as st
import base64
from PIL import Image
import io

ANIMATIONS = {
    "🌧️ 비 (Rain)": """
let drops = [];
for(let i=0; i<80; i++) { drops.push({ x: Math.random() * cW, y: Math.random() * cH, l: Math.random() * 1.5 + 15, v: Math.random() * 6 + 12 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH); ctx.strokeStyle = 'rgba(255,255,255,0.25)'; ctx.lineWidth = 1.2; ctx.lineCap = 'round'; ctx.beginPath();
   for(let i=0; i<drops.length; i++) { let p = drops[i]; ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + p.v * 0.1, p.y + p.l); } ctx.stroke();
   for(let i=0; i<drops.length; i++) { drops[i].y += drops[i].v; drops[i].x += drops[i].v * 0.1; if (drops[i].y > cH) { drops[i].y = -20; drops[i].x = Math.random() * cW; } }
}
    """,
    "❄️ 작은 눈 (Snow)": """
let flakes = [];
for(let i=0; i<100; i++) { flakes.push({ x: Math.random() * cW, y: Math.random() * cH, r: Math.random() * 2 + 1, d: Math.random() * 100 }); }
let angle = 0;
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH); ctx.fillStyle = 'rgba(255,255,255,0.6)'; ctx.beginPath();
   for(let i=0; i<flakes.length; i++) { let p = flakes[i]; ctx.moveTo(p.x, p.y); ctx.arc(p.x, p.y, p.r, 0, Math.PI*2, true); } ctx.fill();
   angle += 0.01;
   for(let i=0; i<flakes.length; i++) { let p = flakes[i]; p.y += Math.cos(angle + p.d) + 1 + p.r/2; p.x += Math.sin(angle) * 2; if(p.x > cW+5 || p.x < -5 || p.y > cH) { if(i%3 > 0) { p.x = Math.random() * cW; p.y = -10; } else { if(Math.sin(angle) > 0) { p.x = -5; p.y = Math.random()*cH; } else { p.x = cW+5; p.y = Math.random()*cH; } } } }
}
    """,
    "🌫️ 수증기 / 안개 (Steam/Fog)": """
let puffs = [];
for(let i=0; i<15; i++) { puffs.push({ x: Math.random() * cW, y: cH + Math.random() * 100, s: Math.random() * 50 + 50, a: Math.random(), v: Math.random() * 0.5 + 0.5 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<puffs.length; i++) { let p = puffs[i]; ctx.beginPath(); let rad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.s); rad.addColorStop(0, 'rgba(255,255,255,'+(0.1*p.a)+')'); rad.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = rad; ctx.arc(p.x, p.y, p.s, 0, Math.PI*2); ctx.fill(); p.y -= p.v; p.x += Math.sin(p.a += 0.02) * 0.5; if(p.y < -p.s) { p.y = cH + p.s; p.x = Math.random() * cW; } }
}
    """,
    "✨ 별빛 (Starlight)": """
let stars = [];
for(let i=0; i<80; i++) { stars.push({ x: Math.random() * cW, y: Math.random() * cH, r: Math.random() * 1.5, s: Math.random() * 0.05 + 0.01, a: Math.random() * Math.PI * 2 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<stars.length; i++) { let p = stars[i]; ctx.beginPath(); ctx.fillStyle = 'rgba(255,255,255,' + (Math.sin(p.a)+1)/2 * 0.8 + ')'; ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.fill(); p.a += p.s; }
}
    """,
    "🌸 벚꽃/꽃잎 (Cherry Blossoms)": """
let petals = [];
for(let i=0; i<40; i++) { petals.push({ x: Math.random() * cW, y: Math.random() * cH, w: Math.random() * 8 + 5, h: Math.random() * 6 + 4, a: Math.random() * 360, vY: Math.random() * 1.5 + 1, vX: Math.random() * 2 - 1, rV: Math.random() * 2 - 1, c: 'rgba(255, 183, 197, '+(Math.random()*0.5+0.5)+')' }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<petals.length; i++) { let p = petals[i]; ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a * Math.PI / 180); ctx.fillStyle = p.c; ctx.beginPath(); ctx.ellipse(0, 0, p.w, p.h, 0, 0, Math.PI*2); ctx.fill(); ctx.restore(); p.y += p.vY; p.x += p.vX + Math.sin(p.a*0.02)*0.5; p.a += p.rV; if(p.y > cH + 10) { p.y = -10; p.x = Math.random() * cW; } }
}
    """,
    "☀️ 태양 빛내림 (Sun Rays)": """
let rays = [];
for(let i=0; i<6; i++) { rays.push({ x: Math.random() * cW, w: Math.random() * 100 + 50, a: Math.random() * 0.1 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<rays.length; i++) { let p = rays[i]; ctx.beginPath(); let g = ctx.createLinearGradient(0, 0, p.w, cH); g.addColorStop(0, 'rgba(255,255,240,'+(0.05 + Math.sin(p.a)*0.03)+')'); g.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = g; ctx.moveTo(p.x, 0); ctx.lineTo(p.x + p.w, 0); ctx.lineTo(p.x + p.w + cH*0.5, cH); ctx.lineTo(p.x + cH*0.5, cH); ctx.fill(); p.x += 0.2; p.a += 0.01; if(p.x > cW) { p.x = -150; } }
}
    """,
    "🍂 낙엽 (Autumn Leaves)": """
let leaves = [];
for(let i=0; i<30; i++) { leaves.push({ x: Math.random() * cW, y: Math.random() * cH, s: Math.random() * 6 + 4, a: Math.random() * 360, vY: Math.random() * 2 + 1, vX: Math.random() * 1 - 0.5, rV: Math.random() * 4 - 2, c: Math.random() > 0.5 ? 'rgba(212, 110, 31, '+(Math.random()*0.5+0.5)+')' : 'rgba(189, 73, 23, '+(Math.random()*0.5+0.5)+')' }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<leaves.length; i++) { let p = leaves[i]; ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a * Math.PI / 180); ctx.fillStyle = p.c; ctx.beginPath(); ctx.moveTo(0,-p.s); ctx.bezierCurveTo(p.s,-p.s,p.s,p.s,0,p.s); ctx.bezierCurveTo(-p.s,p.s,-p.s,-p.s,0,-p.s); ctx.fill(); ctx.restore(); p.y += p.vY; p.x += p.vX + Math.sin(p.a*0.01)*0.5; p.a += p.rV; if(p.y > cH + p.s) { p.y = -p.s; p.x = Math.random() * cW; } }
}
    """,
    "🎇 반딧불이 (Fireflies)": """
let flies = [];
for(let i=0; i<40; i++) { flies.push({ x: Math.random() * cW, y: Math.random() * cH, s: Math.random() * 2 + 1, a: Math.random() * Math.PI * 2, vX: Math.random() * 1 - 0.5, vY: Math.random() * 1 - 0.5 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<flies.length; i++) { let p = flies[i]; ctx.beginPath(); let rad = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.s*3); rad.addColorStop(0, 'rgba(200,255,100,'+((Math.sin(p.a)+1)/2 * 0.8 + 0.2)+')'); rad.addColorStop(1, 'rgba(200,255,100,0)'); ctx.fillStyle = rad; ctx.arc(p.x, p.y, p.s*3, 0, Math.PI*2); ctx.fill(); p.x += p.vX + Math.sin(p.a)*0.2; p.y += p.vY + Math.cos(p.a)*0.2; p.a += 0.05; if(p.x < 0 || p.x > cW) p.vX *= -1; if(p.y < 0 || p.y > cH) p.vY *= -1; }
}
    """,
    "🫧 버블 / 물방울 (Bubbles)": """
let bubbles = [];
for(let i=0; i<30; i++) { bubbles.push({ x: Math.random() * cW, y: Math.random() * cH, r: Math.random() * 6 + 2, vY: Math.random() * 1.5 + 0.5, a: Math.random() * Math.PI*2 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<bubbles.length; i++) { let p = bubbles[i]; ctx.beginPath(); ctx.strokeStyle = 'rgba(255,255,255,0.4)'; ctx.lineWidth = 1; ctx.arc(p.x, p.y, p.r, 0, Math.PI*2); ctx.stroke(); ctx.beginPath(); ctx.fillStyle = 'rgba(255,255,255,0.3)'; ctx.arc(p.x - p.r*0.3, p.y - p.r*0.3, p.r*0.2, 0, Math.PI*2); ctx.fill(); p.y -= p.vY; p.x += Math.sin(p.a+=0.05)*0.3; if(p.y < -p.r) { p.y = cH + p.r; p.x = Math.random() * cW; } }
}
    """,
    "☄️ 불티 / 먼지 (Embers/Dust)": """
let embers = [];
for(let i=0; i<50; i++) { embers.push({ x: Math.random() * cW, y: cH + Math.random() * cH, s: Math.random() * 2 + 1, vY: Math.random() * 3 + 1, vX: Math.random() * 2 - 1, a: Math.random() * Math.PI*2 }); }
function drawAnim() {
   ctx.clearRect(0, 0, cW, cH);
   for(let i=0; i<embers.length; i++) { let p = embers[i]; ctx.beginPath(); ctx.fillStyle = 'rgba(255,'+(100+Math.random()*100)+',50,'+((Math.sin(p.a)+1)/2 * 0.8+0.2)+')'; ctx.arc(p.x, p.y, p.s, 0, Math.PI*2); ctx.fill(); p.y -= p.vY; p.x += p.vX + Math.sin(p.a+=0.1)*1; if(p.y < -10) { p.y = cH + 10; p.x = Math.random() * cW; } }
}
    """,
    "❌ 애니메이션 없음 (None)": """
function drawAnim() { ctx.clearRect(0, 0, cW, cH); }
    """
}

def get_average_color(img):
    try:
        img_resized = img.resize((50, 50))
        result = img_resized.convert('P', palette=Image.ADAPTIVE, colors=1)
        result = result.convert('RGB')
        color = result.getpixel((0,0))
        dark_color = (int(color[0]*0.3), int(color[1]*0.3), int(color[2]*0.3))
        light_color = (int(min(color[0]*1.2, 255)), int(min(color[1]*1.2, 255)), int(min(color[2]*1.2, 255)))
        return f"rgb({dark_color[0]}, {dark_color[1]}, {dark_color[2]})", f"rgb({light_color[0]}, {light_color[1]}, {light_color[2]})"
    except Exception as e:
        return "#1a1a1a", "#ffffff"

st.set_page_config(page_title="감성 카드 빌더 2.0", page_icon="☕")
st.title("☕ 나만의 감성 카드 만들기 2.0")
st.write("이미지(다중 슬라이드 지원) 혹은 🎥동영상을 올리고, 멋진 애니메이션을 조합해 카드를 만드세요!")

with st.form("card_form"):
    st.markdown("### 1. 배경 화면 설정")
    st.write("사용할 배경을 위해 이미지 또는 동영상 중 **하나만** 업로드해주세요.")
    
    img_files = st.file_uploader("🖼️ 이미지 슬라이드 (최대 5장, JPG/PNG)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if img_files and len(img_files) > 5:
        st.warning("이미지는 최대 5장까지만 슬라이드가 적용됩니다.")
        img_files = img_files[:5]
        
    st.markdown("---")
    st.warning("⚠️ 동영상의 용량이 크면 생성된 HTML이 매우 무거워질 수 있습니다. 가급적 가벼운 영상을 권장합니다.")
    vid_file = st.file_uploader("🎬 동영상 배경 (MP4/MOV, 이미지 대신 사용할 경우)", type=["mp4", "mov", "webm"])
        
    st.markdown("### 2. 음악 & 효과 설정")
    mp3_file = st.file_uploader("🎵 MP3 배경음악 파일", type=["mp3", "wav"])
    anim_choice = st.selectbox("✨ 애니메이션(화면 효과) 선택", list(ANIMATIONS.keys()))
    
    st.markdown("### 3. 문구 설정")
    main_text = st.text_area("✍️ 상단 메인 문구", "창밖의 비는 세상을 적시고,\n커피는 마음을 데운다")
    sub_text = st.text_input("📝 영문 서브 타이틀", "Rainy day, warm coffee")
    footer_text = st.text_input("📝 하단 푸터 문구", "Rainy day, warm coffee")
    
    submitted = st.form_submit_button("🎨 HTML 감성 카드 생성하기")

if submitted:
    if (not img_files and not vid_file) or not mp3_file:
        st.error("⚠️ 배경 파일(이미지 혹은 동영상)과 MP3 음악 파일을 모두 업로드해주세요.")
    else:
        with st.spinner("마법을 부리는 중입니다..."):
            mp3_bytes = mp3_file.read()
            mp3_b64 = base64.b64encode(mp3_bytes).decode('utf-8')
            audio_ext = mp3_file.name.split('.')[-1].lower()
            audio_mime = f"audio/{audio_ext}"
            
            # Media logic
            media_html = ""
            css_keyframes = ""
            css_img_rules = ""
            bg_color, accent_color = "#1a1a1a", "#ffffff"
            
            if vid_file:
                vid_bytes = vid_file.read()
                vid_b64 = base64.b64encode(vid_bytes).decode('utf-8')
                vid_ext = vid_file.name.split('.')[-1].lower()
                vid_mime = f"video/{vid_ext}"
                bg_color, accent_color = "#1a1a1a", "#ffffff" # Default dark for video
                media_html = f'<video src="data:{vid_mime};base64,{vid_b64}" autoplay loop muted playsinline style="width:100%; height:100%; object-fit:cover; position:absolute; left:0; top:0;"></video>'
            else:
                img_data_list = []
                for idx, f in enumerate(img_files):
                    img_bytes = f.read()
                    if idx == 0:
                        img = Image.open(io.BytesIO(img_bytes))
                        bg_color, accent_color = get_average_color(img)
                    b64 = base64.b64encode(img_bytes).decode('utf-8')
                    ext = f.name.split('.')[-1].lower()
                    mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"
                    img_data_list.append((mime, b64))
                
                if len(img_data_list) == 1:
                    media_html = f'<img src="data:{img_data_list[0][0]};base64,{img_data_list[0][1]}" alt="Card Image">'
                    css_keyframes = """
                    .slideshow img { width: 100%; height: 100%; object-fit: cover; animation: zoom 25s infinite alternate ease-in-out; }
                    @keyframes zoom { from { transform: scale(1); } to { transform: scale(1.15); } }
                    """
                else:
                    n = len(img_data_list)
                    t_time = n * 4
                    p_in = (1.0 / t_time) * 100
                    p_vis = (3.5 / t_time) * 100
                    p_out = (4.0 / t_time) * 100
                    
                    for idx, (mime, b64) in enumerate(img_data_list):
                        media_html += f'<img src="data:{mime};base64,{b64}" class="slide-{idx}">\n'
                        css_img_rules += f".slideshow img.slide-{idx} {{ animation-delay: {idx*4}s; }}\n"
                    
                    css_keyframes = f"""
                    .slideshow img {{ position: absolute; width:100%; height:100%; object-fit: cover; opacity: 0; animation: fade_slide {t_time}s infinite ease-in-out; }}
                    @keyframes fade_slide {{
                        0% {{ opacity: 0; transform: scale(1); }}
                        {p_in:.2f}% {{ opacity: 1; transform: scale(1.02); }}
                        {p_vis:.2f}% {{ opacity: 1; transform: scale(1.08); }}
                        {p_out:.2f}% {{ opacity: 0; transform: scale(1.1); }}
                        100% {{ opacity: 0; transform: scale(1); }}
                    }}
                    {css_img_rules}
                    """

            js_anim_logic = ANIMATIONS.get(anim_choice, "")

            html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotional Card</title>
    <style>
        :root {{ --bg-color: {bg_color}; --accent-color: {accent_color}; }}
        body {{ margin: 0; padding: 20px 0; box-sizing: border-box; background-color: var(--bg-color); color: #fff; font-family: 'Noto Sans KR', 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; overflow-x: hidden; overflow-y: auto; transition: background-color 0.5s ease; }}
        .card-container {{ margin: auto; width: 90%; max-width: 480px; background: rgba(0, 0, 0, 0.4); border-radius: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.15); overflow: hidden; position: relative; display: flex; flex-direction: column; animation: fadeIn 1s ease-out; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        .header {{ padding: 24px 20px; text-align: center; z-index: 10; background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent); }}
        .header h1 {{ font-size: 19px; margin: 0 0 8px 0; font-weight: 400; letter-spacing: 1.5px; line-height: 1.5; text-shadow: 1px 1px 10px rgba(0,0,0,0.8); }}
        .header h2 {{ font-size: 13px; margin: 0; color: rgba(255,255,255,0.7); font-style: italic; font-family: 'Georgia', serif; letter-spacing: 2px; }}
        .image-container {{ position: relative; width: 100%; height: 420px; overflow: hidden; }}
        .slideshow {{ position: absolute; width: 100%; height: 100%; left: 0; top: 0; }}
        {css_keyframes}
        .gradient-overlay {{ position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(to bottom, var(--bg-color) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,0) 75%, var(--bg-color) 100%); z-index: 1; pointer-events: none; }}
        #animCanvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; pointer-events: none; }}
        .controls {{ padding: 20px 25px; background: linear-gradient(to top, var(--bg-color) 80%, transparent); z-index: 10; }}
        #visualizer {{ width: 100%; height: 40px; background: rgba(0,0,0,0.2); border-radius: 8px; margin-bottom: 15px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.3); }}
        .player {{ display: flex; align-items: center; gap: 18px; }}
        .play-btn {{ width: 50px; height: 50px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.1); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; transition: all 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.3); flex-shrink: 0; }}
        .play-btn:hover {{ background: rgba(255,255,255,0.2); transform: scale(1.05); border-color: rgba(255,255,255,0.4); }}
        .progress-wrapper {{ flex-grow: 1; display: flex; flex-direction: column; justify-content: center; }}
        .slider {{ -webkit-appearance: none; width: 100%; height: 4px; border-radius: 2px; background: rgba(255,255,255,0.2); outline: none; margin-bottom: 8px; cursor: pointer; }}
        .slider::-webkit-slider-thumb {{ -webkit-appearance: none; appearance: none; width: 12px; height: 12px; border-radius: 50%; background: var(--accent-color, #fff); cursor: pointer; box-shadow: 0 0 5px rgba(0,0,0,0.5); }}
        .time-display {{ font-size: 11px; color: rgba(255,255,255,0.6); align-self: flex-start; font-family: monospace; letter-spacing: 0.5px; }}
        .volume-control {{ display: flex; align-items: center; gap: 6px; opacity: 0.7; transition: opacity 0.3s; }}
        .volume-control:hover {{ opacity: 1; }}
        .volume-slider {{ width: 50px; }}
        .footer {{ padding: 15px 20px 25px; text-align: center; font-size: 14px; color: rgba(255,255,255,0.8); font-style: italic; font-family: 'Georgia', serif; letter-spacing: 1.5px; background: var(--bg-color); position: relative; }}
        .footer::before {{ content: ''; position: absolute; top: 0; left: 20%; right: 20%; height: 1px; background: linear-gradient(to right, transparent, rgba(255,255,255,0.2), transparent); }}
    </style>
</head>
<body>
<div class="card-container">
    <div class="header">
        <h1>{main_text.replace(chr(10), '<br>')}</h1>
        <h2>{sub_text}</h2>
    </div>
    <div class="image-container">
        <div class="slideshow">
            {media_html}
        </div>
        <div class="gradient-overlay"></div>
        <canvas id="animCanvas"></canvas>
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
        {footer_text}
    </div>
</div>
<audio id="bgm" loop><source src="data:{audio_mime};base64,{mp3_b64}" type="{audio_mime}"></audio>
<script>
const canvas = document.getElementById('animCanvas');
const ctx = canvas.getContext('2d');
let cW = 0, cH = 0;
function resizeWindow() {{ cW = canvas.width = canvas.offsetWidth; cH = canvas.height = canvas.offsetHeight; }}
window.addEventListener('resize', resizeWindow); resizeWindow();

{js_anim_logic}

function loopAnim() {{
    drawAnim();
    requestAnimationFrame(loopAnim);
}}
loopAnim();

const audio = document.getElementById('bgm');
const playBtn = document.getElementById('playBtn');
const progress = document.getElementById('progress');
const timeDisplay = document.getElementById('timeDisplay');
const volumeSlider = document.getElementById('volumeSlider');
const visualizerCanvas = document.getElementById('visualizer');
const vCtx = visualizerCanvas.getContext('2d');
let isPlaying = false, audioCtx, analyser, source;
playBtn.addEventListener('click', () => {{
    if(!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)(); analyser = audioCtx.createAnalyser(); analyser.fftSize = 128;
        source = audioCtx.createMediaElementSource(audio); source.connect(analyser); analyser.connect(audioCtx.destination); visualize();
    }}
    if (audioCtx.state === 'suspended') {{ audioCtx.resume(); }}
    if(isPlaying) {{ audio.pause(); playBtn.innerHTML = '▶'; }} else {{
        let playPromise = audio.play(); if (playPromise !== undefined) {{ playPromise.then(_ => {{ playBtn.innerHTML = '⏸'; }}).catch(e => console.log('Autoplay prevented', e)); }}
    }} isPlaying = !isPlaying;
}});
audio.addEventListener('timeupdate', () => {{
    let p = (audio.currentTime / audio.duration) * 100; if (!isNaN(p)) progress.value = p;
    let curM = Math.floor(audio.currentTime / 60) || 0; let curS = Math.floor(audio.currentTime % 60).toString().padStart(2, '0') || '00';
    let durM = Math.floor(audio.duration / 60) || 0; let durS = Math.floor(audio.duration % 60).toString().padStart(2, '0') || '00';
    if (!isNaN(audio.duration)) {{ timeDisplay.innerText = `${{curM}}:${{curS}} / ${{durM}}:${{durS}}`; }}
}});
progress.addEventListener('input', () => {{ const time = (progress.value / 100) * audio.duration; if (!isNaN(time)) {{ audio.currentTime = time; }} }});
volumeSlider.addEventListener('input', () => {{ audio.volume = volumeSlider.value; }}); audio.volume = volumeSlider.value;
function visualize() {{
    requestAnimationFrame(visualize); if (!analyser) return;
    const bufferLength = analyser.frequencyBinCount; const dataArray = new Uint8Array(bufferLength); analyser.getByteFrequencyData(dataArray);
    visualizerCanvas.width = visualizerCanvas.offsetWidth; visualizerCanvas.height = visualizerCanvas.offsetHeight;
    vCtx.clearRect(0, 0, visualizerCanvas.width, visualizerCanvas.height); const barWidth = (visualizerCanvas.width / bufferLength) * 2.5; let barHeight, x = 0;
    for(let i = 0; i < bufferLength; i++) {{ barHeight = dataArray[i] / 4; vCtx.fillStyle = `rgba(255, 255, 255, ${{0.3 + (dataArray[i]/255)*0.7}})`; vCtx.beginPath(); vCtx.roundRect(x, visualizerCanvas.height - barHeight, barWidth - 1, barHeight, [2, 2, 0, 0]); vCtx.fill(); x += barWidth; }}
}}
</script>
</body>
</html>"""

            st.success("🎉 감성 카드가 성공적으로 생성되었습니다!")
            st.download_button(
                label="💌 생성된 멀티 카드 다운로드 (card.html)",
                data=html_content,
                file_name="card.html",
                mime="text/html",
                use_container_width=True
            )
