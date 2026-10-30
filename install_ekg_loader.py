#!/usr/bin/env python3
"""
install_ekg_loader.py — install THE EKG boot loader (the founder-crowned
loading screen, demo 08 of loader-demos.html) into a page.

Replaces the Angiogenesis loader IN PLACE:
  - the `/* ==== THE ANGIOGENESIS LOADER ==== */` CSS block  -> EKG CSS
  - the loader markup (keeping the page's existing ids so app logic is untouched)
  - index.html:     the old dismissal one-liner script is removed (loader handles it)
  - dashboard.html: the app's hide line is patched to window.ekgDismiss()
                    (graceful fade + minimum hold so the sequence always lands;
                     falls back to the old instant hide if the loader JS failed)

NEVER touches the test page (#screen-block / #endModal / #issueModal / #labPanel
or the --chrome token pin) — the loader is boot-time only.

Idempotent: re-running replaces the previously installed EKG block cleanly.

Usage:  python3 install_ekg_loader.py index.html
        python3 install_ekg_loader.py dashboard.html
"""
import re
import sys

# ---------------------------------------------------------------- tw-9 mark
TW9 = open('/tmp/tw9.txt').read().strip() if False else None
if TW9 is None:  # embedded copy (extracted from loader-demos.html const TW9)
    import os
    _p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'loader-demos.html')
    _m = re.search(r'const TW9 = "([^"]+)"', open(_p, errors='replace').read())
    TW9 = _m.group(1) if _m else ''

# ---------------------------------------------------------------- constants
EKG_D = ("M -20 352 L 112 352 Q 128 344 146 352 L 162 352 L 172 358 L 182 262 "
         "L 192 368 L 202 352 Q 222 342 244 352 L 428 352 Q 448 344 464 352 "
         "L 480 352 L 490 358 L 500 262 L 510 368 L 520 352 Q 540 342 562 352 "
         "L 788 352 Q 806 344 822 352 L 838 352 L 848 358 L 858 262 L 868 368 "
         "L 878 352 Q 898 342 920 352 L 1020 352")

CSS = """/* ==== THE EKG LOADER (Anastomosis.MD) ==== */
.ekg-load{position:fixed;inset:0;z-index:9999;background:#F7F3EB;display:flex;align-items:center;justify-content:center;transition:opacity .6s ease,visibility .6s}
.ekg-load.done{opacity:0;visibility:hidden}
.ekg-load .ekg-stage{width:min(1000px,94vw);position:relative}
.ekg-load svg{width:100%;height:auto;overflow:visible;display:block}
.ekg-trace{fill:none;stroke:#B5342A;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1}
.ekg-trace.run{animation:ekgDraw 1.7s .22s cubic-bezier(.3,.06,.24,1) forwards,ekgTraceFade .8s 2.05s forwards}
@keyframes ekgDraw{to{stroke-dashoffset:0}}
@keyframes ekgTraceFade{to{opacity:.3}}
.ekg-l{opacity:0;transform-box:fill-box;transform-origin:center;fill:#E3DCCC}
.ekg-l.run{animation:ekgBeat .62s cubic-bezier(.3,.6,.4,1) forwards}
@keyframes ekgBeat{0%{opacity:1;transform:scale(1);fill:#E3DCCC}14%{transform:scale(1.26) translateY(-3px);fill:url(#ekgGrad)}32%{transform:scale(.94)}50%{transform:scale(1.1) translateY(-1px)}100%{opacity:1;transform:scale(1) translateY(0);fill:url(#ekgGrad)}}
#ekgWord{transform-box:view-box;transform-origin:500px 298px}
#ekgWord.beat{animation:ekgSystole .75s ease-in-out}
@keyframes ekgSystole{0%,100%{transform:scale(1)}22%{transform:scale(1.05)}45%{transform:scale(.985)}68%{transform:scale(1.025)}}
.ekg-peak{opacity:0;transform-box:fill-box;transform-origin:center}
.ekg-peak.pop{animation:ekgPeakPop .4s cubic-bezier(.22,1.6,.36,1) forwards}
@keyframes ekgPeakPop{0%{opacity:0;transform:scale(0)}60%{opacity:1}100%{opacity:1;transform:scale(1)}}
#ekgScene{transition:opacity .6s}
#ekgScene.dim{opacity:.3}
.ekg-fin{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;opacity:0;pointer-events:none;transition:opacity .7s ease}
.ekg-fin.on{opacity:1}
.ekg-fin .flogo{width:100px;height:100px;border-radius:50%;background-color:#F7F3EB;background-position:center;background-size:cover;box-shadow:0 0 0 1px #E3DCCC,0 22px 44px -18px rgba(16,20,24,.3);transform:scale(.5);opacity:0;transition:transform .65s cubic-bezier(.22,1.5,.36,1),opacity .4s}
.ekg-fin.on .flogo{transform:scale(1);opacity:1}
.ekg-fin .fbrand{font-family:var(--display);font-weight:700;font-size:20px;letter-spacing:-.02em;color:#101418;transform:translateY(8px);opacity:0;transition:transform .5s .12s,opacity .5s .12s}
.ekg-fin.on .fbrand{transform:none;opacity:1}
.ekg-fin .fload{font-family:var(--mono);font-size:10px;letter-spacing:.32em;text-transform:uppercase;color:#8A857A;transform:translateY(8px);opacity:0;transition:transform .5s .22s,opacity .5s .22s}
.ekg-fin.on .fload{transform:none;opacity:1}
@media (max-width:600px){.ekg-fin .flogo{width:72px;height:72px}.ekg-fin .fbrand{font-size:17px}}
@media (prefers-reduced-motion:reduce){.ekg-load *{animation:none!important;transition:none!important}}"""


