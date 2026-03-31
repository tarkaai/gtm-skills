---
name: intent-score-model
description: Build and validate a weighted intent scoring model that combines first-party website signals, third-party research data, and firmographic triggers into a single priority score
category: Prospecting
tools:
  - Clay
  - PostHog
  - Attio
fundamentals:
  - clay-intent-scoring
  - clay-enrichment-waterfall
  - posthog-custom-events
  - attio-lists
  - attio-custom-attributes
---

# Intent Score Model

This drill builds the scoring model that converts raw intent signals into a prioritized outreach queue. It defines what signals matter, how much each one weighs, and what score thresholds trigger action.

## Input

- ICP definition (from `icp-definition` drill)
- At least one active signal source: website visitor identification, G2, Bombora, or manual signal logging
- Historical deal data in Attio (10+ closed-won deals recommended for calibration)

## Steps

### 1. Map your signal universe

Catalog every signal you can capture. Organize into three tiers by predictive strength:

**Tier 1 — Direct intent (highest weight):**
- Visited pricing page
- Requested a demo or started a free trial
- Viewed competitor comparison pages
- G2 "alternatives" or "compare" signal
- Multiple return visits within 7 days

**Tier 2 — Research intent (medium weight):**
- Visited case studies or docs
- Downloaded a resource
- Bombora surge score above 70 on relevant topics
- G2 category browsing
- Read 3+ blog posts in one session

**Tier 3 — Contextual signals (lower weight, multiplier effect):**
- New executive hire in buyer persona role
- Funding round in last 90 days
- Hiring 3+ roles in your product domain
- Adopted a complementary technology
- Competitor technology detected on their site

### 2. Assign signal weights in Clay

Using the `clay-intent-scoring` fundamental, set up a Clay table with columns for each signal and build the weighted scoring formula. Start with these default weights:

| Signal | Points | Max |
|--------|--------|-----|
| Pricing page visit | 15 | 15 |
| Multiple site visits (per visit) | 5 | 25 |
| G2 alternatives/compare signal | 20 | 20 |
| G2 category browsing | 10 | 10 |
| Bombora surge (scaled) | 0.2x score | 15 |
| Recent funding | 10 | 10 |
| New exec hire | 5 | 5 |
| Job postings (per posting) | 2 | 10 |
| Competitor tech detected | 5 | 5 |

Apply time decay: signals older than 7 days lose 15%, older than 14 days lose 40%, older than 30 days lose 70%.

### 3. Define tier thresholds

Using the formula output, define action tiers:

- **Hot (70+):** Contact within 24 hours. Fully personalized outreach referencing specific signals.
- **Warm (40-69):** Contact within 72 hours. Semi-personalized outreach using category-level messaging.
- **Cool (15-39):** Add to nurture sequence. Monitor for score increases.
- **Cold (<15):** No action. Re-evaluate when new signals arrive.

### 4. Calibrate against historical data

Pull closed-won deals from Attio using `attio-lists`. Enrich each deal's account through Clay with the signal data available at the time of engagement. Score them retroactively:

- If fewer than 70% of won deals score Hot or Warm, your weights undervalue the signals that drove those wins. Increase weights on signals those accounts had.
- If more than 50% of lost deals also score Hot, your model is too generous. Raise thresholds or reduce weights on common-but-not-predictive signals.

### 5. Push scores to Attio

Create a custom attribute in Attio using `attio-custom-attributes`:
- `intent_score` (number) on the Company record
- `intent_tier` (select: Hot/Warm/Cool/Cold) on the Company record
- `intent_signals` (text) logging which signals fired

Push from Clay to Attio after every score calculation. Create Attio lists for each tier using `attio-lists` so outreach agents can pull the right accounts.

### 6. Track scoring accuracy

Log every score-to-outcome pair in PostHog using `posthog-custom-events`:
```
Event: intent_score_assigned
Properties: { company_domain, intent_score, intent_tier, signals_fired }

Event: intent_outcome_recorded
Properties: { company_domain, outcome: replied|meeting|deal|closed_won|closed_lost }
```

After 4 weeks, compare: do Hot accounts convert at 3x+ the rate of Cold accounts? If not, the model needs recalibration.

## Output

- Clay table with scored accounts and tier labels
- Attio lists segmented by intent tier
- PostHog tracking for score-to-outcome analysis
- Documented scoring model with weights, thresholds, and decay rules

## Triggers

- Re-run calibration monthly or after every 20 new closed deals
- Re-run whenever a new signal source is added
