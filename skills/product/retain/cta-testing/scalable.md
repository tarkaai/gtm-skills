---
name: cta-testing-scalable
description: >
  CTA Optimization -- Scalable Automation. Expand CTA testing across all 5 instrumented surfaces
  with automated experiment queuing via n8n. Run 2-4 experiments per month, each targeting a
  different surface or variable. Achieve >=20% cumulative CTR lift across all surfaces.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=20% cumulative CTR lift across all surfaces with 2-4 experiments/month velocity"
kpis: ["Cumulative CTR lift (all surfaces)", "Experiment velocity (tests/month)", "Win rate (% of tests that ship)", "Per-surface best CTR", "Conversion rate impact"]
slug: "cta-testing"
install: "npx gtm-skills add product/retain/cta-testing"
drills:
  - ab-test-orchestrator
  - dashboard-builder
  - threshold-engine
---

# CTA Optimization -- Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

CTA testing runs continuously across all 5 instrumented surfaces at a velocity of 2-4 experiments per month. An n8n workflow automates experiment queuing: when one test completes, the next begins. Cumulative CTR lift across all surfaces reaches >= 20%. You have an experiment backlog, a documented win/loss record, and clear evidence of which CTA variables produce the biggest gains.

## Leading Indicators

- Second experiment launches within 3 days of the first experiment completing (pipeline is not stalling)
- At least 2 different surfaces have been tested by end of month 1
- Win rate is >= 40% (at least 2 of every 5 tests ship a winner)
- No surface has gone > 45 days without a test

## Instructions

### 1. Build the experiment backlog

Run the the cta variant pipeline workflow (see instructions below) drill for each of the 5 instrumented surfaces. For each surface, generate 3-5 variant hypotheses and rank them. This produces a backlog of 15-25 hypotheses across all surfaces.

Prioritize the backlog by:
1. **Surface traffic:** higher-traffic surfaces produce faster results and bigger absolute impact
2. **Current CTR gap:** surfaces with CTR far below the cross-surface median have the most headroom
3. **Hypothesis confidence:** prioritize hypotheses backed by session recording observations, support ticket patterns, or user feedback over pure guesses

Store the prioritized backlog in Attio as campaign notes or in a dedicated experiment tracker.

### 2. Automate experiment queuing

Run the `ab-test-orchestrator` drill to configure the test pipeline automation. Build an n8n workflow that:

1. Checks PostHog daily for any experiment in "completed" status (reached significance or hit the 4-week time limit)
2. When an experiment completes: pulls the result, logs the decision (ship/revert/extend), and updates the experiment tracker
3. If the experiment shipped a winner: rolls out the variant to 100% via PostHog feature flag API
4. Pulls the next highest-priority hypothesis from the backlog
5. Creates a new PostHog feature flag and experiment for that hypothesis
6. Alerts the team: "Experiment {X} completed ({result}). Starting experiment {Y} on surface {Z}."

**Human action required:** The first time the n8n workflow queues an experiment, review and approve it. After 3 successful auto-queued experiments, switch to notification-only mode (the agent auto-queues and you review the weekly brief).

**Human action required:** Each new variant requires a code change to render the variant based on the feature flag. Deploy the code within 48 hours of the experiment being queued to avoid pipeline stalls. Consider building a CTA component that reads variant config from PostHog feature flag payloads to eliminate per-test deploys:

```javascript
// Generic CTA component that reads config from PostHog flag payload
const ctaPayload = posthog.getFeatureFlagPayload('cta-variant-{surface}')
if (ctaPayload) {
  renderCTA({ text: ctaPayload.text, color: ctaPayload.color, placement: ctaPayload.placement })
} else {
  renderDefaultCTA()
}
```

### 3. Expand test variables

At Baseline, you tested copy changes on one surface. Now systematically test across all variable categories:

- **Round 1 (Month 1):** Copy variants on the 3 lowest-CTR surfaces. Copy changes are fastest to implement and produce the most consistent lift.
- **Round 2 (Month 1-2):** Placement and timing variants. Test above-fold vs below-fold, immediate vs delayed display (show after 30 seconds), persistent vs dismissible.
- **Round 3 (Month 2):** Design and urgency variants. Test button color, size, urgency framing, social proof elements. These require more implementation effort but can produce large lifts on high-traffic surfaces.

### 4. Monitor cross-surface health

Run the `dashboard-builder` drill with expanded scope: monitor all 5 surfaces simultaneously. Configure alerts for:

- Any surface CTR drops > 20% vs its post-optimization baseline (regression detection)
- Any experiment variant performs > 30% worse than control after 3 days (auto-revert trigger)
- Overall impression volume drops > 30% (traffic problem, not a CTA problem)

### 5. Evaluate against threshold

Run the `threshold-engine` drill monthly. Measure:

- **Cumulative CTR lift:** for each surface, compare current CTR to the pre-optimization baseline from Smoke. Average the lift across all 5 surfaces (weighted by impression volume).
- **Experiment velocity:** count tests completed in the last 30 days. Target: 2-4.
- **Win rate:** percentage of completed tests that shipped a winner.

Threshold: >= 20% cumulative CTR lift across all surfaces AND >= 2 experiments/month velocity.

If PASS after 2 months: proceed to Durable. The testing pipeline is producing consistent gains at volume.

If FAIL: diagnose.
- Low cumulative lift but good velocity: hypotheses are too conservative. Test bigger changes.
- Good lift but low velocity: experiments are running too long. Either increase traffic to surfaces (more impressions = faster convergence) or accept larger minimum detectable effects to reduce required sample size.
- Low win rate (< 25%): hypothesis quality is poor. Review session recordings and user feedback before generating variants.

## Time Estimate

- 6 hours: generate variant backlog for all 5 surfaces (15-25 hypotheses)
- 8 hours: build n8n experiment queuing workflow and test it
- 4 hours: build generic CTA component that reads PostHog flag payloads
- 8 hours: implement and deploy variants for 4-8 experiments over 2 months
- 8 hours: monitor experiments, analyze results, make decisions, update tracker
- 6 hours: monthly threshold evaluation and experiment backlog replenishment

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, event tracking, funnels | Free tier: 1M events/mo, 1M flag requests/mo. Paid: usage-based with step-down rates ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Experiment queuing automation, daily monitoring workflows | Self-hosted: free. Cloud: from EUR 24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |

## Drills Referenced

- the cta variant pipeline workflow (see instructions below) -- generates variant hypotheses for each surface and provides the deployment/measurement framework
- `ab-test-orchestrator` -- configures the automated experiment queuing pipeline in n8n and enforces statistical rigor
- `dashboard-builder` -- monitors all 5 surfaces simultaneously with regression detection and guardrail alerts
- `threshold-engine` -- evaluates cumulative lift and velocity thresholds monthly
