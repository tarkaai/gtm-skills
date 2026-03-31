---
name: plg-sales-hybrid-scalable
description: >
  PLG + Sales-Assist Model — Scalable Automation. Scale to 500+ accounts with
  automated PQL scoring and routing, A/B-tested prompt variants, and seat expansion
  triggers. Target: >=45% conversion at 500+ accounts in the pipeline.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=45% conversion at 500+ accounts in pipeline"
kpis: ["Sales-assist conversion rate", "Self-serve upgrade rate", "PQL volume per week", "MRR added per month", "Routing accuracy"]
slug: "plg-sales-hybrid"
install: "npx gtm-skills add product/upsell/plg-sales-hybrid"
drills:
  - ab-test-orchestrator
  - plg-sales-routing
  - seat-expansion-prompt-delivery
---

# PLG + Sales-Assist Model — Scalable Automation

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Direct

## Outcomes

Scale the PLG-to-sales pipeline from tens of accounts to 500+ without proportional human effort. The PQL scoring and routing engine runs autonomously. A/B tests systematically optimize prompt copy, timing, and routing thresholds. Seat expansion surfaces a new growth vector. Target: >=45% conversion rate across both self-serve and sales-assist paths at 500+ accounts in the pipeline over 2 months.

## Leading Indicators

- PQL pipeline consistently processing 50+ new accounts per week
- A/B tests reaching statistical significance within 2-week cycles
- Seat expansion prompts firing for 20+ accounts per week
- Routing accuracy above 80% (accounts converting on the path they were routed to)
- No single AE handling more than 15 active sales-assist deals simultaneously

## Instructions

### 1. Launch systematic A/B testing on the conversion pipeline

Run the `ab-test-orchestrator` drill to test the highest-leverage elements of the PLG funnel:

**Test 1 (weeks 1-2): Upgrade prompt copy**
- Control: current prompt copy from Baseline
- Variant: rewrite prompt to emphasize the specific value unlocked (not the feature name, but the outcome)
- Example: Control: "Upgrade to Pro for unlimited projects." Variant: "Your team created 47 projects this month. On Pro, you will never hit a limit."
- Primary metric: `plg_prompt_clicked` rate
- Secondary metric: `plg_upgrade_completed` rate

**Test 2 (weeks 3-4): Routing threshold**
- Control: PQL score 65+ routes to sales
- Variant: PQL score 55+ routes to sales (lower threshold catches more accounts)
- Primary metric: sales-assist conversion rate
- Secondary metric: AE meeting utilization (are we wasting rep time?)

**Test 3 (weeks 5-6): Prompt timing**
- Control: prompt appears immediately when PQL threshold is crossed
- Variant: prompt appears on the user's next session after crossing (delay by one session)
- Primary metric: `plg_prompt_clicked` rate
- Hypothesis: users in the middle of a workflow are less receptive; catching them at session start gives better results

**Test 4 (weeks 7-8): Sales handoff format**
- Control: Intercom message + email with Cal.com link
- Variant: Intercom message only with an embedded booking widget (no email)
- Primary metric: meeting booked rate
- Secondary metric: time from PQL signal to meeting booked

Run each test for statistical significance (minimum 200 accounts per variant or 14 days, whichever is longer). Implement winners before starting the next test.

### 2. Deploy the automated PQL scoring and routing engine

Run the `plg-sales-routing` drill to build the full automated pipeline:

1. **PQL signal detection:** Configure all Tier 1 and Tier 2 signals from the drill. At Baseline you used 2-3 signals; now expand to the full set: plan limits, feature gates, team growth, usage volume, integration count, pricing page visits, and engagement score thresholds.

2. **Scoring model:** Deploy the composite PQL score (product signal score 0-60 + account value score 0-40). Wire the scoring to run in real time via n8n webhook when any PQL signal fires.

3. **Routing logic:** Implement the three-path routing:
   - Self-serve (score 40-64): contextual in-app prompt + email
   - Sales-assist (score 65+): Attio deal creation + AE assignment + warm handoff message
   - Sales override (any score): immediate routing when user explicitly requests a conversation

