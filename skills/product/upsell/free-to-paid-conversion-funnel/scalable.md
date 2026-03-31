---
name: free-to-paid-conversion-funnel-scalable
description: >
  Free to Paid Funnel — Scalable Automation. Deploy multiple upgrade surfaces across
  segments, run systematic A/B tests on prompts and pricing, build churn prevention
  for at-risk free users, and maintain ≥8% conversion at 500+ free users.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥8% free-to-paid conversion rate sustained across 500+ free users"
kpis: ["Free-to-paid conversion rate", "Time from signup to upgrade", "Upgrade surface CTR by segment", "Checkout completion rate", "MRR from free-to-paid conversions"]
slug: "free-to-paid-conversion-funnel"
install: "npx gtm-skills add product/upsell/free-to-paid-conversion-funnel"
drills:
  - ab-test-orchestrator
  - upgrade-prompt
  - churn-prevention
---

# Free to Paid Funnel — Scalable Automation

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes
Multiple upgrade surfaces deployed across user segments and product surfaces. Systematic A/B testing finds the highest-converting prompt copy, placement, and timing for each segment. Churn prevention catches at-risk free users before they disengage. Conversion rate holds at ≥8% across a pool of 500+ active free users.

## Leading Indicators
- 3+ upgrade surface types live simultaneously (feature gate, limit alert, time-based, in-app modal)
- At least 2 A/B tests completed with statistically significant results
- Churn prevention save rate (re-engaged / at-risk) is ≥20%
- Prompt fatigue rate stays below 15% of active free users
- MRR from free-to-paid conversions grows month-over-month

## Instructions

### 1. Deploy multi-trigger upgrade prompts
Run the `upgrade-prompt` drill to build a system that detects multiple upgrade triggers and delivers contextual prompts matched to each trigger:

| Trigger | Detection | Prompt |
|---------|-----------|--------|
| **Limit proximity** | User at 80%+ of seats, storage, projects, or API calls | "You've used X of Y [resource]. Upgrade for unlimited." Show in-product when the user is near the limit. |
| **Feature gate** | User clicked a premium feature 2+ times | "This feature is on [Plan]. Here's what you get." Show immediately on gate hit. |
| **Growth signal** | Added 3+ team members in 30 days or usage volume doubled | "Your team is growing — [Plan] includes team analytics and permissions." Show as a banner. |
| **Time-based** | On free plan for 30+ days with 3+ sessions/week | "You've been getting value for [X] weeks. Here's how [Plan] helps you do more." Send via email. |

Configure PostHog cohorts for each trigger. Route high-value accounts (large team, heavy API usage, enterprise domain) to Attio as expansion deals for sales follow-up instead of self-serve upgrade prompts.

### 2. Run systematic A/B tests
Run the `ab-test-orchestrator` drill to test variations across the conversion funnel. Run one test at a time, each for statistical significance (minimum 200 per variant):

**Test 1: Prompt copy** — Compare benefit-led ("Unlock unlimited projects") vs. loss-aversion ("You're 3 projects from your limit") for limit-proximity prompts. Primary metric: `upgrade_surface_clicked` rate.

**Test 2: Prompt placement** — Compare modal (blocks workflow) vs. banner (non-blocking) for feature-gate prompts. Primary metric: `upgrade_completed` rate (not just click rate — modals get more clicks but may not convert better).

**Test 3: Email timing** — Compare day-5 upgrade email vs. day-10 upgrade email in the lifecycle sequence. Primary metric: `upgrade_completed` within 7 days of email send.

**Test 4: Pricing presentation** — Compare showing monthly price vs. showing daily equivalent ("Less than $2/day") on the upgrade surface. Primary metric: `upgrade_started` rate.

After each test concludes, implement the winner permanently and log the result in Attio. Calculate the cumulative lift from all winning variants.

### 3. Build churn prevention for free users
Run the `churn-prevention` drill to detect and intervene with free users who are disengaging before they ever convert. Define churn signals specific to the free-to-paid funnel:

| Signal | Detection | Intervention |
|--------|-----------|-------------|
| Usage decline | 50%+ drop in 7-day sessions vs prior 7 days | Intercom in-app message: "Need help with [feature they last used]?" with a tutorial link |
| Activation stall | Signed up 14+ days ago, never completed activation milestone | Loops email: "Most users find value by doing [first action]. Here's how." |
| Feature abandonment | Stopped using a core free feature they previously used 3+ times/week | Intercom tooltip on that feature: "Did you know you can [advanced use case]?" |
| Return after gap | No session for 7+ days, now returned | Intercom welcome-back message: "Here's what's new since you were last here" with a re-onboarding flow |

Track save rate: how many at-risk free users re-engage within 14 days of intervention. A user saved from disengagement is a user who remains in the conversion pipeline.

### 4. Segment-specific funnel optimization
Create PostHog cohorts for each major user segment and analyze conversion rates separately:

- **By signup source**: Organic search vs. paid ads vs. referral vs. product-led. Some channels bring higher-intent free users.
- **By company size**: Solo users vs. small teams vs. larger teams. Team accounts may convert differently.
- **By activation speed**: Users who activated in <24h vs. 1-7 days vs. 7+ days. Faster activators may respond to earlier upgrade prompts.
- **By feature usage**: Users of feature A vs. feature B. Some features correlate more strongly with upgrade intent.

For each segment with conversion rate >2x the average, increase prompt frequency. For segments with below-average rates, reduce prompts and focus on activation.

### 5. Evaluate against threshold
After 2 months, measure: ≥8% free-to-paid conversion rate sustained across a pool of 500+ active free users.

- **Pass → proceed to Durable.** Document all winning A/B test results, per-segment conversion rates, per-surface performance, and churn prevention save rates.
- **Fail → focus on highest-impact lever.** If activation rate is low, optimize onboarding before prompts. If prompt CTR is low, test more aggressive positioning. If checkout abandonment is high, simplify the payment flow. Re-run Scalable after fixing.

## Time Estimate
- 12 hours: Multi-trigger upgrade prompt system build
- 20 hours: A/B test design, execution, and analysis (4 tests over 2 months)
- 10 hours: Churn prevention system build and monitoring
- 8 hours: Segment analysis and per-segment optimization
- 10 hours: Ongoing monitoring, iteration, and threshold evaluation

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts | Free up to 1M events/mo; $0.00005/event after — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app messages, product tours, churn interventions | From $29/seat/mo; Proactive Support add-on $349/mo — [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Lifecycle emails, triggered sequences, broadcasts | From $49/mo — [loops.so/pricing](https://loops.so/pricing) |
| Stripe | Subscription management, checkout | 2.9% + $0.30/txn — [stripe.com/pricing](https://stripe.com/pricing) |

**Play-specific cost:** Intercom ~$75-350/mo (depending on messaging volume) + Loops ~$49/mo = ~$125-400/mo

## Drills Referenced
- `ab-test-orchestrator` — design, run, and analyze A/B tests on upgrade prompts, email timing, and pricing presentation
- `upgrade-prompt` — build the multi-trigger upgrade prompt system with contextual messaging per trigger type
- `churn-prevention` — detect disengaging free users and trigger automated interventions to keep them in the conversion pipeline