def markup(mode, root_id, caption, caption_id):
    fin_id_attr = f' id="{caption_id}"' if caption_id else ''
    dot_col = 'var(--teal,#1B4E5F)'
    return f"""<!-- ==== EKG LOADER (Anastomosis.MD) ==== -->
<div class="ekg-load" id="{root_id}" role="status" aria-label="Loading Anastomosis.MD">
  <div class="ekg-stage">
    <svg viewBox="0 0 1000 560" aria-hidden="true">
      <defs>
        <linearGradient id="ekgGrad" gradientUnits="userSpaceOnUse" x1="280" y1="0" x2="720" y2="0">
          <stop offset="0" stop-color="#B5342A"/><stop offset=".4" stop-color="#101418"/><stop offset="1" stop-color="#1B4E5F"/>
        </linearGradient>
      </defs>
      <g id="ekgScene">
        <path id="ekgTrace" class="ekg-trace" pathLength="1" d="{EKG_D}"/>
        <text id="ekgProbe" x="500" y="312" text-anchor="middle" font-family="'Instrument Serif',Georgia,serif" font-style="italic" font-size="78" letter-spacing="2" opacity="0">anastomosis</text>
        <g id="ekgWord"><g id="ekgLetters"></g></g>
        <circle class="ekg-peak" cx="182" cy="262" r="3.2" fill="#C9973C"/>
        <circle class="ekg-peak" cx="500" cy="262" r="3.2" fill="#C9973C"/>
        <circle class="ekg-peak" cx="858" cy="262" r="3.2" fill="#C9973C"/>
        <circle id="ekgDot" r="4.5" fill="#C9973C" opacity="0"/>
      </g>
    </svg>
    <div class="ekg-fin" id="ekgFin">
      <div class="flogo" style="background-image:url('data:image/jpeg;base64,{TW9}')"></div>
      <div class="fbrand">Anastomosis<span style="color:{dot_col}">.</span>MD</div>
      <div class="fload"{fin_id_attr}>{caption}</div>
    </div>
  </div>
</div>
<script>
(function(){{
  'use strict';
  var ROOT = document.getElementById('{root_id}');
  var svg = ROOT && ROOT.querySelector('svg');
  if(!ROOT || !svg) return;
  var T0 = performance.now();
  var MODE = '{mode}';
  var TRACE_T0 = 220, TRACE_DUR = 1700;                 /* ms, absolute from T0 */
  var SYSTOLE_AT = 2450, FINALE_AT = 2850;
  var MIN_HOLD = 3600, AUTO_DONE = 4200;                /* dashboard / index dismissal */
  var reduced = false;
  try {{ reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches; }} catch(e){{}}
  var els = {{
    trace: document.getElementById('ekgTrace'),
    probe: document.getElementById('ekgProbe'),
    letters: document.getElementById('ekgLetters'),
    word: document.getElementById('ekgWord'),
    scene: document.getElementById('ekgScene'),
    fin: document.getElementById('ekgFin'),
    dot: document.getElementById('ekgDot'),
    peaks: Array.prototype.slice.call(svg.querySelectorAll('.ekg-peak'))
  }};
  if(!els.trace || !els.probe || !els.letters) return;
  var WORD = 'anastomosis', FS = 78, BASE = 312, LS = 2;
  var faded = false;
  function now(){{ return performance.now() - T0; }}
  function at(ms, fn){{ return setTimeout(fn, Math.max(0, ms - now())); }}
  function fade(){{
    if(faded) return; faded = true;
    ROOT.classList.add('done');
    setTimeout(function(){{ ROOT.style.display = 'none'; }}, 700);
  }}
  /* exact cubic-bezier(.3,.06,.24,1) so the rider dot rides the trace tip */
  function bez(x1,y1,x2,y2){{
    return function(t){{
      var u = t, i, cx = 3*x1, bx = 3*(x2-x1)-cx, ax = 1-cx-bx,
                 cy = 3*y1, by = 3*(y2-y1)-cy, ay = 1-cy-by;
      function f(v){{ return ((ax*v+bx)*v+cx)*v; }}
      function df(v){{ return (3*ax*v+2*bx)*v+cx; }}
      for(i=0;i<8;i++){{ var e = f(u)-t; if(Math.abs(e) < 1e-5) break;
        var d = df(u); if(Math.abs(d) < 1e-6) break; u -= e/d; }}
      return ((ay*u+by)*u+cy)*u;
    }};
  }}
  var ease = bez(.3,.06,.24,1);
  function passAt(x){{ return TRACE_T0 + TRACE_DUR * (x + 20) / 1040; }}
  function buildLetters(){{
    var n = WORD.length, totalW = 0;
    try {{ totalW = els.probe.getSubStringLength(0, n); }} catch(e){{ return false; }}
    if(!totalW) return false;
    var g = document.getElementById('ekgGrad');
    if(g){{
      g.setAttribute('x1', (500 - totalW/2 - 8).toFixed(1));
      g.setAttribute('x2', (500 + totalW/2 + 8).toFixed(1));
    }}
    var NS = 'http://www.w3.org/2000/svg';
    for(var i=0;i<n;i++){{
      var pre = 0, w = 0;
      try {{ pre = els.probe.getSubStringLength(0,i); w = els.probe.getSubStringLength(i,1); }} catch(e){{}}
      var x = 500 - totalW/2 + pre;
      var el = document.createElementNS(NS,'text');
      el.setAttribute('x', x.toFixed(1));
      el.setAttribute('y', BASE);
      el.setAttribute('text-anchor','start');
      el.setAttribute('font-family',"'Instrument Serif',Georgia,serif");
      el.setAttribute('font-style','italic');
      el.setAttribute('font-size', FS);
      el.setAttribute('letter-spacing', LS);
      el.setAttribute('class','ekg-l');
      el.textContent = WORD[i];
      els.letters.appendChild(el);
      if(reduced){{
        el.setAttribute('fill','url(#ekgGrad)');
        el.style.opacity = '1';
        continue;
      }}
      var d = passAt(x + w/2) - now();
      if(d <= 40){{
        el.setAttribute('fill','url(#ekgGrad)');
        el.style.opacity = '1';
      }} else {{
        (function(node, delay){{ at(delay, function(){{ node.classList.add('run'); }}); }})(el, d);
      }}
    }}
    return true;
  }}
  function probeFallback(){{
    els.probe.setAttribute('opacity','1');
    els.probe.setAttribute('fill','url(#ekgGrad)');
  }}
  var fontP;
  try {{
    fontP = Promise.race([
      Promise.all([document.fonts.load("italic 78px 'Instrument Serif'").catch(function(){{}}), document.fonts.ready]),
      new Promise(function(r){{ setTimeout(r, 900); }})
    ]);
  }} catch(e){{ fontP = null; }}
  function build(){{
    var ok = false;
    try {{ ok = buildLetters(); }} catch(e){{ ok = false; }}
    if(!ok) probeFallback();
  }}
  if(fontP && fontP.then) fontP.then(build); else build();

  if(reduced){{
    els.trace.style.strokeDashoffset = '0';
    els.trace.style.opacity = '.3';
    if(els.dot) els.dot.setAttribute('opacity','0');
    els.peaks.forEach(function(p){{ p.style.opacity = '1'; }});
    els.scene.classList.add('dim');
    els.fin.classList.add('on');
  }} else {{
    els.trace.classList.add('run');
    var pathLen = 1000;
    try {{ pathLen = els.trace.getTotalLength(); }} catch(e){{}}
    (function ride(){{
      if(faded) return;
      var t = (now() - TRACE_T0) / TRACE_DUR;
      if(t < 0){{ requestAnimationFrame(ride); return; }}
      if(t > 1){{ els.dot.setAttribute('opacity','0'); return; }}
      try {{
        var p = els.trace.getPointAtLength(ease(t) * pathLen);
        els.dot.setAttribute('cx', p.x.toFixed(1));
        els.dot.setAttribute('cy', p.y.toFixed(1));
        els.dot.setAttribute('opacity','1');
      }} catch(e){{}}
      requestAnimationFrame(ride);
    }})();
    els.peaks.forEach(function(p){{
      var px = parseFloat(p.getAttribute('cx')) || 0;
      at(passAt(px), function(){{ p.classList.add('pop'); }});
    }});
    at(SYSTOLE_AT, function(){{ els.word.classList.add('beat'); }});
    at(FINALE_AT, function(){{
      els.scene.classList.add('dim');
      els.fin.classList.add('on');
    }});
    if(MODE === 'index'){{
      ROOT.style.cursor = 'pointer';
      ROOT.addEventListener('click', fade);
      at(AUTO_DONE, fade);
    }}
  }}
  setTimeout(fade, 12000); /* never trap the user */
  if(MODE === 'dashboard'){{
    window.ekgDismiss = function(){{ at(MIN_HOLD, fade); }};
  }}
}})();
</script>
<!-- ==== /EKG LOADER ==== -->"""


