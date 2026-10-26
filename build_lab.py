#!/usr/bin/env python3
"""Build logo-lab/anastomosis-lab.html + anastomosis-lab.pdf — the 'Anastomosis logo lab' shortlist:
the two originals the founder pointed out (knot, A), their upgrades, the infinity concepts,
and new concepts with mass. All on the warm bone canvas."""
import base64, io, os, re
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"
STYLE_SRC = os.path.join(LAB, "picks.html")

MARKS = [
    ("dc-1.png",        "dc-1",   "The self-tying vessel",        "DC-1",   "The designer's cut: one continuous vessel — artery in through the golden ring, vein out. The infinity performing the anastomosis."),
    ("dc-2.png",        "dc-2",   "The name carries the loop",    "DC-2",   "The wordmark lockup: the two O's of anastOmosis are the loops — the name performing its own meaning."),
    ("wld-1.png",       "wld-1",  "The crossing",                  "WLD-1",  "Two vessels crossing at the centre, one gold suture ring, four open mouths \u2014 the surgical diagram become icon."),
    ("wld-2.png",       "wld-2",  "The ligature",                  "WLD-2",  "A and M sharing one stroke \u2014 a ligature: two letters anastomosed into one glyph."),
    ("wld-3.png",       "wld-3",  "The embrace",                   "WLD-3",  "Two S-curves completing one circle \u2014 the arterial and venous halves of one circulation."),
    ("wld-4.png",       "wld-4",  "The seam",                      "WLD-4",  "Crimson teeth interlocking petrol teeth \u2014 the mechanical anastomosis, one gold hand-stitch at the centre."),
    ("wld-5.png",       "wld-5",  "The bridge",                    "WLD-5",  "Two vertical vessels joined by a horizontal graft \u2014 the letter H as the bypass surgeons build."),
    ("wld-6.png",       "wld-6",  "The dovetail A",                "WLD-6",  "The initial split by a carpenter\u2019s dovetail seam \u2014 the mechanic\u2019s truth wearing the surgeon\u2019s letter."),
    ("wld-7.png",       "wld-7",  "The keystone",                  "WLD-7",  "Two arch halves locked by one gold keystone \u2014 the arch stands only because the join holds."),
    ("wld-8.png",       "wld-8",  "The junction",                  "WLD-8",  "Two tracks merging into one \u2014 the railroad anastomosis, gold pin at the switch."),
    ("wld-9.png",       "wld-9",  "The coupling",                  "WLD-9",  "Two open tubes clasped mouth-to-mouth \u2014 the plumbing of the body as one fitting."),
    ("wld-10.png",      "wld-10", "The braid",                     "WLD-10", "Two vessels woven over and under \u2014 the oldest join humans know, bound in gold."),
    ("wld-11.png",      "wld-11", "The confluence",                "WLD-11", "Four vessels meeting at one golden node \u2014 the medical plus sign, drawn by circulation itself."),
    ("wld-12.png",      "wld-12", "The splice",                    "WLD-12", "Two ropes, six strands interwoven \u2014 the sailor\u2019s end-to-end anastomosis."),
    ("cr-7.png",        "cr-7",   "The crossing — ribbon twist",   "CR-7",   "The kept study: flat ribbons half-twisting through the crossing."),
    ("tex-1.png",       "tex-1",  "The crossing — two-tone",       "TEX-1",  "Same design, new skin: light and dark lengthwise tones — cylinder roundness, flat."),
    ("tex-2.png",       "tex-2",  "The crossing — hatch",          "TEX-2",  "Fine bone hatch lines — the vintage anatomical plate."),
    ("tex-3.png",       "tex-3",  "The crossing — sheen",          "TEX-3",  "One thin lighter line along each tube's upper edge."),
    ("tex-4.png",       "tex-4",  "The crossing — bands",          "TEX-4",  "Fine perpendicular bands — myelin segmentation."),
    ("tex-5.png",       "tex-5",  "The crossing — stipple",        "TEX-5",  "A fine scatter of lighter dots — stipple engraving."),
    ("tex-6.png",       "tex-6",  "The crossing — crosshatch",     "TEX-6",  "Two directions of fine bone lines — classical engraving."),
    ("bt-1.png",        "bt-1",   "The braid — two-tone",          "BT-1",   "The braid, new skin: light and dark lengthwise tones through the weave."),
    ("bt-2.png",        "bt-2",   "The braid — hatch",             "BT-2",  "Fine bone hatch lines following the weave."),
    ("bt-3.png",        "bt-3",   "The braid — sheen",             "BT-3",  "One thin lighter line faithful through every crossing."),
    ("bt-4.png",        "bt-4",   "The braid — bands",             "BT-4",  "Fine perpendicular bands — myelin segmentation through the weave."),
    ("bt-5.png",        "bt-5",   "The braid — stipple",           "BT-5",  "A fine scatter of lighter dots through the weave."),
    ("bt-6.png",        "bt-6",   "The braid — crosshatch",        "BT-6",  "Two directions of fine bone lines on the woven tubes."),
    ("ig-1.png",        "ig-1",   "The emblem — in the wild",      "IG-1",   "The founder's pick: the vessel-join loop as the avatar — artery loop, vein loop, golden crossing, born in the profile view."),
    ("avi-1.png",       "avi-1",  "The AV infinity — the join",     "AVI-1", "The infinity IS the anastomosis: its ends fuse into the artery and the vein — suture rings at both junctions."),
    ("avi-2.png",       "avi-2",  "The AV infinity — the flow",    "AVI-2", "Artery flows into the left loop, vein receives the right — blood changes sides at the golden crossing."),
    ("avi-3.png",       "avi-3",  "The AV infinity — minimal",     "AVI-3", "The 16 px cut: A skeleton, the gold loop bridging artery to vein."),
    ("avi-5.png",       "avi-5",  "The AV infinity — emblem",      "AVI-5", "No letter, pure symbol: an artery and a vein joined by the endless loop."),
    ("lv-1.png",        "lv-1",   "The living A — definitive",     "LV-1", "The thesis: pure letter skeleton, vessel material — organic curves, taper, the branch, open lumen mouths."),
    ("lv-2.png",        "lv-2",   "The living A — infinite crossbar", "LV-2", "The vessel A with the infinity as its crossbar, in gold — the loop held in the letter's own anatomy."),
    ("lv-3.png",        "lv-3",   "The living A — looped feet",    "LV-3", "The vessel A with quiet loops at its feet — the infinity carried at the base."),
    ("lv-4.png",        "lv-4",   "The living A — vivid",          "LV-4", "The recognition test: true arterial red and venous blue — the universal diagram colours."),
    ("lv-5.png",        "lv-5",   "The living A — anatomical hero","LV-5", "Real 3D vessels: organic tubes, the branch with interior depth, the gold suture bar."),
    ("ac-1.png",        "ac-1",   "The clear A — definitive",      "AC-1", "The two non-negotiables: a textbook A readable in half a second, and strokes that are unmistakably vessels — tube mouths, lumens."),
    ("ac-2.png",        "ac-2",   "The clear A — vessel detail",   "AC-2", "Medical-illustration grade: wall-thickness lines, pronounced lumens, one true branch stub."),
    ("ac-3.png",        "ac-3",   "The clear A — minimal",         "AC-3", "The 16 px cut — the letter, the loops, the lumen dots."),
    ("ac-4.png",        "ac-4",   "The clear A — rendered",        "AC-4", "Literal 3D vessels: real tubes, open mouths with interior depth, gold suture ring."),
    ("ac-5.png",        "ac-5",   "The infinite crossbar",         "AC-5", "The clearest integration: a textbook A whose crossbar IS the infinity — drawn in gold."),
    ("ais-1.png",       "ais-1",  "The A-Infinity — your style",  "AIS-1", "The founder's fusion, drawn in the founder's style — composition from one, aesthetic from the other."),
    ("ais-2.png",       "ais-2",  "Your style, our blood",       "AIS-2", "The style you attached, carrying the arteriovenous palette through it."),
    ("ais-3.png",       "ais-3",  "Your style — minimal",        "AIS-3", "The 16 px cut in your style — fewest strokes, both readings alive."),
    ("ais-4.png",       "ais-4",  "Your style — hero",           "AIS-4", "The richest expression of your style on the fused form — the launch asset."),
    ("ainf-1.png",      "ainf-1",  "The A-Infinity — definitive",   "AINF-1", "The founder's fusion, elevated: the A and the infinity as one vessel form — gold suture at the crossing."),
    ("ainf-2.png",      "ainf-2",  "The A-Infinity — sculptural",  "AINF-2", "The fusion extruded into depth — walls, lumens in perspective, two-tone carving."),
    ("ainf-3.png",      "ainf-3",  "The A-Infinity — rendered",    "AINF-3", "The flagship render: studio light, true volume, the gold ring at the junction."),
    ("ainf-4.png",      "ainf-4",  "The A-Infinity — minimal",     "AINF-4", "The 16 px cut — fewest strokes that still read as both A and infinity."),
    ("a-top.png",       "a-top",   "The A — definitive",                  "A-TOP",  "The letter with unmistakable vessel edges: open tube tips, visible lumens, the apex merge."),
    ("bold-3.png",      "a",       "The A — original",                    "A",      "The one you pointed out — edges that read as vessels."),
    ("a-3d.png",        "a-3d",    "The A — sculptural",                  "A-3D",   "The letter extruded into depth: vessels with walls, lumens in perspective."),
    ("a-apex.png",      "a-apex",  "The A — apex junction",               "A-PX",   "The apex IS the anastomosis: two vessels joined by a gold suture ring."),
    ("a-refined.png",   "a-ref",   "The A — refined",                     "A-R",    "Thicker strokes, cleaner merge, premium cut."),
    ("a-vessel.png",    "a-ves",   "The A — one vessel",                  "A-V",    "The A as a single folded vessel: artery in, graft at the peak, vein out."),
    ("a-loop.png",      "a-loop",  "The A — looped",                      "A-L",    "The A whose feet curl into two infinite loops."),
    ("inf-refined.png", "inf-r",   "The endless anastomosis — definitive","INF-R",  "The infinity, perfected: fuller loops, thicker tube, a gold band wrapping the crossing."),
    ("inf-1.png",       "inf-1",   "The endless anastomosis — original",  "INF-1",  "The one you liked — crimson loop, petrol loop, golden suture."),
    ("inf-3d.png",      "inf-3d",  "The endless anastomosis — sculptural","INF-3D", "The infinity with real walls and depth — flat two-tone carving."),
    ("inf-render.png",  "inf-rnd", "The endless anastomosis — rendered",  "INF-RND","The flagship render: studio light, true volume, the gold ring at the heart."),
    ("bold-1.png",      "knot",    "The knot",                            "KNOT",   "Two vessels tied in the surgeon's square knot."),
    ("knot-refined.png","knot-r",  "The knot — tightened",                "KNOT-R", "Reduced to its essential crossings."),
    ("chain.png",       "chain",   "The links",                           "CHAIN",  "Two chain links woven through each other."),
    ("drops.png",       "drops",   "The drops",                           "DROPS",  "Two drops merging at a golden seam."),
]

