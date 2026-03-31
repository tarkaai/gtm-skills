---
name: nps-program-scalable
description: >
  NPS Feedback System — Scalable Automation. Scale NPS across multiple user segments with
  differentiated survey timing and channels, A/B tested survey parameters, automated
  promoter-to-advocate pipeline, and detractor theme detection feeding the product roadmap.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 8 weeks"
outcome: "≥40% response rate across 500+ surveys/month with NPS ≥35 AND ≥10% of promoters complete an advocacy action within 30 days"
kpis: ["NPS response rate", "NPS score", "Survey coverage by segment", "Promoter advocacy conversion", "Detractor save rate", "Experiment velocity"]
slug: "nps-program"
install: "npx gtm-skills add product/referrals/nps-program"
drills:
  - ab-test-orchestrator
  - advocacy-activation-pipeline
---

# NPS Feedback System — Scalable Automation

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

A multi-segment NPS program that surveys 500+ users per month across 6 distinct segments, each with optimized survey timing and channel. A/B tests continuously improve response rates and follow-up effectiveness. Promoters automatically feed into the advocacy pipeline. Detractor themes surface product issues before they become widespread. The system runs without manual intervention except for high-value detractor outreach.

## Leading Indicators

- Survey coverage reaches 50%+ of each segment per quarter
- A/B tests on survey timing produce statistically significant winners within 4 weeks
- Promoter-to-advocacy pipeline begins converting within 2 weeks of launch
- Detractor theme detection fires at least 1 alert in the first month (proves the detection works)
- Response rate holds or improves as volume increases (no fatigue signal)

## Instructions

### 1. Launch multi-segment survey scheduling

Run the the nps segment scaling workflow (see instructions below) drill to deploy differentiated surveys across 6 segments:

| Segment | Criteria | Timing | Channel |
|---------|----------|--------|---------|
| New users | 30-60 days post-signup, activated | 45 days post-signup | In-app (Intercom) |
| Established users | 60-180 days, active last 14 days | Quarterly | Email (Loops) |
| Power users | Top 20% usage, 90+ days | Quarterly, offset 6 weeks | In-app (Intercom) |
| Churning users | Usage declined 50%+ in last 30 days | Triggered on decline | Email (Loops) |
| Post-support users | Closed support ticket in last 7 days | 3 days after close | Email (Loops) |
| Expansion users | Upgraded plan in last 30 days | 21 days post-upgrade | In-app (Intercom) |

The segment scaling drill builds the n8n scheduling engine that enforces priority ordering, daily volume caps, 90-day cool-off periods, and anti-fatigue guardrails.

### 2. Launch A/B tests on survey parameters

Run the `ab-test-orchestrator` drill to test these variables:

**Round 1 (weeks 1-4):** Survey timing
- New users: 30 days vs 45 days vs 60 days post-signup
- Post-support: 3 days vs 7 days after ticket close
- Use PostHog feature flags to split users. Primary metric: response rate. Minimum 200 responses per variant.

**Round 2 (weeks 3-6):** Survey channel and format
- Established users: in-app survey vs email survey
- In-app format: interstitial modal vs slide-in panel
- Primary metric: response rate. Secondary metric: open-text completion rate.

**Round 3 (weeks 5-8):** Follow-up effectiveness
- Promoter thank-you: email with review link vs email with referral link vs email with both
- Passive follow-up: feature recommendation vs help article vs feedback call offer
- Primary metric: promoter advocacy conversion for promoters, NPS improvement on next survey for passives.

After each round, implement the winning variant and document the results. Each test must reach statistical significance before a winner is declared.

### 3. Connect promoters to the advocacy pipeline

Run the `advocacy-activation-pipeline` drill to build the promoter-to-advocate conversion path:

1. When the nps response routing workflow (see instructions below) tags a promoter as `advocacy_ready` (score 9-10, power user, tenure >90 days), automatically enroll them in the advocacy pipeline
2. The pipeline delivers: a personalized thank-you, a specific advocacy ask (review, testimonial, referral, case study), and a reward (early feature access, account credit, or swag)
3. Track the full funnel: promoter identified > advocacy ask sent > action started > action completed
4. Target: ≥10% of promoters complete an advocacy action within 30 days of their NPS response

