#!/usr/bin/env python3
"""Build demo-4-replica.html: the EXACT current landing (layout, copy, screenshots)
transformed only by: the Anastomosis palette, the tw-9 logo, the tree-growth loader,
plus a static re-themed replica of the STATS dashboard (test page never touched)."""
import base64, io, re
from PIL import Image

# ---------- the new mark ----------
img = Image.open('logo-lab/tw-9.png').convert('RGB')
img = img.resize((480, 480), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, 'JPEG', quality=80, optimize=True)
TW9 = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

src = open('index.html', encoding='utf-8').read()
orig_len = len(src)

# ---------- 1. palette token swap (hex — base64 payloads cannot contain '#') ----------
HEXMAP = {
    'F3EFE6': 'F7F3EB',  # paper -> bone
    'EAE5D8': 'EFE9DC',  # paper-2 -> bone-2
    '141311': '101418',  # ink
    'DDD6C6': 'E3DCCC',  # rule
    'E3DCCB': 'E9E2D2',  # sand
    '0E7C78': '1B4E5F',  # teal -> venous petrol
    '0A5F5C': '143C4A',  # teal-2
    'D8ECE8': 'DDE8EC',  # teal-soft
    'E4572E': 'B5342A',  # coral -> arterial crimson
    'C2441F': '8E2921',  # coral-2
    'FBE2D8': 'F2E1DD',  # coral-soft
    'EFA21B': 'C9973C',  # amber -> old gold
    'B87A0C': '9A742C',  # amber-2
    'FBEBC6': 'F4EAD4',  # amber-soft
    'FFB93B': 'D9AC55',  # amber button hover -> bright gold
    'F3C6B6': 'E7C6BE',  # live-demo struck border -> muted crimson family
    '9A6A57': '9E5C52',  # live-demo struck text -> muted crimson
    '8A5A45': '9A742C',  # live-demo why-wrong text -> deep old gold
    'BFDCD6': 'C6D6DC',  # border tint -> petrol family
    '2A2825': '2A2E38',  # ink hover -> cool ink family
}
for old, new in HEXMAP.items():
    src = re.sub('#' + old, '#' + new, src, flags=re.IGNORECASE)

# ---------- 2. rgba palette forms ----------
RGBAMAP = {
    'rgba(20,19,17': 'rgba(16,20,24',
    'rgba(14,124,120': 'rgba(27,78,95',
    'rgba(10,95,92': 'rgba(20,60,74',
    'rgba(228,87,46': 'rgba(181,52,42',
    'rgba(194,68,31': 'rgba(142,41,33',
    'rgba(239,162,27': 'rgba(201,151,60',
    'rgba(184,122,12': 'rgba(154,116,44',
    'rgba(242,239,230': 'rgba(247,243,235',
    'rgba(243,239,230': 'rgba(247,243,235',
}
for old, new in RGBAMAP.items():
    src = src.replace(old, new)

# ---------- 3. the mark: nav + footer imgs and the favicon ----------
src = re.sub(r'(<img[^>]*class="mark"[^>]*src=")data:image/[^"]*(")', r'\g<1>' + TW9 + r'\g<2>', src)
src = re.sub(r'(<link[^>]*rel="icon"[^>]*type=")image/png("[^>]*href=")data:image/[^"]*(")',
             r'\g<1>image/jpeg\g<2>' + TW9 + r'\g<3>', src)

# ---------- 4. brand wordmark + title (text nodes only — never payloads) ----------
src = src.replace('<title>Medchanic — every wrong answer is a clue</title>',
                  '<title>Anastomosis — every wrong answer is a clue</title>')
src = src.replace('in Medchanic carries', 'in Anastomosis carries')
src = src.replace('— Medchanic.MD product screenshot', '— Anastomosis.MD product screenshot')
src = src.replace('Medchanic<em>MD</em>', 'Anastomosis<em>MD</em>')
src = src.replace('Medchanic.MD', 'Anastomosis.MD')   # any remaining text mentions
leftover = src.count('Medchanic')

