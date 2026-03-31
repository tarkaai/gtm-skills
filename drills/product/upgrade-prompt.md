---
name: upgrade-prompt
description: Detect usage thresholds that signal upgrade readiness and trigger contextual upsell prompts
category: Product
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-custom-events
  - posthog-cohorts
  - intercom-in-app-messages
  - loops-transactional
  - attio-deals
---

# Upgrade Prompt

This drill builds a system that identifies users approaching plan limits or demonstrating power-user behavior, then delivers contextual upgrade prompts that feel helpful rather than pushy.

## Prerequisites

- PostHog tracking usage metrics per user and per account
- Clear plan differentiation (what features or limits differ between tiers)
- Intercom configured for in-app messaging
- Loops configured for triggered emails

## Steps

### 1. Define upgrade triggers

Using the `posthog-custom-events` fundamental, identify the usage patterns that correlate with upgrade readiness:

- **Limit proximity**: User is at 80%+ of a plan limit (seats, storage, API calls, projects)
- **Feature discovery**: User tried a premium feature during a trial or repeatedly hit a feature gate
- **Growth signals**: Added 3+ team members in a month, usage volume doubled
- **Power user behavior**: Using advanced features, API access, or integrations that indicate sophistication
- **Time-based**: On free plan for 30+ days with consistent active usage

Each trigger should be validated against historical data: do users who hit this trigger actually upgrade at a higher rate?

### 2. Build the trigger detection

Using `posthog-cohorts`, create cohorts for each upgrade trigger. Set up a daily check (via n8n or PostHog actions) that identifies users entering these cohorts. Score urgency: limit proximity is urgent (they will hit the wall soon), while growth signals are opportunity-based (upgrade would help them do more).

### 3. Design contextual prompts

The upgrade message should be tied to the trigger, not generic. Using `intercom-in-app-messages`:

- **Limit proximity**: "You've used 45 of 50 projects. Upgrade to Pro for unlimited projects." Show when they are in the product, near the limit.
- **Feature gate**: "This feature is available on the Pro plan. Here's what you'll get." Show immediately when they hit the gate.
- **Growth signal**: "Your team is growing — Pro includes advanced permissions and team analytics." Show in a banner, not a blocking modal.

Always include: what they get, the price difference, and a one-click upgrade path.

### 4. Set up email nudges

Using `loops-transactional`, send upgrade emails for non-urgent triggers. Time them 24-48 hours after the trigger event (not immediately — give users time to experience the need). Include a personalized usage summary: "You've created 47 projects this month and invited 5 teammates — sounds like your team is getting value."

### 5. Route high-value accounts to sales

For accounts above a revenue threshold or with enterprise signals (large team, heavy API usage), do not self-serve the upgrade. Using `attio-deals`, create an expansion deal in Attio and assign it to the account owner. Include the usage data and trigger reason so sales can have an informed conversation.

### 6. Measure upgrade funnel

Track the full funnel: trigger fired, prompt shown, prompt clicked, upgrade started, upgrade completed. Calculate conversion rate by trigger type. A/B test prompt copy and placement. Aim for in-app upgrade prompts to convert at 5-10% for limit-proximity triggers.