# ---------------------------------------------------------------- per-page config
CONFIG = {
    'index.html': dict(
        mode='index',
        root_id='angioLoader',           # keep the page's existing id
        caption='two vessels &middot; one mind',
        caption_id=None,
        old_markup_re=r'<div class="angio" id="angioLoader">.*?<div class="acap">two vessels &middot; one mind</div></div>',
        extra_note='removes the old dismissal one-liner (loader handles click-skip + auto-done)',
    ),
    'dashboard.html': dict(
        mode='dashboard',
        root_id='bootLoader',            # keep the page's existing id
        caption='Loading your dashboard',
        caption_id='bootSub',            # the auth-fail path updates this text — keep the id
        old_markup_re=r'<div class="boot-loader" id="bootLoader"[^>]*>.*?<div class="boot-sub" id="bootSub">Loading your dashboard</div>\s*</div>',
        extra_note='patches the app hide line to window.ekgDismiss()',
    ),
}

OLD_CSS_RE = re.compile(
    r'/\* ==== THE ANGIOGENESIS LOADER ==== \*/.*?@keyframes avCap\{to\{opacity:1\}\}\n',
    re.S)

INDEX_OLD_DISMISS_RE = re.compile(
    r'<script>\(function\(\)\{var l=document\.getElementById\(\'angioLoader\'\);function f\(\)\{l\.classList\.add\(\'done\'\)\}l\.addEventListener\(\'click\',f\);setTimeout\(f,3400\);\}\)\(\);</script>\n')