# ---------- 5. inject: loader + dashboard view + nav switch + dswitch ----------
INJECT_CSS = """
<style>
/* ==== DEMO 4 additions (scoped) ==== */
#a4loader{position:fixed;inset:0;z-index:9999;background:var(--paper,#F7F3EB);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;cursor:pointer;transition:opacity .7s,visibility .7s}
#a4loader.done{opacity:0;visibility:hidden}
#a4loader svg{width:min(340px,62vw);overflow:visible}
#a4loader .cap{font-family:var(--serif-accent,'Instrument Serif',Georgia,serif);font-style:italic;font-size:17px;color:var(--ink-2,#4A4741);opacity:0;animation:a4cap .7s 2s forwards}
#a4loader .skip{position:absolute;bottom:26px;font-family:var(--mono,'JetBrains Mono',monospace);font-size:9.5px;letter-spacing:.2em;color:var(--ink-3,#8A857A);text-transform:uppercase}
@keyframes a4cap{to{opacity:1}}
.a4br{fill:none;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:a4grow .85s cubic-bezier(.5,0,.3,1) forwards}
.a4br.t{stroke:#101418;stroke-width:6}
.a4br.a{stroke:#B5342A;stroke-width:3.4}
.a4br.b{stroke:#1B4E5F;stroke-width:3.4}
.a4d1{animation-delay:.22s}.a4d2{animation-delay:.5s}.a4d3{animation-delay:.8s}.a4d4{animation-delay:1.1s}
@keyframes a4grow{to{stroke-dashoffset:0}}
.a4seal{transform-origin:center;transform:scale(0);animation:a4seal .5s 1.7s cubic-bezier(.2,1.6,.4,1) forwards}
@keyframes a4seal{to{transform:scale(1)}}
#a4dash{display:none;font-family:var(--disp,'Inter',sans-serif)}
body.a4dash #a4dash{display:block}
body.a4dash .nav ~ *:not(#a4dash){display:none}
.a4d-topbar{border-bottom:1px solid var(--rule,#E3DCCC);background:rgba(247,243,235,.9);backdrop-filter:blur(12px)}
.a4d-topin{max-width:1240px;margin:0 auto;padding:0 28px;height:64px;display:flex;align-items:center;gap:22px}
.a4d-brand{display:inline-flex;align-items:center;gap:10px;font-weight:800;font-size:19px;letter-spacing:-.035em;cursor:pointer}
.a4d-brand img{width:32px;height:32px;border-radius:50%}
.a4d-brand em{font-family:var(--mono,monospace);font-size:9px;font-style:normal;font-weight:700;letter-spacing:.1em;background:var(--teal,#1B4E5F);color:#fff;padding:3px 5px;border-radius:2px}
.a4d-nav{display:flex;gap:2px;margin-left:6px}
.a4d-nav span{padding:8px 13px;border-radius:4px;font-size:13.5px;font-weight:500;color:var(--ink-2,#4A4741);cursor:pointer}
.a4d-nav span:hover{background:var(--paper-2,#EFE9DC);color:var(--ink,#101418)}
.a4d-nav span.on{background:var(--ink,#101418);color:var(--paper,#F7F3EB)}
.a4d-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.a4d-chip{font-family:var(--mono,monospace);font-size:10.5px;letter-spacing:.08em;background:var(--paper-2,#EFE9DC);border:1px solid var(--rule,#E3DCCC);padding:6px 11px;border-radius:99px;color:var(--ink-2,#4A4741)}
.a4d-up{background:var(--teal,#1B4E5F);color:#fff;font-weight:700;font-size:12px;padding:7px 15px;border-radius:99px;cursor:pointer}
.a4d-out{font-size:12px;color:var(--ink-3,#8A857A);cursor:pointer;font-weight:600}
.a4d-wrap{max-width:1240px;margin:0 auto;padding:34px 28px 110px}
.a4d-hero{display:grid;grid-template-columns:1fr 300px;gap:30px;align-items:start;margin-bottom:30px}
.a4d-date{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-3,#8A857A);display:flex;align-items:center;gap:10px}
.a4d-date i{width:26px;height:1px;background:var(--rule,#E3DCCC)}
.a4d-h1{font-size:clamp(34px,4.6vw,52px);font-weight:800;letter-spacing:-.03em;line-height:1.03;margin:12px 0 8px}
.a4d-h1 em{font-family:var(--serif-accent,'Instrument Serif',serif);font-style:italic;font-weight:400;color:var(--teal,#1B4E5F)}
.a4d-lede{font-size:16px;color:var(--ink-2,#4A4741);max-width:520px}
.a4d-strip{margin-top:16px;display:inline-block;background:var(--teal-soft,#DDE8EC);border:1px solid #C6D6DC;border-radius:6px;padding:9px 14px;font-size:13px;color:var(--ink-2,#4A4741)}
.a4d-strip b{color:var(--teal-2,#143C4A)}
.a4d-strip button{margin-left:8px;background:var(--teal,#1B4E5F);color:#fff;border:none;border-radius:5px;padding:5px 12px;font-size:12px;font-weight:700;cursor:pointer}
.a4d-actions{display:flex;gap:10px;margin-top:22px;flex-wrap:wrap}
.a4d-btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:14px;padding:12px 20px;border-radius:6px;cursor:pointer;border:none}
.a4d-btn.ink{background:var(--ink,#101418);color:var(--paper,#F7F3EB)}
.a4d-btn.line{background:none;border:1.5px solid var(--ink,#101418);color:var(--ink,#101418)}
.a4d-btn.text{background:none;color:var(--teal,#1B4E5F);padding:12px 6px}
.a4d-count{background:var(--card,#FFFDF8);border:1px solid var(--rule,#E3DCCC);border-radius:14px;padding:24px;text-align:center}
.a4d-count .big{font-size:64px;font-weight:800;letter-spacing:-.04em;line-height:1;color:var(--coral,#B5342A);cursor:pointer}
.a4d-count .cap{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3,#8A857A);margin-top:8px}
.a4d-count .date{font-size:13px;font-weight:700;margin-top:12px}
.a4d-count .edit{font-size:11px;color:var(--ink-3,#8A857A);text-decoration:underline;text-underline-offset:3px;cursor:pointer;margin-top:4px}
.a4d-analyst{background:var(--card,#FFFDF8);border:1px solid var(--rule,#E3DCCC);border-radius:14px;padding:24px;margin-bottom:26px}
.a4d-analyst .tag{font-family:var(--mono,monospace);font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--teal,#1B4E5F);font-weight:700}
.a4d-analyst p{font-size:15px;color:var(--ink-2,#4A4741);margin:10px 0 16px;max-width:860px}
.a4d-analyst b{color:var(--ink,#101418)}
.a4d-next{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.a4d-nextc{border:1px solid var(--rule,#E3DCCC);border-radius:10px;padding:16px;background:var(--paper,#F7F3EB)}
.a4d-nextc .h{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--coral,#B5342A)}
.a4d-nextc .t{font-weight:700;font-size:15px;margin:6px 0 4px}
.a4d-nextc .s{font-size:12.5px;color:var(--ink-3,#8A857A)}
.a4d-nextc button{margin-top:12px;width:100%;background:var(--teal,#1B4E5F);color:#fff;border:none;border-radius:6px;padding:9px;font-weight:700;font-size:13px;cursor:pointer}
.a4d-statline{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:34px}
.a4d-stat{background:var(--card,#FFFDF8);border:1px solid var(--rule,#E3DCCC);border-radius:12px;padding:18px 16px}
.a4d-stat .k{font-family:var(--mono,monospace);font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3,#8A857A)}
.a4d-stat .v{font-size:34px;font-weight:800;letter-spacing:-.03em;margin:6px 0 2px;font-variant-numeric:tabular-nums}
.a4d-stat .v small{font-size:15px;font-weight:600;color:var(--ink-3,#8A857A)}
.a4d-stat .v.cteal{color:var(--teal,#1B4E5F)}.a4d-stat .v.ccoral{color:var(--coral,#B5342A)}.a4d-stat .v.cmuted{color:var(--ink-3,#8A857A)}
.a4d-stat .d{font-size:11px;color:var(--ink-3,#8A857A);margin-bottom:10px}
.a4d-stat .d .up{color:var(--teal,#1B4E5F);font-weight:700}
.a4d-bar{height:5px;border-radius:99px;background:var(--paper-2,#EFE9DC);overflow:hidden}
.a4d-bar i{display:block;height:100%;border-radius:99px}
.a4d-sec{display:flex;align-items:center;gap:14px;margin:30px 0 16px}
.a4d-sec .n{font-family:var(--mono,monospace);font-size:11px;color:var(--coral,#B5342A);font-weight:700}
.a4d-sec h2{font-size:24px;font-weight:800;letter-spacing:-.02em}
.a4d-sec .rule{flex:1;height:1px;background:var(--rule,#E3DCCC)}
.a4d-perf{display:grid;grid-template-columns:1.5fr 1fr;gap:14px}
.a4d-card{background:var(--card,#FFFDF8);border:1px solid var(--rule,#E3DCCC);border-radius:14px;padding:22px}
.a4d-sysrow{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dashed var(--rule,#E3DCCC)}
.a4d-sysrow:last-child{border-bottom:none}
.a4d-sysrow .nm{width:170px;font-size:13.5px;font-weight:600}
.a4d-sysrow .bar{flex:1;height:7px;border-radius:99px;background:var(--paper-2,#EFE9DC);overflow:hidden}
.a4d-sysrow .bar i{display:block;height:100%;border-radius:99px;background:var(--teal,#1B4E5F)}
.a4d-sysrow.weak .bar i{background:var(--coral,#B5342A)}
.a4d-sysrow .pc{width:44px;text-align:right;font-family:var(--mono,monospace);font-size:12px;font-weight:700}
.a4d-sysrow.weak .pc{color:var(--coral,#B5342A)}
.a4d-topic{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px dashed var(--rule,#E3DCCC);font-size:13px}
.a4d-topic:last-child{border-bottom:none}
.a4d-topic .rank{font-family:var(--mono,monospace);font-size:10px;color:var(--ink-3,#8A857A)}
.a4d-topic .t{font-weight:600;flex:1}
.a4d-topic .p{font-family:var(--mono,monospace);font-size:11px;color:var(--coral,#B5342A);font-weight:700}
.a4d-topic button{background:none;border:1px solid var(--teal,#1B4E5F);color:var(--teal,#1B4E5F);border-radius:5px;padding:4px 10px;font-size:11px;font-weight:700;cursor:pointer}
#a4switch{position:fixed;right:18px;bottom:16px;z-index:60;display:flex;gap:6px;background:rgba(255,253,248,.92);border:1px solid var(--rule,#E3DCCC);border-radius:99px;padding:6px 9px;backdrop-filter:blur(8px)}
#a4switch a{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:var(--mono,monospace);font-size:11px;font-weight:700;color:var(--ink-3,#8A857A);text-decoration:none}
#a4switch a.on{background:var(--ink,#101418);color:var(--paper,#F7F3EB)}
@media(max-width:900px){.a4d-hero{grid-template-columns:1fr}.a4d-statline{grid-template-columns:1fr 1fr}.a4d-next{grid-template-columns:1fr}.a4d-perf{grid-template-columns:1fr}.a4d-nav{display:none}}
</style>
"""

