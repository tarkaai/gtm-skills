---
name: downgrade-prevention-scalable
description: >
  Downgrade Intervention — Scalable Automation. Expand interventions to cover all segments and plan
  tiers. A/B test offers, messaging, and timing. Build segment-specific playbooks. Validate >=45%
  prevention rate at 500+ users scored per month.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥45% prevention rate at 500+ scored users/month"
kpis: ["Downgrade prevention rate", "Offer acceptance rate", "MRR saved", "Cost per save", "Segment prevention rates"]
slug: "downgrade-prevention"
install: "npx gtm-skills add product/retain/downgrade-prevention"
drills:
  - ab-test-orchestrator
  - downgrade-intercept-flow
  - downgrade-intent-detection
---

# Downgrade Intervention — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Find the 10x multiplier. The Baseline system works for the initial user base. Now scale it to handle 500+ scored users per month across all plan tiers, company sizes, and usage patterns without proportional effort. A/B test every variable (offers, messaging, timing, channel) to find the optimal intervention for each segment. Build segment-specific intervention playbooks that route the right offer to the right user at the right time.

## Leading Indicators

- Detection model covers all plan tiers (not just the highest-value plans)
- At least 3 A/B tests running or completed on intervention variables (offer type, message copy, delivery timing)
- Segment-specific prevention rates are tracked for at least 4 segments (by plan tier, company size, usage pattern, tenure)
- Cost per save is tracked and trending down as interventions optimize
- The system handles 500+ scored users per month without manual intervention or workflow failures

## Instructions

### 1. Expand detection to all segments

Enhance the `downgrade-intent-detection` drill to cover plan- and segment-specific signals:

**Plan-tier-specific signals:** The signals that predict downgrade differ by plan. A user on the Enterprise plan shows different pre-downgrade behavior than a user on the Pro plan. Add plan-aware signal weighting:

- Enterprise users: weight team shrinkage and API usage decline more heavily (these features are the Enterprise differentiator)
- Pro users: weight premium feature underutilization more heavily (Pro users downgrade because they are not using what they pay for)
- Starter-to-free: weight overall usage decline and login gaps (these users are evaluating whether the product is worth paying for at all)

Update the detection model in the n8n workflow to query the user's current plan and apply the correct signal weights.

