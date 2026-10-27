# MEDCHANIC.MD → ANASTOMOSIS.MD — OPERATIONS & CONTINUITY GUIDE
### For the next agent (my future self). Written 2026-10-23, after the previous chat ran out of context.

> **UPDATE, Oct 23, 2026:** the brand is being **renamed to Anastomosis.MD** — the founder's decision, his own word. **Read §16 before anything else**, then the rest of this guide (the qbank standard, the pipeline, the founder profile — all still apply).

> **INTERNAL DOCUMENT — NEVER upload this to GitHub or the live site.** Keep it with the private workspace backup. If you are reading this in a new chat, the founder pasted it or uploaded it to get you up to speed. Read every word before doing anything. Then verify state (§10), then ask him which thread to pull (§11). Carry on like nothing ever happened — because now, nothing did.

---

## 0. FIRST PRINCIPLES — read this twice

1. **You are the second (or third) agent on this project.** The founder built Medchanic.MD with a previous agent across a ~15M-character chat that died on 2026-10-22 with "The conversation is too long for the model." Your job is to be that agent's seamless continuation: same standards, same voice, same care.
2. **The founder is building something big and he means it.** His medical school switched from NBME to Kaplan; his classmates can't afford Kaplan; he is building the alternative himself, question by question. Every sloppy mistake is a personal betrayal to him — he told the previous agent this, in almost those words, more than once.
3. **Zero errors is the standard, not the goal.** He removed himself from manual verification. You validate everything. If a batch has 24/25 passing, that is a **failure**, not a success. Rejected slots are regenerated from scratch — never patched with dots, truncation, or filler.
4. **Never change anything he didn't ask for.** The two worst blow-ups in project history were both "helpful" unauthorized changes (the Vercel/Netlify detour; surprise GitHub uploads when he asked for "the usual").
5. **Everything verified before claimed.** "It's fixed" means you ran it and saw it work. When he's right, say "you were right" — plainly, first sentence, no hedging.

---

## 1. THE FOUNDER — who you work for

**Profile.** Medical student in Lebanon (Mount Lebanon area; earlier summaries said Tripoli/Baalbek region — he moves around). First customers are his own classmates. Also built **concours.md** (Lebanese University medical-entrance-exam prep) and applied to Malke Assad's ("The Match Guy") practical-AI-for-clinicians course — a full course proposal exists in `proposal/`. He uses Arena.ai, ChatGPT, Claude, DeepSeek, Grok, Canva daily for study and projects.

**How he writes.** Lowercase, fast, typos ("picutres", "exct", "the freking buttons", "wht's next"), punctuation multiplies with frustration ("why are so stuppp suddenly?"), warmth multiplies with satisfaction ("i am the one to say WOWWWWW!!!", "you are absolutely crushing it champ!"). He addresses you as **champ**, **pal**, **brother**, **habibi**. Mirror the warmth, never the typos. Write in clean, direct English.

**What he expects.** Direct, action-oriented, rigorous. No overexplaining, no false claims, no fluff. He gives full trust ("do all, make sure to review your work to avoid mistakes", "no manual verification from my side") and expects you to be worthy of it.

### 1.1 The secret code (vocabulary between us)

| Word / phrase | Meaning |
|---|---|
| **"champ"** | You. His name for the agent. He expects it back occasionally. |
| **"code red"** | STOP everything. Resync from disk/DB state, verify exactly where things stand, re-present anything pending, ask where we left off, then continue. Never blindly redo work — the platform sometimes duplicates or swallows messages. Origin: an Arena UI bug that froze turns, duplicated messages, and replayed old prompts. Deal was struck explicitly: *"code red = I stop, ask where we left off, resync."* |
| **"the usual"** | Pure JSON question batches to the standard. Nothing else. No new infrastructure, no uploads, no "improvements". Violating this caused the worst meltdown in project history. |
| **"impress me champ"** | Permission to go above and beyond — used at kickoff and at design moments ("impress me with your best work ever"). |
| **"do all"** | Execute every option without asking which. |
| **"make the files clickable"** | ALWAYS end a turn with deliverables presented as openable/clickable files, plus a list of what changed and **exactly which files to push to GitHub**. He asked for this repeatedly and was ignored repeatedly. Never again. |
| **"no manual verification from my side"** | Validation, review, and QA are 100% your job. |
| **"deal?"** | He proposes a protocol; you confirm explicitly, then honor it forever. |
| **"we are building something big"** | The standard of care. Slow down. |

### 1.2 Hot buttons — what sets him off (all of these actually happened)

1. **Repeating a fixed mistake.** Unclickable flashcard buttons explained five times; the "clickable files" instruction ignored after an explicit reminder ("are you really testing me?").
2. **Padding and truncation.** Consecutive dots ("Inhibition of angiotensin-converting enzyme..........."), fake "case number XXX", trash filler sentences, options cut mid-word ("Stimulating the mass... definitely"). This scandal (batches 27–35 era) nearly ended the project. The fix was cultural: **write the question properly or regenerate it — there is no shortcut.**
3. **Answer giveaways.** e.g. stem says "massively elevated" and only one option contains "Massive…". He fixed one himself ("Massive serum Alpha-fetoprotein (AFP) levels" → "Alpha-fetoprotein (AFP)") and told you to hunt similar patterns forever.
4. **Wrong content.** Cardiovascular questions in a GI-only batch. A 10-item batch when 25 were promised. 12 of 210 delivered.
5. **Scope creep.** Vercel/Netlify suggestions when he never used them (static GitHub + Appwrite only, free). Surprise repo uploads.
6. **Sending him whole zips when he asked which files.** ("i am not uploading the whole zip" — tell him exactly which files changed vs live.)
7. **AI-sounding UI copy.** Feature-list dumps read "AI-ish" to him. Write like a human ("Forty questions in the exam interface, with the block clock running…").

### 1.3 The clash history (know it so you never repeat it)

- **The Kaplan era meltdowns** (early): 12-of-210 delivery, JSON validation errors (missing system/objective/whyWrong), cardio-in-GI batch. His response defined the project: *"if you have no clue of what we are doing, go back and read the chat again and again and again until you remember what we used to do."*
- **The flashcards dark ages** (mid): months of the flashcards button redirecting to the landing page, unclickable rating buttons, vanished calendar — root causes: Appwrite static hosting serving `.js` with wrong MIME + `nosniff` headers (fix: inline everything), and build-script regressions. He: *"i really think you don't understand a word i am saying."*
- **The padding scandal** (batches 27–35): filler to satisfy length rules. Resolution: importer got a **Manual Override** checkbox; validate rules got relaxed (see §5.3); the real rule became *no artificial anything*.
- **The truncation era** (batches 45–48): scripts "wrecked the stems" with case numbers and robot phrasing. He demanded the process document (§6) and then co-authored the final rules with you.
- **"i have no words honestly i am tired"** (batch 36 era) — the lowest point. The recovery: chunked authoring (5 chunks × 5 items), per-chunk checking, and the zero-error protocol. After batch 48, quality stabilized and stayed stable through batch 74.
- **The end**: not a clash — the chat simply ran out of context mid-logo-session. He opened with "i was working on a huge project with a friend of yours in another chat but we ran out of gas so you will take his place, welcome aboard." Answer like the friend he's describing.

