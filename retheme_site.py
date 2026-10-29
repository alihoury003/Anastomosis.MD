#!/usr/bin/env python3
"""THE RE-THEME EXECUTION — Anastomosis.MD palette + tw-9 logo + favicon + wordmark
+ Step-1 removal + the Angiogenesis loader + CSS product screenshots.
THE TEST PAGE (#screen-block + its overlays) STAYS PIXEL-IDENTICAL: its own token
block is untouched and a scoped pin re-freezes the old palette inside it."""
import base64, io, re
from PIL import Image

# ---------------- assets ----------------
im = Image.open('logo-lab/tw-9.png').convert('RGB')
m220 = im.resize((220, 220), Image.LANCZOS)
b = io.BytesIO(); m220.save(b, 'JPEG', quality=78, optimize=True)
TW9 = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
f48 = im.resize((48, 48), Image.LANCZOS)
b2 = io.BytesIO(); f48.save(b2, 'PNG', optimize=True)
FAVICON = 'data:image/png;base64,' + base64.b64encode(b2.getvalue()).decode()
FAV_LINK = f'<link rel="icon" type="image/png" href="{FAVICON}">'

# ---------------- palette ----------------
HEX = {  # case-insensitive; base64 payloads cannot contain '#'
  'F3EFE6':'F7F3EB','EAE5D8':'EFE9DC','141311':'101418','DDD6C6':'E3DCCC','E3DCCB':'E9E2D2',
  'EDE8DC':'EAE2D3',
  '0E7C78':'1B4E5F','0A5F5C':'143C4A','D8ECE8':'DDE8EC',
  'E4572E':'B5342A','C2441F':'8E2921','FBE2D8':'F2E1DD',
  'EFA21B':'C9973C','B87A0C':'9A742C','FBEBC6':'F4EAD4',
  'FFB93B':'D9AC55','F3C6B6':'E7C6BE','9A6A57':'9E5C52','8A5A45':'9A742C',
  'BFDCD6':'C6D6DC','2A2825':'2A2E38','2a2825':'2A2E38',
  # streak-calendar teal ramp -> petrol ramp
  'B9DED8':'C9DCE2','6FBDB4':'7FA9B8','2E9A93':'3E6E80','1B7F77':'2A5666','0F5F5A':'16404E',
}
RGBA = {
  'rgba(20,19,17':'rgba(16,20,24','rgba(14,124,120':'rgba(27,78,95','rgba(10,95,92':'rgba(20,60,74)',
  'rgba(228,87,46':'rgba(181,52,42','rgba(194,68,31':'rgba(142,41,33','rgba(239,162,27':'rgba(201,151,60',
  'rgba(184,122,12':'rgba(154,116,44','rgba(242,239,230':'rgba(247,243,235','rgba(243,239,230':'rgba(247,243,235',
}
def palette(src):
    for old, new in HEX.items():
        src = re.sub('#' + old, '#' + new, src, flags=re.IGNORECASE)
    for old, new in RGBA.items():
        src = src.replace(old, new)
    return src

