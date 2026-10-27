#!/usr/bin/env python3
"""Build logo-lab/anastomosis-final.html — THE FINAL SHORTLIST:
the founder's two crazy-good marks (TREE-1, TREE-3) and their eight descendants,
with star / disqualify / starred-side-by-side, persisted in localStorage."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, size=380, q=80):
    im = Image.open(os.path.join(LAB, name + ".png")).convert("RGB")
    im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

MARKS = [
    ("tree-1", "TREE-1", "The brain tree — original", "The founder's pick: a trunk whose branches anastomose into a brain. Study grows the mind; the growth is the join."),
    ("tree-3", "TREE-3", "The vascularized brain — original", "The founder's pick: the brain silhouette drawn entirely as anastomosed vessels."),
    ("fin-1", "FIN-1", "The brain tree — seamless", "No gold anywhere: crimson and petrol branches fusing colour into colour."),
    ("fin-2", "FIN-2", "The vascularized brain — seamless", "No gold: the hemispheres join by the meeting itself."),
    ("fin-3", "FIN-3", "The brain tree — explicit brain", "The crown unmistakably a brain at first glance, gold rings at the fusions."),
    ("fin-4", "FIN-4", "The brain tree — explicit, seamless", "The unmistakable brain crown, no gold — folds woven of the two vessel colours."),
    ("fin-5", "FIN-5", "Two hemispheres — corpus callosum", "The brain's own anastomosis: two hemispheres, four crossing vessels, gold-sealed joins."),
    ("fin-6", "FIN-6", "Two hemispheres — seamless", "The corpus callosum concept with the gold removed — crimson bridges fusing directly into petrol."),
    ("fin-7", "FIN-7", "The neurovascular unit — masterpiece", "A neuron's axon anastomosing into a vessel — the brain's wiring and the body's plumbing, one system."),
    ("fin-8", "FIN-8", "The infinity brain — masterpiece", "Two brain hemispheres as the loops of an infinity — the brand's two best ideas, one shape."),
]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bone:#F7F3EB;--card:#FFFDF8;--ink:#101418;--ink2:#4A4741;--ink3:#8A857A;--rule:#E2DCD0;
--crimson:#B5342A;--petrol:#1B4E5F;--gold:#C9973C;
--sans:'Inter',system-ui,sans-serif;--serif:'Instrument Serif',Georgia,serif;--mono:'JetBrains Mono',monospace}
body{background:var(--bone);color:var(--ink);font-family:var(--sans);padding:48px 22px 100px}
.wrap{max-width:1240px;margin:0 auto}
.eyebrow{font-family:var(--mono);font-size:10px;letter-spacing:.24em;color:var(--petrol);font-weight:700;text-transform:uppercase}
h1{font-family:var(--serif);font-style:italic;font-weight:400;font-size:clamp(34px,5vw,58px);margin:10px 0 10px}
.sub{color:var(--ink3);font-size:14.5px;line-height:1.65;max-width:820px;margin-bottom:22px}
.sub b{color:var(--ink2)}
.bar{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:6px 0 34px;position:sticky;top:0;background:var(--bone);padding:12px 0;border-bottom:1px solid var(--rule);z-index:5}
.tab{font-size:13px;font-weight:700;padding:9px 18px;border-radius:99px;border:1px solid var(--rule);background:var(--card);color:var(--ink2);cursor:pointer}
.tab.on{background:var(--petrol);border-color:var(--petrol);color:var(--bone)}
.count{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--ink2);margin-left:auto}
.count b{color:var(--gold);font-size:15px}
.ctl{font-size:12px;font-weight:700;padding:8px 14px;border-radius:8px;border:1px solid var(--rule);background:var(--card);color:var(--ink2);cursor:pointer}
.ctl:hover{border-color:var(--ink3)}
.ctl.danger{color:var(--crimson)}
.serieshead{margin:0 0 18px}
.serieshead .eyebrow{color:var(--gold)}
.serieshead h2{font-family:var(--serif);font-style:italic;font-weight:400;font-size:30px;margin-top:6px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:18px}
.card{background:var(--card);border:1px solid var(--rule);border-radius:14px;overflow:hidden;display:flex;flex-direction:column}
.card.starred{border:2px solid var(--gold);box-shadow:0 10px 26px rgba(201,151,60,.18)}
.card.eliminated{opacity:.4}
.card.eliminated img{filter:grayscale(.9)}
.cardhead{display:flex;align-items:center;gap:10px;padding:12px 14px 0;flex-wrap:wrap}
.chip{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;background:#E9E2D2;color:#5A5245;padding:4px 8px;border-radius:4px;font-weight:700}
.cardhead .t{font-size:14.5px;font-weight:800;letter-spacing:-.01em}
.cardbtns{margin-left:auto;display:flex;gap:6px}
.star{font-size:15px;line-height:1;padding:6px 9px;border-radius:7px;border:1px solid var(--rule);background:transparent;cursor:pointer;color:var(--ink3)}
.star.on{background:#F3E4C7;border-color:var(--gold);color:#8A6116}
.elim{font-size:11px;font-weight:700;padding:6px 10px;border-radius:7px;border:1px solid #E5C9C5;background:transparent;color:var(--crimson);cursor:pointer}
.elim.undo{border-color:var(--rule);color:var(--ink3)}
.card img{width:100%;height:auto;display:block;margin-top:10px}
.cardnote{font-size:12px;color:var(--ink3);line-height:1.5;padding:10px 14px 13px}
.card.eliminated .cardnote{text-decoration:line-through}
#starredView .cards{grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px}
.empty{padding:70px 0;text-align:center;color:var(--ink3);font-family:var(--serif);font-style:italic;font-size:26px}
.foot{margin-top:52px;font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--ink3);text-align:center;line-height:2.1}
body.hide-elim .card.eliminated{display:none}
"""

