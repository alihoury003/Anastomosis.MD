#!/usr/bin/env python3
"""Build logo-lab/anastomosis-shortlist.html — 'Anastomosis logo shortlist':
every mark that made the cut — the founder's picks, the wild wave, the second batch."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, maxw=1000):
    im = Image.open(os.path.join(LAB, name)).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

PICKS = [
    ("dc-1.png", "The self-tying vessel", "DC-1",
     "One continuous tube: artery in through the golden ring, vein out — the infinity performing the anastomosis."),
    ("dc-2.png", "The name carries the loop", "DC-2",
     "The wordmark lockup: the two O's of anastOmosis are the infinity's loops — the name performing its own meaning."),
    ("ig-1.png", "The emblem, in the wild", "IG-1",
     "The founder's pick from the first profile-view round — the vessel-join loop as the avatar."),
]

WAVE1 = [
    ("wld-1.png", "The crossing", "WLD-1",
     "Two vessels crossing at the centre, one gold suture ring, four open mouths — the surgical diagram become icon."),
    ("wld-2.png", "The ligature", "WLD-2",
     "A and M sharing one stroke — a ligature in the true typographic sense: two letters anastomosed into one glyph."),
    ("wld-3.png", "The embrace", "WLD-3",
     "Two S-curves completing one circle — the arterial and venous halves of one circulation."),
    ("wld-4.png", "The seam", "WLD-4",
     "Crimson teeth interlocking petrol teeth — the mechanical anastomosis, one gold hand-stitch at the centre."),
    ("wld-5.png", "The bridge", "WLD-5",
     "Two vertical vessels joined by a horizontal graft — the letter H as the bypass surgeons build."),
    ("wld-6.png", "The dovetail A", "WLD-6",
     "The initial split by a carpenter's dovetail seam — the mechanic's truth wearing the surgeon's letter."),
]

WAVE2 = [
    ("wld-7.png", "The keystone", "WLD-7",
     "Two arch halves locked by one gold keystone — the arch stands only because the join holds."),
    ("wld-8.png", "The junction", "WLD-8",
     "Two tracks merging into one — the railroad anastomosis, gold pin at the switch."),
    ("wld-9.png", "The coupling", "WLD-9",
     "Two open tubes clasped mouth-to-mouth — the plumbing of the body as one fitting."),
    ("wld-10.png", "The braid", "WLD-10",
     "Two vessels woven over and under — the oldest join humans know, bound in gold."),
    ("wld-11.png", "The confluence", "WLD-11",
     "Four vessels meeting at one golden node — the medical plus sign, drawn by circulation itself."),
    ("wld-12.png", "The splice", "WLD-12",
     "Two ropes, six strands interwoven — the sailor's end-to-end anastomosis."),
]

CR_STUDIES = [
    ("cr-7.png", "Ribbon twist — kept", "CR-7",
     "The before-last of the first study round — kept by the founder's word; the only survivor."),
    ("tex-1.png", "Two-tone cylinder", "TEX-1",
     "Same design, new skin: each tube split lengthwise into light and dark tones — cylinder roundness, perfectly flat."),
    ("tex-2.png", "Engraved hatch", "TEX-2",
     "Fine parallel hatch lines in the bone colour — the vintage anatomical plate."),
    ("tex-3.png", "Sheen highlight", "TEX-3",
     "One thin lighter line along each tube's upper edge — a quiet sheen, nothing else changed."),
    ("tex-4.png", "Segmented bands", "TEX-4",
     "Fine perpendicular bands in deeper tones — myelin segmentation, surgical instrument markings."),
    ("tex-5.png", "Stipple", "TEX-5",
     "A fine scatter of lighter dots — the stipple engraving of old anatomy plates."),
    ("tex-6.png", "Crosshatch", "TEX-6",
     "Two directions of fine bone-coloured lines — the classic crosshatch of classical engraving."),
]

BT_STUDIES = [
    ("bt-1.png", "Two-tone cylinder", "BT-1",
     "The braid, same design: each tube split lengthwise into light and dark tones \u2014 roundness, perfectly flat."),
    ("bt-2.png", "Engraved hatch", "BT-2",
     "Fine parallel hatch lines in bone \u2014 the vintage anatomical plate, following the weave."),
    ("bt-3.png", "Sheen highlight", "BT-3",
     "One thin lighter line along each tube\u2019s upper edge, faithful through every crossing."),
    ("bt-4.png", "Segmented bands", "BT-4",
     "Fine perpendicular bands in deeper tones \u2014 myelin segmentation through the weave."),
    ("bt-5.png", "Stipple", "BT-5",
     "A fine scatter of lighter dots \u2014 stipple engraving, old anatomy plates."),
    ("bt-6.png", "Crosshatch", "BT-6",
     "Two directions of fine bone lines \u2014 classical engraving depth on the woven tubes."),
]

def section(header_eyebrow, header_title, header_sub, items, chip_cls):
    cards = []
    for img, title, chip, note in items:
        cards.append(f"""  <section class="view">
    <div class="viewhead"><span class="chip {chip_cls}">{chip}</span><h2>{title}</h2></div>
    <div class="frame"><img src="{uri(img)}" alt="{title} — Instagram profile view"></div>
    <p class="note">{note}</p>
  </section>""")
    return f"""  <div class="wavehead">
    <div class="eyebrow">{header_eyebrow}</div>
    <h2>{header_title}</h2>
    <p class="wsub">{header_sub}</p>
  </div>
{chr(10).join(cards)}"""

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anastomosis logo shortlist</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bone:#F7F3EB;--card:#FFFDF8;--ink:#101418;--ink2:#4A4741;--ink3:#8A857A;--rule:#E2DCD0;
--crimson:#B5342A;--petrol:#1B4E5F;--gold:#C9973C;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}}
body{{background:var(--bone);color:var(--ink);font-family:var(--sans);padding:52px 22px 100px}}
.wrap{{max-width:980px;margin:0 auto}}
.eyebrow{{font-family:var(--mono);font-size:10px;letter-spacing:.24em;color:var(--petrol);font-weight:700;text-transform:uppercase}}
h1{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(36px,5.5vw,60px);margin:12px 0 12px}}
.sub{{color:var(--ink3);font-size:14.5px;line-height:1.65;max-width:740px;margin-bottom:20px}}
.sub b{{color:var(--ink2)}}
.wavehead{{margin:56px 0 34px;padding-top:40px;border-top:2px solid var(--rule)}}
.wavehead:first-of-type{{margin-top:36px}}
.wavehead h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:34px;margin:10px 0 8px}}
.wavehead .wsub{{color:var(--ink3);font-size:13.5px;line-height:1.6;max-width:700px}}
.view{{margin-bottom:44px}}
.viewhead{{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}}
.viewhead h2{{font-family:var(--serif);font-style:italic;font-weight:400;font-size:30px}}
.chip{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;padding:5px 10px;border-radius:4px;font-weight:700}}
.chip.pick{{background:#F3E4C7;color:#8A6116}}
.chip.wld{{background:#F2D9D6;color:#8E2A22}}
.chip.b2{{background:#DCE8EC;color:var(--petrol)}}
.chip.cr{{background:#E9E2D2;color:#5A5245}}
.chip.bt{{background:#EDE6D8;color:#7A6A45}}
.frame{{border:1px solid var(--rule);border-radius:16px;overflow:hidden;background:var(--card);box-shadow:0 14px 40px rgba(16,20,24,.07)}}
.frame img{{width:100%;height:auto;display:block}}
.note{{font-size:14px;color:var(--ink2);line-height:1.65;margin-top:13px;max-width:740px}}
.foot{{margin-top:52px;font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--ink3);text-align:center;line-height:2.1}}
</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE SHORTLIST &middot; 23 OCT 2026</div>
  <h1>Anastomosis logo shortlist</h1>
  <p class="sub">Every mark that made the cut: <b>the founder's picks</b>, <b>the wild wave</b>, and <b>the second batch</b> — fifteen icons and eight studies of the fourth — each born inside the profile view, each one a joining-mechanism wearing the brand's blood. One name underneath them all.</p>
{section("THE FOUNDER&rsquo;S PICKS &middot; WHERE WE STAND", "Three marks lead.", "The designer's cut, the wordmark, and the emblem you picked from the wild.", PICKS, "pick")}
{section("THE WILD WAVE &middot; SIX JOINS, SIX ICONS", "The first six.", "Joining-mechanisms turned icons: crossing, ligature, embrace, seam, bridge, dovetail.", WAVE1, "wld")}
{section("THE SECOND BATCH &middot; JOINING-MECHANISMS, ROUND TWO", "Six more.", "Keystone, junction, coupling, braid, confluence, splice — every one an avatar, every one the name.", WAVE2, "b2")}
{section("THE FOURTH MARK, EXPLORED &middot; WLD-1 THE CROSSING", "Same design. New skin.", "The exact crossing, untouched in geometry — only the texture of the vessels changes: two-tone, hatched, sheened, segmented, stippled, crosshatched. Plus the one study kept from the first round.", CR_STUDIES, "cr")}
{section("THE TENTH MARK, EXPLORED &middot; WLD-10 THE BRAID", "The braid, same design. New skin.", "The founder’s actual pick for the texture treatment: two vessels woven over-and-under — only the surface changes: two-tone, hatched, sheened, segmented, stippled, crosshatched.", BT_STUDIES, "bt")}
  <div class="foot">ANASTOMOSIS.MD &middot; FIFTEEN MARKS &middot; THIRTEEN STUDIES &middot; ONE NAME &middot; TWO VESSELS &middot; ONE MIND<br>SAY THE WORD AND IT&rsquo;S LOCKED</div>
</div>
</body></html>"""

out = os.path.join(LAB, "anastomosis-shortlist.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
