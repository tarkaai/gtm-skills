---
name: email-reengagement-inactive-scalable
description: >
  Inactive User Re-engagement — Scalable Automation. Expand to 4+ inactivity
  cohorts, A/B test subject lines and CTAs systematically, add in-app
  welcome-back messaging, and prove >=18% return rate at 500+ inactive users.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=18% return rate sustained across 500+ inactive users per month"
kpis: ["Return rate per cohort", "Reactivation rate per cohort", "Email open rate per step", "Click-to-open rate per step", "Unsubscribe rate per step", "Reactivation quality (action depth)"]
slug: "email-reengagement-inactive"
install: "npx gtm-skills add product/winback/email-reengagement-inactive"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - winback-campaign
---

# Inactive User Re-engagement — Scalable Automation

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

The reengagement system handles 500+ inactive users per month across 4+ inactivity cohorts with >=18% return rate sustained over 2 months. Systematic A/B testing has identified winning subject lines, CTAs, and send timing per cohort. In-app welcome-back messages catch users who return organically. The system scales without proportional effort.

## Leading Indicators

- A/B tests produce statistically significant winners within 2-week cycles
- Return rate per cohort does not decline as volume increases (no diminishing returns at scale)
- Reactivation quality holds: returned users complete at least 1 meaningful product action, not just login
- Unsubscribe rate stays below 0.5% per step across all cohorts
- In-app welcome-back messages show >=40% engagement rate for returning users

## Instructions

### 1. Expand inactivity cohorts

Extend the system from 2 cohorts (Baseline) to 4:

Using `posthog-cohorts`, define:
- **7-14 day inactive (early lapse):** Users who stopped logging in 7-14 days ago. Were active (3+ sessions in prior 30 days). Highest recovery potential. Sequence: 2 emails, lighter tone.
- **14-30 day inactive (recent lapse):** Carried over from Baseline. 3-email sequence.
- **30-60 day inactive (extended lapse):** Carried over from Baseline. 3-email sequence with walkthrough offer.
- **60-90 day inactive (deep lapse):** Users gone 60-90 days. Low recovery rate but high value if recovered. Sequence: 2 emails, lead with biggest product changes, final email offers data export or feedback survey.

Run the `winback-campaign` drill to design sequence content for the 2 new cohorts (7-14d and 60-90d). Build these sequences in Loops. Update the n8n workflow to route users to the correct sequence based on `days_inactive`.

Exclude users inactive >90 days. They are unlikely to return via email and including them drags down deliverability. Suppress them in Loops using the `loops-audience` fundamental.

### 2. Launch systematic A/B testing

Run the `ab-test-orchestrator` drill to test one variable at a time per cohort:

**Month 1 tests (subject line optimization):**
- Test 1 (14-30d cohort): Curiosity subject ("Something changed in [Product]") vs. specific subject ("[Feature X] just shipped — your workspace is ready")
- Test 2 (7-14d cohort): Personal subject ("We noticed you've been away, {{firstName}}") vs. value subject ("3 things you missed in [Product] this week")

**Month 2 tests (CTA and timing optimization):**
- Test 3: Deep-link CTA (link to user's most-used feature) vs. "What's New" landing page CTA
- Test 4: Send timing — morning (9am user timezone) vs. evening (6pm user timezone)

For each test:
1. Use PostHog feature flags to randomly assign users entering the sequence to variant A or B
2. Use the Loops A/B broadcast or create parallel sequence variants
3. Minimum 200 users per variant per test
4. Run each test for 2 weeks or until 200+ users per variant, whichever is longer
5. Measure: open rate (for subject tests), click rate (for CTA tests), return rate (for all tests)
6. Implement the winner and document the learning

### 3. Add in-app welcome-back messaging

Using `intercom-in-app-messages`, create welcome-back messages for users who return to the product after being in a reengagement sequence:

- **Trigger:** User logs in AND has `reengagement_sequence_entered` event in past 30 days AND does not have a `welcome_back_shown` event in past 7 days.
- **Content:** "Welcome back, {{firstName}}. Here's what's new since [last_active_date]." Show 2-3 bullet points of product changes. Include a CTA: "Take a quick tour" or "Jump to [most_used_feature]."
- **Dismiss behavior:** Dismissing the message fires `welcome_back_dismissed`. Clicking the CTA fires `welcome_back_cta_clicked`. Both set `welcome_back_shown`.

This catches users who return organically (not from the email CTA) and ensures they re-discover product value immediately.

### 4. Build churn-to-reengagement feedback loop

Run the `churn-prevention` drill to connect the upstream churn signals to the reengagement system:

- When a user is flagged as at-risk by churn prevention but still churns (goes inactive), enrich their reengagement sequence with the churn signal data. For example: if the churn signal was "stopped using feature X," the reengagement email should specifically highlight improvements to feature X.
- Route churn reason data from the churn-prevention drill into Loops contact properties: `churn_signal`, `churn_signal_date`. The reengagement sequence uses conditional branches to personalize content based on the churn signal.

### 5. Scale volume and monitor efficiency

As the system processes 500+ users per month:
- Monitor return rate per cohort weekly. If any cohort's return rate drops below 12%, investigate: is it a content issue (stale copy), a targeting issue (cohort definition drift), or a product issue (nothing new to highlight)?
- Track reactivation quality: of users who return, what percentage completes a meaningful action? If return rate is high but reactivation rate is low, the product re-entry experience needs improvement (more Intercom tours, better empty states, or onboarding refreshers).
- Monitor Loops deliverability weekly. As volume scales, watch for bounce rate increases or spam complaints. Maintain list hygiene: remove hard bounces immediately, suppress users who have not opened any of the last 5 emails.

### 6. Evaluate against threshold

After 2 months of scaled operation, measure:
- Primary: >=18% return rate across all cohorts combined at 500+ inactive users per month
- Per-cohort rates: 7-14d should be highest (target >25%), 60-90d lowest (target >8%)
- Reactivation rate: >=10% of returned users complete a meaningful action
- A/B test velocity: at least 4 tests completed with documented learnings

If PASS: document the winning sequence variants, optimal timing, and per-cohort benchmarks. Proceed to Durable.
If FAIL: focus on the cohort with the largest volume and worst return rate. Run 2 more A/B tests targeting that cohort's weakest email step. Stay at Scalable and re-evaluate after another 4-week cycle.

## Time Estimate

- 6 hours: Design and build 2 new cohort sequences, update n8n routing
- 8 hours: Set up and run 4 A/B tests (2 hours each: design, implement, analyze)
- 4 hours: Build Intercom welcome-back messages and configure triggers
- 4 hours: Connect churn-prevention signals to reengagement personalization
- 8 hours: Weekly monitoring and iteration (1 hour/week for 8 weeks)
- 4 hours: Final evaluation, documentation, and Durable preparation
- 6 hours: Buffer for iteration on underperforming cohorts

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohort detection, A/B testing via feature flags, funnel analysis | Free up to 1M events/mo; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | 4 reengagement sequence variants (12+ emails total) | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily routing workflow, PostHog-Loops sync, churn signal enrichment | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app welcome-back messages for returning users | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated play-specific cost:** $102-152/mo (Loops + n8n Cloud + Intercom Essential)

## Drills Referenced

- `ab-test-orchestrator` — design, run, and analyze A/B tests on subject lines, CTAs, and send timing per cohort
- `churn-prevention` — connect upstream churn signals to reengagement personalization, enriching sequences with churn reason data
- `winback-campaign` — design sequence content for the 2 new inactivity cohorts (7-14d and 60-90d)
