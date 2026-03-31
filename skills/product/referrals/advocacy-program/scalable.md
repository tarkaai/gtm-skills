---
name: advocacy-program-scalable
description: >
  Formal Advocacy Program — Scalable Automation. Systematic A/B testing of tiers, rewards,
  and messaging. Segment-based personalization. Target 75+ advocates at 500+ user base.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Events"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=75 active advocates, >=25 referrals/quarter, referral conversion rate >=30%"
kpis: ["Active advocate count", "Referrals per advocate per quarter", "Referral conversion rate (submitted to activated)", "Insider-to-Advocate promotion rate", "Advocacy revenue attribution"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - ab-test-orchestrator
  - advocacy-health-monitor
---

# Formal Advocacy Program — Scalable Automation

> **Stage:** Product -> Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Events

## Outcomes

75 or more active advocates (completed at least 1 action in last 90 days), 25 or more referrals per quarter, and a referral conversion rate of 30%+ (referred signups that reach activation). The 10x multiplier: segment-based personalization of asks and rewards, systematic testing of every program variable, and automated tier progression eliminate manual work at scale.

## Leading Indicators

- A/B test velocity: 2+ experiments running per month on program variables
- Insider-to-Advocate promotion rate >= 20% within 90 days of enrollment
- Referral link share rate increasing month-over-month
- Nudge sequence open rate holding above 40% as volume scales
- Advocate retention (action in last 90 days) holding above 70%
- At least 1 Ambassador nominated and enrolled

## Instructions

### 1. Launch systematic A/B testing of program variables

Run the `ab-test-orchestrator` drill to test every variable that affects advocacy performance. Run experiments sequentially (1 at a time per variable to avoid interaction effects):

**Experiment 1 — Enrollment messaging (weeks 1-2):**
Use PostHog feature flags to split new Insider candidates into 2 groups:
- Control: current enrollment message ("Welcome to the Insider program")
- Variant: value-led message ("You are in the top 15% of users. Here is what that unlocks.")
- Measure: enrollment acceptance rate
- Adopt the winner, then test a third variant against the new control

**Experiment 2 — First-ask optimization (weeks 3-4):**
Split newly enrolled advocates:
- Control: testimonial request as first ask
- Variant: referral link share as first ask
- Measure: time-to-first-action and 30-day activation rate
- The lower-friction ask may activate more advocates even if individual action value is lower

**Experiment 3 — Referral incentive structure (weeks 5-6):**
Split active advocates:
- Control: current two-sided reward (referrer credit + referee extended trial)
- Variant: tiered referral rewards (1st referral = small credit, 3rd = feature unlock, 5th = free month)
- Measure: referrals per advocate per month and referral conversion rate

**Experiment 4 — Nudge cadence (weeks 7-8):**
Split enrolled-but-inactive advocates:
- Control: current 7/14/21/30 day nudge cadence
- Variant: accelerated 3/7/14/21 day cadence
- Measure: activation rate and unsubscribe rate (guard against annoying users)

Log every experiment in PostHog with `ab_test_started`, `ab_test_evaluated`, and `ab_test_adopted` events. Store results in Attio.

### 2. Build segment-based personalization

Using PostHog cohorts and Attio custom attributes, personalize the advocacy experience by user segment:

**By product usage pattern:**
- Heavy API users -> ask for developer testimonials, offer API credit as reward
- Collaboration-heavy users -> ask for team case studies, offer extra seats as reward
- Dashboard/analytics users -> ask for data-focused testimonials, offer premium analytics features

**By advocacy behavior:**
- Testimonial-preferring advocates -> route more testimonial asks, skip referral nudges
- Referral-preferring advocates -> emphasize referral rewards, skip testimonial asks
- Event-willing advocates -> invite to webinar speaking, conference panels

Implement personalization via PostHog person properties and Intercom user segments. Each segment gets a tailored Loops sequence variant.

**By tenure:**
- New advocates (< 30 days enrolled) -> focus on activation, easy asks
- Established advocates (30-90 days) -> increase ask complexity, introduce referral goals
- Veteran advocates (90+ days) -> Ambassador track, advisory board, co-marketing

### 3. Deploy the advocacy health monitor

Run the `advocacy-health-monitor` drill to build always-on health tracking for 8 metrics:

- Recruitment rate (new Insiders / eligible users)
- Activation rate (first action within 30 days)
- Insider-to-Advocate conversion (promoted / enrolled 90+ days ago)
- Referral yield (referrals per active advocate per quarter)
- Referral conversion (referred signups activated / referrals submitted)
- Advocate retention (action in last 90 days / total advocates)
- Power user score stability (% of advocates maintaining score >= 60)
- Testimonial/content yield (testimonials + case studies per quarter)

Configure automated interventions:
- Stale enrollment message: auto-rotate to next variant if click rate < 5%
- Activation stall: extra personalized nudge if cohort 14-day activation < 20%
- Referral drought: in-app reminder to top 10 advocates if no referrals in 14 days
- Lapsed advocate: re-engagement email with fresh, contextual ask

Set escalation rules: any metric critical for 3+ days, advocate retention below 50% for 2 weeks, or 3+ interventions in one week with no improvement triggers human review.

### 4. Scale the Ambassador tier

With 75+ advocates in the pipeline, identify and promote the top performers:

1. Query Attio for Advocates with score >= 90 sustained for 3+ months AND 3+ advocacy actions completed
2. Generate a nomination brief: user's usage data, advocacy history, referral count, testimonial quality
3. **Human action required:** Review nominations and approve Ambassador promotions
4. For approved Ambassadors: enable `advocacy-ambassador-perks` feature flag, send personal onboarding (Loops + scheduled 1:1 call via Cal.com), add to advisory board roster in Attio

### 5. Evaluate against threshold

After 2 months, measure:
- **Pass**: >= 75 active advocates AND >= 25 referrals/quarter AND >= 30% referral conversion rate
- **Fail**: identify which segment or funnel stage is underperforming using the health monitor diagnostics. Focus experiments on the weakest metric.

If PASS, proceed to Durable.

## Time Estimate

- 16 hours: A/B test design, implementation, and evaluation (4 experiments x 4 hours)
- 12 hours: segment-based personalization build (cohort definitions, sequence variants, routing logic)
- 16 hours: advocacy health monitor setup (8 metrics, 4 interventions, escalation rules)
- 8 hours: Ambassador tier scaling and nomination pipeline
- 4 hours: weekly monitoring, iteration, threshold evaluation
- 4 hours: documentation and Durable preparation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | A/B experiments, feature flags, cohorts, dashboards, health metrics | Free tier likely sufficient; paid starts at usage-based rates ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Advocate CRM, experiment logging, nomination pipeline | Standard stack |
| Loops | Personalized sequences per segment, re-engagement emails | $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | Segment-targeted in-app messages, referral prompts, health interventions | $29-85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Health monitor crons, intervention triggers, experiment workflows | Standard stack |

**Estimated monthly cost: $78-134/mo** (Loops $49 + Intercom $29-85/seat)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and evaluate 4 sequential experiments on enrollment messaging, first-ask type, referral incentives, and nudge cadence
- `advocacy-health-monitor` — track 8 advocacy-specific health metrics with diagnostic triggers, automated interventions, and escalation rules
