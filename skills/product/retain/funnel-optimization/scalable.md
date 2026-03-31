---
name: funnel-optimization-scalable
description: >
  Conversion Funnel Optimization — Scalable. Find the 10x multiplier by scaling funnel
  optimizations across user segments, running parallel experiments, and building a
  self-serve experimentation pipeline that works across 500+ users per funnel.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable"
time: "60 hours over 2 months"
outcome: ">=15% end-to-end funnel conversion at 500+ monthly users, with per-segment optimizations live for top 3 underperforming segments"
kpis: ["Funnel conversion rate", "Drop-off reduction", "Test velocity", "Segment-level conversion parity"]
slug: "funnel-optimization"
install: "npx gtm-skills add product/retain/funnel-optimization"
drills:
  - funnel-segment-scaling
  - ab-test-orchestrator
  - funnel-optimization-health-monitor
  - dashboard-builder
  - threshold-engine
---

# Conversion Funnel Optimization — Scalable

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The 10x multiplier for funnel optimization is segmentation. A single funnel variant leaves conversion on the table for segments with different friction patterns. At Scalable, you build per-segment funnel variants for the top 3 underperforming segments, run parallel experiments across segments, and build a dashboard that gives real-time visibility into per-segment funnel health. The system handles 500+ users per month across all funnels without proportional human effort.

**Pass threshold:** >=15% end-to-end funnel conversion rate at 500+ monthly users, with per-segment optimizations live and tracked for the top 3 underperforming segments.

## Leading Indicators

- Segment analysis complete: conversion rates calculated for >=5 segments across each funnel
- Top 3 underperforming segments identified with >=20% gap vs best-performing segment
- Per-segment funnel variants deployed behind PostHog feature flags with property-based routing
- At least 4 experiments completed across segments in the first month
- Per-segment dashboard live with segment-level conversion trends
- Experiment win rate >=40% (at least 2 of 5 experiments beat control)

## Instructions

### 1. Build the segment analysis

Before optimizing segments, quantify which segments have the biggest gaps. For each funnel, use the `funnel-segment-scaling` drill's step 1: create PostHog cohorts for each major segment dimension and calculate per-segment funnel conversion rates.

Dimensions to analyze:
- Acquisition source (organic, paid, referral, direct)
- Device type (mobile, desktop, tablet)
- User type (individual, team admin, enterprise)
- Geography (top 5 countries by volume)
- Signup method (email, Google OAuth, GitHub OAuth)

Output: a ranked table of segments by optimization opportunity = `(best_segment_cvr - this_segment_cvr) * this_segment_volume`.

### 2. Deploy per-segment funnel variants

Run the `funnel-segment-scaling` drill for the top 3 underperforming segments. This produces:

- PostHog feature flags routing users into segment-specific funnel variants based on their properties
- Per-segment Intercom messages contextualizing the funnel for each segment's expectations
- Per-segment Loops email sequences for activation and onboarding
- Independent tracking per segment for isolated measurement

Each variant should address the specific friction diagnosed for that segment. Examples:
- Mobile users: single-column layout, sticky CTA, OAuth-first, deferred email verification
- Paid traffic users: continuity from ad promise, social proof matching ad messaging, faster time-to-value path
- Team admins: skip personal setup, go straight to workspace config, show team features immediately

### 3. Run parallel experiments

Run the `ab-test-orchestrator` drill to formalize the experimentation process. At Scalable level, run experiments across segments in parallel (1 active experiment per segment, up to 3 simultaneously across different segments).

For each experiment:
1. Form a hypothesis specific to the segment's friction pattern
2. Calculate required sample size (minimum 200 per variant per segment)
3. Deploy the experiment via PostHog feature flags
4. Monitor with the existing `funnel-optimization-health-monitor` system
5. Evaluate at the planned end date using proper statistical rigor

Target: 4+ experiments completed in the first month, 8+ by end of month 2.

### 4. Build the comprehensive funnel dashboard

Run the `dashboard-builder` drill to create a Product-level funnel dashboard. This should show:

