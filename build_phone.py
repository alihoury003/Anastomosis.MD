#!/usr/bin/env python3
"""Build logo-lab/anastomosis-phone.html — THE PHONE BOOK:
one real-dimension phone page per final-shortlist mark (390×844 frame),
flippable, with index, keyboard/swipe nav, and last-page persistence.
Phone-native portrait shots where generated; square previews elsewhere."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(path, maxw, q=82):
    im = Image.open(os.path.join(LAB, path)).convert("RGB")
    if im.size[0] > maxw:
        im = im.resize((maxw, int(im.size[1] * maxw / im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

PAGES_DEF = [
    ("tree-1", "TREE-1", "The brain tree — original"),
    ("tree-3", "TREE-3", "The vascularized brain — original"),
    ("fin-1", "FIN-1", "The brain tree — seamless"),
    ("fin-2", "FIN-2", "The vascularized brain — seamless"),
    ("fin-3", "FIN-3", "The brain tree — explicit brain"),
    ("fin-4", "FIN-4", "The brain tree — explicit, seamless"),
    ("fin-5", "FIN-5", "Two hemispheres — corpus callosum"),
    ("fin-6", "FIN-6", "Two hemispheres — seamless"),
    ("fin-7", "FIN-7", "The neurovascular unit"),
    ("fin-8", "FIN-8", "The infinity brain"),
    ("bh-0", "POST-1", "The first post — extracted"),
    ("bh-1", "BH-1", "The dual organ"),
    ("bh-2", "BH-2", "The dual organ — seamless"),
    ("bh-3", "BH-3", "The heart feeding the mind"),
    ("bh-4", "BH-4", "The neurocardiac loop"),
    ("bh-5", "BH-5", "The heart's little brain"),
    ("mg-1", "MG-1", "One line, two organs"),
    ("mg-2", "MG-2", "The pulse tree"),
    ("mg-3", "MG-3", "The organ embrace"),
    ("ins-1", "INS-1", "The Rx — vessels"),
    ("ins-2", "INS-2", "The high-yield star"),
    ("ins-3", "INS-3", "The night owl"),
    ("wrd-1", "WRD-1", "The name in vessels"),
    ("wrd-2", "WRD-2", "The capillary wordmark"),
    ("wm-1", "WM-1", "Continuous vessel — no .md"),
    ("wm-2", "WM-2", "Continuous vessel — with .md"),
    ("wm-3", "WM-3", "The O-loops — no .md"),
    ("wm-4", "WM-4", "The O-loops — with .md"),
    ("wm-5", "WM-5", "Capillary perfected — no .md"),
    ("wm-6", "WM-6", "Capillary perfected — with .md"),
    ("wm-7", "WM-7", "The A-lockup — no .md"),
    ("wm-8", "WM-8", "The A-lockup — with .md"),
    ("tw-2", "TW-2", "The tree-word — climbing"),
    ("tw-6", "TW-6", "The tree-word — bold"),
]

pages = []
native_count = 0
for pid, chip, title in PAGES_DEF:
    phone = f"phone-{pid}.png"
    if os.path.exists(os.path.join(LAB, phone)):
        src = uri(phone, 440)
        native = True
        native_count += 1
    else:
        src = uri(f"{pid}.png", 440)
        native = False
    pages.append((chip, title, src, native))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bone:#F7F3EB;--card:#FFFDF8;--ink:#101418;--ink2:#4A4741;--ink3:#8A857A;--rule:#E2DCD0;
--crimson:#B5342A;--petrol:#1B4E5F;--gold:#C9973C;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}
body{background:var(--bone);color:var(--ink);font-family:var(--sans);min-height:100vh;display:flex;flex-direction:column}
header{padding:34px 22px 10px;text-align:center}
.eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.24em;color:var(--petrol);font-weight:700;text-transform:uppercase}
h1{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(30px,4.5vw,46px);margin:8px 0 6px}
.sub{color:var(--ink3);font-size:13.5px;line-height:1.6;max-width:640px;margin:0 auto}
main{flex:1;display:flex;align-items:center;justify-content:center;gap:22px;padding:18px 16px 8px;flex-wrap:wrap}
.navbtn{width:52px;height:52px;border-radius:50%;border:1px solid var(--rule);background:var(--card);color:var(--ink2);font-size:22px;cursor:pointer;flex:0 0 auto}
.navbtn:hover{border-color:var(--ink3)}
.stage{display:flex;flex-direction:column;align-items:center;gap:12px}
.meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;justify-content:center}
.chip{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;background:#E9E2D2;color:#5A5245;padding:4px 8px;border-radius:4px;font-weight:700}
.chip.native{background:#DCE8EC;color:var(--petrol)}
.chip.preview{background:#F3E4C7;color:#8A6116}
.ptitle{font-size:15px;font-weight:800;letter-spacing:-.01em}
.counter{font-family:var(--mono);font-size:11px;color:var(--ink3);letter-spacing:.1em}
.phone{width:390px;height:844px;background:#15161a;border-radius:54px;padding:10px;box-shadow:0 34px 90px rgba(16,20,24,.38);position:relative}
.screen{width:100%;height:100%;border-radius:44px;overflow:hidden;background:var(--bone);position:relative}
.screen img{width:100%;height:auto;display:block}
.homebar{position:absolute;bottom:9px;left:50%;transform:translateX(-50%);width:132px;height:5px;border-radius:99px;background:rgba(16,20,24,.28);pointer-events:none}
.indexbtn{font-size:12px;font-weight:700;padding:10px 18px;border-radius:99px;border:1px solid var(--rule);background:var(--card);color:var(--ink2);cursor:pointer}
.indexbtn:hover{border-color:var(--ink3)}
footer{padding:16px;text-align:center}
.foot{font-family:var(--mono);font-size:9.5px;letter-spacing:.18em;color:var(--ink3);line-height:2}
#indexOverlay{position:fixed;inset:0;background:rgba(247,243,235,.97);display:none;overflow-y:auto;z-index:50;padding:40px 20px}
#indexOverlay.open{display:block}
.idxwrap{max-width:900px;margin:0 auto}
.idxhead{display:flex;align-items:baseline;justify-content:space-between;margin-bottom:22px}
.idxhead h2{font-family:var(--serif);font-style:italic;font-weight:400;font-size:34px}
.closebtn{font-size:12px;font-weight:700;padding:9px 16px;border-radius:99px;border:1px solid var(--rule);background:var(--card);cursor:pointer}
.idxgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.idxitem{border:1px solid var(--rule);border-radius:12px;overflow:hidden;background:var(--card);cursor:pointer;text-align:left;padding:0}
.idxitem img{width:100%;height:150px;object-fit:cover;display:block}
.idxitem .cap{padding:8px 10px;font-size:11px;font-weight:700;color:var(--ink2)}
.idxitem .c2{font-family:var(--mono);font-size:8.5px;color:var(--ink3);letter-spacing:.1em;display:block;margin-top:2px}
@media(max-width:480px){.phone{transform:scale(.92);transform-origin:top center}.navbtn{order:3}}
"""