# ---------------- the Angiogenesis loader ----------------
ANGIO_CSS = """
/* ==== THE ANGIOGENESIS LOADER ==== */
.angio{position:fixed;inset:0;z-index:9998;background:#F7F3EB;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;cursor:pointer;transition:opacity .7s ease,visibility .7s}
.angio.done{opacity:0;visibility:hidden}
.angio .stage{position:relative;width:min(560px,86vw)}
.angio svg{width:100%;height:auto;overflow:visible}
.av{fill:none;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:avGrow 1s cubic-bezier(.55,0,.25,1) forwards}
.av.c{stroke:#B5342A}.av.v{stroke:#1B4E5F}
.av.w4{stroke-width:4.2}.av.w3{stroke-width:3.2}.av.w2{stroke-width:2.4}
@keyframes avGrow{to{stroke-dashoffset:0}}
.af{fill:none;stroke:#C9973C;stroke-width:1.5;stroke-linecap:round;opacity:0;stroke-dasharray:.006 .05;animation:avFlow 1.6s linear infinite, avFadeIn .6s 1s forwards}
@keyframes avFlow{to{stroke-dashoffset:-.556}}
@keyframes avFadeIn{to{opacity:.85}}
.as{transform-origin:center;transform:scale(0);animation:avSeal .5s cubic-bezier(.2,1.6,.4,1) forwards}
@keyframes avSeal{to{transform:scale(1)}}
.arping{fill:none;stroke:#C9973C;stroke-width:1.4;opacity:0;transform-origin:center;animation:avPing 1.1s ease-out forwards}
@keyframes avPing{0%{opacity:.85;transform:scale(.25)}100%{opacity:0;transform:scale(2.4)}}
.alogo{position:absolute;left:50%;top:50%;width:88px;height:88px;margin:-44px 0 0 -44px;border-radius:50%;background:#F7F3EB var(--tw9img) center/cover;box-shadow:0 0 0 1px #E3DCCC,0 20px 44px -18px rgba(16,20,24,.3);opacity:0;transform:scale(.5);animation:avLogo .65s 2.15s cubic-bezier(.2,1.5,.4,1) forwards}
@keyframes avLogo{to{opacity:1;transform:scale(1)}}
.acap{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:10.5px;letter-spacing:.34em;text-transform:uppercase;color:#8A857A;opacity:0;animation:avCap .7s 2.45s forwards}
@keyframes avCap{to{opacity:1}}
"""
ANGIO_SVG = """
<div class="stage">
<svg viewBox="0 0 800 520">
  <g>
    <path class="av c w4" pathLength="1" style="animation-delay:.05s" d="M -30 90 C 120 70, 240 160, 385 235"/>
    <path class="av c w3" pathLength="1" style="animation-delay:.15s" d="M -30 160 C 130 140, 250 200, 392 252"/>
    <path class="av c w3" pathLength="1" style="animation-delay:.25s" d="M -30 230 C 120 220, 260 250, 398 272"/>
    <path class="av c w2" pathLength="1" style="animation-delay:.35s" d="M -30 300 C 130 300, 250 295, 398 292"/>
    <path class="av c w3" pathLength="1" style="animation-delay:.45s" d="M -30 370 C 120 380, 240 340, 392 318"/>
    <path class="av c w4" pathLength="1" style="animation-delay:.55s" d="M -30 440 C 130 450, 250 400, 385 335"/>
    <path class="av v w4" pathLength="1" style="animation-delay:.05s" d="M 830 80 C 680 60, 560 150, 415 232"/>
    <path class="av v w3" pathLength="1" style="animation-delay:.15s" d="M 830 150 C 690 130, 550 195, 408 250"/>
    <path class="av v w3" pathLength="1" style="animation-delay:.25s" d="M 830 230 C 680 215, 540 250, 402 272"/>
    <path class="av v w2" pathLength="1" style="animation-delay:.35s" d="M 830 300 C 690 300, 550 300, 402 294"/>
    <path class="av v w3" pathLength="1" style="animation-delay:.45s" d="M 830 370 C 680 380, 550 345, 408 320"/>
    <path class="av v w4" pathLength="1" style="animation-delay:.55s" d="M 830 440 C 680 450, 560 405, 415 338"/>
  </g>
  <g>
    <path class="af" pathLength="1" d="M -30 90 C 120 70, 240 160, 385 235"/>
    <path class="af" pathLength="1" d="M -30 160 C 130 140, 250 200, 392 252"/>
    <path class="af" pathLength="1" d="M -30 230 C 120 220, 260 250, 398 272"/>
    <path class="af" pathLength="1" d="M -30 300 C 130 300, 250 295, 398 292"/>
    <path class="af" pathLength="1" d="M -30 370 C 120 380, 240 340, 392 318"/>
    <path class="af" pathLength="1" d="M -30 440 C 130 450, 250 400, 385 335"/>
    <path class="af" pathLength="1" d="M 830 80 C 680 60, 560 150, 415 232"/>
    <path class="af" pathLength="1" d="M 830 150 C 690 130, 550 195, 408 250"/>
    <path class="af" pathLength="1" d="M 830 230 C 680 215, 540 250, 402 272"/>
    <path class="af" pathLength="1" d="M 830 300 C 690 300, 550 300, 402 294"/>
    <path class="af" pathLength="1" d="M 830 370 C 680 380, 550 345, 408 320"/>
    <path class="af" pathLength="1" d="M 830 440 C 680 450, 560 405, 415 338"/>
  </g>
  <g>
    <circle class="arping" style="animation-delay:1.05s" cx="399" cy="242" r="11"/>
    <circle class="as" style="animation-delay:1.05s" cx="399" cy="242" r="5.5" fill="#C9973C"/>
    <circle class="arping" style="animation-delay:1.35s" cx="400" cy="272" r="11"/>
    <circle class="as" style="animation-delay:1.35s" cx="400" cy="272" r="5.5" fill="#C9973C"/>
    <circle class="arping" style="animation-delay:1.65s" cx="400" cy="294" r="11"/>
    <circle class="as" style="animation-delay:1.65s" cx="400" cy="294" r="5.5" fill="#C9973C"/>
    <circle class="arping" style="animation-delay:1.95s" cx="401" cy="322" r="11"/>
    <circle class="as" style="animation-delay:1.95s" cx="401" cy="322" r="5.5" fill="#C9973C"/>
  </g>
</svg>
<div class="alogo"></div>
</div>
"""
ANGIO_LANDING = f'<div class="angio" id="angioLoader">{ANGIO_SVG}<div class="acap">two vessels &middot; one mind</div></div>'
ANGIO_LANDING_JS = """<script>(function(){var l=document.getElementById('angioLoader');function f(){l.classList.add('done')}l.addEventListener('click',f);setTimeout(f,3400);})();</script>"""
ANGIO_CSS_WITH_IMG = ANGIO_CSS.replace('var(--tw9img)', f"url('{TW9}')")

