#!/usr/bin/env python3
"""Build logo-lab/finalists.html — self-contained roster of the 6 finalist marks."""
import base64, io, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, "logo-lab")

def data_uri(name, size=480):
    im = Image.open(os.path.join(LAB, name + ".png")).convert("RGB")
    im = im.resize((size, size), Image.LANCZOS)
    im = im.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE).convert("P")
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    b = buf.getvalue()
    return "data:image/png;base64," + base64.b64encode(b).decode(), len(b)

MARKS = [
    dict(key="v2a", name="V2A", tag="THE ORIGINAL", accent="#0E7C78",
         spec="Gentle wave · simple flat bell · single teal",
         note="The one you called \u201cabsolutely crushed it.\u201d Calm, flowing, the purest form of the idea \u2014 the mark that started the wave direction."),
    dict(key="v2d", name="V2D", tag="TWO-COLOUR", accent="#E4572E",
         spec="Heartbeat spike · flat-lying elliptical bell · coral + teal, split at the spike",
         note="The heartbeat with drama: coral rises into the spike, teal falls away. The only two-colour mark left in the running."),
    dict(key="v2e", name="V2E", tag="PREV. RECOMMENDATION", accent="#0E7C78",
         spec="Heartbeat spike · flat-lying elliptical bell · single teal",
         note="V2D in one ink. The previous read: one colour moves the emphasis onto the shape \u2014 more premium, easier to reproduce (one ink, one favicon, one embroidery)."),
    dict(key="v4a", name="V4A", tag="3D DRUM BELL", accent="#0E7C78",
         spec="Heartbeat spike · candidate-3 drum bell (rim + side wall) · single teal",
         note="The heartbeat with the exact bell you kept asking for \u2014 the cylindrical drum resting at an angle, drawn in perspective, no shading."),
    dict(key="v4b", name="V4B", tag="BOTH TERMINALS 3D", accent="#0E7C78",
         spec="Heartbeat spike · drum bell + 3D socket, matched perspective · single teal",
         note="Bell and socket as a matched pair of machined parts. The most \u201cinstrument\u201d of the six \u2014 and the busiest."),
    dict(key="v5", name="V5", tag="THE OWED ONE · NEW", accent="#0E7C78", hero=True,
         spec="Gentle wave (no spike) · candidate-3 drum bell · single teal",
         note="The one that was never delivered: the original wave you loved, carrying the exact 3D bell from candidate 3. Calm body, sculpted head. Your last request, finally answered."),
]

cards = []
for m in MARKS:
    uri, nbytes = data_uri(m["key"])
    hero_cls = " hero" if m.get("hero") else ""
    cards.append(f"""
  <div class="card{hero_cls}">
    <div class="card-head"><span class="chip" style="background:{m['accent']}">{m['tag']}</span></div>
    <div class="mark"><img data-src="{m['key']}" alt="{m['name']} — Medchanic.MD logo candidate"></div>
    <div class="meta">
      <div class="mname">{m['name']}</div>
      <div class="mspec">{m['spec']}</div>
      <div class="mnote">{m['note']}</div>
      <div class="ctx">
        <div class="ctx-item"><div class="ig"><img data-src="{m['key']}" alt=""></div><span>Instagram</span></div>
        <div class="ctx-item"><div class="tab"><span class="tabico"><img data-src="{m['key']}" alt=""></span><span class="tabtxt">Medchanic.MD</span></div><span>Browser tab · 16px</span></div>
        <div class="ctx-item"><div class="dark"><img data-src="{m['key']}" alt=""></div><span>Dark surface</span></div>
      </div>
    </div>
  </div>""")