INJECT_BODY = """
<!-- ==== DEMO 4: the anastomosis loader (replaces the boring circle) ==== -->
<div id="a4loader">
  <svg viewBox="0 0 300 260">
    <path class="a4br t" pathLength="1" d="M 150 250 C 150 200, 146 170, 150 130"/>
    <path class="a4br a a4d1" pathLength="1" d="M 150 130 C 130 105, 105 100, 82 82"/>
    <path class="a4br b a4d1" pathLength="1" d="M 150 130 C 172 108, 198 104, 222 86"/>
    <path class="a4br a a4d2" pathLength="1" d="M 82 82 C 70 66, 66 52, 70 34"/>
    <path class="a4br b a4d2" pathLength="1" d="M 222 86 C 236 70, 240 56, 238 40"/>
    <path class="a4br b a4d3" pathLength="1" d="M 150 130 C 150 108, 148 92, 150 66"/>
    <path class="a4br a a4d3" pathLength="1" d="M 70 34 C 78 22, 92 18, 106 24"/>
    <path class="a4br b a4d4" pathLength="1" d="M 238 40 C 230 28, 216 26, 204 32"/>
    <circle class="a4seal" cx="153" cy="130" r="5.5" fill="#C9973C"/>
  </svg>
  <div class="cap">two vessels &middot; one mind</div>
  <div class="skip">click to enter</div>
</div>

<!-- ==== DEMO 4: the stats dashboard replica (re-themed; test page untouched) ==== -->
<main id="a4dash">
  <div class="a4d-topbar"><div class="a4d-topin">
    <span class="a4d-brand" onclick="a4land()"><img alt="" src="__TW9__">Anastomosis<em>MD</em></span>
    <nav class="a4d-nav"><span class="on">Dashboard</span><span>Create Test</span><span>Previous Tests</span><span>Notebook</span><span>Flashcards</span></nav>
    <div class="a4d-right"><span class="a4d-chip">12-DAY STREAK</span><span class="a4d-up">Upgrade</span><span class="a4d-out">Log out</span></div>
  </div></div>
  <div class="a4d-wrap">
    <section class="a4d-hero">
      <div>
        <div class="a4d-date"><span>MON 02 NOV</span><i></i><span>LICENSING EXAM PREPARATION</span></div>
        <h1 class="a4d-h1">Welcome back<em>.</em></h1>
        <p class="a4d-lede">You're <b>61%</b> through the bank and on pace for your exam date. Endocrine is costing you the most this fortnight — the drill below fixes exactly that.</p>
        <div class="a4d-strip">Free tier: <b>10 questions a day</b>. <button>Start 7-day trial</button></div>
        <div class="a4d-actions">
          <button class="a4d-btn ink">Create a test <svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 8h10M9 4l4 4-4 4"/></svg></button>
          <button class="a4d-btn line">Resume block <span style="font-weight:500;font-size:12px;opacity:.7">&nbsp;12 of 20 left</span></button>
          <button class="a4d-btn text">Drill Endocrine &rarr;</button>
        </div>
      </div>
      <div class="a4d-count">
        <div class="big">84</div>
        <div class="cap">days to your exam</div>
        <div class="date">FEB 24, 2027</div>
        <div class="edit">change date</div>
      </div>
    </section>

    <section class="a4d-analyst">
      <div class="tag">The analyst — it reads every answer you've ever given</div>
      <p>Across <b>12 blocks and 432 answers</b>, your accuracy is climbing (64% &rarr; 71% over three weeks) but <b>Endocrine is your largest single gap</b>: 52% across 38 questions, driven by thyroid and adrenal mechanics. Your pace sits at 84s/question — inside the 90-second target. Two drills a day closes the Endocrine gap by your exam date.</p>
      <div class="a4d-next">
        <div class="a4d-nextc"><div class="h">DO THIS NEXT</div><div class="t">Drill Endocrine, Diabetes &amp; Metabolism</div><div class="s">52% across 38 questions. Your largest single gap.</div><button>20 questions</button></div>
        <div class="a4d-nextc"><div class="h">DO THIS NEXT</div><div class="t">Drill Nervous System</div><div class="s">61% across 44 questions. Your next largest gap.</div><button>20 questions</button></div>
        <div class="a4d-nextc"><div class="h">DO THIS NEXT</div><div class="t">Drill Thyroid disorders</div><div class="s">Your weakest single topic: 40% over 12 questions.</div><button>20 questions</button></div>
      </div>
    </section>

    <section class="a4d-statline">
      <div class="a4d-stat"><div class="k">Overall accuracy</div><div class="v">68<small>%</small></div><div class="d"><span class="up">&uarr; 4</span> vs prior 14 days</div><div class="a4d-bar"><i style="width:68%;background:var(--teal,#1B4E5F)"></i></div></div>
      <div class="a4d-stat"><div class="k">Correct</div><div class="v cteal">812</div><div class="d">in 1,197 answered</div><div class="a4d-bar"><i style="width:68%;background:var(--teal,#1B4E5F)"></i></div></div>
      <div class="a4d-stat"><div class="k">Incorrect</div><div class="v ccoral">334</div><div class="d">each one explained</div><div class="a4d-bar"><i style="width:28%;background:var(--coral,#B5342A)"></i></div></div>
      <div class="a4d-stat"><div class="k">Omitted</div><div class="v cmuted">51</div><div class="d">mostly late-block</div><div class="a4d-bar"><i style="width:4%;background:var(--sand,#E9E2D2)"></i></div></div>
      <div class="a4d-stat"><div class="k">Qbank used</div><div class="v">1,197<small> / 1,822</small></div><div class="d">625 unused questions left</div><div class="a4d-bar"><i style="width:66%;background:var(--ink,#101418)"></i></div></div>
    </section>

    <div class="a4d-sec"><span class="n">01</span><h2>Performance</h2><span class="rule"></span></div>
    <section class="a4d-perf">
      <div class="a4d-card">
        <div class="a4d-sysrow"><span class="nm">Cardiovascular</span><span class="bar"><i style="width:74%"></i></span><span class="pc">74%</span></div>
        <div class="a4d-sysrow weak"><span class="nm">Endocrine</span><span class="bar"><i style="width:52%"></i></span><span class="pc">52%</span></div>
        <div class="a4d-sysrow"><span class="nm">Nervous System</span><span class="bar"><i style="width:61%"></i></span><span class="pc">61%</span></div>
        <div class="a4d-sysrow"><span class="nm">Renal &amp; Urinary</span><span class="bar"><i style="width:70%"></i></span><span class="pc">70%</span></div>
        <div class="a4d-sysrow"><span class="nm">Respiratory</span><span class="bar"><i style="width:77%"></i></span><span class="pc">77%</span></div>
        <div class="a4d-sysrow"><span class="nm">Gastrointestinal</span><span class="bar"><i style="width:72%"></i></span><span class="pc">72%</span></div>
        <div class="a4d-sysrow"><span class="nm">Musculoskeletal</span><span class="bar"><i style="width:69%"></i></span><span class="pc">69%</span></div>
      </div>
      <div class="a4d-card">
        <div class="a4d-sysrow" style="border-bottom:1px solid var(--rule,#E3DCCC)"><span class="nm" style="width:auto;font-weight:800">Weakest topics</span></div>
        <div class="a4d-topic"><span class="rank">01</span><span class="t">Thyroid disorders</span><span class="p">40%</span><button>Drill</button></div>
        <div class="a4d-topic"><span class="rank">02</span><span class="t">Adrenal cortex</span><span class="p">44%</span><button>Drill</button></div>
        <div class="a4d-topic"><span class="rank">03</span><span class="t">Cranial nerves</span><span class="p">48%</span><button>Drill</button></div>
        <div class="a4d-topic"><span class="rank">04</span><span class="t">Acid-base disorders</span><span class="p">52%</span><button>Drill</button></div>
        <div class="a4d-topic"><span class="rank">05</span><span class="t">Lipid metabolism</span><span class="p">55%</span><button>Drill</button></div>
      </div>
    </section>
  </div>
</main>

<div id="a4switch"><a href="demo-1-two-vessels.html">1</a><a href="demo-2-brain-tree.html">2</a><a href="demo-3-editorial.html">3</a><a class="on" href="demo-4-replica.html">4</a></div>

<script>
(function(){
  var loader=document.getElementById('a4loader');
  function fin(){loader.classList.add('done')}
  loader.addEventListener('click',fin); setTimeout(fin,3300);
})();
function a4dash(){document.body.classList.add('a4dash');window.scrollTo({top:0});}
function a4land(){document.body.classList.remove('a4dash');window.scrollTo({top:0});}
(function(){
  var links=document.querySelectorAll('.nav-links a');
  for(var i=0;i<links.length;i++){links[i].addEventListener('click',a4land);}
})();
</script>
"""