# ---------------- CSS product screenshots for the landing ----------------
MOCK_CSS = """
/* ==== live product shots (CSS-built, new palette) ==== */
.shot{width:100%;aspect-ratio:16/10;background:#FFFDF8;border:1px solid #E3DCCC;border-radius:6px;padding:14px 16px;display:flex;gap:12px;overflow:hidden;font-size:8px;color:#4A4741;position:relative}
.shot .ln{height:5px;border-radius:99px;background:#EFE9DC}
.shot .rail{width:52px;display:flex;flex-direction:column;gap:4px;flex-shrink:0}
.shot .rail i{width:100%;aspect-ratio:1;border-radius:3px;background:#EFE9DC;border:1px solid #E3DCCC}
.shot .rail i.on{background:#1B4E5F;border-color:#1B4E5F}
.shot .rail i.cur{outline:1.5px solid #B5342A;outline-offset:1px}
.shot .main{flex:1;display:flex;flex-direction:column;gap:5px;min-width:0}
.shot .bar{display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:7px;letter-spacing:.08em;color:#8A857A}
.shot .bar b{color:#1B4E5F}
.shot .ch{display:flex;align-items:center;gap:6px;border:1px solid #E3DCCC;border-radius:4px;padding:4px 6px;background:#F7F3EB}
.shot .ch i{width:12px;height:12px;border-radius:50%;border:1.5px solid #8A857A;flex-shrink:0}
.shot .ch.sel{border-color:#1B4E5F;background:#DDE8EC}.shot .ch.sel i{border-color:#1B4E5F;background:#1B4E5F}
.shot .ch.str{opacity:.6}.shot .ch.str .ln{text-decoration:line-through;text-decoration-color:#B5342A}.shot .ch.str i{border-color:#B5342A}
.shot .big{font-size:30px;font-weight:800;color:#101418;letter-spacing:-.02em;line-height:1}
.shot .mini{font-size:7px;font-family:'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:#8A857A}
.shot .pill{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:7px;letter-spacing:.06em;background:#DDE8EC;color:#143C4A;border-radius:99px;padding:3px 8px}
.shot .drill{font-size:7.5px;font-weight:700;color:#fff;background:#1B4E5F;border-radius:3px;padding:4px 8px;align-self:flex-start}
.shot .why{border-left:2px solid #C9973C;background:#F4EAD4;border-radius:0 4px 4px 0;padding:4px 7px;font-size:7.5px}
.shot .why b{color:#9A742C}
.shot .row{display:flex;gap:6px;align-items:center}
.shot .grid2{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.shot .sysrow{display:flex;align-items:center;gap:6px}
.shot .sysrow span{width:74px;font-size:7.5px;font-weight:600;color:#101418;white-space:nowrap;overflow:hidden}
.shot .sysrow .b{flex:1;height:5px;border-radius:99px;background:#EFE9DC;overflow:hidden}
.shot .sysrow .b i{display:block;height:100%;background:#1B4E5F;border-radius:99px}
.shot .sysrow.weak .b i{background:#B5342A}.shot .sysrow.weak span{color:#B5342A}
.shot .card-fl{margin:auto;background:#F7F3EB;border:1px solid #E3DCCC;border-radius:8px;padding:16px 20px;text-align:center;max-width:75%}
.shot .card-fl .q{font-size:9.5px;color:#101418;line-height:1.5}
.shot .card-fl .a{margin-top:8px;font-size:9px;font-weight:700;color:#1B4E5F}
"""
MOCKS = {
'block': '''<div class="shot"><div class="rail"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="cur"></i><i></i><i></i><i></i></div><div class="main"><div class="bar"><span>BLOCK 3 · <b>28:36</b></span><span>ITEM 7 OF 20 · <b>01:24</b></span></div><div class="ln" style="width:92%"></div><div class="ln" style="width:78%"></div><div class="ln" style="width:86%"></div><div style="height:4px"></div><div class="ch str"><i></i><span class="ln" style="width:46%"></span></div><div class="ch"><i></i><span class="ln" style="width:52%"></span></div><div class="ch sel"><i></i><span class="ln" style="width:58%"></span></div><div class="ch"><i></i><span class="ln" style="width:44%"></span></div><div class="ch"><i></i><span class="ln" style="width:49%"></span></div></div></div>''',
'report': '''<div class="shot" style="flex-direction:column;gap:8px"><div class="row" style="justify-content:space-between;width:100%"><div class="row" style="gap:10px"><div><div class="mini">Overall</div><div class="big">68%</div></div><div><div class="mini">Correct</div><div class="big" style="color:#1B4E5F">812</div></div><div><div class="mini">Incorrect</div><div class="big" style="color:#B5342A">334</div></div></div><span class="pill">&uarr; 4 vs prior 14 days</span></div><div class="sysrow"><span>Cardiovascular</span><span class="b"><i style="width:74%"></i></span></div><div class="sysrow weak"><span>Endocrine</span><span class="b"><i style="width:52%"></i></span></div><div class="sysrow"><span>Nervous system</span><span class="b"><i style="width:61%"></i></span></div><div class="sysrow"><span>Renal</span><span class="b"><i style="width:70%"></i></span></div><div class="sysrow"><span>Respiratory</span><span class="b"><i style="width:77%"></i></span></div><div class="drill">Drill Endocrine · 20 questions</div></div>''',
'analyst': '''<div class="shot" style="flex-direction:column;gap:7px"><span class="pill" style="background:#F4EAD4;color:#9A742C">THE ANALYST · 12 BLOCKS, 432 ANSWERS</span><div class="ln" style="width:96%"></div><div class="ln" style="width:88%"></div><div class="ln" style="width:92%"></div><div class="ln" style="width:64%"></div><div style="height:3px"></div><div class="grid2"><div class="why"><b>Do this next</b> — Endocrine is your largest gap: 52% across 38 questions.</div><div class="why"><b>Pace</b> — 84s/question, inside the 90-second target.</div></div><div class="row"><span class="drill">Drill Endocrine</span><span class="drill" style="background:#B5342A">Drill Thyroid</span><span class="pill">2 drills/day closes the gap by your exam date</span></div></div>''',
'explain': '''<div class="shot" style="flex-direction:column;gap:6px"><div class="bar"><span>CASE · DISORDERS OF THE EYE</span><span>TUTOR MODE</span></div><div class="ch sel"><i></i><span class="ln" style="width:60%"></span></div><div style="height:2px"></div><div class="why"><b>Why A is wrong:</b> the mechanism it breaks, and the one fact that rules it out.</div><div class="why"><b>Why B is wrong:</b> why it looks inviting — and where the reasoning leaves the road.</div><div class="why"><b>Why D is wrong:</b> the near-miss a student actually picks, explained.</div><div class="why"><b>Why E is wrong:</b> one fact, one line, no "incorrect".</div></div>''',
'cards': '''<div class="shot"><div class="card-fl"><div class="mini" style="margin-bottom:6px">CARD 118 · ENDOCRINE · THYROID</div><div class="q">A 58-year-old man with painless jaundice, weight loss, and a nodule in the head of the pancreas&hellip;</div><div class="a">Courvoisier sign &mdash; the gallbladder is palpable</div><div class="row" style="margin-top:10px;justify-content:center"><span class="pill">Next review: today</span><span class="pill" style="background:#F4EAD4;color:#9A742C">Born from your miss</span></div></div></div>''',
'dash': '''<div class="shot" style="flex-direction:column;gap:8px"><div class="row" style="justify-content:space-between;width:100%"><div><div class="mini">Days to your exam</div><div class="big" style="color:#B5342A">84</div><div class="mini">FEB 24 · change date</div></div><div style="text-align:right"><div class="mini">Accuracy</div><div class="big">68%</div><div class="mini">&uarr; 4 this fortnight</div></div></div><div class="row" style="align-items:flex-end;gap:4px;height:34px"><i class="ln" style="width:9px;height:40%"></i><i class="ln" style="width:9px;height:55%"></i><i class="ln" style="width:9px;height:45%"></i><i class="ln" style="width:9px;height:65%"></i><i class="ln" style="width:9px;height:58%"></i><i class="ln" style="width:9px;height:75%"></i><i class="ln" style="width:9px;height:70%"></i><i class="ln" style="width:9px;height:88%;background:#1B4E5F"></i></div><div class="row" style="justify-content:space-between;width:100%"><span class="pill">Weakest: Thyroid disorders · 40%</span><span class="drill">Drill</span></div></div>''',
}