For promoters who are NOT advocacy-ready (new users, lower usage), send the lighter follow-up: thank-you email with a referral link only. Do not overwhelm new promoters with asks.

### 4. Build the detractor-to-save pipeline at scale

Enhance the routing from Baseline with scaled detractor handling:

- **Automated theme clustering:** Configure the n8n AI node to run nightly, pulling all detractor open-text from the last 7 days. Cluster by theme using Claude. When a new theme reaches 5+ mentions, fire a `nps_theme_alert` event and create an Attio ticket.
- **Save playbook by theme:** For each recurring theme, pre-build a response template:
  - Performance complaints: "We are actively working on performance improvements. Here is our status page: [link]. A team member will share specifics about your case."
  - Missing feature: "This is on our roadmap for [quarter]. Here is the public roadmap link. We have added your vote."
  - Pricing concerns: "Let us review your account to make sure you are on the right plan. Booking link: [Cal.com link]."
- **Save rate tracking:** For each detractor who receives follow-up, track: did their usage stabilize or increase in the 30 days after? Did they submit a higher NPS on their next survey? Calculate save rate = (detractors whose next NPS improved or usage stabilized) / (total detractors who received follow-up).

### 5. Build segment-level NPS dashboards

Expand the Baseline dashboard with segment-level views:

- NPS score by segment, trended monthly (6 segment lines on one chart)
- Response rate by segment and channel
- Survey coverage: % of each segment surveyed this quarter (target: 50%+)
- A/B test results: current experiments, sample sizes, interim results
- Advocacy pipeline: promoters identified > enrolled > first action > completed
- Detractor save rate by theme
- Survey fatigue indicator: response rate for users surveyed 2+ times

### 6. Evaluate against threshold

After 8 weeks of multi-segment operation, measure:

- Response rate: total responses / total surveys sent across all segments. Pass: ≥40%.
- Volume: total surveys sent per month. Pass: ≥500.
- NPS score: trailing 30-day NPS. Pass: ≥35.
- Promoter advocacy conversion: promoters who completed an advocacy action / total promoters. Pass: ≥10%.
- No single segment with response rate below 25% (all segments are healthy).

If PASS: document segment-level NPS scores, winning experiment variants, advocacy conversion rate, and detractor themes. Proceed to Durable.
If FAIL on response rate: check fatigue indicators. If declining for re-surveyed users, extend cool-off periods. If low for a specific segment, test a different channel.
If FAIL on advocacy conversion: the ask may be too heavy. Test lighter advocacy actions (one-click rating vs. written testimonial).

## Time Estimate

- Segment scaling engine setup: 12 hours
- A/B test design and deployment (3 rounds): 15 hours
- Advocacy pipeline connection: 8 hours
- Detractor save pipeline and theme clustering: 8 hours
- Dashboard expansion and evaluation: 7 hours

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app surveys, advocacy enrollment messages | Proactive Support Plus: $99/mo (500 messages). Additional messages billed per unit. [Pricing](https://www.intercom.com/pricing) |
| PostHog | Surveys, experiments, feature flags, dashboards | Surveys: $0.10/response after 1,500 free. Experiments: $0.0001/request. [Pricing](https://posthog.com/pricing) |
| Loops | Email surveys, follow-up sequences, advocacy emails | From $49/mo. Scales with subscriber count. [Pricing](https://loops.so/pricing) |
| Attio | Response storage, advocacy tracking, theme tickets | Plus: $29/user/mo. [Pricing](https://attio.com/pricing) |
| n8n | Survey scheduling, routing, theme clustering, A/B test orchestration | Cloud: from $24/mo. Pro: $60/mo recommended at this scale. [Pricing](https://n8n.io/pricing) |

**Estimated play-specific cost at this level:** ~$100-300/mo. At 500 surveys/month, PostHog survey costs ~$35/mo after free tier. Intercom and Loops costs depend on existing usage. n8n Pro recommended for the execution volume.

## Drills Referenced

- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on survey timing, channel, format, and follow-up effectiveness
- the nps segment scaling workflow (see instructions below) — builds the multi-segment scheduling engine with priority ordering, volume caps, and anti-fatigue guardrails
- `advocacy-activation-pipeline` — converts high-scoring promoters into active advocates through automated enrollment, asks, and reward delivery