# ---------------------------------------------------------------- HTML -------
src = open(STYLE_SRC).read()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
style = re.sub(r'\s*--[a-z0-9_]+:url\("data:image/[a-z]+;base64,[A-Za-z0-9+/=]+"\);?', "", style)
style = re.sub(r"\n\.[a-z0-9_]+\{background-image:var\(--[a-z0-9_]+\)\}", "", style)

def jpeg_uri(path, size=None, q=90):
    im = Image.open(path).convert("RGB")
    if size:
        im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

vars_css = [f'  --{var}:url("{jpeg_uri(os.path.join(LAB, rel), 440)}");' for rel, var, *_ in MARKS]
classes_css = [f".{var}{{background-image:var(--{var})}}" for rel, var, *_ in MARKS]

def card(var, title, num, note):
    return f'''  <article class="card">
    <div class="chead"><h2>{title}</h2><span class="num">{num}</span></div>
    <div class="two">
      <div class="cell">
        <div class="lbl">Instagram</div>
        <div class="ig">
          <div class="igh">&larr; <b>anastomosis.md</b></div>
          <div class="igb"><div class="av {var}"></div>
            <div class="igm"><b>Anastomosis.MD</b><span><b>2</b> posts &nbsp; <b>1,204</b> followers</span></div></div>
          <div class="igbio"><b>Anastomosis.MD</b><br>Two vessels. One mind.</div>
          <div class="igp {var}"></div>
        </div>
      </div>
      <div class="cell">
        <div class="lbl">Product bar</div>
        <div class="nav"><i class="mk {var}"></i><b>Anastomosis</b><em>MD</em><span class="st">11-day streak</span></div>
        <div class="lbl">Size ladder</div>
        <div class="ladder"><i class="lg {var}" style="width:54px;height:54px"></i><i class="lg {var}" style="width:40px;height:40px"></i><i class="lg {var}" style="width:30px;height:30px"></i><i class="lg {var}" style="width:21px;height:21px"></i><i class="lg {var}" style="width:15px;height:15px"></i></div>
        <div class="lbl">Browser tab</div>
        <div class="tabs">
          <div class="tab on"><i class="ti {var}"></i><span>Anastomosis &mdash; ev&hellip;</span></div>
          <div class="tab"><i class="ti {var}"></i><span>Dashboard</span></div>
        </div>
        <div class="tabbar"><div class="addr">anastomosis-md.appwrite.network</div></div>
      </div>
    </div>
    <div class="note">{note}</div>
  </article>'''

