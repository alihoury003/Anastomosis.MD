#!/usr/bin/env python3
"""Build logo-lab/picks.html (old pal's roster design) + logo-lab/picks.pdf.

Picks: candidate 1, 2C, 3, 4M (byte-exact from his roster) + V4B (original file).
HTML: his roster design cloned verbatim (Instagram mock / product bar / size ladder / browser tab).
PDF:  A4 print document — cover + one page per mark, brand palette, size ladder on every page.
"""
import base64, io, os, re
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"
SRC = "/tmp/arena-coding-uploads/roster.html"  # his original roster (still in uploads)

PICKS = [
    # (image file, css var, title, num, note)
    ("originals/candidate-1.jpg",  "mk_1",  "Wrench + scalpel",            "1",   "The original crossing."),
    ("originals/candidate-2c.jpg", "mk_2c", "Stethoscope + wrench",        "2C",  "Natural stethoscope: eartips, Y-join, one long supple tube."),
    ("originals/candidate-3.jpg",  "mk_3",  "Continuous implement",        "3",   "One tool: stethoscope at one end, wrench at the other. The bell every later mark borrowed."),
    ("originals/candidate-4m.jpg", "mk_4m", "The M — two tools (v1)",      "4M",  "Stethoscope left, wrench right."),
    ("v4b.png",                    "v4b",   "The heartbeat — twin drums",  "V4B", "Bell and socket as a matched pair of machined parts, in the same perspective."),
]

# ---------------------------------------------------------------- HTML -------
src = open(SRC).read()
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
style = re.sub(r"(\s*--mk_[a-z0-9]+:url\(\"data:image/[a-z]+;base64,)[A-Za-z0-9+/=]+(\"\);?)+", "", style)
style = re.sub(r"\n\.mk_[a-z0-9]+\{background-image:var\(--mk_[a-z0-9]+\)\}", "", style)

def jpeg_uri(path, size=None, q=90):
    im = Image.open(os.path.join(LAB, path)).convert("RGB")
    if size:
        im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

vars_css, classes_css = [], []
for rel, var, *_ in PICKS:
    if rel.endswith(".jpg"):            # his originals — byte-exact
        data = open(os.path.join(LAB, rel), "rb").read()
        uri = "data:image/jpeg;base64," + base64.b64encode(data).decode()
    else:                               # v4b original PNG -> his JPEG technique
        uri = jpeg_uri(rel, size=440)
    vars_css.append(f'  --{var}:url("{uri}");')
    classes_css.append(f".{var}{{background-image:var(--{var})}}")

def card(var, title, num, note):
    return f'''  <article class="card">
    <div class="chead"><h2>{title}</h2><span class="num">{num}</span></div>
    <div class="two">
      <div class="cell">
        <div class="lbl">Instagram</div>
        <div class="ig">
          <div class="igh">&larr; <b>medchanic.md</b></div>
          <div class="igb"><div class="av {var}"></div>
            <div class="igm"><b>Medchanic.MD</b><span><b>2</b> posts &nbsp; <b>1,204</b> followers</span></div></div>
          <div class="igbio"><b>Medchanic.MD</b><br>Mechanism-first exam prep</div>
          <div class="igp {var}"></div>
        </div>
      </div>
      <div class="cell">
        <div class="lbl">Product bar</div>
        <div class="nav"><i class="mk {var}"></i><b>Medchanic</b><em>MD</em><span class="st">11-day streak</span></div>
        <div class="lbl">Size ladder</div>
        <div class="ladder"><i class="lg {var}" style="width:54px;height:54px"></i><i class="lg {var}" style="width:40px;height:40px"></i><i class="lg {var}" style="width:30px;height:30px"></i><i class="lg {var}" style="width:21px;height:21px"></i><i class="lg {var}" style="width:15px;height:15px"></i></div>
        <div class="lbl">Browser tab</div>
        <div class="tabs">
          <div class="tab on"><i class="ti {var}"></i><span>Medchanic &mdash; ev&hellip;</span></div>
          <div class="tab"><i class="ti {var}"></i><span>Dashboard</span></div>
        </div>
        <div class="tabbar"><div class="addr">medchanic-md.appwrite.network</div></div>
      </div>
    </div>
    <div class="note">{note}</div>
  </article>'''

cards = [card(var, title, num, note) for _, var, title, num, note in PICKS]

html = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The picks — Medchanic mark</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>{style}
{chr(10).join(classes_css)}
</style></head><body>
<h1>The picks</h1>
<p class="sub">5 marks &middot; instagram &middot; product bar &middot; size ladder &middot; browser tab</p>
<div class="grid">
{chr(10).join(cards)}
</div>
<p class="sub" style="margin-top:22px">1 &middot; 2C &middot; 3 &middot; 4M &mdash; byte-exact from the original roster &nbsp;/&nbsp; v4b &mdash; the original file</p>
<p class="sub" style="margin-top:8px">the last five standing &mdash; say the word</p>
</body></html>'''

html = html.replace(":root{\n", ":root{\n" + "\n".join(vars_css) + "\n", 1)
out_html = os.path.join(LAB, "picks.html")
open(out_html, "w").write(html)
print("written:", out_html, os.path.getsize(out_html) // 1024, "KB")

# ---------------------------------------------------------------- PDF --------
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas as _c

W, H = A4
PAPER, CARD = HexColor("#F3EFE6"), HexColor("#FFFDF8")
INK, INK2, INK3 = HexColor("#141311"), HexColor("#4A4741"), HexColor("#8A857A")
RULE, TEAL, TEAL2, TEALSOFT = HexColor("#DDD6C6"), HexColor("#0E7C78"), HexColor("#0A5F5C"), HexColor("#D8ECE8")
M = 57  # margin

def tracked(c, x, y, text, font, size, color, cs=1.4, center=False):
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(cs)
    t.setFillColor(color)
    w = c.stringWidth(text, font, size) + cs * (len(text) - 1)
    t.setTextOrigin(x - (w / 2 if center else 0), y)
    t.textOut(text)
    c.drawText(t)

def img(path):
    return ImageReader(os.path.join(LAB, path))

pdf_path = os.path.join(LAB, "picks.pdf")
c = _c.Canvas(pdf_path, pagesize=A4)
c.setTitle("Medchanic.MD — The picks")
c.setAuthor("Medchanic.MD")

# ---- cover ----
c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
tracked(c, M, H - 78, "MEDCHANIC.MD · THE PICKS · 23 OCT 2026", "Helvetica-Bold", 8, TEAL, 1.6)
c.setFillColor(INK); c.setFont("Times-BoldItalic", 46)
c.drawString(M, H - 138, "Five marks.")
c.setFillColor(INK2); c.setFont("Helvetica", 10.5)
for i, line in enumerate([
    "The last five standing, from the full mark exploration: the original crossing, the natural",
    "stethoscope, the continuous implement that donated its bell to everything after it, the M with",
    "both tools, and the twin-drum heartbeat. One file, one decision left.",
]):
    c.drawString(M, H - 168 - i * 16, line)
# thumbnails row
tw, gap = 85, 14
x0 = (W - (5 * tw + 4 * gap)) / 2
for i, (rel, var, title, num, note) in enumerate(PICKS):
    x = x0 + i * (tw + gap)
    c.setFillColor(CARD); c.setStrokeColor(RULE); c.setLineWidth(1)
    c.roundRect(x, 300, tw, tw, 8, stroke=1, fill=1)
    c.drawImage(img(rel), x + 6, 306, tw - 12, tw - 12, mask="auto")
    tracked(c, x + tw / 2, 282, num, "Helvetica-Bold", 8, TEAL2, 1.2, center=True)
c.setStrokeColor(RULE); c.setLineWidth(1); c.line(M, 240, W - M, 240)
tracked(c, W / 2, 40, "MEDCHANIC.MD — MECHANISM-FIRST EXAM PREP", "Helvetica-Bold", 7, INK3, 1.8, center=True)
c.showPage()

# ---- one page per mark ----
for idx, (rel, var, title, num, note) in enumerate(PICKS, start=1):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    tracked(c, M, H - 64, "MEDCHANIC.MD · THE PICKS", "Helvetica-Bold", 8, TEAL, 1.6)
    # num chip top-right
    chip_w = max(34, c.stringWidth(num, "Helvetica-Bold", 8) + 20)
    c.setFillColor(TEALSOFT)
    c.roundRect(W - M - chip_w, H - 74, chip_w, 18, 4, stroke=0, fill=1)
    tracked(c, W - M - chip_w / 2, H - 68.5, num, "Helvetica-Bold", 8, TEAL2, 1.2, center=True)
    # card + mark
    csz = 430
    cx, cy = (W - csz) / 2, H - 108 - csz
    c.setFillColor(CARD); c.setStrokeColor(RULE); c.setLineWidth(1)
    c.roundRect(cx, cy, csz, csz, 14, stroke=1, fill=1)
    msz = 356
    c.drawImage(img(rel), cx + (csz - msz) / 2, cy + (csz - msz) / 2, msz, msz, mask="auto")
    # name + note
    c.setFillColor(INK); c.setFont("Helvetica-Bold", 21)
    c.drawCentredString(W / 2, cy - 40, title)
    c.setFillColor(INK2); c.setFont("Helvetica", 11)
    for i, line in enumerate(simpleSplit(note, "Helvetica", 11, 440)[:2]):
        c.drawCentredString(W / 2, cy - 64 - i * 15, line)
    # size ladder
    sizes = [54, 40, 30, 21, 15]
    lgap = 16
    total = sum(sizes) + lgap * (len(sizes) - 1)
    lx = (W - total) / 2
    for s in sizes:
        c.drawImage(img(rel), lx, 150, s, s, mask="auto")
        lx += s + lgap
    tracked(c, W / 2, 122, "SIZE LADDER — 54 / 40 / 30 / 21 / 15 PX", "Helvetica-Bold", 6.5, INK3, 1.4, center=True)
    # footer
    tracked(c, W / 2, 40, f"MEDCHANIC.MD · THE PICKS · {idx} / {len(PICKS)}", "Helvetica-Bold", 7, INK3, 1.8, center=True)
    c.showPage()

c.save()
print("written:", pdf_path, os.path.getsize(pdf_path) // 1024, "KB")
