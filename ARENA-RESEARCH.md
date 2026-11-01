# The Arena — research, product direction and honest launch plan

Prepared for Ali · 1 November 2026

## The problem worth solving
The first two arcade waves provide variety, but each game has a narrow loop: solve a puzzle or answer a sequence and finish. A leaderboard alone will not turn a quiz into a game someone wants to replay. The design hypothesis is **meaningful decisions between answers**: a run has changing encounters, risk/reward, a build that changes the way it scores, and a finish worth comparing. Fun, fairness, and actual learning all need to be measured; none is guaranteed by implementing a mechanic.

## What the research says—and what we should borrow

1. **Slay the Spire: each run is a strategy, not just a sequence.** Its official listing describes changing paths, risk, card synergies and worldwide daily climbs. Borrow the *decision structure*: choose a path or build, solve an encounter, adapt, and compare a common challenge. Do not copy its characters or assets. Source: [Slay the Spire on Steam](https://store.steampowered.com/app/646570/Slay_the_Spire/).
2. **NYT Mini: friends create a reason to compare a shared puzzle.** The official help page says the Mini board resets daily, counts the first solve, and shows confirmed friends. It explicitly says there is no global board because cheating is difficult to monitor. Borrow opt-in friends and a shared daily format; take the warning about integrity seriously. [NYT Mini help](https://help.nytimes.com/360011158491-New-York-Times-Games/360025912452-The-Mini-Crossword).
3. **Duolingo: people can compete or collaborate.** Duolingo describes weekly leagues and opt-in shared streaks/friend quests. A cooperative goal can welcome users who dislike rankings. Its 22% figure for friend-streak users is an observational company claim—not evidence our game will cause the same lift. [Duolingo 101](https://blog.duolingo.com/duolingo-101-how-to-learn-a-language-on-duolingo/); [Friend Streak](https://blog.duolingo.com/friend-streak/).
4. **Chess.com: competitive integrity is an ongoing operation.** Its rules prohibit assistance and rating manipulation. A game needs rules, monitoring, appeals and corrections—not just an API that accepts a score. Knowledge games face especially difficult answer-sharing and external-assistance risks. [Fair play policy](https://www.chess.com/legal/fair-play).
5. **Health education evidence supports testing, not miracle claims.** A review of serious gaming in health professions reports potential knowledge benefits but notes many studies were at high risk of bias; game mechanics can distract from the lesson. Measure delayed retention and question quality, not just time spent. [Gentry et al., JMIR 2019](https://www.jmir.org/2019/3/e12994/).

## Five big concepts, ranked as product bets

| Concept | Loop | Why replay? | Competitive hook | Biggest risk |
|---|---|---|---|---|
| **1. Grand Round** (prototype built) | Eight encounters; wager risk, select upgrades, survive | Builds, decisions and varied questions | Shared daily challenge, friends and world board | A small question pool becomes repetitive quickly |
| **2. Diagnostic Heist** | Build a differential from progressively revealed clues; spend limited tests before naming a diagnosis | Different cases, information tradeoffs | Fewest test points on identical case | Clinical cases need careful editing and unambiguous scoring |
| **3. Ward Wars** | Asynchronous 1v1: each player tackles the same three cases and can choose risk modifiers | Rivalry and rematches | Invite link, round-by-round reveal | Cheating, spoilers and delays between turns |
| **4. Outbreak Command** | Cooperatively investigate a spreading outbreak; select tests, contain sources, allocate scarce actions | Branching emergent scenarios | Small friend teams, shared weekly objective | Substantial simulation and content authoring |
| **5. Pathway Architect** | Place mechanism cards to repair a disrupted physiologic pathway; chain bonuses | Multiple valid builds and strategic combos | Same seed and card pool; weekly challenge | Avoid rewarding medically incorrect shortcuts |

**Recommendation:** test Grand Round first. If people keep asking for rematches but find it too quiz-like, prototype Diagnostic Heist before investing in the rest. Do not build five unvalidated games at once.

## What is actually built

`arena.html` is a standalone, mobile-friendly **prototype**, not a production route. It contains 24 original short questions, eight encounters per run, three starting lives, optional all-in risk, two upgrade choices, explanations and a personal board stored on the current device. Daily mode uses a deterministic UTC date seed; practice randomizes on each run. Replaying the daily is allowed in this demo. Runs save locally only; there are no live friends, world rankings, accounts, API submissions or qbank integration. The first 24 questions are prototypes requiring independent medical review, expansion, and source citations before production. Clinical explanations are not medical advice.

The prototype is a **hypothesis**: there is no evidence yet that it is replayable for hours or improves exam performance. Static question content and answer keys are visible to the browser, so it cannot be a trustworthy ranked competition.

## Competitive product spec (proposed, not implemented)

- **Daily ranked:** one server-selected, versioned challenge per UTC day, identical encounters and game rules for everyone. One ranked attempt per authenticated account per day; unlimited clearly marked unranked practice. Explain reset time and tie-breaking visibly. Complete a run before it expires; no restarting after seeing answers.
- **Score:** server computes from submitted choices and allowed risk/upgrade events. Example: base 100; +25 per previous consecutive correct answer (capped +100); all-in +100 if correct, minus two lives on a miss; normal miss minus one life. Server records ordered events, one answer per encounter; deterministic upgrade decisions, legal state transitions and encounter order are verified. Separate each season/ruleset; never mix scores generated by different rules or content versions.
- **Friends:** opt-in invite and mutual acceptance; separate private friendships from public profile. Friend board filtered from the same daily scores. Support revoke/block; never expose email, qbank data, medical history, or private study activity. Moderated display names; default pseudonyms; public visibility opt-in.
- **World:** daily and seasonal boards; deterministic ties by score, then correct answers, then earlier validated completion, then opaque stable ID. Do not rank by unlimited time-spent or sell power upgrades. Pagination and around-me results; mark fresh accounts provisionally. Avoid presenting a global board until abuse reporting and moderation are operational.
- **Asynchronous 1v1 later:** challenge invitation, common server-held content, deadline, both plays independently, results revealed after both finish or expiry; rating only after a fair-play pilot. Small study groups and leagues can follow once real activity warrants them.
- **Fair play:** server issues signed/opaque run IDs; server retains correct answers, controls the next encounter, computes score, verifies completion, enforces rate limits and account quotas, and stores append-only events plus ruleset ID. Never accept a client-submitted score as authoritative. Avoid sending future answers to clients. These steps limit simple tampering, not external help, answer-sharing, multiple accounts or bots. Require moderation, auditing, dispute handling and corrections; communicate that cheating cannot be eliminated.

## Zero-budget architecture and operational reality

- Use existing Appwrite authentication; no secrets or server API keys in browser code. Appwrite says elevated logic belongs in Functions and that client validation is not authoritative: [Appwrite security guidance](https://appwrite.io/blog/post/common-appwrite-mistakes-and-how-to-avoid-them).
- One server-side function can route `start`, `answer`, `finish`, `board`, and friendship actions if the project has capacity. Client SDK execution permissions must explicitly allow the intended users; authenticate the actor server-side and use least privilege. [Appwrite Functions guide](https://appwrite.io/blog/post/appwrite-functions-guide).
- Proposed tables/collections: `arena_profiles` (public pseudonym, visibility), `arena_friendships` (private pair/status), `arena_challenges` (day, ruleset and immutable question references), `arena_runs` (owner, challenge, state, result, version), `arena_events` (run, sequence, action, answer, idempotency key), and derived `arena_daily_scores` (public-safe score and rank fields). Private answer keys never have public read access. Add required indexes, stable pagination and per-record authorization; transaction/atomicity behavior must be tested against the actual deployed Appwrite version.
- Idempotent answer submissions and race-safe finish operations are required: retries cannot count twice, and concurrent requests cannot consume extra turns. Test unauthorized reads, replayed IDs, two simultaneous answers, partial failures, and leaderboard ties with multiple real accounts before launch.
- Free-plan capacity is not infinite: Appwrite announced a limit of **two functions per free project** (January 2026); check existing functions and current pricing/quotas before provisioning. Appwrite lists 750k included executions on Free, but bandwidth, compute time, storage and abuse limits also matter. A 10-call run × 100 daily players × 30 days is roughly 30,000 executions/month before boards, retries and friendship traffic. [Free function limit](https://appwrite.io/changelog/entry/2026-01-08); [plan comparison](https://appwrite.io/blog/post/introducing-appwrite-cloud-start-plan). No capacity or cost is guaranteed.
- Do not connect the premium qbank or publish its answer keys from this prototype. Decide whether game content is separately authored and free, confirm usage rights, and avoid bypassing existing subscription limits.

## Validate before a launch

1. Ali plays three fresh runs and one daily run; note where a decision feels real vs decorative, and whether he voluntarily replays.
2. Five to ten students test independently on phone; ask them to explain the rules, choose upgrades, identify what felt repetitive, and report whether they would challenge a friend. Observe—not just ask.
3. Independent clinician/editor checks every item and explanation for accuracy, ambiguity, scope and citations; build a much larger bank. Avoid repetitive identical answer positions and overly obvious distractors. No patient-identifiable material.
4. Instrument (with consent): start-to-first-answer, run completion, voluntary second-run rate, 7-day return, friend invite acceptance, and delayed recall on a small controlled set. Set targets after a baseline. Do not optimize for compulsive play or shame users for missing days; offer breaks and optional competition.
5. Build and test the authenticated backend only after the core loop earns its place. Then a small private friends pilot, then a moderated global board.

## Follow-up: moving beyond multiple choice — 1 November 2026

### What a second research pass changes

- **Balatro:** the official game description emphasizes combinations of modifiers rather than a fixed reward per hand. The implication is not "add badges": let two choices interact to produce a discoverable strategy, with readable rules and counterplay. Our Grand Round offers individual upgrades but **does not yet have deep synergies**; test that weakness rather than claiming it matches Balatro. [Official Steam listing](https://store.steampowered.com/app/2379780/Balatro/).
- **GeoGuessr:** its official page places a daily challenge, friend duels, and worldwide ranks around the same recognizable skill. The product lesson is to create **one signature skill with several social contexts**, rather than 13 unrelated mini-games sharing only a leaderboard. It is an analogy, not a prediction of our adoption. [GeoGuessr](https://www.geoguessr.com/free).
- **Retrieval and spacing:** a health-professions systematic review found 43 of 63 experiments showed statistically significant benefit of distributed practice and/or retrieval compared with controls; interventions and comparisons varied. This is rationale to test delayed retrieval, not a claim that our prototype improves learning. [Systematic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC11078833/).
- **Concurrency:** Appwrite documents a Transactions API for grouping writes atomically and checking conflicts. Whether the existing project's API/SDK version, plan, schema and permissions support our exact design must be verified in a staging project; atomic writes alone do not stop cheating. [Appwrite Transactions API](https://appwrite.io/blog/post/announcing-transactions-api).

### Prototype 2: Diagnostic Heist

`diagnostic-heist.html` is an independent, self-contained, **unranked** playable prototype. It replaces the question-rush loop with an information economy: five cases from a ten-case sample, three lives, up to three optional clues at a cost of 35 points each, 200 base points for a correct diagnosis, and a capped streak bonus. Guess early to score more or buy evidence to reduce uncertainty. Detailed explanations and a local run record complete the loop.

A dated daily seed creates the same case and answer order for players using the **same build**. On a hosted HTTP(S) copy, the share button copies a link carrying the UTC date; a downloaded `file:` copy explicitly tells the player that its local file address cannot be shared. A friend link does not transmit, verify, or compare scores. Practice shuffles cases. This is a feasibility test, not secure competition: content and correct answers are visible in the browser and the small bank repeats rapidly. The clinical content is simplified and requires independent review and citations before real student use.

**Test it against Grand Round:** (1) Can a first-time player articulate why they bought or skipped a clue? (2) After finishing, do they want another attempt without being prompted? (3) Can they recall the distinguishing fact one week later? (4) Would two friends actually share the same file and compare results? A small structured study with matched exposure is needed; self-selected replay does not establish educational benefit.

### Real-world competition: phased acceptance criteria

1. **Offline prototypes today:** local score history only, replayable dated puzzles. No claim of a global rank, authentication, privacy guarantee across devices, anti-cheat or secure scores.
2. **Private pilot:** explicit consent and pseudonyms, accepted friends-only invitations, daily server-held content, one ranked attempt and unlimited separate practice, server-controlled turn transitions, idempotent submissions, capped rate limits, and recoverable interrupted runs. Test two-account access and invite revocation.
3. **Global beta:** same versioned daily content/rules, stable ranking/tie order, report and appeal path, audit logs, anti-abuse review and correction of invalid scores. Reassess answer-sharing risk (a globally shared fixed daily puzzle is intrinsically spoilable); publish fair-play rules and do not promise cheating is impossible.
4. **Longer-term options:** asynchronous duels with independently completed identical cases and delayed reveal; weekly cooperative objectives; optional cosmetic seasonal identities. No pay-to-win power, public email addresses, simulated user rows represented as real, or penalties for taking a break.