cards = [card(var, title, num, note) for _, var, title, num, note in MARKS]

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anastomosis logo lab</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{style}
{chr(10).join(classes_css)}
</style></head><body>
<h1>Anastomosis logo lab</h1>
<p class="sub">{len(MARKS)} marks &middot; instagram &middot; product bar &middot; size ladder &middot; browser tab</p>
<div class="grid">
{chr(10).join(cards)}
</div>
<p class="sub" style="margin-top:22px">avi leads &mdash; the infinity IS the anastomosis &nbsp;/&nbsp; lv &middot; the living A &nbsp;/&nbsp; ac &middot; the clear series &nbsp;/&nbsp; the fusion &amp; families &nbsp;/&nbsp; the rest held &nbsp;/&nbsp; rendered style dropped &mdash; avatar-first from here</p>
<p class="sub" style="margin-top:8px">say the word and the winner gets the rollout</p>
</body></html>'''

html = html.replace(":root{\n", ":root{\n" + "\n".join(vars_css) + "\n", 1)
out_html = os.path.join(LAB, "anastomosis-lab.html")
open(out_html, "w").write(html)
print("written:", out_html, os.path.getsize(out_html) // 1024, "KB")

# ---------------------------------------------------------------- PDF --------
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas as _c

W, H = A4
BONE, CARD = HexColor("#F7F3EB"), HexColor("#FFFDF8")
INK, INK2, INK3 = HexColor("#101418"), HexColor("#4A4741"), HexColor("#8A857A")
RULE, PETROL, PETROL2 = HexColor("#E2DCD0"), HexColor("#1B4E5F"), HexColor("#143A47")
M = 57

def tracked(c, x, y, text, font, size, color, cs=1.4, center=False):
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(cs)
    t.setFillColor(color)
    w = c.stringWidth(text, font, size) + cs * (len(text) - 1)
    t.setTextOrigin(x - (w / 2 if center else 0), y)
    t.textOut(text)
    c.drawText(t)

_pdf_cache_dir = "/tmp/pdfcache"
os.makedirs(_pdf_cache_dir, exist_ok=True)

def img(path):
    """PDF images at 800px JPEG — keeps the PDF lean."""
    key = os.path.splitext(path)[0].replace("/", "_")
    cached = os.path.join(_pdf_cache_dir, key + ".jpg")
    if not os.path.exists(cached):
        im = Image.open(os.path.join(LAB, path)).convert("RGB")
        if max(im.size) > 800:
            im = im.resize((800, 800), Image.LANCZOS)
        im.save(cached, "JPEG", quality=85, optimize=True)
    return ImageReader(cached)

pdf_path = os.path.join(LAB, "anastomosis-lab.pdf")
c = _c.Canvas(pdf_path, pagesize=A4)
c.setTitle("Anastomosis logo lab")
c.setAuthor("Anastomosis.MD")

# cover
c.setFillColor(BONE); c.rect(0, 0, W, H, stroke=0, fill=1)
tracked(c, M, H - 78, "ANASTOMOSIS.MD · THE LOGO LAB · 23 OCT 2026", "Helvetica-Bold", 8, PETROL, 1.6)
c.setFillColor(INK); c.setFont("Times-BoldItalic", 44)
c.drawString(M, H - 136, "Anastomosis logo lab.")
c.setFillColor(INK2); c.setFont("Helvetica", 10.5)
for i, line in enumerate([
    "Sixty-five marks for the new name: the designer's cut, the wild waves, and",
    "their texture studies — then the founder's pick, the AV infinity, the living",
    "A, and the rest. One lab, one decision at the end of it.",
]):
    c.drawString(M, H - 164 - i * 16, line)
tw, gap = 85, 14
x0 = (W - (5 * tw + 4 * gap)) / 2
rows = [MARKS[i:i + 5] for i in range(0, len(MARKS), 5)]
ytop = 310
for row in rows:
    total = len(row) * tw + (len(row) - 1) * gap
    x = (W - total) / 2
    for rel, var, title, num, note in row:
        c.setFillColor(CARD); c.setStrokeColor(RULE); c.setLineWidth(1)
        c.roundRect(x, ytop, tw, tw, 8, stroke=1, fill=1)
        c.drawImage(img(rel), x + 6, ytop + 6, tw - 12, tw - 12, mask="auto")
        tracked(c, x + tw / 2, ytop - 18, num, "Helvetica-Bold", 8, PETROL2, 1.2, center=True)
        x += tw + gap
    ytop -= 84
c.setStrokeColor(RULE); c.setLineWidth(1); c.line(M, ytop + 44, W - M, ytop + 44)
tracked(c, W / 2, 40, "ANASTOMOSIS.MD — TWO VESSELS. ONE MIND.", "Helvetica-Bold", 7, INK3, 1.8, center=True)
c.showPage()

# one page per mark
for idx, (rel, var, title, num, note) in enumerate(MARKS, start=1):
    c.setFillColor(BONE); c.rect(0, 0, W, H, stroke=0, fill=1)
    tracked(c, M, H - 64, "ANASTOMOSIS.MD · THE LOGO LAB", "Helvetica-Bold", 8, PETROL, 1.6)
    chip_w = max(34, c.stringWidth(num, "Helvetica-Bold", 8) + 20)
    c.setFillColor(HexColor("#DCE8EC"))
    c.roundRect(W - M - chip_w, H - 74, chip_w, 18, 4, stroke=0, fill=1)
    tracked(c, W - M - chip_w / 2, H - 68.5, num, "Helvetica-Bold", 8, PETROL2, 1.2, center=True)
    csz = 430
    cx, cy = (W - csz) / 2, H - 108 - csz
    c.setFillColor(CARD); c.setStrokeColor(RULE); c.setLineWidth(1)
    c.roundRect(cx, cy, csz, csz, 14, stroke=1, fill=1)
    msz = 356
    c.drawImage(img(rel), cx + (csz - msz) / 2, cy + (csz - msz) / 2, msz, msz, mask="auto")
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(W / 2, cy - 40, title)
    c.setFillColor(INK2); c.setFont("Helvetica", 11)
    for i, line in enumerate(simpleSplit(note, "Helvetica", 11, 440)[:2]):
        c.drawCentredString(W / 2, cy - 64 - i * 15, line)
    sizes = [54, 40, 30, 21, 15]
    lgap = 16
    total = sum(sizes) + lgap * (len(sizes) - 1)
    lx = (W - total) / 2
    for s in sizes:
        c.drawImage(img(rel), lx, 150, s, s, mask="auto")
        lx += s + lgap
    tracked(c, W / 2, 122, "SIZE LADDER — 54 / 40 / 30 / 21 / 15 PX", "Helvetica-Bold", 6.5, INK3, 1.4, center=True)
    tracked(c, W / 2, 40, f"ANASTOMOSIS.MD · THE LOGO LAB · {idx} / {len(MARKS)}", "Helvetica-Bold", 7, INK3, 1.8, center=True)
    c.showPage()

c.save()
print("written:", pdf_path, os.path.getsize(pdf_path) // 1024, "KB")
