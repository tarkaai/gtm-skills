---
name: feature-announcement-campaign-scalable
description: >
  New Feature Announcements — Scalable Automation. Systematic A/B testing of
  announcement copy, timing, and channel mix across user segments. Automated
  adoption tracking and churn prevention for users who disengage after announcements.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "40 hours over 8 weeks"
outcome: "≥35% feature trial rate at 1,000+ users per announcement AND adoption decay ratio ≥0.35"
kpis: ["Feature trial rate at scale", "Adoption decay ratio", "Channel-level conversion", "Experiment win rate", "Churn save rate from announcement-triggered interventions"]
slug: "feature-announcement-campaign"
install: "npx gtm-skills add product/retain/feature-announcement-campaign"
drills:
  - ab-test-orchestrator
  - feature-adoption-monitor
  - churn-prevention
---

# New Feature Announcements — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Announcements reach 1,000+ users per release with a ≥35% trial rate and adoption decay ratio ≥0.35 (meaning at least 35% of peak usage becomes steady-state usage). Systematic testing identifies the optimal announcement format, timing, and channel mix for each user segment. Users who disengage after feature announcements are caught by automated churn prevention.

## Leading Indicators

- A/B tests producing statistically significant results within 2-week windows
- Decay ratio improving across successive announcements
- Channel-level conversion rates diverging (one channel clearly better for specific segments)
- Churn intervention triggered for disengaged users within 48 hours

## Instructions

### 1. Run systematic announcement experiments

Run the `ab-test-orchestrator` drill to test these variables one at a time across announcements:

**Copy variants:**
- Benefit-first headline vs. feature-name headline
- Short copy (2 sentences + CTA) vs. detailed copy (paragraph + screenshot + CTA)
- Social proof inclusion ("500 teams already using this") vs. no social proof

**Timing variants:**
- Announce on feature ship day vs. 3 days after ship (letting early adopters find it organically first)
- Morning email (9am user timezone) vs. afternoon (2pm)
- In-app message on login vs. in-app message when user visits a related feature

**Channel variants:**
- In-app only vs. email only vs. in-app + email
- In-app banner vs. modal vs. tooltip
- For Tier 2 features: test whether email adds value over in-app alone

Use PostHog feature flags to split users into test and control for each experiment. Run each test for a minimum of 7 days or until 200+ users per variant, whichever is longer. Measure feature trial rate and 7-day retention, not just click-through rate.

### 2. Expand adoption monitoring across segments

Run the `feature-adoption-monitor` drill with expanded scope:

- Track adoption funnels per user segment: plan type (free, paid, enterprise), tenure (<30 days, 30-90 days, 90+ days), usage level (light, moderate, power)
- Calculate the adoption decay ratio for each feature: `steady_state_usage / peak_usage` measured at Day 14 vs. Day 1-3 peak
- Identify which segments have the highest decay (announcement works initially but does not stick) — these need better post-announcement onboarding
- Configure per-segment stalled-user interventions: power users get a "what's new in the API" nudge, new users get a "here's how to get started" walkthrough

### 3. Build announcement-triggered churn prevention

Run the `churn-prevention` drill with announcement-specific signals:

- **Announcement fatigue signal**: User dismissed 3+ announcements in 30 days without clicking any. This user is tuning out — reduce announcement frequency for them and switch to organic feature discovery (tooltips, empty state CTAs).
- **Feature disappointment signal**: User tried an announced feature, used it once, and never returned. The feature did not meet the expectation the announcement set. Trigger a "need help with [feature]?" in-app message.
- **Segment mismatch signal**: User in a segment that consistently has <10% trial rate for announcements. Remove them from announcement targeting and find alternative discovery channels.

For each signal, configure the intervention tier:
- Low risk: reduce announcement frequency, rely on organic discovery
- Medium risk: send a personalized "here's what you might have missed" digest email monthly instead of per-feature announcements
- High risk: flag for manual review — this user may be disengaging from the product entirely

### 4. Evaluate against threshold

Measure against: ≥35% feature trial rate at 1,000+ users per announcement AND adoption decay ratio ≥0.35.

Calculate across the most recent 3 announcements. Both thresholds must be met.

If PASS: the announcement system scales and retains. Proceed to Durable for autonomous optimization.

If FAIL: review experiment results. If trial rate is below 35%, the best-performing announcement variant from A/B tests has not been broadly adopted — roll it out as the new default. If decay ratio is below 0.35, the post-announcement experience needs improvement — focus on the stalled-user interventions and in-product feature onboarding.

## Time Estimate

- 12 hours: A/B test design, setup, and analysis across 4-6 experiments
- 10 hours: expanded adoption monitoring setup per segment
- 10 hours: churn prevention signal definition and intervention configuration
- 8 hours: ongoing monitoring, analysis, and iteration over 8 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app announcements, nudges, and churn interventions | https://www.intercom.com/pricing — Pro $99/seat/mo (for A/B testing features) |
| Loops | Email announcements and lifecycle follow-ups | https://loops.so/pricing — Growth $99/mo for 10,000 contacts |
| PostHog | Feature flags, experiments, funnels, and cohorts | https://posthog.com/pricing — Free up to 1M events/mo, $0.00045/event after |
| n8n | Churn signal detection and intervention automation | https://n8n.io/pricing — Free self-hosted |

**Play-specific cost:** ~$100-250/mo (increased Intercom and Loops tiers for A/B testing and larger segments)

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on announcement copy, timing, and channel mix
- `feature-adoption-monitor` — tracks per-segment adoption funnels, decay ratios, and stalled-user interventions
- `churn-prevention` — detects announcement fatigue, feature disappointment, and segment mismatch signals; triggers tiered interventions
