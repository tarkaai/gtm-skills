---
name: engagement-alert-routing
description: Route engagement drop alerts to the right intervention channel based on risk tier, account value, and drop pattern
category: Product
tools:
  - n8n
  - Intercom
  - Loops
  - Attio
  - PostHog
fundamentals:
  - n8n-workflow-basics
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
  - loops-sequences
  - attio-deals
  - attio-lists
  - posthog-custom-events
---

# Engagement Alert Routing

This drill takes the output from `usage-drop-detection` and routes each flagged account to the appropriate intervention: automated in-app nudge, re-engagement email, or human outreach. The routing logic matches intervention intensity to risk severity and account value.

## Input

- Webhook payload from `usage-drop-detection` containing: person_id, risk_tier, pct_change, baseline_weekly, current_weekly, engagement_alert_count
- Attio account data (plan, MRR, account owner, lifecycle stage)
- Intercom configured for in-app messaging
- Loops configured for triggered emails

## Steps

### 1. Enrich the alert with account context

When the n8n webhook receives a drop alert, pull account context from Attio using the `attio-deals` fundamental:

- Account plan tier (free, starter, pro, enterprise)
- Monthly recurring revenue (MRR)
- Account owner (who on the team is responsible)
- Days since signup
- Previous intervention history (have we already reached out?)

This context determines routing. A $50/mo free-tier account gets an automated email. A $5,000/mo enterprise account gets immediate human outreach.

### 2. Define the routing rules

Build routing logic in n8n using `n8n-workflow-basics`:

**Alert tier (pct_change -50% to -80%):**
- If MRR < $100 → Send automated re-engagement email via Loops
- If MRR $100-$1000 → Send in-app message via Intercom + email via Loops
- If MRR > $1000 → Create Attio task for account owner + in-app message + email

**Critical tier (pct_change below -80% or zero activity):**
- If MRR < $100 → Send urgent re-engagement email via Loops + in-app message
- If MRR $100-$1000 → Create Attio task for account owner + email + in-app message
- If MRR > $1000 → Create urgent Attio task + Slack alert to account owner + personal email draft

**Repeat alerts (engagement_alert_count > 2):**
- Escalate one level regardless of MRR. If already at max escalation, flag for strategic review.

### 3. Build automated email interventions

Using the `loops-transactional` fundamental, create three email templates:

**Template: usage-drop-gentle (for Alert tier, low MRR)**
Subject: "Need a hand with {{productName}}?"
Body: Acknowledge they have been less active. Highlight a specific feature relevant to their past usage patterns. Include a direct link to resume their last workflow. Add a help link and a calendar booking link.

**Template: usage-drop-urgent (for Critical tier)**
Subject: "We miss you — here's what's new in {{productName}}"
Body: Share 2-3 product updates since their last active period. Include a one-click link to their dashboard. Offer a personal call with their account contact.

**Template: usage-drop-personal (for high-MRR accounts)**
Subject: "Quick check-in from {{accountOwnerName}}"
Body: Written as a personal note from their account owner. Reference their specific use case. Ask a direct question about whether something is blocking them. Include a calendar link.

Using `loops-sequences`, create a 3-email re-engagement sequence for accounts that do not respond to the first email: Day 0 (template above), Day 3 (value reminder with case study), Day 7 (final reach-out with a direct ask).

### 4. Build in-app message interventions

Using the `intercom-in-app-messages` fundamental, create targeted messages:

**For Alert tier accounts:** A subtle banner when they next log in: "Welcome back! Pick up where you left off →" with a deep link to their last active area of the product. Display once, dismiss on click.

**For Critical tier accounts:** A more prominent message: "We noticed you haven't been around lately. Can we help?" with two CTAs: "Show me what's new" and "Talk to support." Display on every login until engaged.

**For recovered accounts (came back after alert):** A positive reinforcement message: "Great to see you back! Here's a tip to get even more from {{productName}}." This rewards re-engagement behavior.

### 5. Build human routing for high-value accounts

Using `attio-lists`, maintain an "Engagement Alerts — Needs Human" list. When routing rules determine human outreach is needed:

1. Add the account to this list with context: drop percentage, last active date, previous usage patterns, intervention history
2. Create an Attio task assigned to the account owner with a 24-hour deadline
3. Include a pre-drafted email the account owner can personalize and send
4. If the account owner does not act within 48 hours, escalate to their manager

### 6. Track intervention outcomes

Using `posthog-custom-events`, track the full lifecycle:

```javascript
// When intervention is sent
posthog.capture('engagement_intervention_sent', {
  person_id: accountId,
  risk_tier: 'alert',
  intervention_type: 'email',  // email | in_app | human
  template_id: 'usage-drop-gentle'
});

// When user re-engages after intervention
posthog.capture('engagement_intervention_converted', {
  person_id: accountId,
  intervention_type: 'email',
  days_to_reengage: 3
});

// When user churns despite intervention
posthog.capture('engagement_intervention_failed', {
  person_id: accountId,
  intervention_type: 'email',
  days_to_churn: 21
});
```

Calculate weekly: total alerts routed, interventions sent by type, re-engagement rate by intervention type, save rate (prevented churns / total interventions). Feed this data back to optimize routing rules — if emails outperform in-app messages for a segment, shift routing toward email.

## Output

- n8n routing workflow that processes drop alerts and dispatches to the right channel
- Three Loops email templates and a 3-email re-engagement sequence
- Two Intercom in-app message templates (alert and critical)
- Attio task creation for high-value human outreach
- Intervention outcome tracking in PostHog

## Triggers

Fires automatically when `usage-drop-detection` sends a webhook. Runs for each individual account flagged. Respects a 7-day cooldown per account (do not send a second intervention within 7 days of the first unless the account moves from alert to critical).
