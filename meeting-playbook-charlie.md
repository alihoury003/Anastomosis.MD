# The Meeting Playbook — Charlie from Paddle
*Rewritten Oct 23 after the reveal: Charlie is from Paddle, our payment provider · PRIVATE*

## The reframe (read this first)

This is not a consultant call. **Paddle is a merchant of record** — they're the legal seller of your product, they handle VAT/GST/sales tax in 200+ countries, chargebacks, fraud, and invoices [1](https://dev.to/onsen/paddle-review-2026-pros-cons-pricing-explained-4cgk). They take **5% + $0.50 per transaction, nothing monthly** — meaning **Charlie earns exactly when you earn.** His incentive is your launch succeeding.

So the posture flips: you're not guarding against a pitch — you're extracting every free resource a payments partner can give a soon-to-launch merchant. The three rules still stand (decide nothing on the call, take everything free, you're evaluating him too), but the "decline equity/retainers" worries are gone. New worries, smaller: don't restructure your pricing model to fit their features, and don't sign any *new* agreement without reading it.

## Your 30-second pitch (unchanged — he'll ask)

> "I'm a medical student, and I built **Anastomosis.MD** — a USMLE Step 1 question bank where **every wrong answer is explained**. 1,800 original questions so far, targeting 5,200 — two-step clinical vignettes, full rationales, all four distractors explained, flashcards born from each question. The platform is live on near-zero infrastructure, priced **$15/mo · $54/6mo · $99/yr** — auto-renew only if a student explicitly asks for it. Paddle checkout is already wired in. I haven't launched marketing yet — that's the next 90 days."

## The five questions that matter MOST (ask these, in this order)

### 1. Payouts to Lebanon — THE question
"How exactly do payouts reach me in Lebanon? What methods, what currency, what schedule, what minimums, what fees?"
- Paddle pays out on a rolling schedule via bank transfer (ACH, SEPA, international wire) [1](https://dev.to/onsen/paddle-review-2026-pros-cons-pricing-explained-4cgk) — but **Lebanon's banking situation is the real issue**. Get specifics: can they wire to a Lebanese bank in USD? Is there a Payoneer/Wise-style alternative? What has worked for other sellers in similar markets?
- If Lebanese banks are a problem: ask what documentation/setup makes payouts smoothest. **This is the single most important operational question of the call.**

### 2. Verification & underwriting — protect the launch
"What do I need to complete on my account so nothing freezes or delays when sales start?"
- Paddle tightened underwriting in 2026 after a 2025 FTC settlement — approvals take longer and some business types get rejected [2](https://www.aitoolbox.hk/tools/paddle/). You do NOT want a verification hold in launch week.
- Ask: what's outstanding on the account? What does the site/domain need to show? (Note: this interacts with the rebrand — see below.)

### 3. The rebrand — get the migration checklist
"I'm rebranding Medchanic.MD → Anastomosis.MD before launch. What do I need to update on the Paddle side, and in what order?"
- Product names in the dashboard, checkout branding, the domain on the success URLs (currently `medchanic-md.appwrite.network`), invoices customers see, statement descriptors (what appears on students' bank statements).
- Key sequencing question: **is it easier to rebrand inside Paddle now, or launch and update after?** Get his recommendation — he's seen a hundred merchants do this.

### 4. Fees — the real math on small transactions
"Confirm the fee structure — and the effective rate on a $15 transaction?"
- The math to have in your head: **$15 → $1.25 fee (8.3% effective) · $54 → $3.20 (5.9%) · $99 → $5.45 (5.5%)** [3](https://makerstack.co/reviews/paddle-review/). The monthly plan carries the heaviest effective rate — which is an argument for nudging students toward the 6-month and annual tiers (which your pricing already does).
- Ask if there are any surcharges by payment method or currency to watch for.

### 5. Conversion & checkout — take the free expertise
"What moves checkout conversion for student markets — and what should my checkout do that it doesn't yet?"
- Paddle's checkout auto-shows local currency with tax included and local payment methods by region [3](https://makerstack.co/reviews/paddle-review/) — ask him what students in Lebanon/Gulf will actually see.
- Ask about: Apple Pay / Google Pay (huge for mobile-first students), coupons for a launch discount, PayPal availability in the region.

## Still worth asking

- **Taxes as MoR**: "Confirm I need to do nothing — no VAT registrations anywhere?" (Correct answer: nothing. That's what the 5% buys [4](https://owelet.app/for-paddle-sellers).) *(Separate, for later: how income tax works for you in Lebanon — that's an accountant, not Charlie.)*
- **Refunds/disputes**: how are they handled, and does anything need configuring to match the refund policy page?
- **The WhatsApp/OMT local payments**: acknowledge that local Lebanese rails (OMT, Whish) will stay manual outside Paddle — but ask if he's seen merchants pair Paddle + manual local rails cleanly ( invoicing, reconciliation).
- **"What would you do in my first 30 days?"** — still a great question; his answer tells you how much he actually knows about launches.

## What to ACCEPT (it's almost all free)

- Setup and verification help — take everything
- Checkout optimization advice, conversion tips for the region
- The rebrand migration checklist
- Any launch resources, guides, or introductions Paddle offers merchants

## What to be careful about (a much shorter list now)

| Careful about | Why | Your line |
|---|---|---|
| Adding opt-in auto-renew subscriptions alongside one-time payments | ON the table — "auto-renew is your choice, not our default" — but only with three conditions: opt-in toggle **default OFF** at checkout, **one-click cancel** in our app, **pre-renewal reminder emails**. If Paddle can't honor all three, it stays one-time. | "We promise no auto-renewal without explicit consent — opt-in, default off, one-click cancel. How do mixed catalogs work in Paddle, who sends renewal reminders, and can we cancel via your API from inside our app?" |
| Making auto-renew the default (pre-checked boxes, hidden opt-outs) | That's the legacy trap we're positioned against — it kills the differentiation. | Never. |
| Any new agreement or plan change | New terms = new fine print (payout schedules, fees). | "Send it over — I'll read it and come back to you." |
| Monthly-fee plans / premium tiers | You're on the standard 5% + $0.50 with no monthly fee [1](https://dev.to/onsen/paddle-review-2026-pros-cons-pricing-explained-4cgk). At your volume, monthly fees are pure loss. | "Not at this stage." |
| Deciding anything live | Same rule as always. | "I'll confirm after the call." |

## The numbers card (know these cold)

- **1,822** live questions · **26** systems · target **~5,200** · batches of 25, one enforced quality standard
- Pricing: **$15 / $54 / $99** — one-time by default, opt-in auto-renew (toggle off, one-click cancel); free tier = first block free + 10/day + 7-day trial
- **Paddle fee math: $15 → net $13.75 · $54 → net $50.80 · $99 → net $93.55** (5% + $0.50)
- Infra cost: ~$0 · Competitors: UWorld $579/yr · AMBOSS $448 · qbankly $35/yr
- Beachhead: my school (NBME→Kaplan switch), then Gulf + diaspora
- Current Paddle wiring: checkout overlay + promo codes + success URL on `medchanic-md.appwrite.network`

## After the call

1. Write down every promise and every "I'll check on that for you."
2. If he sends anything to sign — **bring it to me first.** Same for any fee schedule or new agreement.
3. The two answers that most shape next steps: **Lebanon payouts** and **verification status**. Everything else is optimization.

## Final thought

You're not a student asking a company for permission — you're a **merchant about to send Paddle transaction volume**. Their whole model is betting on merchants like you. Walk in as the founder who built a working product on zero budget and is about to launch. Because you are. 🛠️