4. **Handoff enrichment:** For every sales-routed account, auto-generate an account brief: full PostHog usage history, engagement score breakdown, PQL signal timeline, support history from Intercom, and company enrichment data. Attach to the Attio deal so the AE walks in prepared.

5. **Mis-route detection:** Track accounts that were self-serve routed but ended up contacting sales (should have been sales-assisted), and accounts that were sales-routed but self-served anyway (wasted AE time). Feed mis-route data back to recalibrate the PQL score thresholds monthly.

### 3. Activate seat expansion as a growth vector

Run the `seat-expansion-prompt-delivery` drill to surface seat-based expansion opportunities:

1. Configure signal detection for: team invite attempts that fail (seat limit hit), invite frequency spikes, collaboration signals (sharing with non-members), and admin visits to team settings.

2. Deploy contextual prompts per signal type:
   - Seat limit hit: modal blocking the invite flow with a one-click add-seats button
   - Growth signals: non-blocking banner suggesting team plan benefits
   - Collaboration signals: subtle Intercom post suggesting adding collaborators as members

3. Route high-MRR accounts (>$500/mo) to the account owner for personal outreach instead of self-serve prompts.

4. Track the full expansion funnel: signal detected -> prompt shown -> prompt clicked -> seats added -> MRR impact. Target: seat expansion adds 15-25% of total MRR growth from this play.

### 4. Evaluate at scale

After 2 months, measure against the threshold with 500+ accounts in the pipeline:

- **Primary metric:** Overall conversion rate (accounts that upgraded, expanded, or closed a deal / total PQL-flagged accounts). Target: >=45%.
- **Breakdown by path:** Self-serve conversion rate (target: >=20%), sales-assist conversion rate (target: >=50%), seat expansion conversion rate (target: >=10% of prompted accounts add seats).
- **Efficiency metrics:** AE time per deal, MRR per PQL signal, routing accuracy.
- **A/B test results:** Net lift from all implemented winning variants.

**Pass (>=45% at 500+ accounts):** The pipeline scales. Document the winning configurations, PQL thresholds, and A/B test results. Proceed to Durable.

**Fail (<45%):** Identify which path is dragging the average. If self-serve is below 20%, the prompts are not converting -- run more prompt copy/timing tests. If sales-assist is below 50%, the routing is sending the wrong accounts or the AE process needs improvement. If volume is below 500, the PQL signals are too restrictive -- expand the signal set or lower thresholds.

## Time Estimate

- 12 hours: A/B test design, setup, and analysis (4 tests over 8 weeks)
- 20 hours: PQL scoring and routing engine build, including handoff enrichment
- 12 hours: seat expansion signal detection and prompt configuration
- 8 hours: monitoring, mis-route analysis, and threshold recalibration
- 8 hours: final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | PQL scoring, A/B tests via feature flags, funnel tracking | Usage-based: ~$0.00005/event after 1M free ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app prompts, chat handoff, seat expansion messages | Advanced: $85/seat/mo; Proactive Support: $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Triggered upgrade and expansion emails | From $49/mo based on contact count ([loops.so/pricing](https://loops.so/pricing)) |
| Cal.com | Sales meeting booking | Free tier or $12/seat/mo for team features ([cal.com/pricing](https://cal.com/pricing)) |
| Attio | Deal pipeline, account enrichment, AE assignment | Standard stack (excluded) |
| n8n | Real-time PQL scoring, routing workflows, handoff automation | Standard stack (excluded) |

**Play-specific cost:** ~$150-450/mo (Intercom Advanced seat + Proactive Support for advanced targeting + Loops paid tier)

## Drills Referenced

- `ab-test-orchestrator` -- design, run, and analyze 4 sequential A/B tests on the PLG conversion funnel
- `plg-sales-routing` -- build the automated PQL scoring engine and three-path routing system
- `seat-expansion-prompt-delivery` -- detect seat growth signals and deliver contextual expansion prompts