def swap_marks(src):
    src = re.sub(r'(<img[^>]*class="(?:mark|logo-mark)"[^>]*src=")data:image/[^"]*(")', r'\g<1>' + TW9 + r'\g<2>', src)
    return src

def de_medchanic(src):
    src = src.replace('Medchanic', 'Anastomosis').replace('MEDCHANIC', 'ANASTOMOSIS')
    return src

def add_favicon(src):
    if 'rel="icon"' in src:
        return src
    return src.replace('</head>', FAV_LINK + '\n</head>')

def report(name, src, allow_old=()):
    old = [h for h in ('#0E7C78', '#E4572E', '#EFA21B', '#F3EFE6', '#141311', '#D8ECE8', '#FBE2D8', '#FBEBC6')
           if h.lower() in src.lower() and h not in allow_old]
    print(f'{name}: {len(src)//1024} KB | old palette left: {old or "none"} | Medchanic: {src.count("Medchanic")} | Step 1: {src.count("Step 1")}')

# ================= INDEX (landing) =================
src = open('index.html', encoding='utf-8').read()
src = palette(src)
src = swap_marks(src)
src = de_medchanic(src)
src = add_favicon(src)
src = src.replace('The standard Step 1 window — buy exactly the length of the job.',
                  'The standard dedicated window — buy exactly the length of the job.')
