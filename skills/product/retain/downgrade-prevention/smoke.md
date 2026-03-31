---
name: downgrade-prevention-smoke
description: >
  Downgrade Intervention — Smoke Test. Manually identify users showing downgrade intent signals
  in PostHog, build a single intercept surface, and test whether personalized intervention
  prevents at least 40% of downgrades in a small cohort.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥40% prevention rate in test cohort of 10-30 users"
kpis: ["Downgrade prevention rate", "Intercept engagement rate", "Offer acceptance rate"]
slug: "downgrade-prevention"
install: "npx gtm-skills add product/retain/downgrade-prevention"
drills:
  - downgrade-intent-detection
  - downgrade-intercept-flow
  - threshold-engine
---

# Downgrade Intervention — Smoke Test

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

Prove the concept: can you detect users who are about to downgrade and stop them with a personalized intervention? No automation, no always-on. One manual agent run that identifies at-risk users from PostHog data, builds a single intercept surface, and tests whether the intervention prevents downgrades in a small cohort.

## Leading Indicators

- PostHog query identifies at least 5 users with 2+ downgrade intent signals (billing page visits, pricing comparison, premium feature decline)
- The intercept surface (in-app message or email) is deployed and renders correctly for the target cohort
- At least 50% of targeted users engage with the intervention (open email, see in-app message, click CTA)
- At least 1 user who received the intervention remains on their current plan when they would have otherwise downgraded

## Instructions

### 1. Verify PostHog data readiness

Confirm your PostHog project tracks the events needed to detect downgrade intent. Check that these event types exist:

- Billing page views (`billing_page_viewed` or equivalent)
- Pricing/plan comparison views (`pricing_page_viewed`, `plan_comparison_viewed`)
- Premium/paid feature usage events (any events tied to features exclusive to higher tiers)
- Downgrade or cancellation page views (if instrumented)

Run this verification query via PostHog API or HogQL:

```sql
SELECT event, count()
FROM events
WHERE timestamp > now() - interval 30 day
  AND event IN ('billing_page_viewed', 'pricing_page_viewed', 'plan_comparison_viewed',
                'downgrade_page_viewed', 'premium_feature_used')
GROUP BY event
ORDER BY count() DESC
```

If fewer than 2 of these event types exist, instrument tracking first using the `posthog-custom-events` fundamental before proceeding. At minimum, you need billing page views and premium feature usage.

### 2. Identify your test cohort manually

Run the `downgrade-intent-detection` drill in manual mode (skip the n8n automation, run the queries directly). Pull users on paid plans who show 2+ downgrade signals in the last 14 days. Typical signals to look for:

- Visited billing or pricing page 2+ times in 7 days
- Premium feature usage dropped 50%+ vs. their 30-day average
- Visited the downgrade or cancellation page
- Filed a support ticket about billing or value

Sort the results by signal count and plan value (higher plan = more MRR at risk). Select 10-30 users as your test cohort.

**Human action required:** Review the cohort list. Do these users look like genuine downgrade risks based on your knowledge of the accounts? Remove any obvious false positives (e.g., users who just renewed, internal test accounts).

### 3. Build a single intercept surface

Run the `downgrade-intercept-flow` drill to build ONE intervention for this test. Choose the intervention type based on the dominant signal in your cohort:

- **If most users show premium feature underutilization:** Build a feature education intervention. Create an Intercom in-app message highlighting the premium features they have not been using, with a "show me how" CTA linking to a help article or product tour.
- **If most users show billing/pricing exploration:** Build a retention offer intervention. Create a Loops transactional email with a personalized usage summary ("You used [feature] [N] times this month") and a retention offer (20% discount for 3 months, or plan pause for 30 days).
- **If users are hitting the downgrade page:** Build a downgrade page intercept showing what they would lose and offering an alternative.

Deploy to only your test cohort. Use a PostHog feature flag to gate the intervention:

```
Feature flag: downgrade-prevention-smoke
Filter: person_id IN [list of test cohort IDs]
Rollout: 100% of matching users
```

Track all interactions via PostHog events:
- `downgrade_intervention_sent` (in-app shown or email sent)
- `downgrade_intervention_engaged` (CTA clicked, email opened)
- `downgrade_intercept_action` (if using the page intercept: keep_plan, request_discount, continue_downgrade)

### 4. Monitor for 7 days

Over the next 7 days, track:
- How many test cohort users saw or received the intervention
- How many engaged with it (clicked, responded, took the suggested action)
- How many remained on their current plan
- How many downgraded despite the intervention

Do not intervene further during the test period. Let the single intervention play out.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against the pass threshold: **>=40% prevention rate**. Prevention rate = (users who remained on their plan) / (total test cohort users who showed downgrade intent).

Also calculate:
- Engagement rate: what percentage of users interacted with the intervention
- If an offer was used: acceptance rate and which offer resonated
- Qualitative: for users who downgraded anyway, can you identify why the intervention did not work? (Wrong signal, wrong offer, wrong timing?)

### 6. Document and decide

Record:
- Test cohort size and composition (plan types, MRR at risk)
- Intervention type deployed
- Prevention rate vs. 40% threshold
- Engagement rate by channel
- Top downgrade signals that predicted actual downgrades
- Signals that produced false positives (intent detected but user was not actually at risk)

If PASS (>=40% prevention rate), proceed to Baseline. If FAIL, examine: were the signals wrong (detection problem), or was the intervention wrong (intercept problem)? Adjust and re-run.

## Time Estimate

- 1 hour: verify PostHog data, run detection queries, identify test cohort
- 1.5 hours: build the intercept surface (in-app message, email, or page intercept)
- 0.5 hours: deploy to test cohort via feature flag, verify events fire
- 1.5 hours: monitor over 7 days (check daily, 15 min each)
- 0.5 hours: evaluate results, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage data queries, cohort identification, event tracking, feature flags | Free up to 1M events/mo -- [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app intervention messages (if chosen) | Essential $29/seat/mo -- [intercom.com/pricing](https://intercom.com/pricing) |
| Loops | Email intervention sequences (if chosen) | Free up to 1,000 contacts -- [loops.so/pricing](https://loops.so/pricing) |

**Estimated cost for Smoke: Free** (PostHog free tier + existing Intercom/Loops subscription)

## Drills Referenced

- `downgrade-intent-detection` -- extracts behavioral signals from PostHog and identifies users showing downgrade intent (run manually, skip automation)
- `downgrade-intercept-flow` -- builds the intervention surface (in-app message, email, or page intercept) for the test cohort
- `threshold-engine` -- evaluates whether the prevention rate meets the >=40% pass threshold
