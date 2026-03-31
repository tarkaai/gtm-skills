---
name: at-risk-intervention-baseline
description: >
  At-Risk User Intervention — Baseline Run. Automate churn risk scoring and tiered
  interventions as an always-on system. First continuous automation with daily scoring
  and triggered outreach across in-app, email, and personal channels.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥40% response rate AND ≥25% save rate sustained over 2 weeks"
kpis: ["Response rate", "Save rate", "Intervention reach", "Time-to-response"]
slug: "at-risk-intervention"
install: "npx gtm-skills add product/winback/at-risk-intervention"
drills:
  - churn-risk-scoring
  - churn-prevention
  - posthog-gtm-events
  - threshold-engine
---

# At-Risk User Intervention — Baseline Run

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

Turn the manual Smoke batch into an always-on system. The agent configures daily churn risk scoring, automated intervention triggers, and continuous tracking. This is the first time interventions fire without human initiation.

Pass threshold: **≥40% response rate AND ≥25% save rate** (users who return to low risk within 14 days of intervention) sustained over 2 consecutive weeks.

## Leading Indicators

- Daily churn risk scoring workflow runs without errors for 7+ consecutive days
- Intervention messages are triggered and delivered automatically within 24 hours of a user entering medium/high/critical risk tier
- Response rate holds above 35% after the first week (trending toward 40%)
- At least some users show reduced risk scores within 7 days of intervention

## Instructions

### 1. Set up intervention event tracking

Run the `posthog-gtm-events` drill to instrument the full intervention lifecycle. Create these PostHog events:

- `churn_risk_scored` — emitted daily per user by the scoring workflow. Properties: `risk_score`, `risk_tier`, `top_signals`, `score_date`
- `intervention_sent` — emitted when an intervention is triggered. Properties: `user_id`, `channel`, `risk_tier`, `risk_score`, `message_variant`
- `intervention_engaged` — emitted when a user responds. Properties: `user_id`, `channel`, `engagement_type` (opened, clicked, replied, action_taken)
- `intervention_saved` — emitted when a user's risk tier improves to low within 14 days. Properties: `user_id`, `original_tier`, `days_to_save`
- `intervention_lost` — emitted when a user churns despite intervention. Properties: `user_id`, `original_tier`, `channel`, `days_to_churn`

Build a PostHog funnel: `intervention_sent` -> `intervention_engaged` -> `intervention_saved`. This is the core conversion funnel for the play.

### 2. Automate daily churn risk scoring

Run the full `churn-risk-scoring` drill. Configure the daily n8n workflow (step 3 of that drill) to:
1. Score all active users at 06:00 UTC daily
2. Sync scores to PostHog as `churn_risk_scored` events
3. Update Attio records with current risk tier
4. Create dynamic PostHog cohorts for each risk tier

Verify the workflow runs successfully for 3 consecutive days before enabling automated interventions.

### 3. Automate tiered interventions

Run the `churn-prevention` drill to build the automated intervention system. Configure n8n workflows that trigger based on PostHog cohort membership:

- **Medium risk users:** Trigger an Intercom in-app message within 4 hours of entering the medium cohort. Use the message template validated in Smoke. Set frequency cap: maximum 1 in-app intervention per user per 14 days.
- **High risk users:** Trigger a Loops transactional email within 2 hours of entering the high cohort. Personalize with the user's specific risk signals (e.g., "We noticed you haven't used [feature] recently"). Include a calendar booking link. Frequency cap: 1 email per user per 14 days.
- **Critical risk users:** Create an Attio task for the account owner with the user's risk data, usage history, and recommended talking points. Trigger within 1 hour. Frequency cap: 1 personal outreach per user per 30 days.

### 4. Monitor and evaluate over 2 weeks

Let the system run for 2 full weeks. Monitor daily:
- Are scoring workflows completing without error?
- Are interventions being sent within the target time window?
- Are users engaging with interventions?

After week 1, check interim metrics. If response rate is below 30%, diagnose:
- Are the right users being scored as at-risk? (Check false positive rate)
- Are messages being delivered? (Check Intercom/Loops delivery stats)
- Is the messaging resonating? (Check open rates and click-through rates separately)

### 5. Evaluate against threshold

Run the `threshold-engine` drill at the end of week 2 and again at the end of week 3:

- **Pass (≥40% response rate AND ≥25% save rate for 2 consecutive weeks):** The automated system works. Proceed to Scalable.
- **Marginal (35-40% response OR 20-25% save):** Stay at Baseline. Adjust message copy, intervention timing, or risk score thresholds. Run 1 more week.
- **Fail (<35% response OR <20% save):** Review the scoring model accuracy (are you targeting the right users?) and the intervention relevance (does the message address the user's actual situation?). Re-run Smoke with revised signals if needed.

## Time Estimate

- 4 hours: Set up PostHog events and funnels
- 6 hours: Configure daily churn risk scoring workflow in n8n
- 6 hours: Build automated intervention triggers (Intercom, Loops, Attio tasks)
- 2 hours: Monitor and debug during first week
- 2 hours: Evaluate metrics and decide pass/fail

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, funnels | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app intervention messages | $29/seat/mo Essential; +$99/mo for Proactive Support (500 messages) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered intervention emails | $49/mo (1,000+ contacts) — [loops.so/pricing](https://loops.so/pricing) |
| n8n | Workflow automation for scoring + triggers | Self-hosted free; Cloud from $24/mo — [n8n.io/pricing](https://n8n.io/pricing) |

**Play-specific cost at Baseline:** ~$75-175/mo (Intercom Proactive Support + Loops paid tier if >1,000 contacts)

## Drills Referenced

- `churn-risk-scoring` — automated daily risk scoring model synced to PostHog and Attio
- `churn-prevention` — tiered intervention system triggered by risk tier changes
- `posthog-gtm-events` — intervention lifecycle event tracking and funnels
- `threshold-engine` — evaluate response and save rates against pass thresholds
