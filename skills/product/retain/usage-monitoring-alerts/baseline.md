---
name: usage-monitoring-alerts-baseline
description: >
  Usage Drop Alerting — Baseline Run. Deploy always-on daily engagement drop detection
  with automated alert routing to email and in-app channels. First continuous
  monitoring system.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "20 hours over 3 weeks"
outcome: "≥40% re-engagement rate from automated interventions over 3 consecutive weeks"
kpis: ["Daily detection run success rate", "Alert-to-intervention latency (hours)", "Re-engagement rate within 14 days", "False positive rate"]
slug: "usage-monitoring-alerts"
install: "npx gtm-skills add product/retain/usage-monitoring-alerts"
drills:
  - usage-drop-detection
  - engagement-alert-routing
  - posthog-gtm-events
  - threshold-engine
---

# Usage Drop Alerting — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Deploy always-on automated detection and intervention. The n8n workflow runs daily, flags engagement drops, classifies risk tiers, and routes alerts to the right channel — all without human involvement for standard cases. Only high-value critical accounts get routed to humans.

## Leading Indicators

- n8n detection workflow runs successfully every day for 3+ weeks without errors
- Flagged accounts receive automated interventions within 4 hours of detection
- False positive rate stays below 30% (fewer than 30% of flagged accounts are false alarms)
- At least some accounts respond to automated emails or engage after in-app messages

## Instructions

### 1. Set up the event taxonomy

Run the `posthog-gtm-events` drill to establish tracking for the alert system. Define and implement these events:

```
usage_drop_detected      — fired when the detection query flags an account
usage_drop_tier_assigned — fired when risk tier is classified (watch/alert/critical)
engagement_intervention_sent     — fired when email or in-app message is dispatched
engagement_intervention_opened   — fired when the intervention email is opened
engagement_intervention_clicked  — fired when the user clicks through from intervention
engagement_intervention_converted — fired when the user returns to active usage
```

Attach properties to each event: `person_id`, `risk_tier`, `pct_change`, `intervention_type`, `template_id`.

### 2. Deploy automated drop detection

Run the full `usage-drop-detection` drill including the n8n automation (Steps 4 and 5). Set up:

- Daily 08:00 UTC cron job in n8n that executes the detection HogQL queries
- Automatic risk tier classification (watch at -30%, alert at -50%, critical at -80%)
- Attio record updates with engagement risk data
- Three PostHog dynamic cohorts: `usage-drop-watch`, `usage-drop-alert`, `usage-drop-critical`
- Webhook trigger to fire the engagement-alert-routing drill for alert and critical accounts

### 3. Deploy automated intervention routing

Run the `engagement-alert-routing` drill to build the full routing system:

- Create the three Loops email templates (gentle, urgent, personal)
- Create the Intercom in-app message templates (alert banner, critical prompt)
- Build the n8n routing workflow that matches intervention to risk tier and MRR
- Configure the 7-day intervention cooldown per account
- Set up the Attio task creation for high-MRR critical accounts

**Human action required:** Review and approve the email templates and in-app message copy before going live. Ensure the Attio task routing assigns to the correct account owners.

### 4. Run for 3 weeks and measure

Let the system run autonomously for 3 weeks. During this period:

- Monitor the n8n workflow execution log daily for the first week, then weekly after that
- Check that detection → routing → intervention happens within 4 hours
- Review the "Engagement Drops — Needs Human" Attio list daily and ensure human outreach happens within 48 hours for high-value accounts
- Track false positives: when a flagged account turns out to be on vacation, seasonal, or otherwise not at real risk, log it

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: **≥40% re-engagement rate from automated interventions over 3 consecutive weeks.**

Re-engagement = the flagged account returns to at least 50% of their baseline weekly activity within 14 days of intervention.

If PASS: The automated system works. Move to Scalable.

If FAIL: Diagnose by intervention type:
- If email re-engagement is low: test different subject lines, send times, or personalization depth
- If in-app re-engagement is low: test different message placement, copy, or CTAs
- If false positive rate is high: tighten the drop thresholds or add exclusion rules
- If detection is working but interventions are not converting: the problem is messaging, not detection

## Time Estimate

- 4 hours: Set up PostHog event taxonomy and verify tracking
- 6 hours: Deploy n8n detection workflow with risk tier classification
- 6 hours: Build Loops templates, Intercom messages, and routing workflow
- 4 hours: Monitor, diagnose issues, and evaluate over 3 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Engagement queries, cohorts, event tracking | Free up to 1M events/mo; https://posthog.com/pricing |
| n8n | Daily cron detection + routing workflows | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Loops | Re-engagement email templates and sequences | Free up to 1,000 contacts; https://loops.so/pricing |
| Intercom | In-app messages for flagged users | Starter from $39/mo; https://www.intercom.com/pricing |
| Attio | Account risk tracking, human routing tasks | Free for small teams; https://attio.com/pricing |

## Drills Referenced

- `usage-drop-detection` — Full automated deployment: daily detection cron, risk tiers, Attio enrichment
- `engagement-alert-routing` — Route alerts to email, in-app, or human based on risk and MRR
- `posthog-gtm-events` — Establish event taxonomy for the alert system
- `threshold-engine` — Evaluate re-engagement rate against pass threshold
