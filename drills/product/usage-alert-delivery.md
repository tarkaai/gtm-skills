---
name: usage-alert-delivery
description: Deliver contextual usage threshold alerts via in-app messages and email, routing high-value accounts to sales for expansion conversations
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

# Usage Alert Delivery

This drill takes the output from `usage-threshold-detection` and delivers contextual alerts that feel helpful rather than pushy. The alert message is tied to the specific resource the user is consuming, their current usage numbers, and a one-click path to resolve the situation (upgrade, optimize, or contact sales).

## Input

- Webhook payload from `usage-threshold-detection` containing: account_id, resource_type, urgency_tier, pct_consumed, plan_limit, current_count, plan_tier, projected_hit_date
- Attio account data (plan, MRR, account owner, lifecycle stage)
- Intercom configured for in-app messaging
- Loops configured for triggered emails

## Steps

### 1. Enrich the alert with account context

When the n8n webhook receives a threshold alert, pull account context from Attio using the `attio-deals` fundamental:

- Account plan tier and MRR
- Account owner (who on the team is responsible)
- Days since signup
- Previous alert history (have we already alerted this account about this resource?)
- Total team size and active user count

This context determines routing. A self-serve account gets automated alerts. A $5,000/mo enterprise account gets a personal expansion conversation.

### 2. Define the routing rules

Build routing logic in n8n using `n8n-workflow-basics`:

**Imminent tier (85-94% consumed):**
- If MRR < $200 → In-app message via Intercom showing usage + upgrade path
- If MRR $200-$2000 → In-app message + follow-up email via Loops (24h delay)
- If MRR > $2000 → In-app message + create Attio expansion deal for account owner

**Critical tier (95-100% consumed):**
- If MRR < $200 → In-app banner (persistent until dismissed or upgraded) + immediate email
- If MRR $200-$2000 → In-app banner + email + Attio task for account owner
- If MRR > $2000 → In-app banner + Attio urgent task + Slack alert to account owner + personal email draft

**Exceeded tier (>100% consumed, soft limits):**
- All accounts: In-app blocking modal explaining the limit + upgrade CTA + fallback "contact us" link
- If MRR > $500: Also create an urgent Attio task and Slack-alert the account owner

**Repeat alerts (same resource alerted 2+ times in 30 days without upgrade):**
- Escalate one routing level. If already at max escalation, flag for strategic review — this account may need a different plan structure or a concession.

### 3. Build contextual in-app messages

Using the `intercom-in-app-messages` fundamental, create resource-specific alert templates. Each template includes the actual numbers, not generic copy.

**Template: usage-alert-imminent**
Placement: Banner at top of product when user is in relevant area.
Content: "You've used {{current_count}} of {{plan_limit}} {{resource_name}}. Upgrade to {{next_tier}} for {{next_tier_limit}}."
CTA: "See upgrade options" (links to pricing page with current plan pre-selected).
Dismiss: Once per session. Re-shows on next login if still in imminent tier.

**Template: usage-alert-critical**
Placement: Modal overlay when user attempts to consume more of the limited resource.
Content: "You're at {{pct_consumed}}% of your {{resource_name}} limit. You'll hit your cap {{projected_hit_text}}. Upgrade now to avoid interruption."
CTA primary: "Upgrade to {{next_tier}}" (one-click upgrade if billing is self-serve).
CTA secondary: "Talk to us" (opens Intercom conversation).
Dismiss: Cannot dismiss without choosing an action. Shows once per day.

**Template: usage-alert-exceeded**
Placement: Blocking modal when user tries to use the exceeded resource.
Content: "You've reached your {{resource_name}} limit on the {{plan_tier}} plan. Upgrade to continue."
CTA primary: "Upgrade now"
CTA secondary: "Contact sales"
Behavior: Blocks the specific action that requires the exceeded resource. Other product areas remain accessible.

### 4. Build email alert sequences

Using `loops-transactional`, create triggered emails for each tier:

**Email: usage-threshold-imminent**
Subject: "Heads up: you're using {{pct_consumed}}% of your {{resource_name}}"
Body: Friendly tone. Show a visual usage bar. Explain what happens when they hit the limit. Highlight what the next tier includes (not just limits — value). Include a one-click upgrade link. Include a "Not ready to upgrade? Here are tips to optimize your usage" section for goodwill.

**Email: usage-threshold-critical**
Subject: "{{resource_name}} limit: {{days_until_limit}} days remaining at current pace"
Body: Urgency without panic. Show projected hit date. Explain exactly what will happen (degraded service, blocking, etc.). Include immediate upgrade link. For high-value accounts, include a calendly link to discuss custom plans.

Using `loops-sequences`, create a 2-email follow-up for accounts that receive the imminent email but do not upgrade:
- Day 0: Imminent email (above)
- Day 3: "Still growing? Here's what {{next_tier}} users get" — social proof email with usage stats from similar companies on the next tier

### 5. Route high-value accounts to sales

For accounts above the MRR threshold or showing enterprise signals (large team, API-heavy usage, multiple resources near limits), do not rely on self-serve upgrade.

Using `attio-deals`, create an expansion deal with:
- Deal title: "Usage expansion — {{account_name}} — {{resource_type}}"
- Deal value: estimated ARR increase if they upgrade
- Context notes: current usage per resource, projected hit dates, usage velocity, team size
- Assigned to: account owner

Using `attio-lists`, add to the "Expansion Pipeline — Usage Triggered" list so the team can review all usage-triggered expansion opportunities in one view.

### 6. Track alert delivery and engagement

Using `posthog-custom-events`, track the full lifecycle:

```javascript
// Alert delivered
posthog.capture('usage_alert_shown', {
  account_id: accountId,
  resource_type: 'api_calls',
  urgency_tier: 'imminent',
  channel: 'in_app',  // in_app | email | human
  template_id: 'usage-alert-imminent'
});

// User engaged with alert
posthog.capture('usage_alert_clicked', {
  account_id: accountId,
  resource_type: 'api_calls',
  action: 'view_upgrade',  // view_upgrade | dismiss | contact_sales | optimize_tips
  channel: 'in_app'
});

// User upgraded after alert
posthog.capture('usage_alert_converted', {
  account_id: accountId,
  resource_type: 'api_calls',
  previous_tier: 'starter',
  new_tier: 'pro',
  days_from_alert: 2,
  channel: 'in_app'
});
```

Calculate weekly: alerts delivered by tier and channel, click-through rate, upgrade conversion rate by trigger resource, median time from alert to upgrade, revenue uplift from alert-driven upgrades. Feed this data back to optimize alert copy and timing.

## Output

- n8n routing workflow that processes threshold alerts and dispatches to the right channel
- Three Intercom in-app message templates (imminent, critical, exceeded)
- Two Loops email templates and a 2-email follow-up sequence
- Attio expansion deal creation for high-value accounts
- Alert delivery and conversion tracking in PostHog

## Triggers

Fires automatically when `usage-threshold-detection` sends a webhook. Runs for each individual account-resource pair flagged. Respects a 7-day cooldown per resource per account — do not re-alert about the same resource within 7 days unless the urgency tier escalated.
