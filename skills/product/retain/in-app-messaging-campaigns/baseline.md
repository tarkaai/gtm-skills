---
name: in-app-messaging-campaigns-baseline
description: >
  Behavioral In-App Messages — Baseline Run. Automate 3-5 behavior-triggered message campaigns
  running always-on across multiple user segments, with PostHog funnel tracking and
  automated Intercom delivery.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥45% CTR across all campaigns, ≥12% message-to-action conversion rate"
kpis: ["Message CTR", "Message-to-action conversion rate", "Dismissal rate", "Delivery rate"]
slug: "in-app-messaging-campaigns"
install: "npx gtm-skills add product/retain/in-app-messaging-campaigns"
drills:
  - feature-announcement
  - activation-optimization
  - feature-adoption-monitor
---

# Behavioral In-App Messages — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

3-5 behavior-triggered in-app message campaigns running always-on, collectively achieving 45% CTR and 12% message-to-action conversion rate over 2 weeks. "Always-on" means messages fire automatically whenever a user matches the trigger criteria — no manual activation needed. This proves that behavioral messaging sustains engagement at scale beyond the initial Smoke test.

## Leading Indicators

- Number of distinct behavioral triggers configured and firing (target: 3-5)
- Per-campaign delivery rate (target: >90% per campaign)
- Per-campaign dismissal rate (target: <30% per campaign, identifies fatiguing messages early)
- Unique users messaged per week (validates reach across user base)
- Time-to-action after message click (shorter means the CTA deep link is well-placed)

## Instructions

### 1. Expand behavioral triggers to cover the retention lifecycle

Run the `activation-optimization` drill to identify the key drop-off points in your product funnel. Each drop-off point is a candidate for a behavioral message. Build campaigns for at least 3 of these scenarios:

**Stall recovery:** User started a core workflow but did not complete it within the session. Trigger: `workflow_started` event followed by no `workflow_completed` event within 30 minutes. Message: tooltip near the next step, copy referencing what they started. CTA: deep link to resume.

**Feature discovery:** User is active on feature A but has never used related feature B. Trigger: 5th use of feature A AND 0 uses of feature B. Message: banner highlighting how B extends what they are already doing with A. CTA: deep link to feature B.

**Usage milestone:** User reaches a significant usage threshold (10th project, 100th record, 50th message sent). Trigger: counter event crosses the milestone. Message: congratulatory banner with a next-level tip. CTA: link to the advanced capability they have earned access to.

**Churn signal response:** User's session frequency drops below 50% of their average. Trigger: PostHog cohort match for declining engagement. Message: "We noticed you haven't been around as much. Here's what's new since your last visit." CTA: link to changelog or most relevant new feature.

**Error recovery:** User encounters a known error or confusion point (visits help docs, hits a 4xx error, abandons a form). Trigger: specific error or help-seeking event. Message: proactive help tooltip. CTA: link to the solution or offer to connect with support.

For each campaign, use the `feature-announcement` drill to create the Intercom message with proper targeting, copy, CTA, and event tracking.

### 2. Configure always-on delivery automation

For each campaign, set up the automation pipeline:

1. PostHog fires the trigger event
2. PostHog webhook or n8n workflow detects the trigger and checks eligibility (user has not seen this message before, user is not in the fatigue cohort, user matches the target segment)
3. Intercom API receives the message delivery request with the user ID and message template
4. PostHog receives the delivery confirmation event

Run the `feature-adoption-monitor` drill to build the tracking layer that monitors whether users who receive messages actually change their behavior. Track the full funnel per campaign: trigger fired, message delivered, message seen, message clicked, target action completed.

### 3. Build per-campaign funnel dashboards

For each campaign, create a PostHog funnel:

```
trigger_event_fired
  -> in_app_msg_delivered
    -> in_app_msg_seen
      -> in_app_msg_clicked
        -> in_app_msg_converted
```

Break down by: user plan, signup cohort week, and device type. Compare campaigns against each other to identify which behavioral triggers produce the highest conversion. The worst-performing campaign is your optimization target for the next iteration.

### 4. Evaluate against threshold

Measure across all campaigns combined over 14 days:
- **CTR (clicked / seen):** Target >=45%
- **Conversion rate (converted / clicked):** Target >=12%

Per-campaign breakdown:
- If any single campaign is below 30% CTR, pause it and review the trigger relevance and copy
- If any campaign has dismissal rate above 40%, reduce its frequency or narrow its audience
- If conversion is high but action completion is low, the product flow after the CTA needs fixing (not a messaging problem)

**Pass:** Proceed to Scalable. **Fail:** Identify the weakest campaign, replace it with a new trigger hypothesis, and re-run for another 2 weeks.

## Time Estimate

- 3 hours: Funnel analysis, trigger identification, cohort definition for each campaign
- 5 hours: 3-5 Intercom message configurations, copy, targeting, CTA deep links
- 3 hours: n8n automation setup for always-on delivery, PostHog webhook configuration
- 2 hours: PostHog funnel dashboards, per-campaign tracking verification
- 3 hours: Monitoring and analysis over 14 days (15 min/day + 1-hour final analysis)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavioral event tracking, cohort creation, funnel dashboards | Free up to 1M events/mo, then ~$0.00005/event — https://posthog.com/pricing |
| Intercom | In-app message delivery, behavioral targeting | Essential $29/seat/mo, Proactive Support add-on $349/mo for >500 messages — https://www.intercom.com/pricing |
| n8n | Webhook-to-Intercom delivery automation | Self-hosted free, Cloud from $24/mo — https://n8n.io/pricing |
| Loops | Fallback email for users who did not see in-app messages | Free up to 1,000 contacts, $49/mo for 5K — https://loops.so/pricing |

**Play-specific cost:** ~$0-50/mo (Intercom and PostHog free tiers cover most early-stage usage; n8n self-hosted is free)

## Drills Referenced

- `feature-announcement` — build each behavior-triggered message campaign in Intercom
- `activation-optimization` — identify drop-off points that become behavioral triggers
- `feature-adoption-monitor` — track whether messaging drives actual feature adoption
