import math
import random

import streamlit as st


st.set_page_config(page_title="Ruota della fortuna", page_icon="🎡", layout="centered")

COLORS = ["#2563EB"] * 6 + ["#16A34A"] * 4 + ["#DC2626"] * 2
LABELS = ["BLU"] * 6 + ["VERDE"] * 4 + ["ROSSO"] * 2
N = len(COLORS)


def sector_path(cx, cy, radius, start_deg, end_deg):
    def point(angle):
        rad = math.radians(angle - 90)
        return cx + radius * math.cos(rad), cy + radius * math.sin(rad)

    x1, y1 = point(start_deg)
    x2, y2 = point(end_deg)
    large_arc = 1 if end_deg - start_deg > 180 else 0
    return f"M {cx} {cy} L {x1:.2f} {y1:.2f} A {radius} {radius} 0 {large_arc} 1 {x2:.2f} {y2:.2f} Z"


def wheel_svg(rotation):
    cx = cy = 200
    radius = 176
    parts = []
    angle = 360 / N
    for i, color in enumerate(COLORS):
        start = i * angle
        end = (i + 1) * angle
        mid = math.radians((start + end) / 2 - 90)
        tx = cx + 112 * math.cos(mid)
        ty = cy + 112 * math.sin(mid)
        parts.append(
            f'<path d="{sector_path(cx, cy, radius, start, end)}" fill="{color}" stroke="#fff" stroke-width="3"/>'
            f'<text x="{tx:.1f}" y="{ty:.1f}" transform="rotate({(start + end) / 2} {tx:.1f} {ty:.1f})" class="label">{LABELS[i]}</text>'
        )
    return f'''<div class="wheel-wrap"><div class="pointer"></div><div class="wheel" style="transform:rotate({rotation}deg)">
    <svg viewBox="0 0 400 400" role="img" aria-label="Ruota con dodici settori">{''.join(parts)}
      <circle cx="200" cy="200" r="177" fill="none" stroke="#fff" stroke-width="8"/>
      <circle cx="200" cy="200" r="29" fill="#172033" stroke="#fff" stroke-width="6"/>
      <circle cx="200" cy="200" r="8" fill="#F4B942"/>
    </svg></div></div>'''


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&display=swap');
.stApp { background: radial-gradient(circle at 50% 0%, #263653 0, #111827 48%, #080d18 100%); color:#f8fafc; }
.block-container { max-width: 760px; padding-top: 2.5rem; }
h1 { text-align:center; letter-spacing:-1px; font-weight:800; }
.subtitle { text-align:center; color:#aab7cc; margin:-8px 0 20px; }
.wheel-wrap { width:min(82vw, 520px); aspect-ratio:1; margin:14px auto 26px; position:relative; filter:drop-shadow(0 18px 24px rgba(0,0,0,.38)); }
.wheel { width:100%; height:100%; transition:transform 4.2s cubic-bezier(.12,.76,.18,1); }
.wheel svg { width:100%; height:100%; display:block; }
.label { fill:#fff; font:800 12px Manrope, sans-serif; text-anchor:middle; dominant-baseline:middle; letter-spacing:1px; }
.pointer { position:absolute; z-index:2; left:50%; top:-9px; transform:translateX(-50%); width:0; height:0; border-left:17px solid transparent; border-right:17px solid transparent; border-top:40px solid #f8fafc; filter:drop-shadow(0 3px 3px rgba(0,0,0,.45)); }
.legend { display:flex; justify-content:center; gap:18px; flex-wrap:wrap; color:#cbd5e1; font-size:13px; margin:4px 0 20px; }
.dot { display:inline-block; width:11px; height:11px; border-radius:50%; margin-right:6px; vertical-align:-1px; }
.stButton button { width:100%; border:0; border-radius:14px; padding:13px 16px; background:linear-gradient(135deg,#f59e0b,#f97316); color:#111827; font-size:18px; font-weight:800; box-shadow:0 8px 20px rgba(249,115,22,.25); }
.stButton button:hover { background:linear-gradient(135deg,#fbbf24,#fb923c); color:#111827; }
.result { text-align:center; padding:15px 20px; border:1px solid #334155; border-radius:16px; background:rgba(15,23,42,.72); margin-top:18px; }
.result strong { font-size:24px; display:block; margin-top:4px; }
</style>
""", unsafe_allow_html=True)

st.title("🎡 Ruota della fortuna")
st.markdown('<div class="subtitle">Gira la ruota e scopri il colore estratto</div>', unsafe_allow_html=True)

if "rotation" not in st.session_state:
    st.session_state.rotation = 0
    st.session_state.result = None

if st.button("GIRA LA RUOTA  ✦"):
    winner = random.randrange(N)
    # Il centro del settore vincente deve arrivare sotto il puntatore in alto.
    target = 360 - (winner * 360 / N + 180 / N)
    st.session_state.rotation += 360 * random.randint(5, 8) + target
    st.session_state.result = LABELS[winner]

st.markdown(wheel_svg(st.session_state.rotation), unsafe_allow_html=True)
st.markdown('''<div class="legend"><span><i class="dot" style="background:#2563EB"></i>6 blu</span><span><i class="dot" style="background:#16A34A"></i>4 verdi</span><span><i class="dot" style="background:#DC2626"></i>2 rossi</span></div>''', unsafe_allow_html=True)

if st.session_state.result:
    st.markdown(f'<div class="result">Hai estratto<strong>{st.session_state.result}</strong></div>', unsafe_allow_html=True)
