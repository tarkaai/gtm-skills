---
name: in-app-messaging-campaigns-scalable
description: >
  Behavioral In-App Messages — Scalable Automation. Scale to 10+ campaigns with segment-specific
  targeting, A/B test message copy and timing, automate churn interventions, and expand
  to upgrade prompts — all maintaining ≥40% CTR at 500+ users.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "40 hours over 6 weeks"
outcome: "≥40% CTR sustained across 500+ unique users messaged per week"
kpis: ["Message CTR", "Message-to-action conversion rate", "Dismissal rate", "Users messaged per week", "Experiment win rate"]
slug: "in-app-messaging-campaigns"
install: "npx gtm-skills add product/retain/in-app-messaging-campaigns"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---

# Behavioral In-App Messages — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

10+ behavior-triggered in-app message campaigns running always-on across multiple segments, maintaining 40% CTR while reaching 500+ unique users per week. The 10x multiplier at this level comes from three sources: (1) segment-specific message variants so the same trigger serves different copy to different user types, (2) systematic A/B testing that compounds improvements, and (3) expanding into churn prevention and upgrade prompts — messaging that directly drives revenue, not just engagement.

## Leading Indicators

- Number of active campaigns (target: 10+)
- Unique users messaged per week (target: 500+)
- A/B test velocity (target: 2+ experiments running concurrently across different campaigns)
- Experiment win rate (target: 30%+ of tests produce a statistically significant winner)
- Churn intervention save rate (target: 15%+ of at-risk users re-engage after messaging)
- Upgrade prompt conversion (target: 5%+ of prompted users begin the upgrade flow)

## Instructions

### 1. Scale campaigns with segment-specific variants

Take the 3-5 campaigns from Baseline and create segment-specific variants for each. A "stall recovery" message should say different things to:

- **New users (< 14 days):** Emphasize the getting-started path, link to onboarding resources
- **Active users (14-90 days):** Reference their specific usage pattern, link to the next logical feature
- **Power users (90+ days):** Acknowledge their expertise, link to advanced capabilities or beta features
- **Team admins:** Focus on team-level outcomes, link to admin dashboards or team features

For each base campaign, create 2-3 segment variants in Intercom. Use PostHog cohorts to segment users and sync segment membership to Intercom user properties. Each variant gets its own `message_variant` property in PostHog events so performance is tracked independently.

Additionally, create new campaigns for scenarios not covered at Baseline:

- **Re-engagement after absence:** User returns after 7+ days of inactivity. Welcome-back message highlighting what changed while they were away.
- **Collaboration triggers:** User is the only active member on a team account. Prompt to invite teammates.
- **Integration discovery:** User has not connected any integrations after 14+ days. Show the integration that is most relevant to their usage pattern.
- **Feedback moments:** User just completed a significant workflow successfully. Ask for a micro-survey (1 question) about the experience.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test message variables across campaigns. Test one variable at a time per campaign:

**Copy tests:** For each campaign, create 2 message variants:
- Variant A: Benefit-led copy ("Save 2 hours this week with...")
- Variant B: Curiosity-led copy ("Did you know you can...")
Use PostHog feature flags to randomly assign users to variants. Run each test for 7 days or until 200+ impressions per variant, whichever is longer.

**Timing tests:** For trigger-based messages, test delivery delay:
- Variant A: Immediate (within 3 seconds of trigger)
- Variant B: Delayed (next session after trigger, delivered on login)
Some actions benefit from immediate context; others benefit from a fresh session.

**Format tests:** Test message format per campaign:
- Variant A: Banner (persistent, non-blocking)
- Variant B: Tooltip pointing at the relevant UI element
- Variant C: Slideout panel with more detail
Track both CTR and dismissal rate — a format that gets higher CTR but also higher dismissal may be net negative.

**Frequency tests:** Test how often recurring messages show:
- Variant A: Show once per user per trigger type (conservative)
- Variant B: Show up to 3 times with 7-day cooldown between (persistent)
Monitor dismissal rate closely on the persistent variant.