DASH_OLD_HIDE = ("    const loader = $('bootLoader'); if (loader) loader.style.display = 'none';")
DASH_NEW_HIDE = ("    if (window.ekgDismiss) { window.ekgDismiss(); } else { const loader = $('bootLoader'); if (loader) loader.style.display = 'none'; }")


def install(fname):
    cfg = CONFIG[fname]
    html = open(fname, errors='replace').read()
    NEW = markup(cfg['mode'], cfg['root_id'], cfg['caption'], cfg['caption_id'])

    ekg_block_re = re.compile(
        r'<!-- ==== EKG LOADER \(Anastomosis\.MD\) ==== -->.*?<!-- ==== /EKG LOADER ==== -->', re.S)
    ekg_css_re = re.compile(
        r'/\* ==== THE EKG LOADER \(Anastomosis\.MD\) ==== \*/.*?'
        r'@media \(prefers-reduced-motion:reduce\)\{\.ekg-load \*\{animation:none!important;transition:none!important\}\}\n', re.S)

    # 1. markup: replace a previously installed EKG block, else the old angio loader
    if ekg_block_re.search(html):
        html = ekg_block_re.sub(lambda m: NEW, html, count=1)
    else:
        mk = re.search(cfg['old_markup_re'], html, re.S)
        assert mk, f"{fname}: old loader markup not found"
        html = html[:mk.start()] + NEW + html[mk.end():]

    # 2. CSS: angio block -> ekg block (or refresh an existing ekg block)
    if OLD_CSS_RE.search(html):
        assert len(OLD_CSS_RE.findall(html)) == 1, f"{fname}: expected 1 angio CSS block"
        html = OLD_CSS_RE.sub(lambda m: CSS + '\n', html, count=1)
    elif ekg_css_re.search(html):
        html = ekg_css_re.sub(lambda m: CSS + '\n', html, count=1)
    else:
        raise AssertionError(f"{fname}: no loader CSS block found to replace")

    # 3. per-page wiring (conditional — absent on re-runs)
    if cfg['mode'] == 'index':
        if INDEX_OLD_DISMISS_RE.search(html):
            html = INDEX_OLD_DISMISS_RE.sub('', html)
    else:
        if DASH_OLD_HIDE in html:
            html = html.replace(DASH_OLD_HIDE, DASH_NEW_HIDE, 1)

    assert 'id="ekgTrace"' in html
    open(fname, 'w').write(html)
    print(f"{fname}: EKG loader installed ({cfg['extra_note']})")


if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in CONFIG:
        print(__doc__)
        sys.exit(1)
    install(sys.argv[1])
