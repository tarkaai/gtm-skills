---
name: multi-year-deal-negotiation-scalable
description: >
  Multi-Year Deal Negotiation — Scalable Automation. Find the 10x multiplier:
  proactively identify multi-year candidates via readiness scoring and intent
  signals, run segment-specific campaigns, and A/B test deal structures to
  optimize close rate and TCV without proportional effort.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=30% close rate on multi-year proposals, average TCV >=2x annual ACV, and 3x proposal volume vs Baseline over 2 months"
kpis: ["Multi-year close rate", "Average TCV", "Proposal volume (total and proactive vs reactive)", "Experiment win rate", "Average discount efficiency"]
slug: "multi-year-deal-negotiation"
install: "npx gtm-skills add sales/proposed/multi-year-deal-negotiation"
---

# Multi-Year Deal Negotiation — Scalable Automation

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email

## Outcomes

Scale multi-year deal volume without proportional effort. Instead of waiting for deals to reach Proposed stage, proactively identify candidates via readiness scoring and intent signals. A/B test deal structures to find the optimal discount, term, and presentation combination. Target: >=30% close rate on multi-year proposals, average TCV at least 2x annual ACV, and 3x the proposal volume achieved at Baseline — all within 2 months.

## Leading Indicators

- Readiness scoring model running weekly on all active deals
- At least 30% of multi-year proposals triggered proactively (from scoring) vs reactively (from stage change)
- Intent signals from Clay feeding into readiness scores
- At least 1 A/B experiment running at all times
- Segment-specific deal structures deployed (different templates for high/mid/growth ACV)
- Experiment history tracking populated with at least 2 completed experiments
- Multi-year pipeline coverage: >50% of eligible deals scored

## Instructions

### 1. Build the proactive pipeline engine

Run the the multi year pipeline scaling workflow (see instructions below) drill to create the system that identifies multi-year candidates before they reach the Proposed stage:

1. Analyze historical multi-year wins in Attio to build the multi-year ICP profile
2. Create the readiness scoring model in Clay with 8 weighted signals (ICP match, ACV, pain ratio, stage, fiscal timing, champion, competitive, commitment history)
3. Deploy the weekly scoring workflow in n8n that evaluates all active deals
4. Store `multiyear_readiness_score` and `multiyear_readiness_tier` on each deal in Attio
5. Build segment-specific deal structure templates (high-ACV, mid-ACV, growth)
6. Configure the proactive campaign: when a deal hits High readiness (score >= 80), auto-trigger the proposal automation from Baseline
7. Set up Clay intent signal monitoring: funding rounds, budget-cycle indicators, competitive switching signals

Verify the scoring model against Baseline data:
- Score all deals from Baseline retroactively
- Check: would the scoring model have identified the deals that closed as multi-year?
- If false negative rate > 30% (scoring misses deals that actually closed), adjust weights
- If false positive rate > 50% (scoring flags deals that never close multi-year), tighten criteria

### 2. Launch A/B testing on deal structures

Run the the deal term ab testing workflow (see instructions below) drill to start optimizing deal terms:

**First experiment (weeks 1-4): Discount level**
- Control: Current discount rates (from Baseline)
- Variant: 5 percentage points tighter discount
- Hypothesis: Tighter discounts will reduce close rate by <5% but increase average TCV by >8%
- Minimum: 20 proposals per variant before evaluating

**Second experiment (weeks 5-8): Number of options presented**
- Control: 3 options (anchor, target, concession)
- Variant: 2 options (target and premium only — remove the low-end concession)
- Hypothesis: Fewer options reduce decision fatigue and increase average TCV by anchoring between two higher-value options

For each experiment:
1. Create the PostHog feature flag
2. Modify the proposal automation workflow to check the flag
3. Apply the correct variant to each deal
4. Tag all proposals with `experiment_variant` for tracking
5. Evaluate after reaching minimum volume: adopt, iterate, or revert

### 3. Scale proposal volume

With readiness scoring and proactive triggers running:
- Target 30-50 multi-year proposals per month (3x Baseline volume)
- Monitor the proposal automation workflow for errors or bottlenecks
- Watch email deliverability — if sending volume increases, ensure Instantly warmup and domain health are maintained
- If proposal volume exceeds what the founder can negotiate alone, document the negotiation playbook and delegate to a team member

### 4. Optimize the negotiation playbook

Using data from the `deal-negotiation-tracking` events (from Baseline), identify patterns:
- Which concession sequence closes fastest? (e.g., offer rate lock first, then payment flexibility, then small discount)
- Which delivery method has the highest engagement? (live walkthrough vs email)
- Which champion seniority closes best? (VP vs Director vs Manager)
- What's the optimal time to propose multi-year? (days before fiscal year end)

Update the deal-term-modeling parameters and proposal automation workflow based on findings. This manual optimization at Scalable sets the baseline for autonomous optimization at Durable.

### 5. Evaluate against threshold

At the end of 2 months, review:
- Total proposals sent (must be >= 3x Baseline volume)
- Close rate on multi-year proposals (target: >= 30%)
- Average TCV of closed multi-year deals (target: >= 2x annual ACV)
- Proactive vs reactive proposal split (target: >= 30% proactive)
- Experiment results: at least 1 experiment completed with a clear outcome

If PASS: document all optimizations made, winning deal structures, and scoring model performance. Proceed to Durable.
If FAIL:
- If volume is below 3x: scoring model is too conservative or pipeline is too small. Loosen readiness thresholds or increase top-of-funnel.
- If close rate dropped vs Baseline: proactive proposals may be targeting the wrong accounts. Tighten scoring criteria.
- If TCV ratio dropped: experiments may have pushed discounts too high. Revert losing experiments.
- If experiments are inconclusive: need more volume. Extend the Scalable period by 2 weeks.

## Time Estimate

- 15 hours: building readiness scoring model and proactive pipeline (Clay, n8n, Attio)
- 10 hours: setting up A/B testing framework (PostHog feature flags, workflow modifications)
- 10 hours: running and evaluating experiments (2 experiments over 8 weeks)
- 15 hours: monitoring pipeline, handling negotiations at higher volume
- 10 hours: pattern analysis, playbook optimization, threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal pipeline, readiness scores, negotiation data | Standard stack (excluded) |
| PostHog | Experiments, feature flags, funnels, cohort analysis | Standard stack (excluded) |
| n8n | Scoring workflows, proposal automation, experiment routing | Standard stack (excluded) |
| Clay | Readiness scoring, intent signals, account enrichment | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Instantly | Email delivery at higher volume | Hypergrowth: $97/mo — [pricing](https://instantly.ai/pricing) |
| Anthropic Claude API | Deal term generation at scale (30-50 proposals/mo) | ~$30-60/mo — [pricing](https://docs.anthropic.com/en/docs/about-claude/pricing) |

**Play-specific cost:** ~$310-340/mo (Clay + Instantly + Claude API)

## Drills Referenced

- the multi year pipeline scaling workflow (see instructions below) — readiness scoring model, proactive identification workflow, segment-specific deal templates, intent signal monitoring
- the deal term ab testing workflow (see instructions below) — experiment framework for testing discount levels, option count, payment terms, presentation formats; with PostHog feature flags and evaluation protocol
