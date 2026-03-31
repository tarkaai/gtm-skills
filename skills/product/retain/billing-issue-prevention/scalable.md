---
name: billing-issue-prevention-scalable
description: >
  Payment Failure Recovery — Scalable Automation. A/B test dunning sequences, segment recovery
  strategies by failure type and account value, and scale to 500+ monthly failures while
  maintaining ≥65% recovery rate.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥65% recovery rate at 500+ monthly failures"
kpis: ["Recovery rate", "Involuntary churn rate", "Median time to recovery", "Revenue recovered ($)", "Dunning conversion by step"]
slug: "billing-issue-prevention"
install: "npx gtm-skills add product/retain/billing-issue-prevention"
drills:
  - ab-test-orchestrator
  - dashboard-builder
---

# Payment Failure Recovery — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Find the 10x multiplier. The Baseline proved the recovery system works at small scale. Scalable makes it work at 500+ monthly failures without proportional effort by: A/B testing every element of the dunning sequence (subject lines, send times, copy, CTA placement), segmenting recovery strategies by failure type and account value, optimizing Smart Retry timing with Stripe, and measuring dunning step ROI to eliminate waste. The pass threshold is maintaining ≥65% recovery rate at 500+ monthly failures.

## Leading Indicators

- A/B tests produce statistically significant winners (p < 0.05) within 2-week test cycles
- Segmented dunning sequences outperform the generic sequence by at least 10% for the top failure type
- Proactive card expiry update rate exceeds 50% (preventing half of expiry-related failures)
- Revenue recovered per month exceeds 3x the revenue lost to involuntary churn
- Time-to-recovery median decreases by 20%+ vs. Baseline level

## Instructions

### 1. A/B test the dunning sequence systematically

Run the `ab-test-orchestrator` drill to test each element of the dunning sequence independently. Use PostHog feature flags to split traffic and Loops A/B testing for email variants.

**Test 1 — Subject lines (Week 1-2):**
Test the Day 0 email subject across 3 variants:
- Control: "Action needed: update your payment method"
- Variant A: "Your {{productName}} payment did not go through"
- Variant B: "Quick fix needed for your {{productName}} subscription"
Measure: open rate and recovery rate within 48 hours of send.

**Test 2 — Email send timing (Week 3-4):**
Test when the first dunning email is sent after failure detection:
- Control: immediate (within 5 minutes)
- Variant A: 2 hours after failure (gives Stripe one retry first)
- Variant B: next morning at 09:00 local time
Measure: recovery rate within 7 days.

**Test 3 — Recovery CTA placement (Week 5-6):**
Test where the one-click update link appears in the email:
- Control: single button after explanation paragraph
- Variant A: two CTAs — one at top, one at bottom
- Variant B: inline text link in the first sentence + button at bottom
Measure: click-through rate and recovery rate.

**Test 4 — Dunning cadence (Week 7-8):**
Test the time between emails:
- Control: Day 0, 3, 7, 12
- Variant A: Day 0, 1, 4, 8 (faster escalation)
- Variant B: Day 0, 5, 10, 14 (slower, less pressure)
Measure: recovery rate and unsubscribe rate (too-fast cadence may annoy).

After each test, implement the winner and move to the next test. Never stack tests — one variable at a time.

### 2. Segment recovery strategies by failure type

Not all failures are equal. Build segmented dunning paths:

**Expired card segment:**
These are the easiest to recover. These customers want to stay — their card just expired. Skip the "we noticed an issue" framing and go straight to: "Your card expired. Here is a one-click link to add your new card." Compress the sequence: Day 0 and Day 3 only. Recovery target: 85%+.

**Insufficient funds / generic decline:**
These customers may have temporary cash flow issues. Use empathetic framing: "We understand billing issues happen." Offer a grace period option if your product supports it. Space the sequence wider: Day 0, Day 5, Day 10, Day 14. Recovery target: 55%+.

**Authentication required (3DS/SCA):**
These customers need to complete a bank verification step. Send them directly to the Stripe hosted invoice page (not the billing portal). The email should explain: "Your bank requires you to verify this payment. It takes 30 seconds." Recovery target: 70%+.

Modify the the dunning sequence automation workflow (see instructions below) drill's n8n workflow to route each failure type to its segment-specific email templates and cadence.

### 3. Optimize Stripe Smart Retries

Review your Stripe Smart Retry performance:
- Query retry success rate by day-of-week and time-of-day
- Compare Smart Retry recovery rate against your dunning email recovery rate
- If Smart Retries recover 30%+ on their own, delay your first dunning email by 24 hours to let the retry succeed first (avoid sending "update your card" when the retry would have worked)

Work with Stripe's recovery settings to maximize automatic recoveries before your dunning sequence takes over.

### 4. Scale the health monitoring

Enhance the `dashboard-builder` for scale:

Add segments to the weekly health report:
- Recovery rate by failure type (compare against targets from Step 2)
- Recovery rate by account MRR bracket
- Recovery rate by dunning channel (in-app vs. email vs. human)
- A/B test results and next recommended test

Add a revenue-impact panel to the dashboard:
- Monthly Revenue Saved = sum of recovered subscription MRR
- Cost of Recovery = tool costs + human outreach time
- ROI = Revenue Saved / Cost of Recovery

### 5. Evaluate at scale

After 2 months, evaluate against the threshold: ≥65% recovery rate at 500+ monthly failures.

500+ monthly failures may sound like a lot, but at scale this includes: all failure types across all customers, proactive expiry warnings that converted to updates (count as prevented failures), and Smart Retry recoveries. The total volume grows with your customer base.

If PASS, proceed to Durable. If FAIL:
- If recovery rate is high but volume is low: you may not have enough failures to hit 500 — this is actually good news. Adjust the threshold to match your actual volume.
- If recovery rate dropped at scale: identify which segment degraded. Usually it is the "generic decline" segment where the dunning copy is not personalized enough.
- If a specific test hurt performance: revert to the pre-test configuration and try a different variable.

## Time Estimate

- 8 hours: design and configure 4 A/B tests (2 hours each: hypothesis, variants, feature flags, measurement)
- 12 hours: build segmented dunning paths (3 failure-type-specific sequences with custom templates)
- 4 hours: Stripe Smart Retry optimization analysis
- 8 hours: enhance health monitoring for segments and revenue impact
- 28 hours: monitoring, test analysis, winner implementation, and iteration over 2 months (~3.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Stripe | Payment data, Smart Retries, billing portal | Included with Stripe account — [stripe.com/pricing](https://stripe.com/pricing) |
| Loops | Segmented dunning email sequences, A/B test variants | $49/mo for 5K contacts — [loops.so/pricing](https://loops.so/pricing) |
| Intercom | In-app recovery banners, segment-specific messaging | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| PostHog | Experiments (feature flags + A/B testing), funnels, dashboards | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Sequence orchestration, segment routing, scheduling | Free self-hosted; cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost: $75-150/mo** (Loops + Intercom + n8n cloud; PostHog free tier likely sufficient)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on dunning sequence elements using PostHog feature flags
- the dunning sequence automation workflow (see instructions below) — the multi-channel recovery system, now with segment-specific paths for each failure type
- `dashboard-builder` — enhanced with per-segment metrics, revenue impact tracking, and A/B test reporting
