---
name: trial-to-paid-conversion-smoke
description: >
  Trial-to-Paid Conversion — Smoke Test. Manually guide 10-20 trial users through activation
  milestones with targeted touchpoints. Prove that structured trial follow-up produces conversion
  signal above organic baseline.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Email, Product, Direct"
level: "Smoke Test"
time: "8 hours over 1 week"
outcome: ">=40% trial-to-paid conversion rate within trial period for a 10-20 user cohort"
kpis: ["Trial-to-paid conversion rate", "Activation milestone completion rate", "Time to first value", "Engagement score"]
slug: "trial-to-paid-conversion"
install: "npx gtm-skills add product/onboard/trial-to-paid-conversion"
drills:
  - icp-definition
  - onboarding-sequence-design
  - threshold-engine
---

# Trial-to-Paid Conversion — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Email, Product, Direct

## Outcomes

A cohort of 10-20 active trial users receives structured activation guidance and conversion touchpoints. At least 40% convert to paid within the trial window. Users who hit >= 3 activation milestones convert at >= 2x the rate of users who hit < 3. You have a documented activation milestone ladder and touchpoint cadence that produces measurable conversion signal.

## Leading Indicators

- Trial users reach the first activation milestone within 48 hours of signup
- Users who receive a Day 3 check-in email reply or click at >= 30% rate
- Users who complete >= 3 milestones show measurably higher product engagement (sessions, actions) than those who complete < 3
- At least 2 trial users schedule an onboarding call via the Cal.com link

## Instructions

### 1. Define trial ICP and activation milestones

Run the `icp-definition` drill scoped to trial users. Define:

- **Who starts a trial:** persona (role, seniority), company size, use case, typical signup source
- **What activated means:** the single core action that best predicts paid conversion (e.g., completed first workflow, invited a teammate, connected an integration)
- **Trial window:** the length of the free trial period (7, 14, or 30 days)
- **Conversion action:** the specific event that constitutes paid conversion (payment_completed, plan_selected, subscription_activated)
- **3-5 intermediate milestones** between signup and activation, ordered by the path most users take

Store the ICP definition and activation milestone ladder in Attio as a note on the play record. Each milestone must map to a trackable PostHog event.

### 2. Design the touchpoint sequence

Run the `onboarding-sequence-design` drill to create a manual email cadence for the smoke test cohort. Write the actual email content — subject lines, body, and CTAs — for each touchpoint:

**Day 0 — Welcome email:**
- Subject: "[Product] — your first [core action] in 5 minutes"
- Body: One clear next step. Link directly to the action that completes Milestone 1, not to the dashboard.
- CTA: "Start your first [action]"

**Day 1 — Setup nudge (if Milestone 1 not completed):**
- Subject: "Quick question — did you get stuck on setup?"
- Body: Shortest path to completing Milestone 1. Include a screenshot or GIF showing the exact steps.
- CTA: deep link to the setup step they need

**Day 3 — Use-case coaching:**
- Subject: "How [similar company] uses [Product] for [outcome]"
- Body: One concrete example of a company like theirs getting value. Include the specific workflow they followed.
- CTA: "Try this workflow"

**Day 7 — Personal check-in (if not activated):**
- Subject: "Can I help you get set up?"
- Body: Written from the founder. Acknowledge where the user is in their trial. Offer help. Include a Cal.com booking link for a 15-minute call.
- CTA: "Book a call" or "Reply to this email"

**Day 10 — Upgrade prompt (if activated):**
- Subject: "You're getting great results — here's what's next"
- Body: Summarize what the user has accomplished. Show what they unlock on the paid plan. Clear price and upgrade link.
- CTA: "Upgrade now"

**Day 12 — Urgency (if not yet converted):**
- Subject: "Your trial ends in [N] days — keep your [work]"
- Body: Remind them what they have built. Create urgency around data/work preservation. One-click upgrade CTA.
- CTA: "Upgrade to keep everything"

Send each email manually for this smoke test. Track opens and clicks in a spreadsheet or Attio notes.

### 3. Instrument basic tracking in PostHog

Log these events for each trial user in the cohort:

- `trial_started` — when the trial begins, with properties: `signup_source`, `company_size`, `use_case`
- `activation_milestone_hit` — when any milestone is completed, with property: `milestone_name`, `milestone_number`, `days_since_trial_start`
- `trial_engaged` — daily login or meaningful session, with property: `session_actions_count`
- `trial_converted` — when payment completes, with property: `plan_selected`, `trial_day`
- `trial_expired` — when the trial window closes without conversion, with property: `milestones_completed`, `last_active_day`

This does not need full automation yet — PostHog event capture via the SDK is sufficient.

### 4. Execute the touchpoint cadence

**Human action required:** For each of the 10-20 trial users:

1. Check their activation progress daily in PostHog or the product admin
2. Send the appropriate email from the sequence above based on their trial day and milestone status
3. Skip emails that do not apply (e.g., skip the Day 1 nudge if they already completed Milestone 1)
4. When a user hits >= 2 milestones and is at Day 8+, call them directly: "You've been getting great results with [specific milestone]. Let's talk about moving to paid so you can [unlock specific benefit]."
5. Log every touchpoint sent and the user's response in Attio or a tracking spreadsheet

### 5. Evaluate against threshold

Run the `threshold-engine` drill after the trial window closes for the full cohort. Measure:

- **Primary:** trial-to-paid conversion rate (target: >= 40%)
- **Milestone correlation:** conversion rate for users with >= 3 milestones vs. users with < 3 milestones (target: >= 2x difference)
- **Supporting:** time to first value (days to activation), touchpoint engagement rates (open/click/reply), call booking rate

If PASS: document the activation milestone ladder, touchpoint cadence, and conversion data. These become the specification for Baseline automation. Proceed to Baseline.
If FAIL: identify which touchpoint or milestone has the weakest signal. Revise that single element and re-run with a fresh cohort of 10-20 users.

## Time Estimate

- 1.5 hours: ICP definition and activation milestone mapping
- 2 hours: Touchpoint sequence writing (email content, CTAs)
- 0.5 hours: PostHog event instrumentation
- 3 hours: Daily monitoring and sending touchpoints over the trial window
- 1 hour: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking for trial milestones and conversion | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM, trial user tracking, play record logging | Standard stack |
| Cal.com | Booking link for onboarding calls | Free tier available ([cal.com/pricing](https://cal.com/pricing)) |

**Estimated play-specific cost:** $0 (all within free tiers at smoke test volume)

## Drills Referenced

- `icp-definition` — defines who the trial targets, what activation means, and the milestone ladder from signup to conversion
- `onboarding-sequence-design` — designs the email touchpoint sequence with content, timing, and behavioral branching logic
- `threshold-engine` — evaluates trial-to-paid conversion against the 40% pass threshold and milestone correlation targets
