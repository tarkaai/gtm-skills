---
name: email-subject-testing-smoke
description: >
  Email Subject-Line A/B Testing — Smoke Test. Run 5 manual subject-line A/B tests on retention
  emails to prove that systematic testing produces measurable open-rate lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "5 subject-line tests completed with documented open-rate data per variant"
kpis: ["Open rate per variant", "Click rate per variant", "Unsubscribe rate per variant"]
slug: "email-subject-testing"
install: "npx gtm-skills add product/retain/email-subject-testing"
drills:
  - email-subject-test-pipeline
  - threshold-engine
---

# Email Subject-Line A/B Testing — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Email

## Outcomes

Run 5 subject-line A/B tests on retention emails sent via Loops. Each test compares one control subject against one variant. Collect open-rate, click-rate, and unsubscribe-rate data per variant. Pass threshold: all 5 tests completed with data recorded.

## Leading Indicators

- Loops broadcasts or sequences are actively sending to retained users (>100 recipients per send)
- PostHog events are firing for email sends and opens
- At least 1 test shows a measurable open-rate difference (>3 percentage points)

## Instructions

### 1. Identify 5 retention emails to test

Select 5 emails from your active Loops sequences or upcoming broadcasts that target retained users. Good candidates:
- Re-engagement emails to users inactive 7-14 days
- Feature announcement emails for existing users
- Usage summary or milestone emails
- Renewal reminder emails
- Product tips or best-practices emails

For each email, record the current subject line and its historical open rate from Loops. These are your 5 controls.

### 2. Generate 1 subject-line variant per email

For each control subject, write 1 variant using a different framing dimension. Run the `email-subject-test-pipeline` drill for each test. Use these framing categories across your 5 tests to learn which approach works for your audience:

- Test 1: **Personalization** — add the user's name or usage data to the subject
- Test 2: **Curiosity gap** — tease a benefit without revealing it
- Test 3: **Social proof** — reference what similar users are doing
- Test 4: **Direct value** — state the benefit plainly
- Test 5: **Urgency** — add a time-bound element

Keep the email body identical between control and variant. Change ONLY the subject line.

### 3. Send each test via Loops

For each of the 5 tests:
1. Create two versions of the email in Loops with different subject lines
2. Split the audience: send variant A to 50%, variant B to 50%
3. Wait 48 hours for results to accumulate
4. Pull open rate, click rate, and unsubscribe rate per variant from Loops

**Human action required:** Review each pair of subject lines before sending. Ensure the variants are meaningfully different (not just word-order swaps) and that the body content is identical.

### 4. Record results in a structured log

For each test, log:
- Test number (1-5)
- Email type (re-engagement, feature, renewal, etc.)
- Control subject line and open rate
- Variant subject line and open rate
- Framing category used
- Winner (control, variant, or tie if <3pp difference)
- Click rate and unsubscribe rate for both

### 5. Evaluate against threshold

Run the `threshold-engine` drill. Pass criteria: 5 tests completed with open-rate data per variant recorded. If PASS, document the initial patterns (which framing categories performed best) and proceed to Baseline. If FAIL (fewer than 5 tests completed), check that your email volume supports testing and extend the time window.

## Time Estimate

- 1 hour: Select 5 emails and pull baseline open rates
- 2 hours: Write 5 variant subject lines and configure tests in Loops
- 1 hour: Monitor sends and collect results over 48-hour windows
- 1 hour: Record results and document patterns

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Send A/B test emails to retained users | Free up to 1,000 contacts / 2,000 sends/mo; Starter $49/mo for 5,000 contacts — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Track email open and click events | Free up to 1M events/mo — [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost:** Free (within free tiers for Smoke volume)

## Drills Referenced

- `email-subject-test-pipeline` — runs each individual subject-line A/B test: variant generation, send split, metric collection, winner selection
- `threshold-engine` — evaluates pass/fail against the 5-test completion threshold