jsdict = ",".join(f'"{k}":"{data_uri(k)[0]}"' for k in [m["key"] for m in MARKS])
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Medchanic.MD — Logo Finalists</title>
<style>
  :root {{
    --paper:#F3EFE6; --paper2:#ECE6D9; --ink:#141311; --teal:#0E7C78; --coral:#E4572E; --amber:#EFA21B;
    --rule:#D8D1C2; --mut:#6E675C;
    --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
    --serif:"Instrument Serif","Iowan Old Style",Georgia,"Times New Roman",serif;
  }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--paper); color:var(--ink); font-family:var(--sans); padding:48px 20px 80px; }}
  .wrap {{ max-width:1180px; margin:0 auto; }}
  .eyebrow {{ font-size:12px; letter-spacing:.22em; color:var(--teal); font-weight:700; }}
  h1 {{ font-family:var(--serif); font-style:italic; font-weight:400; font-size:clamp(34px,5vw,54px); margin:10px 0 6px; }}
  .sub {{ color:var(--mut); font-size:15.5px; max-width:760px; line-height:1.55; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(330px,1fr)); gap:22px; margin-top:34px; }}
  .card {{ background:#FBF8F1; border:1px solid var(--rule); border-radius:14px; overflow:hidden; display:flex; flex-direction:column; }}
  .card.hero {{ border:2px solid var(--teal); box-shadow:0 10px 30px rgba(14,124,120,.13); }}
  .card-head {{ display:flex; justify-content:flex-end; padding:12px 14px 0; }}
  .chip {{ color:#FBF8F1; font-size:10px; font-weight:800; letter-spacing:.14em; padding:5px 10px; border-radius:999px; }}
  .mark {{ padding:4px 26px 0; }}
  .mark img {{ width:100%; height:auto; display:block; border-radius:10px; }}
  .meta {{ padding:16px 22px 22px; }}
  .mname {{ font-size:22px; font-weight:800; letter-spacing:.01em; }}
  .mspec {{ font-size:12px; color:var(--teal); font-weight:700; margin-top:3px; letter-spacing:.02em; }}
  .mnote {{ font-size:13.5px; color:var(--mut); line-height:1.55; margin-top:9px; }}
  .ctx {{ display:flex; gap:18px; margin-top:16px; padding-top:14px; border-top:1px dashed var(--rule); }}
  .ctx-item {{ display:flex; flex-direction:column; align-items:center; gap:7px; font-size:10px; letter-spacing:.08em; color:var(--mut); font-weight:600; }}
  .ig {{ width:56px; height:56px; border-radius:50%; overflow:hidden; border:1px solid var(--rule); }}
  .ig img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .tab {{ width:132px; background:#DEDEDE; border-radius:9px 9px 0 0; padding:6px 9px 6px 7px; display:flex; align-items:center; gap:6px; }}
  .tabico {{ width:16px; height:16px; flex:0 0 16px; border-radius:3px; overflow:hidden; }}
  .tabico img {{ width:16px; height:16px; display:block; }}
  .tabtxt {{ font-size:10.5px; color:#3D3D3D; white-space:nowrap; overflow:hidden; }}
  .dark {{ width:56px; height:56px; border-radius:12px; background:var(--ink); display:flex; align-items:center; justify-content:center; }}
  .dark img {{ width:40px; height:40px; border-radius:7px; display:block; }}
  .read {{ margin-top:44px; background:#FBF8F1; border:1px solid var(--rule); border-radius:14px; padding:28px 30px; }}
  .read h2 {{ font-family:var(--serif); font-style:italic; font-weight:400; font-size:30px; margin-bottom:14px; }}
  .read p {{ font-size:14.5px; line-height:1.65; color:#3E3A32; margin-bottom:12px; max-width:900px; }}
  .read b {{ color:var(--ink); }}
  .read .teal {{ color:var(--teal); font-weight:700; }}
  .foot {{ margin-top:26px; text-align:center; color:var(--mut); font-size:13px; }}
  .foot b {{ color:var(--ink); }}
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">MEDCHANIC.MD · ICON DECISION · 23 OCT 2026</div>
  <h1>The finalists.</h1>
  <p class="sub">Six marks, one decision. All regenerated fresh in this session from the exact construction specs \u2014 including <b>V5</b>, the version that was owed: the original gentle wave carrying candidate&nbsp;3's drum bell. Check each at full size, then as an Instagram circle, a 16&nbsp;px browser tab, and on a dark surface. Then say the name.</p>
  <div class="grid">{''.join(cards)}
  </div>

  <div class="read">
    <h2>My read.</h2>
    <p><b>The two families.</b> V2A and V5 are the calm wave \u2014 steady, breathing, confident. V2D, V2E, V4A and V4B are the heartbeat \u2014 one moment of drama in a calm line. The bell question is now really a question of <b>personality</b>: the flat ring (V2A) is quiet and geometric; the elliptical disc (V2D/V2E) adds subtle depth; the drum (V4A/V4B/V5) is the sculptural one you kept coming back to \u2014 it finally reads unmistakably as a stethoscope.</p>
    <p><b>V5 is the synthesis.</b> It carries the exact bell you asked for, on the exact wave you loved \u2014 the first mark that is fully yours, with no compromise on either component. If the bell feels heavy against the calm wave, V4A is the same bell with the spike giving the mark a second focal point; if the drum is too literal, V2E is the elegant one-colour minimal take.</p>
    <p><b>The 16&nbsp;px truth.</b> Whatever wins, the spike (if any) will dominate at favicon size and the bell will shrink to a blob \u2014 that is normal and fixable: the production mark gets a dedicated simplified 16&nbsp;px cut (spike amplitude compressed \u224825%, bell reduced to its silhouette). Every finalist here survives that treatment.</p>
    <p><b>My call, if you want it:</b> <span class="teal">V5</span> \u2014 the calm wave with the drum bell \u2014 with V4A as the close second if you want the ECG energy. Two colours (V2D) is beautiful but busier; one ink is the premium move.</p>
    <p>After you pick, the rollout is: browser-tab favicon on every page, the loading animation inspired by the mark (noted for later), social avatars, and the mark replaces the old wrench in nav, footer and the landing page's part-6 screenshot.</p>
  </div>

  <script>
  var IMGS = {{ {jsdict} }};
  document.querySelectorAll("[data-src]").forEach(function(el){{ el.src = IMGS[el.getAttribute("data-src")]; }});
  </script>
  <div class="foot">Say the name \u2014 <b>\u201cV5\u201d</b>, <b>\u201cV4A\u201d</b>\u2026 \u2014 and we lock it and move to the next thing. &nbsp;·&nbsp; Regenerated 2026-10-23 · single-file roster, works offline.</div>
</div>
</body>
</html>"""

out = os.path.join(LAB, "finalists.html")
with open(out, "w") as f:
    f.write(html)
print("written:", out, f"{os.path.getsize(out)//1024} KB")