# replace the 6 screenshot <img> payloads with the CSS mocks (in document order)
order = ['block', 'report', 'analyst', 'explain', 'cards', 'dash']
imgs = re.findall(r'<img src="data:image/jpeg;base64,[^"]*" alt="[^"]*"', src)
print(f'index: found {len(imgs)} screenshot imgs')
for img, key in zip(imgs, order):
    src = src.replace(img, MOCKS[key])
# inject mocks CSS + loader
src = src.replace('</style>', MOCK_CSS + '\n</style>')
src = src.replace('</head>', '<style>' + ANGIO_CSS_WITH_IMG + '</style>\n</head>')
src = src.replace('<body>', '<body>\n' + ANGIO_LANDING)
src = src.replace('</body>', ANGIO_LANDING_JS + '\n</body>')
open('index.html', 'w', encoding='utf-8').write(src)
report('index.html', src)

# ================= PRICING =================
src = open('pricing.html', encoding='utf-8').read()
src = palette(src); src = swap_marks(src); src = de_medchanic(src); src = add_favicon(src)
src = src.replace('The standard Step 1 dedicated window — buy exactly the length of the job.',
                  'The standard dedicated window — buy exactly the length of the job.')
open('pricing.html', 'w', encoding='utf-8').write(src)
report('pricing.html', src)