**Row 1 — Executive summary:** End-to-end conversion rate for each funnel with trend lines and threshold indicators
**Row 2 — Segment breakdown:** Per-segment conversion rates for the primary funnel, sorted by performance
**Row 3 — Experiment tracker:** Active experiments with interim results, completed experiments with outcomes
**Row 4 — Optimization velocity:** Experiments per month, win rate, cumulative lift since play start
**Row 5 — Bottleneck tracker:** Current primary bottleneck per funnel with trend direction

This dashboard is the primary visibility surface for the team. Set it as the default Product dashboard in PostHog.

### 5. Build the experimentation pipeline

Create a systematic pipeline so experiments flow without manual orchestration:

Using `funnel-optimization-health-monitor` outputs, build an n8n workflow that:
1. Detects when a funnel step degrades (warning/critical status for 3+ days)
2. Automatically runs `funnel-drop-off-diagnosis` logic: pulls segment breakdown, identifies the worst-performing segment, generates hypotheses via Claude
3. Proposes the top experiment to the team via Slack: "Signup funnel step 3 degraded 12% this week. Root cause hypothesis: mobile validation errors increased after last deploy. Proposed experiment: inline validation with mobile-optimized error messages. Approve?"
4. On approval (Slack reaction or button), creates the PostHog experiment and feature flag automatically
5. Monitors the experiment and posts results when significant

**Human action required:** Approve proposed experiments. The system proposes; humans approve at Scalable. At Durable, low-risk experiments run autonomously.

### 6. Track cross-segment learnings

After 4+ weeks of per-segment experimentation, analyze which optimizations transfer across segments:

- Optimizations that improve >=3 segments: promote to the general funnel (they are universal improvements)
- Optimizations that improve only 1 segment: keep as segment-specific variants
- Optimizations that improve 1 segment but hurt another: keep segment-specific and add exclusion rules

Log these learnings in Attio for institutional memory. They inform which future experiments to run across all segments vs. targeted segments.

### 7. Evaluate against threshold

Run the `threshold-engine` drill: is end-to-end funnel conversion >=15% at 500+ monthly users with per-segment optimizations live?

If PASS: Proceed to Durable. The segmented optimization system is producing gains at scale.
If FAIL: Diagnose — is the issue insufficient segment coverage (need more variants), low experiment velocity (need faster cycles), or traffic below 500/mo (product-level issue, not funnel-level)?

## Time Estimate

- 8 hours: Segment analysis across all funnels (cohort creation, metric calculation, ranking)
- 12 hours: Build and deploy 3 per-segment funnel variants (feature flags, Intercom messages, Loops sequences)
- 15 hours: Run 8+ experiments over 2 months (hypothesis, setup, monitoring, evaluation)
- 8 hours: Build comprehensive dashboard and experimentation pipeline
- 10 hours: Weekly monitoring, cross-segment analysis, iteration
- 7 hours: Documentation, threshold evaluation, Durable prep

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, feature flags, experiments, session recordings, dashboards | Growth from $0 (usage-based, ~$50-150/mo at 500+ users) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Experimentation pipeline automation, monitoring workflows | Pro EUR60/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | Per-segment in-app messaging, product tours, help triggers | Essential $39/seat/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Per-segment lifecycle email sequences | Growth from $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Claude API | Hypothesis generation for experimentation pipeline | ~$10-25/mo — [anthropic.com](https://console.anthropic.com) |

**Estimated play-specific cost:** ~$200-400/mo (PostHog usage + n8n + Intercom + Loops + Claude API)

## Drills Referenced

- `funnel-segment-scaling` — Builds per-segment funnel variants with property-based routing and independent tracking
- `ab-test-orchestrator` — Formalizes hypothesis-driven experimentation with statistical rigor
- `funnel-optimization-health-monitor` — Always-on monitoring feeding the experimentation pipeline
- `dashboard-builder` — Comprehensive funnel dashboard for real-time team visibility
- `threshold-engine` — Evaluates >=15% conversion at 500+ users with segment coverage
