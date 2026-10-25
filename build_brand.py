#!/usr/bin/env python3
"""Build logo-lab/anastomosis-brand.html — the Anastomosis.MD brand system:
palette tokens (with 1:1 mapping to the current site tokens), the five marks,
context tests, and a re-themed UI preview in the new palette."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, size=None, q=90):
    im = Image.open(os.path.join(LAB, name)).convert("RGB")
    if size:
        im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

hero = uri("anastomosis-6.png", 640)
dark = uri("anastomosis-7.png", 460)
seam = uri("anastomosis-8.png", 460)
circle = uri("anastomosis-9.png", 460)
render = uri("anastomosis-10.png", 460)
hero_s = uri("anastomosis-6.png", 240)
knot = uri("bold-1.png", 640)
bowtie = uri("bold-2.png", 460)
letA = uri("bold-3.png", 460)
union = uri("bold-4.png", 460)
knot_dark = uri("bold-5.png", 460)
union_dark = uri("bold-6.png", 460)
knot_s = uri("bold-1.png", 240)

SWATCHES = [
    ("Bone", "#F7F3EB", "the field — paper, warmed and whitened"),
    ("Ink", "#101418", "the text and the merged vessel — graphite, blue-undertoned"),
    ("Arterial crimson", "#B5342A", "the artery — the living accent, replaces coral"),
    ("Venous petrol", "#1B4E5F", "the vein — the primary brand colour, replaces teal"),
    ("Old gold", "#C9973C", "the suture — the rare accent, replaces amber"),
]

MAPPING = [
    ("--paper #F3EFE6", "--bone #F7F3EB", "backgrounds"),
    ("--ink #141311", "--ink #101418", "text"),
    ("--teal #0E7C78", "--petrol #1B4E5F", "primary actions, links, good data"),
    ("--coral #E4572E", "--crimson #B5342A", "problems, wrong answers, energy"),
    ("--amber #EFA21B", "--gold #C9973C", "watch-outs, highlights, the suture"),
]

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anastomosis.MD — the brand system</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bone:#F7F3EB; --card:#FFFDF8; --ink:#101418; --ink2:#4A4741; --ink3:#8A857A; --rule:#E2DCD0;
  --crimson:#B5342A; --petrol:#1B4E5F; --gold:#C9973C;
  --sans:'Inter',system-ui,sans-serif; --serif:'Instrument Serif',Georgia,serif; --mono:'JetBrains Mono',monospace;
}}
body{{background:var(--bone);color:var(--ink);font-family:var(--sans);padding:48px 22px 90px}}
.wrap{{max-width:1100px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:var(--petrol);font-weight:700;text-transform:uppercase}}
h1{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(36px,5vw,60px);margin:10px 0 10px}}
.sub{{color:var(--ink3);font-size:15px;line-height:1.65;max-width:760px;margin-bottom:44px}}
.sub b{{color:var(--ink2)}}
h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:32px;margin:56px 0 18px}}
/* palette */
.swatches{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}}
.sw{{background:var(--card);border:1px solid var(--rule);border-radius:12px;overflow:hidden}}
.sw .chip{{height:86px}}
.sw .meta{{padding:12px 14px}}
.sw .nm{{font-size:13.5px;font-weight:800}}
.sw .hx{{font-family:var(--mono);font-size:10.5px;color:var(--ink3);margin-top:2px}}
.sw .role{{font-size:11px;color:var(--ink3);margin-top:6px;line-height:1.5}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--rule);border-radius:12px;overflow:hidden;margin-top:16px}}
tr{{border-bottom:1px solid var(--rule)}} tr:last-child{{border-bottom:none}}
td{{padding:10px 16px;font-size:12.5px;font-family:var(--mono);color:var(--ink2)}}
td:last-child{{font-family:var(--sans);color:var(--ink3)}}
/* marks */
.herowrap{{background:var(--card);border:1px solid var(--rule);border-radius:16px;padding:34px;display:grid;grid-template-columns:minmax(260px,420px) 1fr;gap:34px;align-items:center}}
@media(max-width:820px){{.herowrap{{grid-template-columns:1fr}}}}
.herowrap img{{width:100%;border-radius:12px;display:block}}
.heronote{{font-size:14px;color:var(--ink2);line-height:1.7}}
.heronote b{{color:var(--ink)}}
.ctx{{display:flex;gap:20px;margin-top:20px;align-items:flex-end;flex-wrap:wrap}}
.ctx-item{{display:flex;flex-direction:column;align-items:center;gap:8px;font-size:9.5px;letter-spacing:.1em;color:var(--ink3);font-weight:700;font-family:var(--mono)}}
.ig{{width:64px;height:64px;border-radius:50%;overflow:hidden;border:1px solid var(--rule)}}
.ig img{{width:100%;height:100%;object-fit:cover;display:block}}
.tab{{width:150px;background:#DEDEDE;border-radius:9px 9px 0 0;padding:6px 9px;display:flex;align-items:center;gap:6px}}
.tab img{{width:16px;height:16px;border-radius:3px}}
.tab span{{font-size:10.5px;color:#3C3C3C;white-space:nowrap}}
.ladder{{display:flex;gap:10px;align-items:flex-end}}
.ladder img{{border-radius:5px}}
.grid4{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:16px}}
.g4{{background:var(--card);border:1px solid var(--rule);border-radius:14px;padding:16px}}
.g4 img{{width:100%;border-radius:9px;display:block}}
.g4 .cap{{font-size:11px;color:var(--ink3);margin-top:10px;font-family:var(--mono);letter-spacing:.08em;text-transform:uppercase;font-weight:700}}
/* UI preview */
.uiprev{{background:var(--card);border:1px solid var(--rule);border-radius:16px;padding:26px;margin-top:16px}}
.nav{{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--bone);border:1px solid var(--rule);border-radius:10px}}
.nav img{{width:26px;height:26px;border-radius:6px}}
.nav b{{font-size:15px;font-weight:800;letter-spacing:-.02em}}
.nav .md{{font-family:var(--mono);font-size:9px;background:var(--petrol);color:var(--bone);padding:2px 5px;border-radius:3px;letter-spacing:.08em;font-weight:700}}
.nav .streak{{margin-left:auto;font-family:var(--mono);font-size:9.5px;color:var(--ink3)}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:16px}}
.stat{{background:var(--bone);border:1px solid var(--rule);border-radius:10px;padding:14px 16px}}
.stat .v{{font-size:26px;font-weight:800;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.stat .v.pet{{color:var(--petrol)}} .stat .v.cri{{color:var(--crimson)}} .stat .v.gol{{color:var(--gold)}}
.stat .l{{font-family:var(--mono);font-size:8.5px;letter-spacing:.14em;color:var(--ink3);margin-top:4px;text-transform:uppercase}}
.ctcard{{background:var(--bone);border:1px solid var(--rule);border-radius:10px;padding:18px;margin-top:16px;max-width:420px}}
.ctcard .n{{font-size:52px;font-weight:800;letter-spacing:-.03em;line-height:1}}
.ctcard .nl{{font-family:var(--mono);font-size:9px;letter-spacing:.16em;color:var(--ink3);margin-top:6px}}
.bar{{height:5px;background:var(--rule);border-radius:99px;margin-top:14px;overflow:hidden}}
.bar i{{display:block;height:100%;width:62%;background:var(--petrol);border-radius:99px}}
.start{{display:block;width:100%;margin-top:14px;background:var(--petrol);color:var(--bone);border:none;border-radius:9px;padding:12px 0;font-size:13.5px;font-weight:700;font-family:var(--sans)}}
.exam{{margin-top:16px;background:var(--petrol);color:var(--bone);border-radius:8px;padding:9px 16px;font-family:var(--mono);font-size:10px;letter-spacing:.14em}}
.note{{margin-top:16px;border-left:3px solid var(--gold);background:var(--bone);padding:12px 16px;border-radius:0 8px 8px 0;font-size:13px;color:var(--ink2)}}
.foot{{margin-top:48px;font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--ink3);text-align:center;line-height:2}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE BRAND SYSTEM &middot; 23 OCT 2026</div>
  <h1>Two vessels. One brand.</h1>
  <p class="sub">With the colour cabinet open, the palette stopped being decoration and became the concept: <b>an arterial crimson vessel and a venous petrol vessel, merging into one graphite graft, sealed with a single golden suture</b> — the arteriovenous anastomosis that surgeons really build. Every colour has a job, and every job maps one-to-one onto the current site tokens: <b>re-theming the whole website is five hex values and one logo swap.</b></p>

  <h2>The palette.</h2>
  <div class="swatches">
    {''.join(f'<div class="sw"><div class="chip" style="background:{hx}"></div><div class="meta"><div class="nm">{nm}</div><div class="hx">{hx}</div><div class="role">{role}</div></div></div>' for nm, hx, role in SWATCHES)}
  </div>
  <table><tr><td><b>CURRENT TOKEN</b></td><td><b>NEW TOKEN</b></td><td><b>ROLE ON THE SITE</b></td></tr>
  {''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in MAPPING)}
  </table>

  <h2>The bold series — marks with mass.</h2>
  <div class="herowrap">
    <img src="{knot}" alt="The knot — two vessels tied together">
    <div>
      <p class="heronote"><b>The knot.</b> Two thick ropes — artery crimson and vein petrol — tied in the surgeon's square knot, a gold bead at the centre. The most surgical object there is, drawn with mass: a silhouette you could cut from paper with a knife and still recognize at 16 px. This is the series that answers "it looks like nothing" — filled forms, presence, weight.</p>
      <div class="ctx">
        <div class="ctx-item"><div class="ig"><img src="{knot_s}" alt=""></div>INSTAGRAM</div>
        <div class="ctx-item"><div class="tab"><img src="{knot_s}" alt=""><span>Anastomosis — Dashboa…</span></div>BROWSER TAB · 16 PX</div>
        <div class="ctx-item"><div class="ladder"><img src="{knot_s}" style="width:48px" alt=""><img src="{knot_s}" style="width:34px" alt=""><img src="{knot_s}" style="width:24px" alt=""><img src="{knot_s}" style="width:16px" alt=""></div>FAVICON LADDER</div>
      </div>
    </div>
  </div>
  <div class="grid4">
    <div class="g4"><img src="{bowtie}" alt=""><div class="cap">The bowtie — two bodies, one meeting point</div></div>
    <div class="g4"><img src="{letA}" alt=""><div class="cap">The A — a letterform that is an anastomosis</div></div>
    <div class="g4"><img src="{union}" alt=""><div class="cap">The union — two vessels, one golden chamber</div></div>
    <div class="g4"><img src="{knot_dark}" alt=""><div class="cap">The knot — night mode</div></div>
    <div class="g4"><img src="{union_dark}" alt=""><div class="cap">The union — night mode</div></div>
  </div>

  <h2>The line series — the quiet originals.</h2>
  <div class="herowrap">
    <img src="{hero}" alt="The Anastomosis mark — arteriovenous union">
    <div>
      <p class="heronote"><b>The arteriovenous union — the line cut.</b> The artery (crimson) and the vein (petrol) curve toward each other and merge into one graphite vessel — the graft — with a single golden suture at the junction. The mark a surgeon would recognize in one glance, drawn flat, bold, and quiet. Below: how it lives in the wild.</p>
      <div class="ctx">
        <div class="ctx-item"><div class="ig"><img src="{hero_s}" alt=""></div>INSTAGRAM</div>
        <div class="ctx-item"><div class="tab"><img src="{hero_s}" alt=""><span>Anastomosis — Dashboa…</span></div>BROWSER TAB · 16 PX</div>
        <div class="ctx-item"><div class="ladder"><img src="{hero_s}" style="width:48px" alt=""><img src="{hero_s}" style="width:34px" alt=""><img src="{hero_s}" style="width:24px" alt=""><img src="{hero_s}" style="width:16px" alt=""></div>FAVICON LADDER</div>
      </div>
    </div>
  </div>

  <h2>The family.</h2>
  <div class="grid4">
    <div class="g4"><img src="{dark}" alt=""><div class="cap">The dark hero — bone graft on ink</div></div>
    <div class="g4"><img src="{seam}" alt=""><div class="cap">The seam — artery and vein, gold sutures</div></div>
    <div class="g4"><img src="{circle}" alt=""><div class="cap">The circle — Willis, fed by both colors</div></div>
    <div class="g4"><img src="{render}" alt=""><div class="cap">The render — for hero moments</div></div>
  </div>

  <h2>The site, re-themed.</h2>
  <p class="sub" style="margin-bottom:0">Same components, same typography, same layout discipline — only the five tokens swapped. The claim to test: <b>still as professional, still as beautiful.</b></p>
  <div class="uiprev">
    <div class="nav"><img src="{hero_s}" alt=""><b>Anastomosis</b><span class="md">MD</span><span class="streak">11-DAY STREAK</span></div>
    <div class="stats">
      <div class="stat"><div class="v pet">2,000+</div><div class="l">QUESTIONS</div></div>
      <div class="stat"><div class="v">4,000+</div><div class="l">FLASHCARDS</div></div>
      <div class="stat"><div class="v gol">26</div><div class="l">SYSTEMS</div></div>
      <div class="stat"><div class="v cri">98.2%</div><div class="l">EXPLAINED DISTRACTORS</div></div>
    </div>
    <div class="ctcard">
      <div class="n">40</div>
      <div class="nl">QUESTIONS IN THIS BLOCK</div>
      <div class="bar"><i></i></div>
      <button class="start">Start block</button>
    </div>
    <div class="exam">SECTION 1 · 40 ITEMS · 60 MINUTES · MARKED 2</div>
    <div class="note"><b>What to fix next:</b> three systems are holding your score back — Cardiovascular, Renal, and the acid-base family. The suture is gold for a reason: one stitch, right where it matters.</div>
  </div>

  <div class="foot">ANASTOMOSIS.MD &middot; ARTERY MEETS VEIN &middot; FIVE TOKENS &middot; ONE STITCH<br>SAY THE WORD AND THE SITE GETS ITS NEW SKIN</div>
</div>
</body></html>'''

out = os.path.join(LAB, "anastomosis-brand.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