# ================= DASHBOARD (test page frozen) =================
src = open('dashboard.html', encoding='utf-8').read()
src = palette(src)
# freeze the test page: pin the OLD palette inside the block screen + its overlays
PIN = """
/* ==== TEST PAGE FREEZE — the block screen keeps today's exact palette (founder's rule: DO NOT TOUCH) ==== */
#screen-block, #endModal, #issueModal, #labPanel {
  --paper:#F3EFE6; --paper-2:#EAE5D8; --card:#FFFDF8; --ink:#141311; --ink-2:#4A4741; --ink-3:#8A857A;
  --rule:#DDD6C6; --rule-2:#EDE8DC; --sand:#E3DCCB;
  --teal:#0E7C78; --teal-2:#0A5F5C; --teal-soft:#D8ECE8;
  --coral:#E4572E; --coral-2:#C2441F; --coral-soft:#FBE2D8;
  --amber:#EFA21B; --amber-2:#B87A0C; --amber-soft:#FBEBC6;
}
"""
src = src.replace('</style>', PIN + '\n</style>', 1)
src = swap_marks(src)
src = de_medchanic(src)
src = add_favicon(src)
src = src.replace('(new Step 1 format · 30 minutes)', '(the new exam format · 30 minutes)')
src = src.replace('the new Step 1 format) — then 10/day', 'the new exam format) — then 10/day')
# boot-loader: the spinner circle dies; the angiogenesis is born (ids kept for the app's dismiss JS)
old_boot = re.search(r'<div class="boot-loader" id="bootLoader">.*?</div>\s*\n\s*<!-- ===================== DASHBOARD', src, re.S)
NEW_BOOT = ('<div class="boot-loader" id="bootLoader" style="display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px">\n'
            + ANGIO_SVG
            + '  <div class="boot-brand">Anastomosis<span style="color:var(--teal)">.</span>MD</div>\n'
            + '  <div class="boot-sub" id="bootSub">Loading your dashboard</div>\n'
            + '</div>\n\n<!-- ===================== DASHBOARD')
if old_boot:
    src = src[:old_boot.start()] + NEW_BOOT + src[old_boot.end():]
    print('dashboard: boot-loader replaced')
else:
    print('dashboard: BOOT-LOADER PATTERN NOT FOUND — check!')
# boot-loader CSS: replace the spinner rule block with the angio css
src = src.replace('.boot-loader .spinner { width: 30px; height: 30px; border: 3px solid var(--rule); border-top-color: var(--te);', '.boot-loader .spinner { display:none;', 1)
src = re.sub(r'\.boot-loader \.spinner \{[^}]*\}', '.boot-loader .spinner{display:none}', src, count=1)
src = src.replace('</style>', ANGIO_CSS_WITH_IMG + '\n</style>')
open('dashboard.html', 'w', encoding='utf-8').write(src)
report('dashboard.html', src, allow_old=('#F3EFE6', '#0E7C78', '#E4572E', '#EFA21B', '#D8ECE8', '#FBE2D8', '#FBEBC6', '#141311'))  # pinned tokens allowed

# ================= AUTH + LEGAL + IMPORT =================
for f in ['login.html', 'signup.html', 'forgot-password.html', 'reset-password.html',
          'terms.html', 'privacy.html', 'refund-policy.html', 'import.html']:
    src = open(f, encoding='utf-8').read()
    src = palette(src); src = swap_marks(src); src = de_medchanic(src); src = add_favicon(src)
    open(f, 'w', encoding='utf-8').write(src)
    report(f, src)

# ================= STYLE.CSS (auth + legal pages) =================
src = open('style.css', encoding='utf-8').read()
src = palette(src)
open('style.css', 'w', encoding='utf-8').write(src)
report('style.css', src)

print('\nTW9 mark:', len(TW9)//1024, 'KB | favicon:', len(FAVICON)//1024, 'KB')
