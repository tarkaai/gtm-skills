---
name: free-trial-optimization-smoke
description: >
  Trial Conversion Optimization — Smoke Test. Run one cohort of trial users through a
  structured onboarding flow with tracked activation milestones. Prove that a guided trial
  experience produces measurable conversion signal.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=25% trial-to-paid conversion in a 10-50 user test cohort"
kpis: ["Trial-to-paid conversion rate", "72-hour activation rate", "Time to first value moment"]
slug: "free-trial-optimization"
install: "npx gtm-skills add product/onboard/free-trial-optimization"
drills:
  - icp-definition
  - onboarding-flow
  - threshold-engine
---

# Trial Conversion Optimization — Smoke Test

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

A single test cohort of 10-50 trial users passes through a structured onboarding experience. At least 25% convert to paid within the trial window. You have PostHog data showing the exact funnel steps where users convert or drop off.

## Leading Indicators

- Trial users reach the activation milestone (first core action) within 72 hours of signup
- Onboarding email open rates exceed 40%
- In-app product tour completion rate exceeds 60%
- Users who reach activation convert at 2x+ the rate of users who do not

## Instructions

### 1. Define trial ICP and activation milestone

Run the `icp-definition` drill scoped to trial users. Define:
- Who starts a free trial (persona, company size, use case)
- What "activated" means for your product (the single action that best predicts conversion)
- What the trial window is (7 days, 14 days, 30 days)
- What the conversion action is (entering payment info, selecting a plan, completing checkout)

Store the ICP and activation definition in Attio as a note on the play record.

### 2. Build the trial onboarding experience

Run the `onboarding-flow` drill to create the guided experience:

**In-app (Intercom):**
- Create a product tour triggered on first login that walks the user to the activation milestone in 3-5 steps. Each step should have a clear action, not just a tooltip. End the tour with the user having completed their first core action.
- Create a contextual in-app message that fires if the user has not reached activation after 24 hours. The message should offer specific help: a link to a quick-start resource or a calendar booking link for a 15-minute onboarding call.

**Email (Loops):**
- Email 1 (immediate): Welcome email with a single CTA linking directly to the first onboarding step. Subject: "[Product] — your first [core action] in 5 minutes."
- Email 2 (Day 1): If activation not reached, send a tutorial showing the fastest path to value. Include a screenshot or GIF.
- Email 3 (Day 3): Social proof email. One customer quote about the specific value moment. CTA to resume where they left off.
- Email 4 (Day 5): Personal check-in from founder. Ask if they need help. Include Cal.com booking link.

Configure Loops to skip emails when the user has already reached the corresponding milestone.

**Tracking (PostHog):**
- Instrument these events: `trial_started`, `onboarding_tour_started`, `onboarding_tour_completed`, `activation_reached`, `upgrade_prompt_shown`, `upgrade_started`, `payment_completed`
- Attach properties to each event: `user_id`, `signup_source`, `trial_day` (days since trial start), `plan_interest`

### 3. Launch to test cohort

**Human action required:** Enable the experience for a test cohort of 10-50 new trial signups using a PostHog feature flag. Do not launch to all traffic yet. Monitor the first 3-5 users manually to verify the tour loads correctly, emails deliver, and events fire in PostHog Live Events.

### 4. Evaluate against threshold

Run the `threshold-engine` drill after the trial window closes for the test cohort. Measure:
- Primary: trial-to-paid conversion rate (target: >=25%)
- Supporting: 72-hour activation rate, tour completion rate, email engagement

If PASS: document what worked, capture the funnel data, proceed to Baseline.
If FAIL: identify the highest drop-off step in the PostHog funnel. Fix that single step and re-run with a new cohort.

## Time Estimate

- 1 hour: ICP definition and activation milestone selection
- 2 hours: Building the onboarding tour, emails, and tracking
- 0.5 hours: Launching to test cohort and verifying instrumentation
- 1.5 hours: Monitoring, analyzing results, documenting findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, feature flags | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Product tours, in-app messages | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Lifecycle email sequences | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | CRM, play record logging | Standard stack |
| Cal.com | Booking link for onboarding calls | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost:** $0 (within free tiers at this volume)

## Drills Referenced

- `icp-definition` — defines who the trial targets and what activation means
- `onboarding-flow` — builds the in-app tour, email sequence, and milestone tracking
- `threshold-engine` — evaluates trial-to-paid conversion against the 25% pass threshold
