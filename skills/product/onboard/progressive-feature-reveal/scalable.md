---
name: progressive-feature-reveal-scalable
description: >
  Progressive Feature Discovery — Scalable Automation. Personalize reveal paths
  by persona, run systematic A/B tests on gating criteria and reveal UX, and
  maintain ≥40% adoption at 500+ users with automated churn and expansion triggers.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥40% post-unlock adoption sustained at 500+ active users"
kpis: ["Post-unlock adoption rate at scale", "Persona-level adoption rates", "Experiment win rate", "Churn save rate", "Expansion conversion rate"]
slug: "progressive-feature-reveal"
install: "npx gtm-skills add product/onboard/progressive-feature-reveal"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - upgrade-prompt
---

# Progressive Feature Discovery — Scalable Automation

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

≥40% post-unlock adoption sustained across 500+ active users. The progressive reveal system works at scale without manual intervention, with persona-specific paths and systematic experimentation improving the unlock-to-adoption conversion continuously.

## Leading Indicators

- Adoption rate holding steady (±3pp) as user volume increases from 50 to 500+
- At least 2 A/B tests completed per month with 1+ winner implemented
- Stalled-user intervention save rate ≥15%
- Per-persona adoption rates within 5pp of each other (no persona left behind)

## Instructions

### 1. Build persona-specific reveal paths

Using PostHog cohorts and feature flags, create differentiated reveal experiences for 2-3 user personas. Different users have different readiness curves — a technical user may be ready for Advanced features in 3 days while a non-technical user needs 14 days.

Define personas using PostHog person properties (role, company size, signup source, or a self-reported onboarding question). For each persona, configure:

| Persona | Readiness Criteria Adjustment | Reveal UX |
|---------|-------------------------------|-----------|
| Technical power user | Faster criteria: 2 Core actions in 1 session unlocks Intermediate | Minimal reveal — small toast notification, they want to explore |
| Business user | Standard criteria: 3 Core actions in 2+ sessions | Full product tour at each unlock, guiding them to the feature |
| Evaluator (trial) | Accelerated: show all features teased from Day 1, unlock based on engagement | Emphasis on value — "Here's what your team gets on [Plan]" |

Create separate PostHog feature flags per persona: `tier-intermediate-technical`, `tier-intermediate-business`, etc. Use n8n to route users to the correct persona path based on their properties.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test variations of the progressive reveal system. Run tests sequentially (one at a time) with minimum 200 users per variant and 7-day duration. Priority test queue:

1. **Gating criteria strictness**: Current criteria vs. relaxed criteria (e.g., 2 Core actions vs. 3) — does a lower bar reduce quality of adoption?
2. **Reveal moment UX**: Banner notification vs. modal with mini-tour vs. email digest of unlocked features — which drives highest click-through?
3. **Locked state**: Hidden feature vs. teased/grayed-out feature — which drives faster Core completion?
4. **Timing**: Immediate unlock vs. next-session unlock (build anticipation) — which produces higher adoption?

Log every test result in PostHog: hypothesis, variants, sample size, duration, winner, confidence level.

### 3. Roll out to 100% of new signups

After 2+ winning experiments are implemented, remove the 50/50 A/B split from Baseline. All new signups now get the progressive reveal experience (with persona routing). Keep the control holdout at 5% for ongoing measurement.

### 4. Deploy churn prevention at the feature level

Run the `churn-prevention` drill adapted for progressive reveal. Standard churn signals plus reveal-specific signals:

- **Feature regression**: User was actively using Intermediate features, then stopped for 7+ days. They may have hit a wall.
- **Tier stagnation**: User has been at Intermediate for 30+ days with no progress toward Advanced. They may not see value in progressing.
- **Unlock without use**: User unlocked a tier 14+ days ago and has not used any feature from it. The reveal moment failed silently.

Configure tiered interventions:
- Feature regression → Intercom in-app message: "Need help with [feature]? Here are 3 things other teams do with it."
- Tier stagnation → Loops email: showcase an Advanced feature with a concrete use case relevant to their persona.
- Unlock without use → Intercom tooltip on the unlocked feature next time they log in.

### 5. Wire up expansion triggers

Run the `upgrade-prompt` drill integrated with the tier system. Users who reach Power tier are your most engaged — they are ideal expansion candidates. Configure triggers:

- Power-tier user on free plan → upgrade prompt showing what paid features they would use based on their behavior
- Power-tier user on paid plan → upsell to next tier or seats based on team size growth
- Advanced-tier user approaching plan limits → contextual upgrade prompt tied to the limit they are hitting

### 6. Evaluate at scale

After 2 months with 500+ active users in the progressive reveal system:

**Primary:** Post-unlock adoption rate ≥40% across all tiers and personas.
**Secondary:** At least 2 experiment winners implemented. Churn save rate ≥15%. Expansion prompt conversion ≥5%.

**Pass:** Proceed to Durable.
**Fail on adoption:** Check per-persona rates. If one persona drags the average down, fix that persona's path. If all personas declined, the system may not scale — check whether the n8n automation is keeping up with volume.

## Time Estimate

- 8 hours: persona definition, per-persona flag setup, n8n routing
- 12 hours: A/B test setup and monitoring (4 tests x 3 hours each)
- 8 hours: churn prevention configuration (signal definition, intervention setup, effectiveness tracking)
- 6 hours: upgrade-prompt integration with tier system
- 8 hours: 100% rollout, monitoring, and iteration
- 8 hours: weekly reviews (8 x 1 hour) and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| [PostHog](https://posthog.com/pricing) | Feature flags, experiments, funnels, cohorts | Free up to 1M events/mo; ~$50/mo for 1-2M events |
| [Intercom](https://www.intercom.com/pricing) | Unlock messages, stalled-user nudges, churn interventions, product tours | Essential $29/seat/mo + Proactive Support Plus $99/mo; additional message charges ~$50-150/mo at 500+ users |
| [Loops](https://loops.so/pricing) | Stalled-user and churn-prevention emails, expansion nurtures | $49/mo (up to 5,000 contacts) |
| [n8n](https://n8n.io/pricing) | Persona routing, unlock automation, churn detection | Standard stack (not counted) |

**Estimated play-specific cost:** $150-300/mo (Intercom messaging at scale + Loops)

## Drills Referenced

- `ab-test-orchestrator` — systematic testing of gating criteria, reveal UX, locked-state design, and timing
- `churn-prevention` — detect feature regression, tier stagnation, and unlock-without-use signals; trigger interventions
- `upgrade-prompt` — wire expansion triggers to the tier system for Power-tier users