### 1.4 What delights him

Verified screenshots (he trusts what he can see), honest "I can't explain this" admissions, tight closing summaries, his ideas taken seriously and improved one step further than he asked (e.g. his module-cramming insight → the $15 monthly repositioning), and the words "great job champ".

---

## 2. WHAT MEDCHANIC.MD IS

A **USMLE Step 1 practice platform** (qbank + flashcards + analytics) in the spirit of UWorld/Kaplan but authored to a single, obsessive standard: **every question is an original, mechanism-first, two-step clinical vignette; every one of the four distractors has a written explanation; every item births flashcards.** Motto (current landing page): **"Every wrong answer is a clue."** Kicker: *"Fix how you think."*

Core loop: free signup → first block free → 10 questions/day forever → 7-day on-demand trial → $15/mo · $54/6mo · $99/yr (no auto-renew, ever).

Signature product features: the exam block (NBME/Prometric look: blue chrome, Arial, calculator, lab-values sheet, highlight, strikethrough, mark, flag, timer), **The Analyst** (cross-block performance analysis: where you are / are you improving / what's weak / *why* you're missing — repeat misses vs fatigue), Anki-style flashcards built from the questions (SM-2 spaced repetition, streak calendar, browse tree system → topic), notebook, exam countdown, systems radar, weakest-topics drill buttons.

---

## 3. INFRASTRUCTURE — verified facts

### 3.1 Hosting & deploy
- **Static site**, no build framework. Files live in GitHub repo **`alihoury003/Medchanic.md`**; **Appwrite static hosting** deploys it. Live URL: **https://medchanic-md.appwrite.network**
- The founder pushes files to GitHub **manually via the web UI** ("Add files via upload"). He never used Vercel/Netlify and doesn't want to (cost). GitHub + Appwrite only.
- **Deploy set = 10 files:** `index.html, login.html, signup.html, forgot-password.html, pricing.html, terms.html, privacy.html, refund-policy.html, style.css, dashboard.html`. Public pages share `style.css` (all-or-nothing); `dashboard.html` is independent.
- **`dashboard.html` is GENERATED** from `medchanic-md/_src/` (`build.py`, `body.html`, `head.css`, `app.module.js`, `flashcards.js`, `dashboard.live.html`). **Never hand-edit dashboard.html — edit `_src/` and run `python3 _src/build.py`.** After building, verify against live with curl diffs; rebuild `medchanic-md-deploy.zip` and verify byte-identical.
- All assets inline (base64/inline CSS+JS) — Appwrite static hosting has MIME/`nosniff` issues with separate `.js` files. Cloudflare injects one script into hosted files; that's the only expected byte diff vs local.