# nav button to enter the dashboard view (injected before the nav CTA)
NAVBTN = '<button id="a4navbtn" onclick="a4dash();return false" style="font-family:var(--mono,monospace);font-size:11px;letter-spacing:.08em;padding:8px 13px;border-radius:4px;background:none;border:1px solid var(--rule,#E3DCCC);color:var(--ink-2,#4A4741);cursor:pointer">DASHBOARD</button>'

# ---- perform injections ----
src = src.replace('</head>', INJECT_CSS + '\n</head>')
# nav button: before the first .nav-cta link
m = re.search(r'(<a class="nav-cta"[^>]*>)', src)
if m:
    src = src[:m.start()] + NAVBTN + '\n    ' + src[m.start():]
else:
    src = src.replace('</head>', '', 1)  # fallback shouldn't happen
src = src.replace('</body>', INJECT_BODY.replace('__TW9__', TW9) + '\n</body>')

open('demo-4-replica.html', 'w', encoding='utf-8').write(src)
print(f'written demo-4-replica.html: {len(src)//1024} KB (from {orig_len//1024} KB)')
print('palette hex swaps:', {k: v for k, v in list(HEXMAP.items())[:3]}, '... total', len(HEXMAP), 'tokens')
print('leftover "Medchanic" occurrences (expected 0):', leftover)
print('tw-9 embedded:', TW9[:40] + '...')
