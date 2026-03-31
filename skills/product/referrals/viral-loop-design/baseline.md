---
name: viral-loop-design-baseline
description: >
  Built-In Virality — Baseline Run. Production-grade viral loop with full PostHog instrumentation,
  automated attribution, and always-on monitoring. First continuous viral acquisition channel.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "Viral coefficient ≥0.5 sustained over 2 weeks with full funnel tracking"
kpis: ["Viral coefficient (K)", "Invites sent per active user", "Invite-to-signup conversion rate", "Referee activation rate"]
slug: "viral-loop-design"
install: "npx gtm-skills add product/referrals/viral-loop-design"
drills:
  - viral-loop-instrumentation
  - referral-program
---

# Built-In Virality — Baseline Run

> **Stage:** Product → Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The Smoke mechanic is polished into a production-grade viral loop with comprehensive PostHog instrumentation, automated referral attribution, and a reward system that reinforces sharing behavior. Viral coefficient sustains at K >= 0.5 over 2 consecutive weeks with always-on tracking.

## Leading Indicators

- Viral funnel conversion rates are stable day-over-day (no large variance)
- Referral attribution is working: every viral signup is linked to a referrer
- Rewards are being fulfilled automatically without manual intervention
- Referee activation rate (viral signups reaching the product's activation metric) is within 80% of organic signup activation rate
- Active referrer count grows week-over-week

## Instructions

### 1. Instrument the full viral funnel

Run the `viral-loop-instrumentation` drill. This sets up:

- Complete PostHog event taxonomy for every stage of the viral loop (trigger, share, landing, signup, activation, loop-close)
- Viral funnel insight with channel and cohort breakdowns
- Four viral cohorts (active referrers, viral signups, loop closers, dormant referrers)
- Viral Metrics Dashboard with K-factor trend, funnel chart, invite volume by channel, time-to-activation comparison, and chain depth distribution
- n8n attribution webhook that links every viral signup to its referrer in Attio
- Weekly automated summary of viral metrics posted to Slack

### 2. Build the reward system

Run the `referral-program` drill. Configure:

- Incentive structure: choose two-sided reward (both referrer and referee benefit), referrer-only reward, or tiered rewards based on your product economics. Keep the incentive explainable in one sentence.
- Reward fulfillment automation: n8n workflow that triggers on `viral_signup_completed` and `viral_referee_activated` events. Deliver rewards via Loops transactional emails. Track reward delivery in Attio.
- Referral prompts at moments of delight: configure Intercom in-app messages triggered after successful workflows, positive NPS responses, usage milestones, and first-month anniversaries.
- Referrer dashboard: surface each user's referral count, pending rewards, and earned rewards inside the product.

### 3. Polish the viral UX

**Human action required:** Based on Smoke test data, fix the weakest funnel step:

- If invite rate is low (users are not sharing): simplify the share mechanic to 1 click. Pre-populate the invite message. Add social proof ("12 teammates already here").
- If click-through is low (non-users ignore the shared artifact): improve the shared artifact preview. Show more product value before requiring signup.
- If signup conversion is low (non-users land but do not sign up): reduce signup friction. Pre-fill fields from the invite. Offer a guest preview before requiring an account.
- If activation is low (viral signups do not activate): personalize the onboarding for referred users. Show them what the referrer created. Connect them to the referrer's workspace immediately.

### 4. Launch to full user base via feature flag

Use PostHog feature flags to roll out the viral mechanic:

- Week 1: 50% of active users see the viral mechanic (treatment), 50% do not (control)
- Track K, invite rate, and conversion rate for treatment vs. control
- Week 2: if treatment K >= 0.5 and no negative impact on core product metrics (retention, NPS), roll out to 100%

### 5. Evaluate against threshold

Measure viral coefficient over the full 2-week period:

```
K = (total invites sent / active user count) * (viral signups / total invite recipients)
```

**Pass threshold:** K >= 0.5 sustained over 2 consecutive weeks.

Also verify:
- Referee activation rate >= 60% of organic activation rate
- Reward fulfillment is automated with <1% failure rate
- No degradation in core product metrics for non-referring users

If K >= 0.5, proceed to Scalable. If K is 0.3-0.5, identify the bottleneck funnel step, fix it, and run another 2-week evaluation.

## Time Estimate

- 4 hours: viral loop instrumentation (drill + PostHog setup + n8n webhooks)
- 4 hours: referral program setup (rewards, prompts, fulfillment automation)
- 3 hours: viral UX polish based on Smoke data
- 2 hours: feature flag rollout and A/B monitoring
- 3 hours: 2-week evaluation, analysis, and threshold check

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags, dashboards | Free tier: 1M events/mo. Paid: usage-based from $0.00005/event. https://posthog.com/pricing |
| n8n | Attribution webhooks, reward fulfillment automation, weekly summaries | Community (self-hosted): free. Cloud Starter: ~$20/mo. https://n8n.io/pricing |
| Loops | Transactional reward emails, referral notification sequences | Free tier: 1,000 contacts. Paid from $49/mo. https://loops.so/pricing |
| Intercom | In-app referral prompts at moments of delight | Essential: $29/seat/mo. Advanced: $85/seat/mo. https://intercom.com/pricing |
| Attio | Referrer/referee CRM records, referral attribution logging | Free tier available. Paid plans from $29/seat/mo. https://attio.com/pricing |

## Drills Referenced

- `viral-loop-instrumentation` — instruments the complete viral funnel in PostHog with cohorts, funnels, dashboard, and attribution webhooks
- `referral-program` — designs and launches the reward system, referrer prompts, and fulfillment automation