Document every test result. After 6 weeks, implement all winning variants as the new defaults.

### 3. Build churn prevention messaging

Run the `churn-prevention` drill to configure automated in-app interventions for at-risk users:

1. Define churn signal thresholds in PostHog: 50%+ drop in weekly session count, 14+ days since last core action, billing/cancellation page visits
2. Create a PostHog cohort for each risk level (low, medium, high)
3. Build Intercom in-app messages for each risk tier:
   - **Low risk:** Subtle banner: "Here's what's new this week" with a link to the most relevant recent feature. Non-intrusive, maintains presence.
   - **Medium risk:** Tooltip on their most-used feature: "We've improved [feature] — check out what's changed." Re-engage through their existing habits.
   - **High risk:** Slideout panel: "We want to make sure you're getting value. Here are 3 things other [role] users love." Include a link to book a support call.
4. Track save rate: what percentage of at-risk users who received the intervention returned to healthy usage within 14 days

### 4. Set up expansion messaging

Run the `upgrade-prompt` drill to configure upgrade and expansion triggers as in-app messages:

1. **Limit proximity:** User at 80%+ of a plan limit. Message: "You've used X of Y [resource]. Upgrade to [plan] for unlimited." Show as a banner near the limit indicator in the UI.
2. **Feature gate:** User attempts to access a premium feature. Message: "This is available on [plan]. Here's what you'll get." Show immediately at the gate point.
3. **Power user threshold:** User's usage volume is in the top 20% of their plan tier. Message: "You're getting serious value — [plan] would give you [specific benefit]." Show once per month.

Track the upgrade funnel: prompt shown, prompt clicked, upgrade page visited, upgrade started, upgrade completed. Calculate revenue attributable to in-app prompts.

### 5. Evaluate against threshold

Measure across all campaigns over the final 2 weeks of the 6-week period:

- **CTR (clicked / seen) across all campaigns:** Target >=40%
- **Unique users messaged per week:** Target >=500

Per-campaign audit:
- Pause campaigns with CTR below 25% — they are dragging down the average
- Campaigns with dismissal rate above 40% get frequency reduced or audience narrowed
- Churn intervention campaigns are measured on save rate, not CTR (a low-CTR churn message that still retains users via awareness is valid)
- Upgrade prompt campaigns are measured on revenue impact, not CTR alone

**Pass:** Proceed to Durable. **Fail:** Focus testing on the 3 lowest-performing campaigns. If the portfolio cannot sustain 40% CTR at 500+ users after 2 more weeks of optimization, revisit the trigger event taxonomy — the behavioral signals may not be strong enough.

## Time Estimate

- 8 hours: Segment variant creation, new campaign setup, Intercom configuration
- 8 hours: A/B test design, PostHog feature flag setup, experiment launch
- 8 hours: Churn prevention system (signal definition, cohort creation, message setup)
- 6 hours: Upgrade prompt system (limit detection, gate messaging, revenue tracking)
- 6 hours: Dashboard expansion, experiment monitoring, threshold evaluation
- 4 hours: Final analysis, winning variant implementation, portfolio audit

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavioral events, cohorts, feature flags, experiments, funnels | Free up to 1M events/mo, ~$0.00005/event beyond — https://posthog.com/pricing |
| Intercom | In-app message delivery, segment targeting, message variants | Advanced $85/seat/mo, Proactive Support $349/mo + usage — https://www.intercom.com/pricing |
| n8n | Automation for cohort syncing, trigger routing, experiment scheduling | Self-hosted free, Cloud from $24/mo — https://n8n.io/pricing |
| Loops | Fallback email campaigns for users who missed in-app messages | Free up to 1,000 contacts, $49/mo for 5K contacts — https://loops.so/pricing |

**Play-specific cost:** ~$100-400/mo (Intercom Proactive Support add-on is the primary incremental cost at scale)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and analyze A/B tests on message copy, timing, format, and frequency
- `churn-prevention` — detect at-risk users and trigger retention-focused in-app interventions
- `upgrade-prompt` — identify upgrade-ready users and deliver contextual expansion prompts