**Segment-specific cohorts:** Create additional PostHog cohorts using `posthog-cohorts`:
- "Downgrade Intent: Enterprise" (enterprise users with moderate+ intent)
- "Downgrade Intent: High-MRR" (users with MRR > $200 and moderate+ intent)
- "Downgrade Intent: New" (users in first 90 days with moderate+ intent -- may be buyer's remorse)
- "Downgrade Intent: Veteran" (users with 6+ months tenure with moderate+ intent -- long-term value erosion)

### 2. A/B test intervention variables

Run the `ab-test-orchestrator` drill to systematically test each variable in the intervention system. Use PostHog feature flags to split users into control and variant groups. Run each test for statistical significance (minimum 7 days and 50+ users per variant).

**Tests to run (in priority order):**

Test 1 -- Offer type: Compare discount (20% for 3 months) vs. plan pause (30 days) vs. feature coaching session for high-intent users. Primary metric: prevention rate at 30 days.

Test 2 -- Intercept page copy: Compare "Here's what you'll lose" (loss-framed) vs. "Here's what you've accomplished" (gain-framed) on the downgrade page intercept. Primary metric: keep rate on intercept page.

Test 3 -- Intervention timing: Compare immediate intervention (within 2 hours of scoring) vs. next-day intervention for moderate-intent users. Primary metric: engagement rate.

Test 4 -- Channel: Compare in-app message vs. email vs. both for moderate-intent users. Primary metric: prevention rate per dollar spent.

Test 5 -- Message personalization depth: Compare generic ("Your plan includes premium features") vs. specific ("You used Advanced Analytics 23 times last month -- on Starter, you lose access to this"). Primary metric: engagement rate.

Document each test result in Attio: hypothesis, variants, sample sizes, results, confidence level, decision (adopt/iterate/revert).

### 3. Build segment-specific intervention playbooks

Based on A/B test results, build differentiated intervention paths for each segment. Update the `downgrade-intercept-flow` drill's n8n workflows to route users to the correct playbook:

```
IF plan = 'enterprise' AND intent_tier = 'high':
  -> personal outreach from account owner within 4 hours
  -> include: team usage summary, ROI calculation, executive escalation offer

ELSE IF plan = 'pro' AND intent_tier = 'high' AND top_signal = 'premium_feature_decline':
  -> in-app modal: "You haven't used [feature] in 2 weeks. Here's a 3-min refresher."
  -> email day 2: usage optimization guide
  -> email day 5: 20% discount offer (if still moderate+)

ELSE IF plan = 'pro' AND intent_tier = 'high' AND top_signal = 'billing_exploration':
  -> in-app modal: personalized usage summary + retention offer
  -> email within 2 hours: plan pause offer

ELSE IF plan = 'starter' AND intent_tier = 'moderate':
  -> in-app banner: highlight 1 premium feature they have access to but are not using
  -> email day 3: "Getting value from [product]? Here are 3 tips."
  -> no discount offer (margins too thin on starter)

ELSE IF tenure < 90 days AND intent_tier >= 'high':
  -> personal outreach: "We want to make sure you had a good onboarding experience"
  -> offer: free 1:1 setup session via Cal.com
```

### 4. Scale offer fulfillment

Extend the n8n offer fulfillment workflow to handle volume:

- Batch discount application: process up to 50 offers per day via billing API
- Automated plan pause with scheduled reactivation reminders
- Coaching session scheduling via Cal.com with automatic calendar availability check
- Offer budget guardrails: set a monthly discount budget (e.g., maximum $X in discounts per month). If the budget is exhausted, fall back to non-monetary interventions (feature education, coaching)
- Track offer economics in Attio: discount given vs. MRR retained vs. 60-day retention of saved users

### 5. Evaluate at scale

After 2 months, evaluate against the pass threshold: **>=45% prevention rate at 500+ scored users per month**.

Measure:
- Overall prevention rate across all segments
- Prevention rate per segment (plan tier, company size, tenure, top signal)
- MRR saved per month (total)
- Cost per save (total intervention cost / number of saves)
- Offer ROI by type (MRR retained per dollar of discount given)
- A/B test velocity: how many tests completed, how many produced statistically significant winners
- Channel efficiency: prevention rate per channel per dollar
- False positive rate: has detection accuracy improved or degraded at higher volume?

If PASS, proceed to Durable. If FAIL, identify the weakest segment and focus:
- If enterprise prevention is low -> the offers are wrong for high-value accounts (need human touch, not discounts)
- If new user prevention is low -> the problem is onboarding, not retention (route to onboarding plays)
- If cost per save is too high -> test non-monetary interventions (feature education, coaching)

## Time Estimate

- 8 hours: expand detection to all segments, plan-tier-specific signal weighting
- 15 hours: design and run 5 A/B tests (3 hours each for setup, monitoring, evaluation)
- 12 hours: build segment-specific intervention playbooks in n8n
- 8 hours: scale offer fulfillment workflows, budget guardrails
- 10 hours: monitoring during 2-month run (weekly check-ins, 1.5 hours each)
- 7 hours: evaluation, documentation, segment analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Detection, experiments, feature flags, funnels, cohorts | Free up to 1M events/mo; paid from $0.00031/event -- [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Detection workflows, intervention routing, offer fulfillment | Self-hosted free; Cloud from EUR20/mo -- [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | Segment-specific in-app messages and modals | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Segment-specific email sequences and transactional emails | $49/mo for 5,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost: $100-300/mo** (Loops sequences + Intercom messages + retention offer discounts)

## Drills Referenced

- `ab-test-orchestrator` -- designs, runs, and evaluates A/B tests on offer types, messaging, timing, and channels
- `downgrade-intercept-flow` -- expanded with segment-specific routing and scaled offer fulfillment
- `downgrade-intent-detection` -- enhanced with plan-tier-specific signal weighting and segment cohorts
