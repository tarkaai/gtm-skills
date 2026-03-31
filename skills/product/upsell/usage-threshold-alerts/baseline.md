---
name: usage-threshold-alerts-baseline
description: >
  Plan Limit Notifications — Baseline Run. Always-on detection and alerting pipeline that
  identifies users approaching plan limits daily, delivers contextual in-app and email alerts
  automatically, and tracks the full alert-to-upgrade funnel.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥40% upgrade rate from alerted users, sustained over 2 weeks"
kpis: ["Upgrade rate from alerted users", "Alert click-through rate", "Median hours from alert to upgrade", "Detection accuracy (true positive rate)"]
slug: "usage-threshold-alerts"
install: "npx gtm-skills add product/upsell/usage-threshold-alerts"
drills:
  - usage-threshold-detection
  - usage-alert-delivery
  - posthog-gtm-events
---

# Plan Limit Notifications — Baseline Run

> **Stage:** Product -> Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The first always-on version. A daily detection pipeline identifies accounts approaching limits, classifies urgency tiers, and triggers automated alerts via in-app messages and email. The system runs continuously for 2 weeks. Results must hold over time — not just a one-shot spike from Smoke.

## Leading Indicators

- Detection pipeline runs daily without errors for 14 consecutive days
- Alerts fire for at least 10 unique accounts per week (sufficient volume)
- In-app alert click-through rate exceeds 30%
- Email alert open rate exceeds 40%
- At least 50% of critical-tier users see an alert within 24 hours of being flagged
- No spike in support tickets or complaints about alert messages

## Instructions

### 1. Deploy the detection pipeline

Run the `usage-threshold-detection` drill in full automated mode:

1. Configure the plan cap mapping (resource limits per tier) as a JSON config in n8n
2. Build the daily detection workflow in n8n that queries PostHog for accounts at 70%+ of any limit
3. Implement the consumption velocity calculation to project when each account will hit the limit
4. Set up the four PostHog cohorts: `usage-approaching`, `usage-imminent`, `usage-critical`, `usage-exceeded`
5. Configure Attio custom attributes for threshold data storage
6. Activate the daily cron schedule (06:00 UTC)

Verify the pipeline works by checking the first daily run output. Confirm:
- The query returns results matching your manual Smoke test analysis
- Urgency tier classification is correct for 5+ known accounts
- Velocity projections are reasonable (not projecting limit hits in 0 days for accounts growing slowly)

### 2. Deploy the alert delivery system

Run the `usage-alert-delivery` drill in full automated mode:

1. Create the three Intercom in-app message templates: imminent, critical, exceeded
2. Create the two Loops email templates: imminent and critical
3. Create the 2-email follow-up sequence in Loops for non-upgraders
4. Build the n8n routing workflow that receives detection webhooks and dispatches to the right channel
5. Configure routing rules based on MRR thresholds and urgency tiers
6. Set up the 7-day per-resource cooldown to prevent alert fatigue

**Human action required:** Review all alert copy before activating. Ensure upgrade links point to the correct pricing page. Ensure the exceeded-tier blocking modal has a fallback path (users should never be completely stuck). Test each template with a staging account.

### 3. Configure event tracking

Run the `posthog-gtm-events` drill to set up detailed tracking for the alert system. Ensure these events fire:

- `usage_threshold_detected` — when detection flags an account
- `usage_alert_shown` — when an in-app message or email is delivered
- `usage_alert_clicked` — when a user interacts with the alert
- `usage_alert_converted` — when a user completes an upgrade after being alerted

Build a PostHog funnel: `detected -> shown -> clicked -> converted`. Break down by resource type, urgency tier, and channel. This funnel is the core measurement for the play.

### 4. Run a feature-flag controlled rollout

Do not launch to 100% of users immediately. Using PostHog feature flags, launch the alert system to 50% of accounts. The other 50% is a control group that does not receive usage threshold alerts (they still see whatever upgrade prompts you had before).

After 2 weeks, compare:
- Upgrade rate: alerted group vs. control group
- Time to upgrade: alerted group vs. control group
- Support ticket volume: alerted group vs. control group (ensure alerts are not generating confusion)
- Revenue impact: total MRR increase attributable to the alert system

### 5. Monitor system health daily

For the first week, check daily:
- Did the detection pipeline run? (Check n8n execution logs)
- How many accounts were flagged? (Check PostHog cohort sizes)
- How many alerts were delivered? (Check Intercom and Loops delivery reports)
- Any delivery failures? (Check n8n error logs)
- Any user complaints? (Check Intercom conversations and support tickets)

Fix any issues immediately. A broken detection pipeline means users hit limits without warning — the opposite of the play's goal.

### 6. Evaluate against threshold

After 2 weeks, measure against the pass threshold: at least 40% of users who received a usage threshold alert upgraded within 14 days.

Also evaluate:
- Is the control group's upgrade rate significantly lower? (The alert system should outperform no-alerts by at least 2x)
- Which urgency tier converts best? (Critical should convert highest — if not, the urgency messaging needs work)
- Which channel converts best? (In-app should outperform email for active users)
- Are alert-driven upgrades retaining? (Check if any upgraded users downgraded within the 2-week window)

If PASS, proceed to Scalable. If FAIL, diagnose the funnel drop-off: detection working but alerts not shown (delivery bug), alerts shown but not clicked (copy problem), clicked but not converted (upgrade flow friction). Fix the weakest link and re-run.

## Time Estimate

- 4 hours: deploy detection pipeline (n8n workflow, PostHog queries, Attio config)
- 4 hours: deploy alert delivery (Intercom templates, Loops emails, n8n routing)
- 2 hours: configure event tracking and build PostHog funnel
- 2 hours: set up feature flag rollout and control group
- 2 hours: daily monitoring over 2 weeks (15 min/day)
- 2 hours: evaluation, analysis, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage detection, cohorts, funnels, feature flags | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app alert messages (imminent, critical, exceeded) | Essential $29/seat/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email alerts and follow-up sequences | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Detection scheduling, alert routing, webhook handling | Free self-hosted; Cloud from EUR 24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Estimated play-specific cost: $50-100/mo** (Loops emails + Intercom messages; PostHog and n8n likely already in stack)

## Drills Referenced

- `usage-threshold-detection` — daily pipeline that identifies accounts approaching limits, classifies urgency tiers, and stores data in Attio
- `usage-alert-delivery` — routes detection output to contextual in-app and email alerts based on urgency tier and account value
- `posthog-gtm-events` — configures the event tracking and funnel that measures the alert-to-upgrade conversion path