SCRIPT = """
<script>
(function(){
  var KEY='anastomosis-final-v1';
  var st={stars:{},elim:{}};
  try{var raw=localStorage.getItem(KEY);if(raw){var p=JSON.parse(raw);st.stars=p.stars||{};st.elim=p.elim||{}}}catch(e){}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
  var cards=[].slice.call(document.querySelectorAll('.card[data-id]'));
  var cTotal=document.getElementById('cTotal'),cStar=document.getElementById('cStar'),cElim=document.getElementById('cElim');
  var gallery=document.getElementById('galleryView'),starred=document.getElementById('starredView');
  var tabG=document.getElementById('tabGallery'),tabS=document.getElementById('tabStarred');
  var starredGrid=document.getElementById('starredGrid');
  function apply(){
    var ns=0,ne=0;
    cards.forEach(function(c){
      var id=c.getAttribute('data-id');
      var sb=c.querySelector('.star'),eb=c.querySelector('.elim');
      if(st.stars[id]){c.classList.add('starred');sb.classList.add('on');sb.textContent='\\u2605';ns++}
      else{c.classList.remove('starred');sb.classList.remove('on');sb.textContent='\\u2606'}
      if(st.elim[id]){c.classList.add('eliminated');eb.textContent='Undo';eb.classList.add('undo');ne++}
      else{c.classList.remove('eliminated');eb.textContent='Disqualify';eb.classList.remove('undo')}
    });
    cTotal.textContent=cards.length;cStar.textContent=ns;cElim.textContent=ne;
    tabS.textContent='Starred ('+ns+')';
    renderStarred();
  }
  function renderStarred(){
    starredGrid.innerHTML='';
    var n=0;
    cards.forEach(function(c){
      var id=c.getAttribute('data-id');
      if(!st.stars[id]||st.elim[id])return;
      n++;
      var img=c.querySelector('img').getAttribute('src');
      var title=c.querySelector('.t').textContent;
      var chip=c.querySelector('.chip').textContent;
      var d=document.createElement('div');
      d.className='card starred';
      d.innerHTML='<div class="cardhead"><span class="chip">'+chip+'</span><span class="t">'+title+'</span>'+
        '<div class="cardbtns"><button class="star on">\\u2605</button></div></div>'+
        '<img src="'+img+'" alt="'+title+'">';
      d.querySelector('.star').addEventListener('click',function(){delete st.stars[id];save();apply()});
      starredGrid.appendChild(d);
    });
    var empty=document.getElementById('starredEmpty');
    if(empty)empty.style.display=n?'none':'block';
  }
  cards.forEach(function(c){
    var id=c.getAttribute('data-id');
    c.querySelector('.star').addEventListener('click',function(){
      if(st.stars[id])delete st.stars[id];else st.stars[id]=1;save();apply();
    });
    c.querySelector('.elim').addEventListener('click',function(){
      if(st.elim[id])delete st.elim[id];else st.elim[id]=1;save();apply();
    });
  });
  tabG.addEventListener('click',function(){gallery.style.display='block';starred.style.display='none';tabG.classList.add('on');tabS.classList.remove('on')});
  tabS.addEventListener('click',function(){gallery.style.display='none';starred.style.display='block';tabS.classList.add('on');tabG.classList.remove('on')});
  document.getElementById('hideBtn').addEventListener('click',function(){
    document.body.classList.toggle('hide-elim');
    this.textContent=document.body.classList.contains('hide-elim')?'Show disqualified':'Hide disqualified';
  });
  document.getElementById('resetStars').addEventListener('click',function(){st.stars={};save();apply()});
  document.getElementById('resetElim').addEventListener('click',function(){st.elim={};save();apply()});
  apply();
})();
</script>
"""

