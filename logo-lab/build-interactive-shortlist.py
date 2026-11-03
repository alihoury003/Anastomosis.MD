#!/usr/bin/env python3
"""Build the self-contained 100-logo interactive November shortlist.

Run: python3 logo-lab/build-interactive-shortlist.py
Requires Pillow. Reads the already-approved-to-review 100 concept files and
embeds resized PNGs and local fonts; it never touches production site assets.
"""
import base64
import io
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LAB = ROOT / 'logo-lab'
paths = list(LAB.glob('fresh-[0-9][0-9]-*.png')) + list(LAB.glob('november-[0-9]*-*.png'))
def number(path):
    m = re.fullmatch(r'(?:fresh|november)-(\d+)-.+\.png', path.name)
    if not m:
        raise ValueError(f'Invalid asset name: {path}')
    return int(m.group(1))
paths.sort(key=number)
assert [number(p) for p in paths] == list(range(1, 101)), 'Expected exactly concepts 01–100, once each.'
logos = []
for path in paths:
    with Image.open(path) as original:
        im = original.convert('RGB').resize((512, 512), Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        im.save(buffer, format='PNG', optimize=True)
        logos.append({'id': number(path), 'src': 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')})

def font64(name):
    return base64.b64encode((ROOT / 'social-kit' / 'fonts' / name).read_bytes()).decode('ascii')

html = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anastomosis November — 100 Logo Shortlist</title>
<style>
@font-face{font-family:Instrument;src:url(data:font/ttf;base64,__SERIF__) format('truetype');font-style:italic;font-display:swap}
@font-face{font-family:JetBrains;src:url(data:font/ttf;base64,__MONO__) format('truetype');font-display:swap}
:root{--bone:#f7f3eb;--paper:#fffdf7;--ink:#101418;--muted:#696b64;--line:#e3dccc;--red:#b5342a;--petrol:#1b4e5f;--soft-red:#f2e1dd;--soft-petrol:#dde8ec}*{box-sizing:border-box}body{margin:0;background:var(--bone);color:var(--ink);font:15px/1.55 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input{font:inherit}button{cursor:pointer}button:focus-visible,input:focus-visible{outline:3px solid var(--petrol);outline-offset:3px}.wrap{max-width:1380px;margin:auto;padding:0 28px}.masthead{border-bottom:1px solid var(--line)}.mast-inner{display:flex;justify-content:space-between;gap:20px;align-items:center;min-height:76px}.brand{font:italic 31px Instrument,Georgia,serif;letter-spacing:-.02em}.tag,.kicker,.meta,.number,.mini{font:600 10px JetBrains,monospace;letter-spacing:.14em;text-transform:uppercase}.tag{color:var(--petrol)}.hero{display:flex;justify-content:space-between;align-items:end;gap:35px;padding:55px 0 34px}.kicker{color:var(--red)}h1{font:italic clamp(50px,6vw,78px)/.97 Instrument,Georgia,serif;letter-spacing:-.02em;margin:14px 0 16px}.intro{max-width:590px;margin:0;color:#555851;line-height:1.7}.summary{display:grid;grid-template-columns:repeat(3,minmax(100px,1fr));gap:0;border:1px solid var(--line);background:var(--paper);border-radius:10px;min-width:350px}.summary>div{padding:18px;border-right:1px solid var(--line)}.summary>div:last-child{border:0}.summary b{display:block;font:italic 37px/1 Instrument,Georgia,serif}.summary span{display:block;margin-top:8px;color:var(--muted)}.actions{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:15px 0}.filters,.tools{display:flex;gap:6px;align-items:center;flex-wrap:wrap}.filter,.tool{border:1px solid transparent;background:transparent;color:#555851;border-radius:7px;padding:9px 11px;font-size:13px;font-weight:650}.filter[aria-pressed=true]{border-color:var(--petrol);background:var(--soft-petrol);color:var(--petrol)}.tool{border-color:var(--line);background:var(--paper)}.tool:hover,.filter:hover{border-color:var(--petrol)}.tool:disabled{opacity:.45;cursor:not-allowed}.search{width:128px;border:1px solid var(--line);background:var(--paper);border-radius:7px;padding:9px 10px;color:var(--ink);font-size:13px}.info{display:flex;justify-content:space-between;gap:20px;align-items:center;padding:19px 0;color:var(--muted);font-size:12px}.info p{margin:0}.feedback{min-height:1.4em;color:var(--petrol)}.warning{border-left:3px solid var(--red);background:var(--soft-red);padding:10px 14px;margin:0 0 16px;font-size:13px}.hidden{display:none!important}.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.card{background:var(--paper);border:1px solid var(--line);border-radius:11px;overflow:hidden}.card.favorited{border-color:var(--petrol)}.card.eliminated{border-color:#e3c1bb}.card-top{padding:15px 17px 0;display:flex;justify-content:space-between;align-items:center}.number{font-size:12px;color:var(--ink)}.state{font-size:10px;color:var(--muted)}.state.favorite{color:var(--petrol)}.state.disqualified{color:var(--red)}.image-button{display:block;width:100%;padding:8px 20px 14px;background:transparent;border:0}.avatar{display:block;width:min(100%,225px);aspect-ratio:1;border:1px solid var(--line);border-radius:50%;overflow:hidden;background:var(--bone);margin:auto}.avatar img{display:block;width:100%;height:100%;object-fit:cover}.card-actions{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--line)}.card-actions button{background:transparent;border:0;padding:12px 5px;font-size:12px;font-weight:700;color:#59605d}.card-actions button+button{border-left:1px solid var(--line)}.card-actions .fav[aria-pressed=true]{background:var(--soft-petrol);color:var(--petrol)}.card-actions .dq[aria-pressed=true]{background:var(--soft-red);color:var(--red)}.card-actions button:hover{background:var(--bone)}.empty{border:1px dashed var(--line);border-radius:10px;padding:35px;text-align:center;color:var(--muted)}.bottom{padding:35px 0 80px;color:var(--muted);font-size:12px}.bottom button{border:0;background:none;color:var(--red);font-size:12px;padding:0;font-weight:700}.modal{position:fixed;inset:0;z-index:50;background:rgba(247,243,235,.94);display:grid;place-items:center;padding:18px}.modal-panel{background:var(--paper);border:1px solid var(--line);border-radius:12px;max-width:560px;width:100%;max-height:95vh;overflow:auto;padding:20px}.modal-head{display:flex;align-items:center;justify-content:space-between}.modal-title{font:italic 31px Instrument,Georgia,serif}.modal-close{background:none;border:0;color:var(--petrol);font-weight:700}.modal-avatar{max-width:440px;margin:14px auto}.modal-tools{display:flex;justify-content:space-between;gap:10px;margin-top:14px}.modal-tools button{border:1px solid var(--line);background:var(--paper);border-radius:7px;padding:9px 14px;font-weight:700}.modal-tools button:disabled{opacity:.35;cursor:not-allowed}@media(max-width:850px){.hero{display:block;padding:40px 0 25px}.summary{margin-top:24px;min-width:0;max-width:430px}.grid{grid-template-columns:repeat(3,minmax(0,1fr))}.wrap{padding:0 18px}}@media(max-width:560px){.mast-inner{min-height:64px}.brand{font-size:27px}.tag{font-size:9px}.grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.summary>div{padding:13px}.summary b{font-size:31px}.actions{display:block}.filters{margin-bottom:10px}.tool,.filter{font-size:12px;padding:8px}.search{width:110px}.card-top{padding:12px 12px 0}.image-button{padding:8px 12px 12px}.card-actions button{font-size:11px;padding:11px 3px}.info{align-items:flex-start;display:block}.info p+ p{margin-top:7px}.wrap{padding:0 14px}}
</style></head><body>
<header class="masthead"><div class="wrap mast-inner"><div class="brand">Anastomosis November</div><div class="tag">100 CONCEPTS · PRIVATE REVIEW</div></div></header>
<main class="wrap"><section class="hero"><div><div class="kicker">THE LOGO SHORTLIST / 01—100</div><h1>Choose what stays.</h1><p class="intro">Explore all 100 concepts in their Instagram profile circles. Mark favorites, disqualify the ones you don’t want, and change your mind whenever you like.</p></div><div class="summary" aria-label="Selection summary"><div><b id="favCount">0</b><span class="mini">Favorites</span></div><div><b id="dqCount">0</b><span class="mini">Disqualified</span></div><div><b id="openCount">100</b><span class="mini">Undecided</span></div></div></section>
<div class="actions"><nav class="filters" aria-label="Filter concepts"><button class="filter" data-filter="all" aria-pressed="true">All <span id="allBadge">100</span></button><button class="filter" data-filter="undecided" aria-pressed="false">Undecided <span id="openBadge">100</span></button><button class="filter" data-filter="favorite" aria-pressed="false">Favorites <span id="favBadge">0</span></button><button class="filter" data-filter="disqualified" aria-pressed="false">Disqualified <span id="dqBadge">0</span></button></nav><div class="tools"><input id="search" class="search" type="search" inputmode="numeric" placeholder="Number" aria-label="Find logo by number"><button class="tool" id="undo" disabled>Undo</button><button class="tool" id="copy">Copy favorites</button><button class="tool" id="export">Export</button><button class="tool" id="import">Import</button><input id="file" class="hidden" type="file" accept="application/json,.json" aria-label="Import selection file"></div></div>
<div class="info"><p>Saved on this browser and device when available. Export a backup to move your selections.</p><p id="feedback" class="feedback" role="status" aria-live="polite"></p></div><div id="storageWarning" class="warning hidden" role="alert">Browser storage is unavailable. Your changes are temporary; use Export to keep them.</div><div id="grid" class="grid"></div><div id="empty" class="empty hidden">No concepts in this view. Try another filter or number.</div><div class="bottom"><span>These are numbered concept images, not final trademark-cleared logos. Earlier concepts retain their original colors.</span> <button id="clear">Clear all selections</button></div></main>
<div class="modal hidden" id="modal" role="dialog" aria-modal="true" aria-labelledby="modalTitle"><div class="modal-panel"><div class="modal-head"><div class="modal-title" id="modalTitle">Concept 01</div><button class="modal-close" id="close" aria-label="Close image">Close ✕</button></div><div class="avatar modal-avatar"><img id="modalImage" alt=""></div><div class="modal-tools"><button id="prev">← Previous</button><span class="mini" id="modalState"></span><button id="next">Next →</button></div></div></div>
<script>
'use strict';
const LOGOS=__DATA__;
const KEY='anastomosis-november-shortlist-v1';
const $=id=>document.getElementById(id);
const label=n=>String(n).padStart(2,'0');
let selections=Object.create(null), previous=null, filter='all', query='', modalId=null, restoreFocus=null;
function decode(obj){
 if(!obj||typeof obj!=='object'||Array.isArray(obj)||obj.format!=='anastomosis-november'||obj.version!==1||!obj.marks||typeof obj.marks!=='object'||Array.isArray(obj.marks))throw new Error('Not an Anastomosis November selection file.');
 const next=Object.create(null);
 for(const [key,value] of Object.entries(obj.marks)){
  if(!/^(?:[1-9]|[1-9][0-9]|100)$/.test(key)||!['favorite','disqualified'].includes(value))throw new Error('The file contains an invalid selection.');
  next[key]=value;
 }
 return next;
}
function payload(){return {format:'anastomosis-november',version:1,marks:{...selections}}}
function snapshot(){return {...selections}}
function storageWarning(show){$('storageWarning').classList.toggle('hidden',!show)}
try{let saved=localStorage.getItem(KEY);if(saved)selections=decode(JSON.parse(saved))}catch(e){storageWarning(true)}
function save(){try{localStorage.setItem(KEY,JSON.stringify(payload()));storageWarning(false)}catch(e){storageWarning(true)}}
function announce(s){$('feedback').textContent=s}
function change(id,kind){
 previous=snapshot();
 if(selections[id]===kind)delete selections[id];else selections[id]=kind;
 save();render();announce(`Concept ${label(id)}: ${selections[id]==='favorite'?'favorite':selections[id]==='disqualified'?'disqualified':'undecided'}.`)
}
function counts(){const v=Object.values(selections);const fav=v.filter(x=>x==='favorite').length,dq=v.filter(x=>x==='disqualified').length;return {fav,dq,open:100-fav-dq}}
function render(){
 const c=counts();$('favCount').textContent=c.fav;$('dqCount').textContent=c.dq;$('openCount').textContent=c.open;$('favBadge').textContent=c.fav;$('dqBadge').textContent=c.dq;$('openBadge').textContent=c.open;
 $('undo').disabled=previous===null;document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===filter)));
 let visible=LOGOS.filter(o=>{const v=selections[o.id];return (filter==='all'||(filter==='undecided'?!v:v===filter))&&(!query||label(o.id).includes(query)||String(o.id).includes(query))});
 $('grid').innerHTML=visible.map(o=>{const v=selections[o.id],f=v==='favorite',d=v==='disqualified';return `<article class="card ${f?'favorited':d?'eliminated':''}" aria-label="Concept ${label(o.id)}"><div class="card-top"><span class="number">${label(o.id)}</span><span class="meta state ${v||''}">${f?'FAVORITE':d?'DISQUALIFIED':'UNDECIDED'}</span></div><button class="image-button" data-view="${o.id}" aria-label="View concept ${label(o.id)} larger"><span class="avatar"><img loading="lazy" src="${o.src}" alt="Concept ${label(o.id)} inside a circular profile crop"></span></button><div class="card-actions"><button class="fav" data-fav="${o.id}" aria-pressed="${f}">${f?'★ Favorite':'☆ Favorite'}</button><button class="dq" data-dq="${o.id}" aria-pressed="${d}">${d?'↶ Restore':'× Disqualify'}</button></div></article>`}).join('');
 $('empty').classList.toggle('hidden',visible.length>0);
}
$('grid').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.fav)change(Number(b.dataset.fav),'favorite');else if(b.dataset.dq)change(Number(b.dataset.dq),'disqualified');else if(b.dataset.view)openModal(Number(b.dataset.view),b)});
document.querySelectorAll('[data-filter]').forEach(b=>b.addEventListener('click',()=>{filter=b.dataset.filter;render();announce(`${b.textContent.trim()} view.`)}));
$('search').addEventListener('input',e=>{query=e.target.value.trim();render()});
$('undo').addEventListener('click',()=>{if(previous===null)return;selections=Object.assign(Object.create(null),previous);previous=null;save();render();announce('Last change undone.')});
$('clear').addEventListener('click',()=>{if(!Object.keys(selections).length){announce('There are no selections to clear.');return}if(!confirm('Clear every favorite and disqualification? You can undo this once.'))return;previous=snapshot();selections=Object.create(null);save();render();announce('Selections cleared.')});
$('copy').addEventListener('click',async()=>{const ids=Object.keys(selections).filter(k=>selections[k]==='favorite').map(Number).sort((a,b)=>a-b).map(label);if(!ids.length){announce('No favorites yet.');return}const text='Anastomosis November favorites: '+ids.join(', ');try{await navigator.clipboard.writeText(text);announce('Favorite numbers copied.')}catch(e){window.prompt('Copy your favorite numbers:',text)}});
$('export').addEventListener('click',()=>{try{const blob=new Blob([JSON.stringify(payload(),null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='anastomosis-november-selections.json';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);announce('Selection backup exported.')}catch(e){announce('Export failed. Try another browser.')}});
$('import').addEventListener('click',()=>$('file').click());
$('file').addEventListener('change',async e=>{const f=e.target.files[0];e.target.value='';if(!f)return;try{if(f.size>65536)throw new Error('Selection file is too large.');const loaded=decode(JSON.parse(await f.text()));if(!confirm('Replace the selections on this device with the imported backup?'))return;previous=snapshot();selections=loaded;save();render();announce('Selection backup imported.')}catch(err){announce('Import failed: '+(err.message||'invalid file.'))}});
function openModal(id,focus){modalId=id;restoreFocus=focus||restoreFocus;const o=LOGOS[id-1];$('modalTitle').textContent='Concept '+label(id);$('modalImage').src=o.src;$('modalImage').alt='Concept '+label(id)+' in a circular crop';$('modalState').textContent=selections[id]||'undecided';$('prev').disabled=id===1;$('next').disabled=id===100;$('modal').classList.remove('hidden');$('close').focus()}
function closeModal(){$('modal').classList.add('hidden');modalId=null;if(restoreFocus&&restoreFocus.isConnected)restoreFocus.focus();restoreFocus=null}
$('close').addEventListener('click',closeModal);$('modal').addEventListener('click',e=>{if(e.target===$('modal'))closeModal()});$('prev').addEventListener('click',()=>{if(modalId>1)openModal(modalId-1)});$('next').addEventListener('click',()=>{if(modalId<100)openModal(modalId+1)});document.addEventListener('keydown',e=>{if(modalId===null)return;if(e.key==='Escape')closeModal();else if(e.key==='ArrowLeft'&&modalId>1)openModal(modalId-1);else if(e.key==='ArrowRight'&&modalId<100)openModal(modalId+1)});
render();
</script></body></html>'''
html = html.replace('__DATA__', json.dumps(logos, separators=(',', ':'))).replace('__SERIF__', font64('InstrumentSerif-Italic.ttf')).replace('__MONO__', font64('JetBrainsMono-Regular.ttf'))
out = LAB / 'anastomosis-shortlist.html'
out.write_text(html, encoding='utf-8')
print(f'Built {out.relative_to(ROOT)} — {len(logos)} embedded concepts, {out.stat().st_size:,} bytes')
