# Arcade: eight experiments — prototype notes

The playable file is **`arcade3.html`**. It is one self-contained HTML file; download it from GitHub and open it in a browser. No build step, network connection or separate assets are required to try the games. Nothing in this file changes the live website or test page.

## What is actually playable

| Game | Included in this prototype | Important limits |
|---|---|---|
| **Infinite Med** | A drag/drop and tap-to-combine workbench; 66 handcrafted recipes and 70 reachable nodes; local discovery persistence; hints. | Finite, not generative or infinite. Recipes are playful symbolic associations, **not diagnostic or causal rules**. No live QBank cheat sheets. |
| **The Suika Cell** | Collision physics, falling cells, merges, scoring, restart, mutagens and local best score. | Uses a simplified granulocyte lineage ending in neutrophil, not macrophage. Merging cells and mutagen behavior are fictional. Overflow is a game loss, not a leukemia diagnosis. |
| **The Consult** | Secret roles for 4–8 players, pass-the-device ballots, three cases, ties and role reveal. | **Local pass-and-play only**; no online lobby, chat, realtime vitals, remote multiplayer or real patient monitoring. |
| **Gunner Clicker** | Click/spacebar, five passive upgrades, two 3-question timed gates, local save and capped offline progress. | Sample exam questions are local. No QBank performance multiplier, premium access or subscription rewards. Offline earning is capped at eight hours. |
| **The Anatomy Box** | A flat 2D rotatable-view journal and four sequential puzzle stages: key, valve order, pressure relationship, cycle sequence. | It is **not 3D**; the founder's standing flat-only design rule takes precedence. No real discount code, key or premium unlock. |
| **The Rx Deck** | Four-card hands, select up to two, combos, drug-fact flips, three challenge encounters, draft between bosses, win/loss. | Points, hit points and damage are fictional game mechanics, not treatment effects. No cards are pulled from the QBank. |
| **Immune Survivor** | Mouse/touch/keyboard movement, automatic attacks, enemies, pickups, level-up choices, escalating waves and pathogen fact on defeat. | Stylized, not a literal immune-system model. IgG/complement are support metaphors; macrophages do not independently make IgG. No targeted QBank block is unlocked. |
| **Triage Swipe** | Swipe/tap/arrow choices, four game meters, feedback, 16 reshuffled sample cards and local best. | Simplified cases and fictional meter outcomes; not clinical advice or a connected QBank decision tree. |

## Medical safety and review

All medical wording is a prototype and **requires independent clinical/editorial review before production use**. Correct decisions depend on clinical context, patient characteristics, current guidelines and local protocols; these games must not be used to guide care. Some representative facts were spot-checked against sources below; this is **not** a comprehensive clinical validation or a substitute for review of every item:

- [1](https://medlineplus.gov/opioidoverdose.html): naloxone and emergency response for opioid overdose.
- [5](https://medlineplus.gov/ency/article/000844.htm): anaphylaxis is an emergency and epinephrine is used immediately.
- [1](https://www.merckmanuals.com/professional/nephrology/electrolyte-disorders/hyperkalemia): calcium protects the heart in severe hyperkalemia; other therapy is required to lower potassium.
- [3](https://pmc.ncbi.nlm.nih.gov/articles/PMC2440402/): mitral valve opening follows the left atrium–left ventricle pressure relationship.
- [1](https://www.ncbi.nlm.nih.gov/sites/books/NBK549885/): ACE inhibition can precipitate renal failure in bilateral renal artery stenosis and can increase potassium.
- [1](https://www.cdc.gov/fungal/diseases/pneumocystis-pneumonia/index.html): *Pneumocystis jirovecii* is a fungus associated with opportunistic pneumonia.
- [1](https://medlineplus.gov/ency/article/000528.htm): G6PD deficiency and oxidative hemolysis triggers.

## Validation and next steps

- Browser-tested each screen at mobile width, including complete and failure paths, 4–8 private-role setup, ties, physics merging/mutagen, clicker purchases and both timed gates, idle offline cap, full box, deck caution/draft/win/loss, survivor movement/upgrades/death, and triage swipe/restart. There were no uncaught browser errors in the test runs.
- Checked all 66 craft recipe pairs are unique and all 70 nodes are reachable from the four starting elements.
- Confirmed a standalone `file:` copy opens without remote assets; saved progress is device/browser-dependent. The visible site name was OCR-checked on the actual mobile screenshot.
- `tests/arcade3-smoke.mjs` contains a repeatable optional browser test; `tests/README.md` describes setup. `?debug` exposes test hooks for the demo only.
- Before connecting any game to the live platform: pick the games worth expanding, have every fact and case reviewed, decide free/premium content boundaries, implement and permission-check actual QBank mapping, and design the real multiplayer/server/fair-play system. Never claim rewards, network play or clinical validity that are not implemented.
