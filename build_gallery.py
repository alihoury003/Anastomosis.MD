#!/usr/bin/env python3
"""Build logo-lab/anastomosis-gallery.html — THE MASTER GALLERY:
every Anastomosis mark ever created (97 across 18 series), with Disqualify buttons,
Star buttons, and a separate Starred view for side-by-side comparison.
State persists in localStorage."""
import base64, io, os
from PIL import Image

LAB = "/home/user/Medchanic.md/logo-lab"

def uri(name, size=380, q=80):
    im = Image.open(os.path.join(LAB, name + ".png")).convert("RGB")
    im = im.resize((size, size), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

# (file-stem, chip, title, note)
SERIES = [
    ("I · The Founder's Two + the brand set", [
        ("anastomosis-1", "ANA-1", "The union", "Two vessels merging into one — the word's literal meaning, coral dot at the junction."),
        ("anastomosis-2", "ANA-2", "The bypass", "The CABG silhouette: vessel, bridging arc, two suture dots."),
        ("anastomosis-3", "ANA-3", "The circle", "The Circle of Willis — heptagonal ring, vessel stubs, one coral segment."),
        ("anastomosis-4", "ANA-4", "The seam", "Two vessel walls closed by a row of suture dots."),
        ("anastomosis-5", "ANA-5", "The side-to-side", "Parallel vessels joined by one bridge — pure plumbing."),
        ("anastomosis-6", "ANA-6", "The AV union — hero", "The definitive line mark: crimson artery, petrol vein, graphite graft, golden suture."),
        ("anastomosis-7", "ANA-7", "The dark hero", "Bone graft on ink — the night version (black later banned)."),
        ("anastomosis-8", "ANA-8", "The seam, full colour", "Artery above, vein below, golden stitches."),
        ("anastomosis-9", "ANA-9", "The circle, full colour", "Willis fed by crimson and petrol, gold communicator."),
        ("anastomosis-10", "ANA-10", "The render", "The 3D product-hero of the AV union (render style later dropped)."),
    ]),
    ("II · The bold series — marks with mass", [
        ("bold-1", "BOLD-1", "The knot", "Two thick ropes tied in the surgeon's square knot, gold bead at the centre."),
        ("bold-2", "BOLD-2", "The bowtie", "Two solid triangles meeting at a gold diamond — the diagram given mass."),
        ("bold-3", "BOLD-3", "The A", "The letterform that is an anastomosis — 'edges that read as vessels.'"),
        ("bold-4", "BOLD-4", "The union", "Two bold filled circles, gold overlap chamber."),
        ("bold-5", "BOLD-5", "The knot — night mode", "Knot on ink (black backgrounds later dropped)."),
        ("bold-6", "BOLD-6", "The union — night mode", "Union on ink (black backgrounds later dropped)."),
    ]),
    ("III · The first upgrades", [
        ("a-refined", "A-R", "The A — refined", "Thicker strokes, cleaner merge, premium cut."),
        ("a-vessel", "A-V", "The A — one vessel", "A single folded tube: artery in, graft at the peak, vein out."),
        ("a-loop", "A-L", "The A — looped", "Feet curling into two infinite loops."),
        ("knot-refined", "KNOT-R", "The knot — tightened", "Reduced to its essential crossings."),
    ]),
    ("IV · The clear A", [
        ("a-top", "A-TOP", "The A — definitive", "Textbook letter, unmistakable vessel edges: open tube tips, lumens, apex merge."),
        ("a-3d", "A-3D", "The A — sculptural", "Extruded depth, walls and lumens in perspective."),
        ("a-apex", "A-PX", "The A — apex junction", "The apex IS the anastomosis: gold suture ring joining the vessels."),
    ]),
    ("V · The first infinity", [
        ("inf-1", "INF-1", "The endless anastomosis", "Crimson loop, petrol loop, golden suture at the crossing."),
        ("inf-2", "INF-2", "The flow-through", "One ink vessel crossing itself — artery in, vein out, gold at the pass."),
    ]),
    ("VI · The infinity elevated", [
        ("inf-refined", "INF-R", "The definitive infinity", "Fuller loops, thicker tube, gold band wrapping the crossing."),
        ("inf-3d", "INF-3D", "The sculptural infinity", "Real walls and depth — flat two-tone carving."),
        ("inf-render", "INF-RND", "The rendered infinity", "Studio light, true volume, gold ring at the heart (style later dropped)."),
    ]),
    ("VII · The AV infinity — the infinity IS the anastomosis", [
        ("avi-1", "AVI-1", "The join", "The gold infinity's ends fuse into both vessel walls — suture rings at the junctions."),
        ("avi-2", "AVI-2", "The flow", "Artery flows into the left loop, vein receives the right — the handover in gold."),
        ("avi-3", "AVI-3", "Minimal", "The 16 px cut: A skeleton, gold loop bridging artery to vein."),
        ("avi-4", "AVI-4", "Rendered — dropped style", "The 3D version (banned from social by founder's order — kept for the record)."),
        ("avi-5", "AVI-5", "The emblem", "No letter: artery and vein joined by the endless loop — the pure symbol."),
    ]),
    ("VIII · The living A — pure skeleton, vessel material", [
        ("lv-1", "LV-1", "Definitive", "Aorta-drawn curves, taper, the branch, open mouths — a textbook A made of vessels."),
        ("lv-2", "LV-2", "Infinite crossbar", "The crossbar is a small gold infinity — the loop held in the letter's anatomy."),
        ("lv-3", "LV-3", "Looped feet", "Quiet loops at the base — the infinity carried at the feet."),
        ("lv-4", "LV-4", "Vivid", "True arterial red and venous blue — the universal diagram colours."),
        ("lv-5", "LV-5", "Anatomical hero", "Real 3D vessels with the branch and interior depth (render style later dropped)."),
    ]),
    ("IX · The clear A — second cut", [
        ("ac-1", "AC-1", "Definitive", "The two non-negotiables: a readable A, unmistakable vessels."),
        ("ac-2", "AC-2", "Vessel detail", "Wall-thickness lines, pronounced lumens, one true branch stub — the founder liked the branch."),
        ("ac-3", "AC-3", "Minimal", "The 16 px cut — letter, loops, lumen dots."),
        ("ac-4", "AC-4", "Rendered", "Literal 3D vessels with open mouths and interior depth (style later dropped)."),
        ("ac-5", "AC-5", "The infinite crossbar", "A clean textbook A whose crossbar IS the infinity, in gold."),
    ]),
    ("X · The A-Infinity — the founder's fusion", [
        ("ainf-1", "AINF-1", "Definitive", "The founder's A∞ composition in full vessel language."),
        ("ainf-2", "AINF-2", "Sculptural", "The fusion extruded — walls, lumens, two-tone carving."),
        ("ainf-3", "AINF-3", "Rendered", "The flagship 3D (style later dropped)."),
        ("ainf-4", "AINF-4", "Minimal", "Fewest strokes that read as both A and infinity."),
    ]),
    ("XI · The style transfer", [
        ("ais-1", "AIS-1", "Your style", "The founder's composition drawn in the founder's chosen style."),
        ("ais-2", "AIS-2", "Your style, our blood", "The attached style carrying the arteriovenous palette."),
        ("ais-3", "AIS-3", "Your style — minimal", "The 16 px cut in the founder's style."),
        ("ais-4", "AIS-4", "Your style — hero", "The richest expression on the fused form."),
    ]),
    ("XII · The Designer's Cut", [
        ("dc-1", "DC-1", "The self-tying vessel", "One continuous tube: artery in through the golden ring, vein out — the infinity performing the anastomosis."),
        ("dc-2", "DC-2", "The name carries the loop", "The wordmark: the two O's of anastOmosis are the loops."),
        ("dc-3", "DC-3", "The hidden monogram", "Negative space beneath the crossing whispers an A."),
        ("dc-4", "DC-4", "The launch post", "The hero: mark large, 'Two vessels. One mind.' beneath."),
    ]),
    ("XIII · The wild round — avatar-first, in the profile view", [
        ("ig-1", "IG-1", "The emblem, in the wild", "The founder's pick — the vessel-join loop as the avatar."),
        ("ig-2", "IG-2", "The A, in the wild", "The living A with the golden infinity crossbar, avatar scale."),
        ("ig-3", "IG-3", "The circle-born loop", "The infinity scaled so its curves follow the circle's edge."),
        ("ig-4", "IG-4", "The seal", "The monogram A in a graphite ring — a coin, a stamp, a guild badge."),
        ("ig-5", "IG-5", "The negative-space disc", "One crimson disc, the infinity carved out, the vein flowing through."),
    ]),
    ("XIV · The max wave", [
        ("max-1", "MAX-1", "The definitive emblem", "Every vessel cue at once: curves, taper, lumens, branch, gold ring."),
        ("max-2", "MAX-2", "The twin discs", "The infinity channelled through a crimson disc and a petrol disc."),
        ("max-3", "MAX-3", "The full system", "Highlight covers as a glyph family, a designed post-template grid."),
        ("max-4", "MAX-4", "The wordmark", "The two O's of the name are the loops — the name performing its meaning."),
        ("max-5", "MAX-5", "The founder's cut, elevated", "IG-1 at its absolute maximum — the flagship account."),
    ]),
    ("XV · The wild waves — joining-mechanisms as icons", [
        ("wld-1", "WLD-1", "The crossing", "Two vessels crossing, one gold suture ring, four open mouths — the surgical diagram become icon."),
        ("wld-2", "WLD-2", "The ligature", "A and M sharing one stroke — two letters anastomosed into one glyph."),
        ("wld-3", "WLD-3", "The embrace", "Two S-curves completing one circle — gold rings at both meetings."),
        ("wld-4", "WLD-4", "The seam", "Crimson teeth interlocking petrol teeth — one gold hand-stitch."),
        ("wld-5", "WLD-5", "The bridge", "Two vertical vessels joined by a graft — the letter H as a bypass."),
        ("wld-6", "WLD-6", "The dovetail A", "The initial split by a carpenter's dovetail seam — mechanic truth, surgeon's letter."),
        ("wld-7", "WLD-7", "The keystone", "Two arch halves locked by one gold keystone."),
        ("wld-8", "WLD-8", "The junction", "Two tracks merging into one — the railroad anastomosis."),
        ("wld-9", "WLD-9", "The coupling", "Two open tubes clasped mouth-to-mouth."),
        ("wld-10", "WLD-10", "The braid", "Two vessels woven over-and-under, bound in gold — the founder's favorite."),
        ("wld-11", "WLD-11", "The confluence", "Four vessels at one golden node — the medical plus sign, drawn by circulation."),
        ("wld-12", "WLD-12", "The splice", "Six strands interwoven — the sailor's end-to-end join."),
    ]),
    ("XVI · The crossing studies", [
        ("cr-1", "CR-1", "Atlas style", "Double-contour vessels — the anatomical atlas wall."),
        ("cr-2", "CR-2", "Calligraphic", "Strokes that swell and taper like a brush."),
        ("cr-3", "CR-3", "The weave — no gold", "The over-under gap does the work — no gold at all."),
        ("cr-4", "CR-4", "Pure — no gold", "The exact mark with the golden part removed."),
        ("cr-5", "CR-5", "Monumental", "Ultra-thick bars, no lumens, no gold — the favicon cut."),
        ("cr-6", "CR-6", "Branched", "One small branch per arm — the anatomical telling."),
        ("cr-7", "CR-7", "Ribbon twist — kept", "Flat ribbons half-twisting through the crossing — the only study kept from this round."),
        ("cr-8", "CR-8", "Wide-mouthed", "Generous flared lumens — the strongest vessel cue."),
    ]),
    ("XVII · The crossing textures — same design, new skin", [
        ("tex-1", "TEX-1", "Two-tone cylinder", "Lengthwise light/dark split — roundness, perfectly flat."),
        ("tex-2", "TEX-2", "Engraved hatch", "Fine bone hatch lines — the vintage anatomical plate."),
        ("tex-3", "TEX-3", "Sheen highlight", "One thin lighter line along each upper edge."),
        ("tex-4", "TEX-4", "Segmented bands", "Perpendicular bands — myelin segmentation."),
        ("tex-5", "TEX-5", "Stipple", "Fine scatter of lighter dots — old-plate engraving."),
        ("tex-6", "TEX-6", "Crosshatch", "Two directions of bone lines — classical engraving."),
    ]),
    ("XVIII · The braid textures — the founder's actual pick", [
        ("bt-1", "BT-1", "Two-tone cylinder", "Light and dark tones through the weave."),
        ("bt-2", "BT-2", "Engraved hatch", "Hatch lines following the weave."),
        ("bt-3", "BT-3", "Sheen highlight", "The line faithful through every crossing."),
        ("bt-4", "BT-4", "Segmented bands", "Myelin bands woven through."),
        ("bt-5", "BT-5", "Stipple", "Stipple dots through the weave."),
        ("bt-6", "BT-6", "Crosshatch", "Classical crosshatch on the woven tubes."),
    ]),
    ("XIX · The inspiration volley — designed to outclass the reference", [
        ("sup-1", "SUP-1", "The braid, elevated", "The competitor's confidence on our braid — woven vessels, gold band, monumental."),
        ("sup-2", "SUP-2", "The self-tying vessel, elevated", "The competitor's instant readability on the artery-through-the-golden-ring mark."),
        ("sup-3", "SUP-3", "The AV union, elevated", "Corporate-grade confidence on the artery-vein-graft union."),
        ("sup-4", "SUP-4", "The emblem, elevated", "The vessel-join infinity at flagship confidence."),
        ("sup-5", "SUP-5", "The free interpretation", "The generator's own best read: everything the reference has, plus anatomy."),
    ]),
    ("XX · The med-student lens — exam iconography, joined", [
        ("qst-1", "QST-1", "The question", "Five answer-vessels; the correct option is the anastomosis — the answer is the join."),
        ("qst-2", "QST-2", "The score ring", "The ring every qbank shows — petrol arc of right answers, crimson of wrong, gold cursor."),
        ("qst-3", "QST-3", "The correct answer", "A checkmark whose long stroke is completed by the join — the reward, drawn as an operation."),
        ("qst-4", "QST-4", "The question mark", "The question drawn as a vessel; its dot is an open mouth waiting to be joined."),
        ("qst-5", "QST-5", "The flashcard", "The card split crimson and petrol, gold flip line — two facts, one card, the app icon."),
        ("qst-6", "QST-6", "The match", "The matching question: crimson stub, petrol stub, one gold connector — the match is the anastomosis."),
    ]),
    ("XXI · The name × the mission — the operation performed on the mission", [
        ("msn-1", "MSN-1", "The becoming", "From student to physician: two vessel-beings, joined at the gold — who you are and who you are becoming, anastomosed."),
        ("msn-2", "MSN-2", "The graft", "The knowledge gap, bridged: a crimson vessel with a missing segment, sealed by a gold graft — every wrong answer shows the gap; the explanation is the graft."),
        ("msn-3", "MSN-3", "The fragments", "Everything you've studied, finally one flow: scattered vessel stubs converging into a single joined current."),
        ("msn-4", "MSN-4", "The transformation", "Where memorized facts become understood mechanisms: rigid ink pipe-work joined into a living vessel — mechanism-first, literally."),
        ("msn-5", "MSN-5", "The bypass", "Fix how you think: the blocked flow, bypassed by a gold-sealed graft — the old motto performed as an operation."),
        ("msn-6", "MSN-6", "Two vessels, one mind", "The bio line made anatomy: two vascular trees, one joined crown — two trees of learning, a single mind."),
    ]),
    ("XXII · The education signal — the founder's trees, and friends", [
        ("tree-1", "TREE-1", "The brain tree", "The founder's idea: a trunk whose branches anastomose into a brain — study grows the mind, and the growth is the join."),
        ("tree-2", "TREE-2", "The letter tree", "The founder's idea: a living trunk that splits, fuses, and grows into the letter A — the name rising out of the ground."),
        ("tree-3", "TREE-3", "The vascularized brain", "The brain silhouette drawn entirely as anastomosed vessels — crimson hemisphere, petrol hemisphere, gold-sealed midline."),
        ("tree-4", "TREE-4", "The arbor vitae", "The insider's mark: the real tree that lives inside the cerebellum — neuroanatomy's own anastomosing tree."),
        ("tree-5", "TREE-5", "The mind map, made anatomy", "A central lumen node with anastomosed vessel branches radiating — every study session, drawn as vasculature."),
        ("tree-6", "TREE-6", "The rooted loop", "A sapling above ground; the infinity loop as its roots below — the learning loop feeding the growth."),
    ]),
    ("XXIII · The final ten — the brain era, descended", [
        ("fin-1", "FIN-1", "The brain tree — seamless", "The brain tree with no gold: crimson and petrol branches fusing colour into colour."),
        ("fin-2", "FIN-2", "The vascularized brain — seamless", "The brain of vessels with no gold: the hemispheres join by the meeting itself."),
        ("fin-3", "FIN-3", "The brain tree — explicit brain", "The crown unmistakably a brain at first glance, gold rings at the fusions."),
        ("fin-4", "FIN-4", "The brain tree — explicit, seamless", "The unmistakable brain crown, no gold — folds woven of the two vessel colours."),
        ("fin-5", "FIN-5", "Two hemispheres — corpus callosum", "The brain's own anastomosis: two hemispheres, four crossing vessels, gold-sealed joins."),
        ("fin-6", "FIN-6", "Two hemispheres — seamless", "The corpus callosum concept with the gold removed — crimson bridges fusing into petrol."),
        ("fin-7", "FIN-7", "The neurovascular unit — masterpiece", "A neuron's axon anastomosing into a vessel — wiring and plumbing, one system."),
        ("fin-8", "FIN-8", "The infinity brain — masterpiece", "Two brain hemispheres as the loops of an infinity — the two best ideas, one shape."),
    ]),
    ("XXIV · The brain × the heart — the founder's fusion, and pure magic", [
        ("bh-0", "POST-1", "The first post — extracted", "The graphic from the first grid post of the vascularized-brain profile, made a standalone mark."),
        ("bh-1", "BH-1", "The dual organ", "Half brain in petrol, half heart in crimson, gold-sealed midline — the two organs of every physician."),
        ("bh-2", "BH-2", "The dual organ — seamless", "The brain-heart fusion with no gold — colour into colour."),
        ("bh-3", "BH-3", "The heart feeding the mind", "A heart whose great vessels rise and anastomose into a brain."),
        ("bh-4", "BH-4", "The neurocardiac loop", "Brain and heart joined by one endless vessel looping into an infinity between them."),
        ("bh-5", "BH-5", "The heart's little brain", "A heart containing a brain woven of its own coronary vessels — the forty thousand neurons in the heart."),
        ("mg-1", "MG-1", "One line, two organs", "A single unbroken vessel: a brain fold above, a heartbeat below, the gold suture between."),
        ("mg-2", "MG-2", "The pulse tree", "The brain tree on an ECG trunk — knowledge grows on a heartbeat."),
        ("mg-3", "MG-3", "The organ embrace", "A brain-lobe and a heart-lobe nested like yin and yang, completing one circle."),
    ]),
    ("XXV · The field research + the founder's wordmark", [
        ("ins-1", "INS-1", "The Rx — vessels", "The prescription sign drawn as one continuous vessel — the crossing gold-sealed."),
        ("ins-2", "INS-2", "The high-yield star", "Anki's star made anatomy: five vessel arms from a gold node."),
        ("ins-3", "INS-3", "The night owl", "The mascot lesson in vessel language: an owl of one loop, lumen eyes."),
        ("wrd-1", "WRD-1", "The name in vessels", "Anastomosis written in one continuous crimson-to-petrol tube."),
        ("wrd-2", "WRD-2", "The capillary wordmark", "Each letter a capillary bed on a baseline feeder — angiography typography."),
    ]),
    ("XXVI · The wordmark era — paired versions, with and without .md", [
        ("wm-1", "WM-1", "Continuous vessel — no .md", "The perfected one-tube wordmark: crimson to petrol, looped o's, gold-sealed t's."),
        ("wm-2", "WM-2", "Continuous vessel — with .md", "The same wordmark with a quiet gold '.md' — the domain finishing the name."),
        ("wm-3", "WM-3", "The O-loops — no .md", "Geometric type whose two o's are the infinity's loops."),
        ("wm-4", "WM-4", "The O-loops — with .md", "The O-loops wordmark with a gold '.md'."),
        ("wm-5", "WM-5", "Capillary, perfected — no .md", "Intricate capillary-bed letters on a bold baseline feeder."),
        ("wm-6", "WM-6", "Capillary, perfected — with .md", "The capillary wordmark with a gold '.md'."),
        ("wm-7", "WM-7", "The A-lockup — no .md", "A vessel-A leading 'nastomosis' in clean ink."),
        ("wm-8", "WM-8", "The A-lockup — with .md", "The A-lockup with a gold '.md'."),
    ]),
]

TOTAL = sum(len(marks) for _, marks in SERIES)

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
.serieshead{margin:44px 0 18px;padding-top:26px;border-top:2px solid var(--rule)}
.serieshead:first-child{margin-top:0;border-top:none;padding-top:0}
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
.stamp{position:absolute}
#starredView .cards{grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:22px}
.empty{padding:70px 0;text-align:center;color:var(--ink3);font-family:var(--serif);font-style:italic;font-size:26px}
.foot{margin-top:52px;font-family:var(--mono);font-size:10px;letter-spacing:.18em;color:var(--ink3);text-align:center;line-height:2.1}
body.hide-elim .card.eliminated{display:none}
"""

SCRIPT = """
<script>
(function(){
  var KEY='anastomosis-gallery-v1';
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

sections = []
for series_name, marks in SERIES:
    cards = []
    for stem, chip, title, note in marks:
        cards.append(
            '<div class="card" data-id="%s">'
            '<div class="cardhead"><span class="chip">%s</span><span class="t">%s</span>'
            '<div class="cardbtns"><button class="star" title="Star this mark">&#9734;</button>'
            '<button class="elim" title="Disqualify this mark">Disqualify</button></div></div>'
            '<img src="%s" alt="%s — Anastomosis mark">'
            '<div class="cardnote">%s</div></div>'
            % (chip, chip, title, uri(stem), title, note)
        )
    sections.append(
        '<div class="serieshead"><div class="eyebrow">SERIES %s</div><h2>%s</h2></div>\n'
        '<div class="cards">%s</div>' % (series_name.split(" · ")[0], series_name.split(" · ", 1)[1], "\n".join(cards))
    )

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Every Anastomosis mark ever — the master gallery</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>%s</style></head><body>
<div class="wrap">
  <div class="eyebrow">ANASTOMOSIS.MD &middot; THE MASTER GALLERY &middot; 23 OCT 2026</div>
  <h1>Every mark ever.</h1>
  <p class="sub">All <b>%d Anastomosis marks</b> across %d series — from the first five icons to the braid and its six skins. <b>Disqualify</b> what you don't like (it dims and stays out of your way), <b>star</b> what survives (it turns gold), and open the <b>Starred</b> page to compare your shortlist side by side. Your choices persist in this browser.</p>
  <div class="bar">
    <button id="tabGallery" class="tab on">Gallery</button>
    <button id="tabStarred" class="tab">Starred (0)</button>
    <button id="hideBtn" class="ctl">Hide disqualified</button>
    <button id="resetStars" class="ctl">Reset stars</button>
    <button id="resetElim" class="ctl danger">Reset disqualifications</button>
    <div class="count"><b id="cStar">0</b> starred &middot; <span id="cElim">0</span> disqualified &middot; <span id="cTotal">%d</span> total</div>
  </div>
  <div id="galleryView">%s</div>
  <div id="starredView" style="display:none">
    <div class="serieshead"><div class="eyebrow">YOUR SHORTLIST</div><h2>The starred, side by side.</h2></div>
    <div class="empty" id="starredEmpty">Nothing starred yet &mdash; go back to the gallery and tap the stars.</div>
    <div class="cards" id="starredGrid"></div>
  </div>
  <div class="foot">ANASTOMOSIS.MD &middot; %d MARKS &middot; %d SERIES &middot; TWO VESSELS &middot; ONE MIND<br>STAR TO SHORTLIST &middot; DISQUALIFY TO ELIMINATE &middot; COMPARE SIDE BY SIDE</div>
</div>
%s
</body></html>""" % (CSS, TOTAL, len(SERIES), TOTAL, "\n".join(sections), TOTAL, len(SERIES), SCRIPT)

out = os.path.join(LAB, "anastomosis-gallery.html")
open(out, "w").write(html)
print("written:", out, os.path.getsize(out) // 1024, "KB")
print("marks:", TOTAL, "| series:", len(SERIES))