SCRIPT = """
<script>
(function(){
  var PAGES = %s;
  var KEY='anastomosis-phone-page';
  var i=0;
  try{var s=parseInt(localStorage.getItem(KEY));if(!isNaN(s)&&s>=0&&s<PAGES.length)i=s;}catch(e){}
  var img=document.getElementById('screenimg'),chip=document.getElementById('pchip'),
      ttl=document.getElementById('ptitle'),cnt=document.getElementById('counter');
  function show(n){
    i=((n%%PAGES.length)+PAGES.length)%%PAGES.length;
    var p=PAGES[i];
    img.src=p.s; img.alt=p.t;
    chip.textContent=p.n?'PHONE-NATIVE':'SQUARE PREVIEW';
    chip.className='chip '+(p.n?'native':'preview');
    ttl.textContent=p.c+' \\u00b7 '+p.t;
    cnt.textContent=(i+1)+' / '+PAGES.length;
    try{localStorage.setItem(KEY,String(i))}catch(e){}
  }
  document.getElementById('prev').addEventListener('click',function(){show(i-1)});
  document.getElementById('next').addEventListener('click',function(){show(i+1)});
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft')show(i-1);
    if(e.key==='ArrowRight')show(i+1);
  });
  var tx=null;
  document.addEventListener('touchstart',function(e){if(e.touches.length===1)tx=e.touches[0].clientX},{passive:true});
  document.addEventListener('touchend',function(e){
    if(tx===null)return;
    var dx=e.changedTouches[0].clientX-tx;
    if(dx<-40)show(i+1); else if(dx>40)show(i-1);
    tx=null;
  },{passive:true});
  var ov=document.getElementById('indexOverlay');
  document.getElementById('indexBtn').addEventListener('click',function(){ov.classList.add('open')});
  document.getElementById('closeIdx').addEventListener('click',function(){ov.classList.remove('open')});
  var grid=document.getElementById('idxGrid');
  PAGES.forEach(function(p,n){
    var b=document.createElement('button');b.className='idxitem';
    b.innerHTML='<img src="'+p.s+'" alt=""><span class="cap">'+p.c+'<span class="c2">'+p.t+'</span></span>';
    b.addEventListener('click',function(){show(n);ov.classList.remove('open')});
    grid.appendChild(b);
  });
  show(i);
})();
</script>
"""

