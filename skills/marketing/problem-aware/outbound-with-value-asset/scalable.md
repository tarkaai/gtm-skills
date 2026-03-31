---
name: outbound-with-value-asset-scalable
description: >
  Outbound With Value Asset — Scalable Automation. Scale to 1,000+ prospects/month
  with multi-segment assets, automated A/B testing, signal-triggered sends, and
  n8n workflows that run the full cycle without manual intervention.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=15 asset-referencing replies and >=5 meetings booked over 2 months with reply rate holding at >=3%"
kpis: ["Asset link click rate", "Reply rate", "Asset-referencing reply rate", "Meeting rate", "Cost per meeting"]
slug: "outbound-with-value-asset"
install: "npx gtm-skills add marketing/problem-aware/outbound-with-value-asset"
drills:
  - enrich-and-score
  - follow-up-automation
  - ab-test-orchestrator
  - value-asset-refresh-pipeline
---

# Outbound With Value Asset — Scalable Automation

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Scalable finds the 10x multiplier. You move from a single asset and sequence to a system that: segments prospects and assigns them the most relevant asset, A/B tests every variable, automates follow-ups across channels, and scales volume to 1,000+ prospects/month without proportional effort increase.

**Pass threshold:** >=15 asset-referencing replies AND >=5 meetings booked over 2 months, with reply rate holding at >=3% as volume scales from 200 to 1,000+ per month.

## Leading Indicators

- Reply rate stays within 20% of Baseline rate as volume scales (no quality dilution)
- A/B tests produce at least 2 winning variants that outperform the original by 10%+
- Asset click rate holds above 15% across all segments
- Automated follow-up workflows generate at least 20% of total replies
- Cost per meeting stays below $150
- Multiple asset versions in rotation with measurable performance differences

## Instructions

### 1. Segment prospects and build multiple assets

Run the `enrich-and-score` drill to score and tier your full prospect pipeline. Create at least 2 distinct segments based on:
- Company size (e.g., 10-50 employees vs 50-200)
- Industry vertical
- Pain point category (derived from Clay enrichment)

For each segment, either adapt the existing asset or create a new one using the `value-asset-refresh-pipeline` drill. Each segment gets the asset version most relevant to their specific pain. In Clay, add an `assigned_asset` column that maps each prospect to their asset variant.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to set up experiments on:

**Priority 1 — Email subject lines:**
Test 3 variants per segment: (a) pain-point lead, (b) curiosity gap, (c) direct asset mention. Minimum 100 sends per variant before declaring a winner.

**Priority 2 — Asset format:**
If you have a checklist and a benchmark, split-test which format generates more asset-referencing replies. Track not just reply rate but quality of replies (do they reference the content?).

**Priority 3 — Sequence timing:**
Test: (a) standard cadence (Day 0, 4, 9), (b) compressed cadence (Day 0, 2, 5), (c) extended cadence (Day 0, 7, 14). Different audiences may have different response rhythms.

**Priority 4 — Email 3 CTA:**
Test: (a) Cal.com link, (b) "reply with your availability", (c) "I'll send over a 2-minute demo video." Track which CTA converts replies to meetings.

Use PostHog feature flags to randomly assign variants. Never run more than 1 test per prospect. Run each test for its full planned duration — no early stopping.

### 3. Build automated follow-up workflows

Run the `follow-up-automation` drill to create n8n workflows for:

- **Asset clicker, no reply (48 hours after click):** Send a follow-up highlighting the specific section they likely read (based on time-on-page if trackable) or the asset's key finding. Do NOT mention that you tracked their click.
- **Positive reply, no meeting (5 days after reply):** Send a gentle nudge with 2-3 specific time slots. Keep it brief: "Still happy to chat if the timing works — here are a few slots this week: [times]."
- **Meeting no-show (2 hours after missed meeting):** Auto-send a reschedule message with new times.
- **New prospect enters pipeline from signal:** When Clay detects a buying signal (job change, funding, hiring), auto-assign the relevant asset and add to the next batch.

Set guardrails: maximum 6 total touches per prospect across all channels. Suppress anyone who replied negatively or opted out.

### 4. Scale volume to 1,000+ prospects/month

Increase Clay enrichment to process 250-300 new prospects per week:
- Run Apollo sourcing weekly with fresh ICP filters
- Apply the scoring model from `enrich-and-score` — only prospects scoring 70+ enter the sequence
- Auto-push qualified prospects from Clay to Instantly via n8n
- Rotate sending accounts to maintain deliverability at higher volume (add 1 new domain per 500 monthly sends)

### 5. Monitor and optimize continuously

Track weekly in PostHog:
- Reply rate by segment, asset variant, and sequence step
- A/B test progress and results
- Cost per meeting trending over time
- Funnel conversion: send -> click -> reply -> meeting -> pipeline

Monthly: Run the `value-asset-refresh-pipeline` drill to assess asset performance, retire underperformers, and generate new asset topics based on reply patterns.

After 2 months, evaluate against threshold: >=15 asset-referencing replies AND >=5 meetings booked, with reply rate >=3%.

**If PASS:** The play scales profitably. Proceed to Durable to deploy autonomous optimization.

**If FAIL:** Diagnose:
- Reply rate declined as volume scaled: ICP scoring threshold is too low. Tighten scoring.
- Meetings low despite replies: Email 3 CTA is not converting. Test different meeting formats (async video, written proposal).
- One segment performs, others do not: Double down on the winning segment. Create hyper-specific assets for underperforming segments or drop them.

## Time Estimate

- Prospect segmentation and scoring: 4 hours
- New asset creation (1-2 additional assets): 6 hours
- A/B test setup (4 experiments): 6 hours
- Follow-up automation workflows: 6 hours
- Volume scaling and domain setup: 4 hours
- Weekly monitoring (1 hr/week x 8 weeks): 8 hours
- Monthly asset review and optimization: 4 hours
- Final evaluation: 2 hours
- **Total: ~40 hours over 2 months**

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email at scale with A/B testing | Hypergrowth: $78/mo annual — 25,000 contacts, 125,000 emails ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Enrichment, scoring, and segmentation | Launch: $185/mo — 2,500 credits ([clay.com/pricing](https://www.clay.com/pricing)) |
| Apollo | Prospect sourcing at volume | Basic: $49/user/mo — unlimited email credits ([apollo.io/pricing](https://www.apollo.io/pricing)) |
| Attio | CRM pipeline and deal tracking | Plus: $29/user/mo ([attio.com](https://attio.com)) |
| PostHog | Funnel tracking and experimentation | Free tier likely sufficient; paid starts at ~$0.00005/event over 1M ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation workflows | Pro: ~$60/mo — 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |

**Estimated monthly cost: ~$400-500/mo** (Instantly Hypergrowth + Clay Launch + Apollo Basic + Attio Plus + n8n Pro)

## Drills Referenced

- `enrich-and-score` — score and segment prospects for multi-asset routing
- `follow-up-automation` — build n8n workflows for automated cross-channel follow-ups
- `ab-test-orchestrator` — design, run, and evaluate experiments on every sequence variable
- `value-asset-refresh-pipeline` — create new assets, A/B test formats, retire underperformers
