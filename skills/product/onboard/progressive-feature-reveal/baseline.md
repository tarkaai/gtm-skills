---
name: progressive-feature-reveal-baseline
description: >
  Progressive Feature Discovery — Baseline Run. Gate all feature tiers behind
  readiness signals, run always-on unlock automation, and validate ≥45% adoption
  rate with ≥10pp lift over ungated control group across 50%+ of new signups.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "20 hours over 4 weeks"
outcome: "≥45% post-unlock adoption AND ≥10pp lift vs. ungated control"
kpis: ["Post-unlock adoption rate", "Lift vs. control", "Tier transition rate", "Stalled user %"]
slug: "progressive-feature-reveal"
install: "npx gtm-skills add product/onboard/progressive-feature-reveal"
drills:
  - feature-readiness-gating
  - feature-adoption-monitor
  - activation-optimization
---

# Progressive Feature Discovery — Baseline Run

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

≥45% of users who unlock a feature tier actually use at least one feature from that tier within 14 days, AND the gated group shows ≥10 percentage point higher adoption than an ungated control group. This proves progressive reveal is not just functional but genuinely superior to showing everything at once.

## Leading Indicators

- Tier transition rate: ≥60% of active users reach Intermediate within 7 days
- Stalled-at-Core rate below 25% after 14 days
- Unlock message click-through rate ≥40%
- Time-to-first-unlock decreasing week over week

## Instructions

### 1. Extend gating to all feature tiers

Run the full `feature-readiness-gating` drill (all 7 steps). Expand beyond the single Smoke-test feature to gate all Intermediate, Advanced, and Power tier features behind their respective readiness signals. Create PostHog feature flags for each tier: `tier-intermediate-features`, `tier-advanced-features`, `tier-power-features`.

Define readiness criteria for each tier:

| Tier | Unlock Criteria |
|------|----------------|
| Intermediate | Completed 3+ Core actions across 2+ sessions |
| Advanced | Used 2+ Intermediate features, active for 7+ days |
| Power | Used 1+ Advanced feature consistently for 14+ days |

### 2. Build the always-on unlock automation

Complete `feature-readiness-gating` Step 6: build the n8n workflow that listens for PostHog webhook events, evaluates readiness state in real time, updates person properties to trigger cohort-based flags, fires Intercom events for unlock messages, and logs tier transitions to Attio.

This is the first always-on automation for this play. Once deployed, every new user automatically gets the progressive reveal experience without manual intervention.

### 3. Set up A/B test: gated vs. ungated

Split new signups 50/50 using a PostHog feature flag `progressive-reveal-experiment`:
- **Treatment (50%):** Full progressive reveal — features gated behind readiness signals
- **Control (50%):** All features visible from signup (traditional approach)

Track the same events for both groups. The comparison proves whether gating improves adoption or hinders it.

### 4. Deploy the feature adoption monitor

Run the `feature-adoption-monitor` drill to build:
- The adoption funnel (signup → Core → Intermediate unlock → Intermediate use → Advanced unlock → Advanced use)
- Tier transition velocity metrics
- Stalled-user detection (daily n8n workflow)
- Automated nudges for stalled users at each tier

### 5. Optimize the activation bottleneck

Run the `activation-optimization` drill focused on the largest drop-off in the adoption funnel. If users are stalling between signup and first Core action, the onboarding is the problem. If they complete Core actions but do not unlock Intermediate, the readiness criteria may be too strict. If they unlock but do not use, the reveal moment needs work.

Test 2-3 variations at the bottleneck point using PostHog feature flags. Run each variation for at least 7 days with 100+ users per variant.

### 6. Evaluate against threshold

After 4 weeks, query PostHog:

**Primary metric:** Of users in the treatment group who triggered `feature_tier_unlocked`, what percentage triggered `feature_first_used` within 14 days? Must be ≥45%.

**Lift metric:** Compare feature adoption rates between treatment and control. Treatment must show ≥10pp higher adoption of Intermediate+ features.

**Pass:** Both metrics met. Proceed to Scalable.
**Fail on adoption:** Users unlock but do not use — improve reveal moment, feature discoverability, or onboarding at that tier.
**Fail on lift:** Gating does not outperform ungated — readiness criteria may be misaligned with actual user readiness. Re-examine which actions truly predict feature adoption.

## Time Estimate

- 4 hours: extend gating to all tiers (flags, cohorts, unlock messages)
- 4 hours: build n8n unlock automation workflow
- 3 hours: configure A/B test and ensure both variants track correctly
- 4 hours: deploy feature-adoption-monitor (funnel, dashboard, stalled-user detection)
- 3 hours: run activation-optimization at the bottleneck
- 2 hours: weekly monitoring (4 x 30min) and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| [PostHog](https://posthog.com/pricing) | Feature flags, experiments, funnels, cohorts | Free up to 1M events/mo; paid: ~$0.00005/event after 1M |
| [Intercom](https://www.intercom.com/pricing) | Unlock messages, stalled-user nudges, product tours | Essential $29/seat/mo + Proactive Support Plus $99/mo (500 msgs included) |
| [Loops](https://loops.so/pricing) | Stalled-user email nudges | Free up to 1,000 contacts; $49/mo up to 5,000 contacts |
| [n8n](https://n8n.io/pricing) | Unlock automation, stalled-user detection | Standard stack (not counted in play budget) |

**Estimated play-specific cost:** $99-148/mo (Intercom Proactive Support Plus add-on + Loops if beyond free tier)

## Drills Referenced

- `feature-readiness-gating` — full setup: all tiers gated with flags, cohorts, unlock messages, and n8n automation
- `feature-adoption-monitor` — funnel tracking, tier velocity, stalled-user detection and nudges
- `activation-optimization` — identify and fix the biggest drop-off in the adoption funnel