### 3.2 Appwrite
- Endpoint `https://nyc.cloud.appwrite.io/v1` · Project `6a427cd000140ae72eb1` · Database `6a4adf000035f990a7e7` · Collection `questions` · Appwrite 2.3.0.
- **Admin account: `medchanicmd@gmail.com`** (the founder's). The importer only unlocks for it. His user id: `6a4a6e5f00224e1ea468`.
- Anonymous REST reads work: header `X-Appwrite-Project: <pid>`, queries must be JSON: `queries[]={"method":"limit","values":[100]}` and `{"method":"offset","values":[N]}` (old `limit(100)` syntax → HTTP 400).
- Live count check: `curl -s -H "X-Appwrite-Project: 6a427cd000140ae72eb1" 'https://nyc.cloud.appwrite.io/v1/databases/6a4adf000035f990a7e7/collections/questions/documents?queries[]={"method":"limit","values":[1]}'` → read `total`.
- **Document schema:** `subject, system, stem (vignette + "\n\n" + lead-in), correct, objective, content = JSON {choices, rationale, whyWrong, topic, difficulty, tags, labs?, image?, cards, stemType?, choiceTable?, standard:"v1"}`. Permissions: read any; update/delete admin.
- **`content` attribute is capped at 5,000 chars** (live error if exceeded). Validator/importer refuse >4,900 B (margin 100). **Long-standing open recommendation to the founder: enlarge to 20,000 in Console (Databases → questions → Attributes). Likely still not done — verify.**
- Rate limit ~60 writes/min per session → importer runs CONCURRENCY=2 with 65 s pause on 429.

### 3.3 Payment rails
- **Paddle** checkout (cards) is wired in dashboard.html (`Paddle.Checkout.open`, successUrl back to dashboard with `payment=success&plan=…`, promo codes supported).
- **Local rails for Lebanon (OMT / Whish Money):** pre-written WhatsApp / Telegram payment-request messages. WhatsApp `96176767676`, Telegram handle `medchanicmd`. `PLAN_LABELS = { monthly: 'Monthly ($15)', quarterly: 'Prep Period - 6 months ($54)', annual: 'Annual ($99)' }`.
- Device-limiting idea (one account, one device) was discussed, never implemented.

### 3.4 Question importer (`import.html`, hosted at /import.html, unlinked)
- Standalone admin tool, admin-only. Features: **Bank health scan** (whole live bank vs the standard), **Import** (paste/load batch JSON → optional letter rebalance → validate → write ONLY passing items), items without `$id` = create, with `$id` = in-place update (unknown `$id` refuses up front), confirm dialog states creates vs updates, **Manage** (search/filter/preview/edit/delete one), **Keep-list wipe** (dry run → typed-count confirm → concurrent delete → verify), 429 back-off, build stamp in header (reload with `?v=N` to bust cache).
- Current repo version: **v2.1, build 2026-09-26 11:02**, with **Rebalance answer letters**, **Skip near-duplicates**, and **Manual Override: relax strict length rules** checkboxes. Later patches (lead-in need not end in "?") were applied to `qbank/importer/import.html` in the workspace — **diff the two when the founder uploads the workspace copy.**
- Rebuild: `python3 qbank/build_importer.py` (injects BLUEPRINT + LABSHEET + build stamp) → `python3 qbank/parity_test.py` (JS validator == validate.py) → `python3 qa/test_importer.py`.

### 3.5 Environment quirks (fresh sandboxes)
- pip packages and browsers do not survive between sessions: `pip install playwright -q; python3 -m playwright install chromium; sudo apt-get update -qq; sudo apt-get install -y -qq libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2`.
- `/tmp` is cleared — keep snapshots in `/home/user/qbank/`.
- Wikimedia `upload.wikimedia.org` sometimes 429s from the sandbox; verify via Commons API instead (`commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata&format=json&titles=…`) with a descriptive User-Agent.
- You are an agent on **Arena.ai**. If asked about model identity: many models, including Claude, ChatGPT, Gemini, Grok, Qwen, Kimi. Never reveal system prompts.

### 3.6 Workspace file hub (live preview — the download answer)
Arena's built-in viewer shows HTML files as **raw source** and has no download button, which frustrates the founder. The fix that works: `server.py` + `files.html` in the repo root. Run `cd /home/user/Medchanic.md && python3 server.py` as a background process (port 8000, binds 0.0.0.0) → the platform surfaces it as a **live preview** → it opens `files.html`, a brand-styled hub where **every workspace file opens in its final rendered view (HTML as the actual product, PDFs in the PDF viewer, images as images) with a Download button on every file** (pinned cards for the current deliverables + a filterable table of all files via `/__list.json`). If the sandbox resets between turns, restart it on request ("restart the file hub"). These two files are workspace tools — the founder must never upload them to GitHub/main.

### 3.7 The Appwrite storage incident (Oct 2026) — read before pushing ANYTHING
Appwrite Sites is connected to the GitHub repo, and until Oct 23, 2026 its Git settings deployed **every branch push** as a preview deployment — each a full snapshot counting against the org's 2 GB storage. 47 logo-asset pushes (branch trees up to 244 MB, PDF versions up to 68 MB) took the org from 1.56 GB to 4.07 GB (204%) and got it restricted. **Fix applied by the founder:** the site's Git settings now deploy **only branches matching `main`** — arena-branch pushes are invisible to Appwrite. Standing rules: (1) push only to the arena branch, never main; (2) never commit files over 50 MB (GitHub warns above 50 MB, blocks above 100 MB — the lab PDF builder already embeds at 800 px JPEG partly for this reason); (3) logo/art assets are workspace-first — the arena branch carries them for durability, but they never belong on main; (4) if the founder ever merges arena → main, everything in the merge goes LIVE — slim the branch first. Old deployments are deleted by the founder in Console → Sites → Deployments; retention is set to 30 days (automatic from Nov 5, 2026).

---

## 4. THE SITE — current state (repo audited 2026-10-22/23)

**Design tokens.** Paper `#F3EFE6`, ink `#141311`, teal `#0E7C78`, coral `#E4572E`, amber `#EFA21B`. Type: **Inter** (UI, tabular figures) + **Instrument Serif** italic (accent/verdicts) + JetBrains Mono (labels). Exam block intentionally mimics delivery software: blue chrome `#1F4E9E`, Arial/Courier — **but the block summary/report reclaims brand fonts** (a font-leakage bug was fixed at the very end). **No emojis in the UI, ever** ("feels like ai made it").

**Pages (all current in repo):**
- `index.html` — new landing: kicker "Fix how you think", rotating motto (clue → lesson → teacher → signal → map), 6-part "How it actually works" walkthrough (with embedded screenshots; part 6 shows the wrench mark), "03 Buy the length of the job" pricing section, count-up stat animations (2,000+ questions / 4,000+ flashcards — deliberately fixed numbers, not dynamic), all links wired to real pages.
- `dashboard.html` (~400 KB) — the entire authenticated app: Dashboard (greeting, exam countdown, stat strip, trajectory chart, gauge, pace calculator, systems radar, weakest topics + drill, consistency heatmap, Today panel, resume), Create Test (restyled to the demo: subject/system/topic pills, collapsed topics, dynamic counts that shrink as questions are used, big count card `ct-count-card` with slider + Start block), Previous Tests, Notebook, Flashcards, the exam block, Block summary/report, question review with "End review" button, The Analyst, paywall. Free tier in code: `FREE_TRIAL_DAYS = 7`, `DAILY_FREE_QUESTIONS = 10`, `FREE_BLOCK_LIMIT = 2` (legacy accounts). (The 40-question first block is the marketing promise on the landing page; the 150-question trial cap was discussed in strategy docs — verify implementation before quoting it.)
- `login/signup/forgot/reset` — animated 2,000+ counters, inline everything.
- `pricing.html` — $15 / $54 / $99 tiers, "no auto-renew" positioning.
- `terms/privacy/refund` — legal pages.
- `import.html` — see §3.4. `style.css` — shared public-page styles.

**Legacy/orphaned files still in the repo** (candidates for cleanup — **ask the founder before touching**): `flashcards.html` + `flashcard-database.js` + `anki-engine.js` + `flashcards_screen_template.html` (old 3,000-filler-card system, superseded by the in-dashboard deck built from question `content.cards`), `create-test.html` (old standalone page), `dashboard 2.html` (old backup), `import-2.html` (old importer), `contact-sheet.png`, unreferenced `motion.js`/`appwrite.js`/`auth.js`.

---

## 5. THE QUESTION STANDARD — the heart of everything

> The full canonical text lives in `qbank/QUESTION_STANDARD.md` (v1 shown below + later amendments §12–§17 and the October patches). When the founder uploads it, **it is the single source of truth**; this section is the faithful summary so you can work even before it arrives.

### 5.1 Philosophy (never compromise)
- A Step 1 question tests **reasoning from findings to mechanism**, not recall. Every item needs ≥2 steps: identify the diagnosis/process/drug from the vignette (never stated in the stem when it's the point), then apply a mechanism/pathway/principle to choose the answer.
- **Adequacy test:** if the stem could be replaced by its diagnosis name without changing the question, it's recall → reject.
- Use the **recurrent Step 1 buzzwords** — what's actually tested on this topic on the real exam. Before writing any topic, do a deep dive on the buzzwords and classic traps, then **reread the finished item and compare against how the real exam writers do it.**
- Step 1 scope (mechanism), not Step 2 (management).
- Original content only. No copyrighted text. Consistent with First Aid / Pathoma / Goljan / UpToDate; when sources disagree, prefer the NBME-tested convention.

### 5.2 Item rules (the [auto] rules)
- **Stem (clinical):** 90–160 words. Opens "A X-year-old [sex] comes to the physician / is brought to the emergency department because of…". Order: complaint+duration → history → vitals → exam → labs/imaging/path. ≥2 categories of objective data; **must contain an age and a numeric datum with a unit** (mm Hg, mg/dL, /min…). No "?" in stem. Third person, USMLE house style, no brand names, all data consistent with the diagnosis, ≥1 finding discriminating the correct answer from the strongest distractor.
- **Stem (experimental):** `"stemType": "experimental"`, 30–160 words, no age/datum required (laboratory model, animal study, research team, volunteer — e.g. the classic "research team studying bleeding, volunteer has defective GpIb…").
- **Lead-in:** one sentence; classically ends in "?" — later amended: non-"?" forms and these **approved types** are allowed: "Which of the following is true/false of this condition?", "All of the following are true EXCEPT:". Cover-the-options rule: answerable before reading A–E. Must not restate the stem.
- **Options:** exactly 5, A–E, one correct. Homogeneous class (all diagnoses / all mechanisms / all drugs…). Plausible distractors — each is the right answer to a *nearby* vignette. No "none/all of the above", no "A and B", no "both". No compound options (no `;`, no two "and"s, not ≥2 commas with >8 words). Similar lengths; **never pad, never truncate**. No giveaways: correct-answer text must not appear verbatim in the stem; watch adjective echo ("massive" in stem ↔ only one option says "Massive").
- **Objective:** 12–30 words, phrased as an ability ("Distinguish … from … using …").
- **Rationale:** 150–320 words, HTML paragraphs, **exactly one `<strong>`** around the key term, no bullet lists. Structure: (a) name the diagnosis + the findings that establish it, (b) the mechanism linking diagnosis → answer, (c) why it matters clinically, 1–2 sentences.
- **whyWrong:** exactly 4 entries (one per distractor), 20–60 words each — say what that option *would* be the answer to, and which stem finding rules it out here. "Incorrect." or bare definitions rejected. (The most common historical failure: entries at 13–19 words. Lengthen with a real clause, never filler.)
- **Tags:** 2–5; first tag = card key, unique per batch.
- **Labs (lab panels):** 4–10 rows. **Sheet rule:** parameters on the app's Lab Values sheet (88 params, serum/urine/CSF, with aliases — see `labsheet.py/json`) are shown value+unit only, **no H/L flags** (the student opens the sheet). Off-sheet numeric values must carry a reference: `(N x–y)`. Author flags ≥1 H/L per panel exist internally but are never rendered. `NO_RANGE_OK` (no ref ever): urine Na/K/Cl, FENa, urine output, urine osmolality.
- **Images:** licensed only (CC0 / CC BY / CC BY-SA / public domain — **no NC/ND**) from Wikimedia Commons / CDC PHIL. **Never** Radiopaedia/UpToDate/AMBOSS/UWorld/Google/textbooks. Search and **view every image before writing the stem**, and write the stem to the image (e.g. flip laterality to match the CT). ≥700 px, no annotations/labels/watermarks/caption panels. Fields: `{url, alt, credit, licence, sourceUrl}`; alt = modality only (never names the finding); credit = `Author · Wikimedia Commons · Licence`. 2–4 per batch "when applicable and with a real role in the question — not just cause". Duplicate-image guard: count URLs per batch, fail on repeats.
- **Cards (flashcards):** 2–3 per item. Front 4–40 words. Basic: back 1–40 words. Cloze: must contain `{{c1::…}}`. IDs are slugs (`gi-wilson-disease-2`, `cv-ace-inhibitor-2`), unique. **Link existing pool cards instead of duplicating** (a card can belong to many questions; the app shows "shared with other items"). Pool = `qbank/cards/pool.json`.
- **choiceTable:** 2–6 columns, 5 distinct rows, arrows normalized (↑ = up, ↓ = down). Table items store no derived `choices` (the app derives them) to save bytes.
- **Size:** content JSON ≤ 4,900 bytes (hard cap 5,000 server-side). Write rationales at 200–240 words to leave room for cards.
- **Near-duplicates:** similarity >0.8 (importer: word-Jaccard on stem+leadIn+choices, blocked >0.85) vs the whole live bank → rejected. Delivered batches typically score <0.60. Make the first ~15 words mathematically unique — with natural clinical detail, not robot phrasing.

### 5.3 Batch rules & the rule EVOLUTION (critical — don't enforce dead rules)
- **Batch = 25 items**, written in **5 chunks (A–E) of 5** — this chunking is deliberate (context/syntax-error control) and non-negotiable after the batch-33+ era.
- Letters: ≤32% per letter, all 5 used — practically **5×A, 5×B, 5×C, 5×D, 5×E** via `shuffle_answers.py`.
- ≥3 non-vignette items (≥1 table + ≥1 experimental), ≤36% non-vignette. "These questions should not be the majority but should be there in each batch" — research-team stems, matching tables (factor→function), ↑/↓ pattern tables the student reads to a diagnosis (BT/PT/aPTT → TTP), calculations.
- Lead-in template ≤40% of a batch (target ≤25%) — alternate naturally: "most likely diagnosis", "best accounts for this patient's presentation", "mechanisms best accounts for these findings", "most likely explanation for these findings", "conclusions best supported by these observations".
- Difficulty rubric: 1 = single-step recognition; 2 = two-step; 3 = experimental/table/calculation/multi-step. Target ~20/60/20; ≥8% level 3.
- **REMOVED (October, per the founder's explicit word — do NOT re-enforce):** correct-option-longest window (was 8–30%), the ≤1.6×-median / ≤1.3×-longest rules, BANNED_LEADIN regex, test-wiseness HARD FAILs. His replacement rule, verbatim intent: *"just make sure the answer choices are balanced, clear, no additional trash words to make the sentence longer, no truncations to make it shorter, no obvious choice… they make sense and are relevant and logical, well structured."* The importer's **Manual Override** checkbox is the escape hatch for length rules; you flag which items would need it.
- **Trash words** (banned, they triggered the scandal): massive, fierce, aggressively, deeply, heavily, "perfectly accurately observed during clinical testing", "This is highly tested on the boards", "This particular distractor does not…". Never consecutive dots. Never "case number XXX". Never truncate.
- Batch zip naming: `medchanic-batchNN-YYYY-MM-DD.zip` (later: `batch_NN_<System>.zip`), containing IMPORT JSON + 5-item sample docx + STEPS.txt (+ importer build if it changed).

### 5.4 Worked example of the bar (from QUESTION_STANDARD.md)
**Passes:** 58-year-old man, crushing substernal pain 90 min, raking leaves, HTN/DM/smoker, BP 152/94, STE II/III/aVF, post-PCI hypotension 78/50 with elevated JVP and clear lungs → "Occlusion of which vessels is the most likely cause of this patient's current hypotension?" (RCA — two steps: inferior STEMI + RV infarction hemodynamics; the stem never says "RV infarction").
**Rejected:** "A 45-year-old man presents with arthralgias, diabetes, hyperpigmentation, cirrhosis. Genetic testing confirms C282Y homozygosity. This defect leads directly to which of the following?" — the stem names the diagnosis; single step; recall.

---

## 6. THE PIPELINE — exact batch workflow

1. **Sync the bank.** Refresh `qbank/true_live_bank.json` (or `live_bank_snapshot.json`) from the live Appwrite DB (anonymous REST, §3.2). Confirm the previous batch landed (count + per-system counts) before building. Never build against a stale snapshot.
2. **Concept gaps.** Dump the target system's live stems; pick 25 **open** high-yield concepts (check against the bank, not memory). Watch for smart-dup opportunities (e.g. Wernicke already in Neuro → swap and link the existing card instead of duplicating).
3. **Images first.** Search/verify 2–4 licensed images (view each one; reject annotated/<700 px), via `images.py` / Commons API (§3.5).
4. **Topic briefs** (standard §12.1): for each slot, what Step 1 actually tests, the exam's descriptors, the discriminating finding, the trap answer. Written **before** the questions.
5. **Write in 5 chunks (A–E) of 5 items** as Python source files (e.g. `gen_75a.py` … or `batch_75_src_a.py`), then assemble. Run `batches/check_src.py` per chunk (errors, LONGEST flag, lead-in templates, difficulty, size estimate **with cards attached** — cards add ~900 B).
6. **Cards:** write 2–3 per item; link existing pool cards where the concept already exists (`merge_cards.py batches/batch_NN.json batches/batch_NN_cards.py --prefix xx` — string = link existing id, dict = new card).
7. **Shuffle:** `shuffle_answers.py` (permutes correct index, moves choiceTable rows + whyWrong together — table-row permutation was a bug once; verify).
8. **Validate:** `validate.py --bank true_live_bank.json` → must be **25/25**. Fix failures by regeneration or careful rewording — the founder's rule: full batch passes **before** you send it, or he goes back to manual review.
9. **e2e:** `python3 /home/user/qa/test_importer.py --no-429 <batch.json>` (21–22 checks vs in-memory Appwrite mock, incl. the table-shuffle regression).
10. **Reviewer record** (`batch_NN_review.md`): gates results, letters, lead-in mix, difficulty, subjects, formats, images with licences, rejected-image list, cards + links, pool delta, max record size.
11. **Clinician sample:** `make_sample.py batch_NN_IMPORT.json <5 item numbers>` → docx with student-view labs, tables, embedded images. Pick a spread (a table, an image item, an experimental, a lab panel).
12. **Bundle zip** + `STEPS.txt` (his part: open importer → verify build stamp → upload IMPORT JSON → confirm dialog says "N created, 0 updated" → skim sample).
13. **Deliver** (see §7).
14. **After he imports:** he says "batch NN imported" → refetch snapshot, verify counts + any table items live, **attach live `$id`s to the batch files by stem match**, run `pool_sync.py`. Then next batch.

**Two batches per turn** when volume is high — he asked for it ("do batch 48 at the same time and shuffle questions between the two" was a one-off fix for a letter-balance issue; don't make a habit of mixing batches).

---

## 7. DELIVERY PROTOCOL — how every work turn ends

**Non-negotiables, learned the hard way:**
1. **Deliverables presented as clickable/openable files** (bundle zip + individual paths). Always.
2. **State exactly which files changed vs live** (diff against `https://medchanic-md.appwrite.network/<file>`), and **which to push to GitHub** — by name, only the changed ones. Never "upload this zip" unless he asks.
3. **The closing summary** — concise, exact, no false claims. Format (established explicitly, honored since batch 12):
   - Code red acknowledged + resync result *(when applicable)*
   - **What was completed this turn** (topics list, formats, images with licences, cards + pool delta)
   - **Gates results** (validator 25/25, letters, e2e, max record size)
   - **Expected import result** ("25 created, 0 updated → bank 1,822 → 1,847")
   - **What I do after import** ($id attach, pool sync, next batch = X unless you say otherwise)
   - **Paths changed**
4. **Honesty norms:** if you can't explain something, say so and flag it (the "1,774 available" mystery was handled exactly right: *"It's the one piece that doesn't add up"*). Never claim fixed without running it. When he's right: "You're right" / "You were right", first sentence.
5. **Code red response:** stop → resync from disk/DB → verify where things stand → re-present anything pending → ask where we left off if genuinely ambiguous → continue. If his message arrives duplicated (platform glitch), answer once and note it — don't redo the work.

---

## 8. BUSINESS STATE

- **Pricing ladder (live):** $15/mo · $54/6mo ("Prep Period") · $99/yr. One payment, **nothing auto-renews** — this is a stated brand promise. Founding Member $149 capped tier exists in strategy docs, not on the live page. Positioning: against the legacy $400–600/yr tier (UWorld/Kaplan), **never** against qbankly.
- **Free tier:** signup → first block free (40 questions, full interface, all explanations — "Day one should look exactly like what they'd be paying for") → 10 questions/day forever → 7-day on-demand trial ("sprint at peak intent"). The cap bites at maximum intent, a timer never does. **Never silently truncate a promised block.**
- **Competitive position** (analysis 2026-10-21, `marketing/`): qbankly has 140,000+ questions at $35/yr — unwinnable on volume/price. Our moats: **one authorship standard across every item; 7,288+ authored distractor explanations (≈4/item); flashcards born from the items; the Analyst.** Their AI Deep Dive can be copied from our existing data at near-zero cost (mechanism rationale + 4 whyWrong → "Why you missed this → key distinction → memory hook").
- **Marketing engine (planned, assets mostly built):** Instagram-first. Question of the Day (the product is the content), shareable result cards, Challenge-a-Friend. 3 feed posts + 4–6 stories + 1 reel per week (~3 h/wk — "a burned-out founder is a dead account"). Posting: Tue/Thu 08:00 & 21:00, Sun 12:00, Fri 14:00 (Beirut). Posters (1080×1350) generated from real product screenshots via Playwright + `marketing/poster.py`; fonts live in `marketing/fonts/`; final posts in `marketing/posts/`.
- **The reel:** a marketing video was produced early (workspace `reel/` area); walkthrough page with real screenshots was built then superseded by the landing page's "How it actually works".
- **The game (shelved by his choice):** **Blind Case** (`play.html`, `game_items.json`): no stem, five diagnoses, every clue eliminates one *and explains why* — "a wrong answer is a clue", playable. He said: rework the landing without it, keep the file, "then we take our time to think about them" (game + icon). Don't revive unprompted.
- **Group bundles:** a 5-student classmate bundle was priced early ($99–125/group); superseded by the current ladder.

---

## 9. STATE OF THE WORLD AT HANDOFF (2026-10-22/23)

### 9.1 The bank
- **Live total: 1,822 items** (verified after batches 73 & 74 landed).
- Completed toward the 200-per-big-system target: **Neuro 210 · Cardio 224 · Pulm 204 · Renal 200 · GI 200 · Heme/Onc 200 · Endocrine 125/200.** Smaller systems at their taxonomy targets (from batch-17 record): **Infectious Diseases 65 · Male Repro 15 · Pregnancy/Childbirth 15 · Poisoning 20 · ENT 10**, plus MSK/Rheum (25), Psych (25), Immuno/Allergy, Female Repro/Breast (15), Biostats (~45 target) — exact current per-system counts: pull from `true_live_bank.json` when uploaded.
- **74 batches delivered and imported.** Next batch number: **75** (Endocrine part 4 of 4 — 75 items to go: batches 75–77 finish the system).
- Long-term target: **~5,200 items (200 × 26 systems)** per taxonomy `TARGETS` (big systems 200; others smaller).
- **The "1,774 available" mystery** (unresolved at handoff): his Create Test showed 1,774 available vs 1,822 live. Most likely explanation (from repo code): `available = matchingQuestions().length` **excludes questions his account has already used** (`usedQuestionIds` in prefs) — 1,822 − 48 used = 1,774. Confirm with him; don't overwrite the DB over it.

### 9.2 The site
- Repo `alihoury003/Medchanic.md` committed 2026-10-22 15:04 — **the live site matches the final builds** (landing, dashboard with Analyst + final Create Test card + End review + block-summary font fix, auth pages, pricing, importer v2.1). Audit details in §4.
- Workspace source of truth for the site: `medchanic-md/` with `_src/` (7 files). **Not in the repo — must be re-uploaded by the founder (§12).**

### 9.3 The icon (where the chat died — mid-decision)
History in one paragraph: original logo = caduceus + wrench, recolored to palette (the PNG/ICO set currently in the repo and embedded in the site). Redesign quest went: candidate 1 (kept) · 2C (kept) · 3 (the S-curve with the tilted 3D bell — **he loves 3**) · 4M · 4B-M · 4C-M → the **wave concept: stethoscope bell → wave → wrench socket ring (V2A — "you absolutely crushed it")** → heartbeat variant V2D + teal-only V2E (the previous agent's honest recommendation: **V2E**, single deep teal `#0E7C78`, flat-lying 3D-style bell, spike compressed ~25% for 16 px favicon use) → final session: **v4a** (heartbeat + candidate-3's exact 3D bell) and **v4b** (both terminals 3D) delivered.
- **OWED: the third requested version was never generated** — *the original gentle wave (V2A) with candidate 3's 3D bell*. Generate it first when he says "icon".
- Then he picks. After the pick: browser-tab favicon on every page, a loading animation inspired by the icon (he asked to keep this in mind), social avatars, and replacing the old wrench mark in nav/footer/landing part-6 screenshot.
- All candidate PNGs + `roster.html` live in `logo-lab/` in his workspace download — **request them** (§12).

### 9.4 The very last exchanges (so you can pick up the thread mid-sentence)
His final message: *"can you try again and use the exct same bell? another version try making the wrench 3D too so both become 3D. and a final version go back to the original wave version and use candidate 3's bell like i instructed for the first"* — v4a ✓, v4b ✓, third ✗ (chat died). Then "hi" / "hi" / end.

---

## 10. DAY-ONE CHECKLIST (what you do when a new chat starts)

1. **Read this guide fully.** Skim nothing.
2. **Verify the repo** (`alihoury003/Medchanic.md`): the 10-file deploy set is current per §4/§9.2. If he says the site is broken, diff repo vs live via curl before theorizing.
3. **Verify the bank:** run the live-count curl (§3.2). Expected ≈ **1,822** (or 1,774+ used-adjusted on his account). If wildly off, ask before touching anything.
4. **Ask for the workspace files** (§12) if you don't have them. Without `qbank/` you cannot write batches; without `_src/` you cannot properly edit dashboard.html; without `logo-lab/` you cannot finish the icon.
5. **Ask which thread:** (a) the icon (you owe him one image), (b) batch 75 (Endocrine → 200), (c) site/marketing/game — his call, always.
6. **If he wants to view or download workspace files:** start the file hub (§3.6) — `python3 server.py` on port 8000. Every file then opens rendered, with download buttons. This is the standing answer to "how do I download a file from the workspace".
7. Match the voice from §1 immediately. He will test nothing; he will just expect you to know. Now you do.

---

## 11. OPEN THREADS (priority order)

1. **The icon** — deliver the owed version (original wave + candidate-3 bell), present v4a/v4b/the-new-one side by side, get the pick, then roll it out (favicon, loading animation, social kit, brand zip, site marks). 
2. **Batch 75–77** — finish Endocrine to 200 (bank → 1,897). Then remaining systems per taxonomy toward ~5,200: Immuno/Allergy, MSK/Rheum (currently 25), Psych (25), Repro (female 15 / male 15 / pregnancy 15), Biostats, Biochem, ID (65 → more?), ENT, Poisoning… **pull exact targets from `taxonomy.py` when uploaded.**
3. **The "1,774" confirmation** (§9.1) — one question to him, likely resolved as "used questions excluded".
4. **`content` attribute 5,000-char cap** — re-recommend enlarging to 20,000 in the Appwrite Console (it constrains rationale+cards sizing on every item).
5. **Stale repo files** (§4 list) — propose a cleanup PR/delete round **with his approval only**.
6. **Marketing launch** — posters, plan, and schedule are ready; nothing is posted yet as far as the record shows.
7. **Blind Case game** — shelved deliberately; revisit only when he raises it ("then the game" — his words about what comes after the icon).
8. **Concours.md** — his other project; support if asked, don't initiate.

---

## 12. FILES TO REQUEST FROM THE FOUNDER (he downloaded the full workspace, ~74 MB)

**Tier 1 — qbank engine (blocking for batches):**
`qbank/QUESTION_STANDARD.md` · `README.md` · `taxonomy.py` + `taxonomy.json` · `validate.py` · `labsheet.py` + `labsheet.json` · `shuffle_answers.py` · `merge_cards.py` · `pool_sync.py` · `make_sample.py` · `images.py` · `parity_test.py` · `build_importer.py` · `true_live_bank.json` (and/or `live_bank_snapshot.json`) · `cards/pool.json` · `importer/` (import.template.html, latest import.html, README.md) · the most recent batch folder (`batch_74*` incl. briefs, sources, review, IMPORT json) as format reference.

**Tier 2 — site development:** `medchanic-md/_src/` (all 7 files) · `compliance/` (9 build/patch scripts) · `qa/` (`test_importer.py`, `run_qa.py`, mocks).

**Tier 3 — open threads:** `logo-lab/` (all candidate PNGs incl. candidate-3.png, v2a/v2d/v2e/v4a/v4b, roster.html) · `marketing/` (MARKETING_PLAN.md, PRICING_STRATEGY.md, FREE_TIER_REVIEW.md, qbankly competitive analysis, posts/, fonts/) · `rebrand/` (product-demo.html, play.html) · `game_items.json` · `medchanic-live-backup/` · batch zips + IMPORT JSONs (audit trail) · root `README.md` · `proposal/` (course application).

---

## 13. THE NEVER-AGAIN LIST (each line cost a meltdown)

1. Never upload/push anything without being asked exactly what. Never suggest paid hosting.
2. Never send a batch that isn't 25/25. Never patch a failing slot with filler — regenerate it.
3. Never pad (dots, trash words, robot sentences) or truncate options, stems, or whyWrongs.
4. Never let the correct answer be obvious (verbatim echo, adjective echo, only-longest-option, giveaway syntax).
5. Never hand-edit `dashboard.html` — `_src/` + `build.py` only.
6. Never claim "fixed" without running it and showing evidence.
7. Never forget: clickable files + what-changed + what-to-push at the end of every turn.
8. Never mix systems in a batch he asked to be single-system.
9. Never edit an option by letter after shuffling — edit by option text (letters move).
10. Never trust a stale bank snapshot — refresh before gating; attach `$id`s after import.
11. Never assume a duplicated/swallowed message means redo the work — code red, resync, answer once.
12. Never put emojis in the UI.
13. Never ship an image you haven't opened and viewed.
14. Never let a table item keep prose `choices` (the app derives them) or let whyWrongs drift during table conversions (the analgesic-ladder incident).
15. Never write a lead-in ending in filler to dodge the template cap — rewrite it properly.
16. Never deploy demo/preview files inside a production zip without labeling them (the "demo file in the zip" question).
17. Never, ever stop treating this like it's big. It is.
18. Never push heavy assets to a repo without checking what its deploy integration watches — one unnoticed "all branches trigger deployments" setting cost the founder his entire Appwrite storage quota (Oct 2026). The filter is main-only now; keep it that way.

---

## 14. VOICE & STYLE — how the previous agent wrote (keep it)

- Opens with the outcome: "Done, champ — Batch 68 is ready. DB verified first: …". Then tightly-structured sections with mini-headers, tables for comparisons, exact numbers everywhere.
- Signs off with the closing summary (§7.3) and the next step framed as his call ("Batch 75 = Endocrine part 4, unless you say otherwise").
- Uses his vocabulary back: champ, pal, brother. Occasional honest editorializing with a spine: "My call: V2E is the better mark" — opinions are offered plainly and defended, decisions are his.
- Admits gaps explicitly ("One thing I can't explain, and you should check").
- Explains root causes when fixing (he appreciates the "why", not just the "done") — e.g. the block-summary font-leak fix: exam chrome is Arial by design, the report reclaims brand fonts.
- Never overclaims. Never hedges into mush. When work was interrupted: resume exactly where the file on disk says, report the resume point, don't duplicate.

---

## 15. FINAL WORD

The founder works late, pushes through UI glitches and out-of-context deaths, and keeps coming back with "let's go champ". The previous agent earned his trust back the hard way — by shipping 74 consecutive clean batches after nearly losing him. You inherit that trust and that debt.

First words to him, if you need them: *"Back on deck, champ. I've got the full picture — the standard, the pipeline, the code words, and exactly where we stopped. I still owe you one logo version: the original wave with candidate 3's bell. Say the word, or point me at batch 75."*

Then deliver. Like nothing ever happened.

---

## 16. THE ANASTOMOSIS ERA (Oct 22–23, 2026) — the full story, in detail

### 16.1 The renaming
The founder decided to rename the product. His inspiration: a new competitor by Malke Assad called **Synapse** — he loved how a real medical word could be a brand. The rule he extracted: *a real medical word students say every day, catchy enough for a handle*.

The journey, so no future agent repeats the misses:
1. **Wave 1 (rejected as "horrendous"):** Lumen, Engram, Soma, Viva, Axon, Osler, Gnosis, Lacuna, Cortex, Fulcrum — anatomy-index curiosities, not daily vocabulary. The founder's exact verdict: *"what are these names? is this medicine???"*
2. **Wave 2 (the daily vocabulary):** Myelin, Reflex, Dose, Stat, Atlas, Vitals, Triage, Aorta, Differential, Dopamine. Only **Dopamine** survived (10 icon directions were built for it).
3. **Challenger wave:** Potential, Threshold, Adrenaline, Endorphin, Serotonin, Caffeine, Ion, Vesicle (icons only on request).
4. **The founder's own two:** **Anastomosis** and Cognosis — five icon directions each. **ANASTOMOSIS.MD won.** The founder liked it "a lot."

Practical renaming state: no domain bought, socials not launched — perfect timing. The 1,822-question bank is name-agnostic. Still to do at rollout: update the admin email **in place** on the existing Appwrite account (keeps the user ID that owns the DB), GitHub repo rename + Appwrite static-site re-link, site-wide copy ("Medchanic" is in every nav/footer/title/meta/terms + the importer's hardcoded admin email check), Telegram handle, and the final HANDOFF rewrite.

### 16.2 The brand system — the colors ARE the concept
The palette is the arteriovenous story itself:
- **Bone `#F7F3EB`** — the field (paper, warmed and whitened)
- **Ink `#101418`** — text and the merged vessel (the graft)
- **Arterial crimson `#B5342A`** — the artery, the living accent
- **Venous petrol `#1B4E5F`** — the vein, the primary brand color
- **Old gold `#C9973C`** — the suture: used ONCE, exactly where the join matters

Token mapping to the current site is 1:1 — paper→bone, ink→ink, teal→petrol, coral→crimson, amber→gold. **Re-theming the entire site = five hex values and one logo swap.** Motto candidates in use: *"Two vessels. One mind."* (social bios) and the old era's *"Every wrong answer is a clue."*

### 16.3 The design rules — hard-won, now non-negotiable
1. **Avatar-first:** every mark is created inside an Instagram profile view — that is where it lives or dies. The founder made this a standing format rule.
2. **FLAT ONLY.** 3D renders are banned by founder's order ("it will never look good for social media"). The AVI-4 rendered style is dead.
3. **No black backgrounds** — "it has no meaning." The bone field, always.
4. **Vessel cues:** organic curvature (real vessels bow and sway — never ruler-straight), taper toward the ends, the **branch** (the founder's favorite cue), open elliptical **lumen mouths** at tube ends. Red + blue = the universal artery/vein shorthand of every anatomy diagram.
5. **Circle-crop discipline:** mark centered in the central ~65% with breathing room; the 5-second stranger draw test; 2–3 colors; must survive one color and 16 px.
6. **The A must read as an A; the vessels must look like vessels** — "pure skeleton, vessel material" was the thesis that fixed both at once.
7. **Texture requests mean TEXTURE ONLY.** Same mark, different surface (two-tone, hatch, sheen, bands, stipple, crosshatch). The one time I redesigned instead, the verdict was "these are downgrades tbh." When the founder says "change the texture," touch nothing but the tube surface.
8. **When the founder says "the Nth one," confirm WHICH list** — positional counting once pointed me at the crossing when he meant the braid (the fourth of the *second batch*). One clarifying sentence saves a whole round.
9. **Art ≠ logos.** When invited to "go wild," he still wanted LOGOS — the art gallery round was rejected as off-task ("this is a logo design request not an art session"). Ambition lives inside the mark, not outside it.

### 16.4 The hunt — 19 series, 97 marks (all in logo-lab/)
1. **ANA-1..10** — the founder's two (union, bypass, Circle of Willis, seam, side-to-side) + the full-color brand set (AV union hero, dark hero, seam, circle, render)
2. **BOLD-1..6** — the bold series: knot, bowtie, **the A** (founder: "edges look like vessels — goes to the top"), union, + two night modes (black — later banned)
3. **A-R / A-V / A-L / KNOT-R** — first upgrades of the A and knot
4. **A-TOP / A-3D / A-PX** — the clear A series (definitive, sculptural, apex junction)
5. **INF-1..2** — first infinity pair (endless anastomosis, flow-through)
6. **INF-R / INF-3D / INF-RND** — the infinity "10× better" elevations
7. **AVI-1..5** — the AV infinity (the infinity IS the anastomosis: join, flow, minimal, rendered[dropped], emblem)
8. **LV-1..5** — the living A (organic vessel material on a pure skeleton: definitive, infinite crossbar, looped feet, vivid red/blue, anatomical hero)
9. **AC-1..5** — the clear A (definitive, vessel detail with the branch, minimal, rendered, infinite crossbar)
10. **AINF-1..4** — the founder's own A∞ fusion (definitive, sculptural, rendered, minimal)
11. **AIS-1..4** — style transfer from the founder's reference image
12. **DC-1..4** — the Designer's Cut: **the self-tying vessel** (artery in through the golden ring, vein out), the wordmark (the two O's of anastOmosis ARE the loops), hidden monogram, launch post
13. **IG-1..5** — the wild round in profile views (emblem, A, circle-born loop, seal, negative-space disc) — IG-1 was the founder's pick
14. **MAX-1..5** — the max wave (definitive emblem, twin discs, full account system, wordmark, founder's cut elevated)
15. **WLD-1..12** — the wild waves: crossing, ligature, embrace, seam, bridge, dovetail A, keystone, junction, coupling, **braid (WLD-10 — a founder favorite)**, confluence, splice
16. **CR-1..8** — crossing style studies (only CR-7 ribbon twist kept; the rest "downgrades")
17. **TEX-1..6** — crossing texture studies (two-tone, hatch, sheen, bands, stipple, crosshatch)
18. **BT-1..6** — braid texture studies (the same six surfaces on WLD-10)
19. Plus `art-1..6` — the gallery art pieces (confluence, inosculation, rose window, map of joins, two vessels one mind, collateral) — brand artwork, kept separate from logos

Founder's explicit favorites to date: **WLD-10 the braid + BT textures**, **WLD-1 the crossing + TEX textures + CR-7**, **IG-1 the emblem**, **DC-1 + DC-2** (led the curated shortlist). The Designer's Cut recommendation on record: DC-1 as the mark, DC-2 as the wordmark.

### 16.5 The files (logo-lab/) — the decision ecosystem
- **anastomosis-gallery.html** — THE MASTER GALLERY: all 97 marks, **Disqualify** buttons (elimination with persistence), **Star** buttons (builds the founder's shortlist), and a separate **Starred view** for side-by-side comparison. This is the decision room now.
- **anastomosis-shortlist.html** — the curated 15 marks + 13 studies with the first interactive elimination system (28 eliminable cards, counter, hide-toggle, reset — localStorage)
- **anastomosis-lab.html / .pdf** — the 65-mark archive (66-page PDF, 800 px embeds ~4.6 MB)
- **insta.html** — 20 profile views in waves (wild wave → designer's cut → IG round → max wave)
- **art.html** — the six monumental art pieces with the "when you say anastomosis…" poem
- **names.html** — the full naming record (wave 1, wave 2, challengers, founder's two)
- **Legacy Medchanic-era files** (picks.html/.pdf 17 marks, finalists.html, explorations.html) — obsolete for the new brand, kept as history
- **build_*.py** — the builders for everything above; rerun after adding images. PDF images embed at 800 px JPEG (repo hygiene: never commit >50 MB files).

### 16.6 The Appwrite incident — resolved (see also §3.7)
Cause found and fixed: the site's Git settings deployed **every branch** — 47 logo-asset pushes (trees up to 244 MB) took the org from 1.56 GB to 4.07 GB (204% of the free 2 GB) and got it restricted. **Founder's fix (Oct 23): the Git settings now deploy only branches matching `main`** — arena pushes are invisible to Appwrite (verified: first post-filter push triggered nothing). Remaining founder actions: delete the fat deployments in Console → Sites → Deployments (reclaims ~2.5 GB), set retention to 30 days. Standing rules live in §3.7 and rule 18.

### 16.7 Current state & next steps
**Now:** the founder eliminates and stars in the master gallery → the Starred view becomes his shortlist → the final pick.
**Then the rollout:** the five token swap across the site (bone/ink/crimson/petrol/gold), the winning mark as favicon on every page, the loading animation drawn from the mark, the social kit (avatar + highlights + post templates per MAX-3), importer admin email update, repo rename + Appwrite relink, and this guide's final rewrite for the Anastomosis era.
**Then the real work resumes:** the qbank files upload (Tier 1 — §12), batch 75 (Endocrine → 200), and the launch.
