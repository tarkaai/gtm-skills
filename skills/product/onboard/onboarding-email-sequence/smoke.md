---
name: onboarding-email-sequence-smoke
description: >
  Onboarding email sequence — Smoke Test. Design and manually send a 5-email
  onboarding sequence to 20-50 new signups. Validate that email-driven nudges
  move users toward activation before investing in automation.
stage: "Product > Onboard"
motion: "Lead Capture Surface"
channels: "Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "Open rate >= 40% and click-to-activation rate >= 5% across the 5-email sequence in 1 week"
kpis: ["Email open rate per step", "Email click rate per step", "Time from signup to activation", "Activation rate for emailed cohort vs control"]
slug: "onboarding-email-sequence"
install: "npx gtm-skills add product/onboard/onboarding-email-sequence"
drills:
  - onboarding-sequence-design
  - threshold-engine
---

# Onboarding Email Sequence — Smoke Test

> **Stage:** Product > Onboard | **Motion:** Lead Capture Surface | **Channels:** Email

## Outcomes

Send a 5-email onboarding sequence to a small cohort of new signups (20-50 users). Measure whether the emails get opened, clicked, and whether emailed users activate at a higher rate than users who received no sequence. Pass threshold: open rate >= 40%, click-to-activation rate >= 5%.

## Leading Indicators

- Email 1 (welcome) open rate above 60% within 24 hours — confirms subject line and sender name work
- Email 2 (quickstart nudge) click rate above 8% — confirms the CTA and content resonate
- At least 1 user who was stuck at Milestone 2 completes it after receiving Email 2
- Users who received the sequence reach activation faster (fewer days) than users who did not

## Instructions

### 1. Design the onboarding email sequence

Run the `onboarding-sequence-design` drill. This produces:
- Your activation metric (the single action that predicts retention)
- 3-5 onboarding milestones between signup and activation
- 5 email specifications with subject lines, body content, CTAs, and timing
- A decision tree showing when each email sends and when it skips

For the smoke test, simplify the sequence to 5 emails (skip Emails 6-7 from the drill output — those are post-activation and will be added at Baseline):

| Email | Trigger | Purpose |
|-------|---------|---------|
| 1 — Welcome | Immediate on signup | Deliver one clear next step |
| 2 — Quickstart nudge | 24h after signup if Milestone 2 not reached | Remove friction for stuck users |
| 3 — Use case | 48h after signup or on Milestone 2 | Show what's possible |
| 4 — Social proof | Day 5 if not activated | Create urgency |
| 5 — Personal help | Day 7 if not activated | Offer human assistance |

### 2. Set up tracking in PostHog

Before sending any emails, instrument tracking. Using PostHog, create these events:

- `onboarding_email_sent` with properties: `{email_step: 1-5, subject: "...", recipient_email: "..."}`
- `onboarding_email_opened` with properties: `{email_step: 1-5}`
- `onboarding_email_clicked` with properties: `{email_step: 1-5, cta_url: "..."}`

Also ensure your activation metric is tracked as a PostHog event (e.g., `activation_reached`).

For the smoke test, you can track these manually in PostHog by logging events via the API after each send, or by using Loops' built-in tracking if you send through Loops.

### 3. Select and split the test cohort

Identify 40-100 new signups in the last 7 days (or wait for new signups to accumulate). Split them:
- **Treatment group (20-50 users):** Will receive the email sequence
- **Control group (20-50 users):** Will receive no onboarding emails (just the standard welcome email if your app sends one)

Log group assignment as a PostHog person property: `onboarding_email_cohort: "treatment"` or `"control"`.

### 4. Send the emails manually through Loops

Create the 5 emails in Loops as transactional templates. For the smoke test, you do NOT need to set up automated triggers — send each email manually at the correct timing:

- **Day 0:** Send Email 1 to all treatment group users via Loops API or dashboard
- **Day 1:** Check which treatment users have NOT completed Milestone 2. Send Email 2 only to those users.
- **Day 2:** Send Email 3 to all treatment users who have completed Milestone 2 but not activated. For those who have not completed Milestone 2, send Email 3 anyway (it still provides value).
- **Day 5:** Send Email 4 to treatment users who have NOT activated.
- **Day 7:** Send Email 5 to treatment users who have NOT activated. Send this from a real person's email address (founder or CSM name), not from the product.

**Human action required:** Review each email's content before the first send. Verify that all CTA links work, personalization renders correctly, and the tone feels right. Send a test email to yourself for each of the 5 emails before sending to real users.

### 5. Log outcomes and measure

After each email send, log the results:
- Check Loops dashboard for open rates and click rates per email
- Check PostHog for milestone completions and activations in the treatment group
- Compare activation rate: treatment group vs control group

### 6. Evaluate against threshold

Run the `threshold-engine` drill with these criteria:

- **Open rate >= 40%** across the full sequence (weighted average of all 5 emails)
- **Click-to-activation rate >= 5%** — of users who clicked any CTA in the sequence, at least 5% reached activation
- **Activation rate lift:** Treatment group activates at a higher rate than control group (any positive delta is a pass at smoke level)

If PASS: The email sequence produces signal. Proceed to Baseline to automate it.
If FAIL on open rate: Rewrite subject lines. Test sending from a person's name vs product name.
If FAIL on click rate: Rewrite CTAs. Make the linked action simpler. Reduce email length.
If FAIL on activation lift: The emails may not be targeting the right action. Revisit your activation metric definition.

## Time Estimate

- 2 hours: Design the sequence (run the drill, write email content, set up PostHog events)
- 30 minutes: Create email templates in Loops and send test emails
- 30 minutes: Select cohort, split groups, send Day 0 emails
- 30 minutes: Daily check-ins over 7 days (send remaining emails, log results)
- 30 minutes: Final analysis and threshold evaluation

Total: ~4 hours spread over 1 week.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Send onboarding emails, track opens/clicks | Free up to 1,000 contacts / 4,000 emails per month. Paid from $49/mo. [Pricing](https://loops.so/pricing) |
| PostHog | Track milestone events, activation, cohort comparison | Free up to 1M events/mo. [Pricing](https://posthog.com/pricing) |

**Estimated cost for smoke test: $0** (both tools have free tiers sufficient for 20-50 users)

## Drills Referenced

- `onboarding-sequence-design` — designs the email sequence: milestones, content, timing, and branching logic
- `threshold-engine` — evaluates open rate, click rate, and activation lift against pass/fail criteria