cards = []
for stem, chip, title, note in MARKS:
    cards.append(
        '<div class="card" data-id="%s">'
        '<div class="cardhead"><span class="chip">%s</span><span class="t">%s</span>'
        '<div class="cardbtns"><button class="star" title="Star this mark">&#9734;</button>'
        '<button class="elim" title="Disqualify this mark">Disqualify</button></div></div>'
        '<img src="%s" alt="%s — Anastomosis final shortlist">'
        '<div class="cardnote">%s</div></div>'
        % (chip, chip, title, uri(stem), title, note)
    )

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The final shortlist — Anastomosis.MD</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>%s</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE FINAL SHORTLIST &middot; 23 OCT 2026</div>
  <h1>The final ten.</h1>
  <p class="sub">The two crazy-good marks you picked — <b>the brain tree</b> and <b>the vascularized brain</b> — and their eight descendants: the <b>seamless no-gold cuts</b>, the <b>explicit-brain</b> and <b>two-hemisphere (corpus callosum)</b> versions with and without gold, and <b>two hidden masterpieces</b>. Star to crown, disqualify to cut, open the Starred page to compare side by side. Your choices persist.</p>
  <div class="bar">
    <button id="tabGallery" class="tab on">Final shortlist</button>
    <button id="tabStarred" class="tab">Starred (0)</button>
    <button id="hideBtn" class="ctl">Hide disqualified</button>
    <button id="resetStars" class="ctl">Reset stars</button>
    <button id="resetElim" class="ctl danger">Reset disqualifications</button>
    <div class="count"><b id="cStar">0</b> starred &middot; <span id="cElim">0</span> disqualified &middot; <span id="cTotal">%d</span> total</div>
  </div>
  <div id="galleryView">
    <div class="serieshead"><div class="eyebrow">THE BRAIN ERA &middot; TREE &amp; MIND</div><h2>Ten marks, one crown.</h2></div>
    <div class="cards">%s</div>
  </div>
  <div id="starredView" style="display:none">
    <div class="serieshead"><div class="eyebrow">THE CROWN</div><h2>The finalists, side by side.</h2></div>
    <div class="empty" id="starredEmpty">Nothing starred yet &mdash; tap the stars on the marks that survive.</div>
    <div class="cards" id="starredGrid"></div>
  </div>
  <div class="foot">ANASTOMOSIS.MD &middot; THE FINAL TEN &middot; TWO VESSELS &middot; ONE MIND<br>STAR TO CROWN &middot; DISQUALIFY TO CUT &middot; COMPARE SIDE BY SIDE</div>
</div>
%s
</body></html>""" % (CSS, len(MARKS), "\n".join(cards), SCRIPT)

out = os.path.join(LAB, "anastomosis-final.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
print("marks:", len(MARKS))