pages_js = "[" + ",".join(
    "{c:%s,t:%s,n:%s,s:%s}" % (
        repr(chip), repr(title), "true" if native else "false", repr(src)
    ) for chip, title, src, native in pages
) + "]"

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The phone book — Anastomosis.MD</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>%s</style></head><body>
<header>
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE PHONE BOOK &middot; REAL PHONE DIMENSIONS &middot; 31 OCT 2026</div>
  <h1>Every finalist, at true scale.</h1>
  <p class="sub">Each mark on its own page, in a real 390&times;844 phone frame — the profile exactly as a scrolling student would meet it. Flip with the arrows, arrow keys, or a swipe. %d of %d pages are phone-native portraits; the rest are square previews until their conversions land.</p>
</header>
<main>
  <button class="navbtn" id="prev" title="Previous">&lsaquo;</button>
  <div class="stage">
    <div class="meta">
      <span class="chip" id="pchip"></span>
      <span class="ptitle" id="ptitle"></span>
      <span class="counter" id="counter"></span>
    </div>
    <div class="phone"><div class="screen"><img id="screenimg" src="" alt=""><div class="homebar"></div></div></div>
    <button class="indexbtn" id="indexBtn">All %d marks &mdash; index</button>
  </div>
  <button class="navbtn" id="next" title="Next">&rsaquo;</button>
</main>
<footer><div class="foot">ANASTOMOSIS.MD &middot; %d PAGES &middot; %d PHONE-NATIVE &middot; TWO VESSELS &middot; ONE MIND<br>SAY &ldquo;CONTINUE&rdquo; TO CONVERT THE REMAINING SQUARE PREVIEWS TO PHONE-NATIVE</div></footer>
<div id="indexOverlay">
  <div class="idxwrap">
    <div class="idxhead"><h2>The index.</h2><button class="closebtn" id="closeIdx">Close</button></div>
    <div class="idxgrid" id="idxGrid"></div>
  </div>
</div>
%s
</body></html>""" % (CSS, native_count, len(pages), len(pages), len(pages), native_count, SCRIPT % pages_js)

out = os.path.join(LAB, "anastomosis-phone.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
print("pages:", len(pages), "| phone-native:", native_count)
